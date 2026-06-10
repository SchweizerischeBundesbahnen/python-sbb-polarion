from __future__ import annotations

import logging
import sys
import time
import uuid
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING

from python_sbb_polarion.testing.generic_test_case import GenericTestCase
from python_sbb_polarion.testing.project_template_uploader import ProjectTemplateUploader


if TYPE_CHECKING:
    from typing import NoReturn

    from requests import Response

    from python_sbb_polarion.core import PolarionApiV1
    from python_sbb_polarion.extensions.test_data import PolarionTestDataApi
    from python_sbb_polarion.types import JsonDict, JsonValue, SparseFields


logger = logging.getLogger(__name__)

# Standard project create/delete endpoints are asynchronous (HTTP 202): the response carries a
# job descriptor, so we poll that job (GET /jobs/{id}) until it reaches a terminal status.
POLL_INTERVAL_SECONDS: float = 2.0
POLL_MAX_ATTEMPTS: int = 60

# Terminal job status types (jobsSingleGetResponse.data.attributes.status.type in the OpenAPI spec).
JOB_STATUS_OK: str = "OK"
JOB_STATUS_FAILURES: frozenset[str] = frozenset({"FAILED", "CANCELLED"})


class TempProject:
    """Temporary Polarion project for system testing.

    Args:
        project_id: Base project ID (will be suffixed with UUID)
        project_name: Human-readable project name
        template_id: ID of the template to use
        template_location: Absolute path to template file. Use abs_path() from your
            test file to resolve relative paths:

            from python_sbb_polarion.util import abs_path

            TempProject(
                project_id="my_project",
                project_name="My Project",
                template_id="my_template",
                template_location=abs_path("test-data/template.zip"),
            )
        mutate_project_id: Whether to append a UUID suffix to project_id for uniqueness
        transform_links: mapping to transform links during template upload, e.g. {"old_project_id": "new_project_id"}
    """

    def __init__(
        self,
        project_id: str,
        project_name: str,
        template_id: str,
        template_location: Path | None = None,
        mutate_project_id: bool = True,
        transform_links: SparseFields | None = None,
    ) -> None:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

        if mutate_project_id:
            self.temp_project_id: str = f"{project_id}_st_{str(uuid.uuid4()).split('-')[-1]}"
        else:
            self.temp_project_id = project_id
        self.temp_project_name: str = project_name
        self.temp_project_template_id: str = template_id
        self.temp_project_template_location: Path | None = template_location

        # Build the API clients once up front; from here on they are always ready to use.
        self.polarion_api: PolarionApiV1 = GenericTestCase.create_polarion_api()
        self.test_data_api: PolarionTestDataApi = GenericTestCase.create_extension_api("test-data")

        self._upload_project_template(transform_links)
        self._create_temp_project()

    def get_temp_project_id(self) -> str:
        return self.temp_project_id

    def _create_temp_project(self) -> None:
        logger.debug(
            "Creating project with id '%s' and name '%s' for template with id '%s'",
            self.temp_project_id,
            self.temp_project_name,
            self.temp_project_template_id,
        )

        # A 404 here just means the project does not exist yet, so suppress the client's non-2xx warning.
        existing_response: Response = self.polarion_api.get_project(self.temp_project_id, print_error=False)
        if existing_response.status_code == HTTPStatus.OK:
            logger.info("'%s' already exists... nothing to do", self.temp_project_id)
            return

        start_time: float = time.time()
        # createProject expects a flat body (not JSON:API); projectId, trackerPrefix and
        # location are required (nullable: false in the OpenAPI schema).
        data: JsonDict = {
            "projectId": self.temp_project_id,
            "trackerPrefix": self.temp_project_id,
            "location": self.temp_project_id,
            "templateId": self.temp_project_template_id,
        }
        response: Response = self.polarion_api.create_project(data)

        # Project creation is asynchronous: the endpoint returns 202 (Accepted) with a job descriptor.
        if response.status_code != HTTPStatus.ACCEPTED:
            self._fail("creation", response)

        # Wait for the job to finish: once it reports OK the project is fully created, so the
        # name PATCH below is guaranteed to land on an existing, writable project.
        self._wait_for_job(response, "creation")

        logger.info(
            "'%s' have been created in %.2f seconds",
            self.temp_project_id,
            time.time() - start_time,
        )

        self._set_project_name()

    def _set_project_name(self) -> None:
        # createProject does not accept a project name; set it afterwards via PATCH. Best-effort.
        data: JsonDict = {
            "data": {
                "type": "projects",
                "id": self.temp_project_id,
                "attributes": {
                    "name": self.temp_project_name,
                },
            },
        }
        response: Response = self.polarion_api.update_project(self.temp_project_id, data)
        if response.status_code not in {HTTPStatus.OK, HTTPStatus.NO_CONTENT}:
            logger.warning(
                "Could not set name for project '%s' (status %s)",
                self.temp_project_id,
                response.status_code,
            )

    def _fail(self, action: str, response: Response) -> NoReturn:
        logger.error("Error during %s project '%s'", action, self.temp_project_id)
        logger.debug("Response status: %s", response.status_code)
        logger.debug("Response headers: %s", response.headers)
        logger.debug("Response content: %s", response.content)
        sys.exit(-1)

    def _wait_for_job(self, response: Response, action: str) -> None:
        """Poll the job referenced by an async 202 response until it reaches a terminal status.

        Args:
            response: The 202 (Accepted) response whose body carries the job descriptor
            action: Human-readable operation name for logging (e.g. "creation", "deletion")
        """
        job_id: str = self._job_id_from_response(response, action)
        logger.info("Waiting for %s job '%s' of project '%s'...", action, job_id, self.temp_project_id)

        for attempt in range(POLL_MAX_ATTEMPTS):
            job_body: JsonDict = self.polarion_api.get_job(job_id).json()
            status_type: str | None
            message: str | None
            status_type, message = self._job_status(job_body)
            if status_type == JOB_STATUS_OK:
                return
            if status_type in JOB_STATUS_FAILURES:
                logger.error("Job to %s project '%s' ended as %s: %s", action, self.temp_project_id, status_type, message)
                sys.exit(-1)
            if attempt < POLL_MAX_ATTEMPTS - 1:
                time.sleep(POLL_INTERVAL_SECONDS)

        logger.error("Timed out waiting for %s job '%s' of project '%s'", action, job_id, self.temp_project_id)
        sys.exit(-1)

    def _job_id_from_response(self, response: Response, action: str) -> str:
        """Extract the job id from an async 202 response body (jobsSinglePostResponse).

        Returns:
            str: The job identifier; exits the process if the body has no usable job id
        """
        body: JsonDict = response.json()
        data: JsonValue = body.get("data")
        if isinstance(data, dict):
            job_id: JsonValue = data.get("id")
            if isinstance(job_id, str) and job_id:
                return job_id
        logger.error("Unexpected async %s response for project '%s': %s", action, self.temp_project_id, body)
        sys.exit(-1)

    @staticmethod
    def _job_status(job_body: JsonDict) -> tuple[str | None, str | None]:
        """Return (status type, status message) from a job body, or (None, None) if absent.

        A still-running job has no terminal status yet, hence the optional return.
        """
        data: JsonValue = job_body.get("data")
        if not isinstance(data, dict):
            return None, None
        attributes: JsonValue = data.get("attributes")
        if not isinstance(attributes, dict):
            return None, None
        status: JsonValue = attributes.get("status")
        if not isinstance(status, dict):
            return None, None
        status_type: JsonValue = status.get("type")
        message: JsonValue = status.get("message")
        type_str: str | None = status_type if isinstance(status_type, str) else None
        message_str: str | None = message if isinstance(message, str) else None
        return type_str, message_str

    def _upload_project_template(self, transform_links: SparseFields | None = None) -> None:
        if self.temp_project_template_location is None:
            logger.warning("Template location is not configured. Skipping upload.")
            return

        uploader: ProjectTemplateUploader = ProjectTemplateUploader(test_data_api=self.test_data_api)
        uploader.upload_template(
            template_id=self.temp_project_template_id,
            template_location=self.temp_project_template_location,
            transform_links=transform_links,
        )

    def tear_down(self) -> None:
        # Delete the temporary project after testing
        start_time: float = time.time()
        response: Response = self.polarion_api.delete_project(self.temp_project_id)

        # Project deletion is asynchronous: the endpoint returns 202 (Accepted) with a job descriptor.
        if response.status_code != HTTPStatus.ACCEPTED:
            self._fail("deletion", response)

        self._wait_for_job(response, "deletion")

        logger.info("'%s' have been deleted in %.2f seconds", self.temp_project_id, time.time() - start_time)
