from __future__ import annotations

import logging
import time
import uuid
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING

from python_sbb_polarion.core import ExtensionApiFactory
from python_sbb_polarion.testing.errors import TempProjectError
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
POLL_INTERVAL_SECONDS: float = 1.0
POLL_MAX_ATTEMPTS: int = 120

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
        parent_location: Repository folder (project group) to create the project under. The project id
            is appended to it, so e.g. parent_location="Demo Projects" places the project at
            "Demo Projects/<project_id>" and thus inside the "Demo Projects" project group. When omitted
            the project is created at the repository root (location == project id), preserving the
            previous default behaviour.
    """

    def __init__(
        self,
        project_id: str,
        project_name: str,
        template_id: str,
        template_location: Path | None = None,
        mutate_project_id: bool = True,
        transform_links: SparseFields | None = None,
        parent_location: str | None = None,
    ) -> None:
        logging.basicConfig(level=logging.INFO, format="%(message)s")

        if mutate_project_id:
            self.temp_project_id: str = f"{project_id}_st_{str(uuid.uuid4()).split('-')[-1]}"
        else:
            self.temp_project_id = project_id
        self.temp_project_name: str = project_name
        self.temp_project_template_id: str = template_id
        self.temp_project_template_location: Path | None = template_location
        # A project's project-group membership is derived from its location in the repository tree.
        # Nest the project under parent_location when a non-blank value is given (so group-scoped
        # behaviour applies); a missing, empty or whitespace-only value intentionally keeps the
        # project at the root using the bare project id. Surrounding whitespace and trailing
        # slashes are stripped so the resulting location never contains a doubled separator.
        normalized_parent: str = (parent_location or "").strip().rstrip("/")
        if normalized_parent:
            self.temp_project_location: str = f"{normalized_parent}/{self.temp_project_id}"
        else:
            self.temp_project_location = self.temp_project_id

        # Build the API clients once up front, sharing a single connection: the test-data extension
        # client is derived from the standard API's connection instead of opening a second one.
        self.polarion_api: PolarionApiV1 = GenericTestCase.create_polarion_api()
        self.test_data_api: PolarionTestDataApi = ExtensionApiFactory.get_extension_api_by_name(
            extension_name="test-data",
            polarion_connection=self.polarion_api.polarion_connection,
        )

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
            logger.info("'%s' already exists... nothing to do", self.temp_project_location)
            return
        # Anything other than "exists" (200) or "not found" (404) is an obstacle (auth, server error)
        # that creation would not solve - surface it here with the real status instead of falling through.
        if existing_response.status_code != HTTPStatus.NOT_FOUND:
            self._fail("look up", existing_response)

        start_time: float = time.time()
        # createProject expects a flat body (not JSON:API); projectId, trackerPrefix and
        # location are required (nullable: false in the OpenAPI schema).
        data: JsonDict = {
            "projectId": self.temp_project_id,
            "trackerPrefix": self.temp_project_id,
            "location": self.temp_project_location,
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
            self.temp_project_location,
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
        if response.status_code != HTTPStatus.NO_CONTENT:
            logger.warning(
                "Could not set name for project '%s' (status %s)",
                self.temp_project_location,
                response.status_code,
            )

    def _fail(self, action: str, response: Response) -> NoReturn:
        logger.error("Error during %s project '%s'", action, self.temp_project_location)
        logger.debug("Response status: %s", response.status_code)
        logger.debug("Response headers: %s", response.headers)
        logger.debug("Response content: %s", response.content)
        raise TempProjectError(f"Failed to {action} project '{self.temp_project_location}' (HTTP {response.status_code})")

    def _wait_for_job(self, response: Response, action: str) -> None:
        """Poll the job referenced by an async 202 response until it reaches a terminal status.

        Args:
            response: The 202 (Accepted) response whose body carries the job descriptor
            action: Human-readable operation name for logging (e.g. "creation", "deletion")

        Raises:
            TempProjectError: If the job fails, is cancelled, or never reaches a terminal status
        """
        job_id: str = self._job_id_from_response(response, action)
        logger.info("Waiting for %s job '%s' of project '%s'...", action, job_id, self.temp_project_location)

        for attempt in range(POLL_MAX_ATTEMPTS):
            job_response: Response = self.polarion_api.get_job(job_id)
            # A non-200 or non-JSON poll (transient 5xx, gateway/SSO HTML page) is treated as
            # "not ready yet" rather than crashing: we keep polling and, if it persists, time out
            # with a clean TempProjectError instead of leaking a raw requests/JSON exception.
            job_body: JsonDict
            if job_response.status_code == HTTPStatus.OK:
                job_body = self._safe_json(job_response)
            else:
                logger.debug("Poll of %s job '%s' returned HTTP %s; retrying", action, job_id, job_response.status_code)
                job_body = {}
            status_type: str | None
            message: str | None
            status_type, message = self._job_status(job_body)
            if status_type == JOB_STATUS_OK:
                return
            if status_type in JOB_STATUS_FAILURES:
                raise TempProjectError(f"Job to {action} project '{self.temp_project_location}' ended as {status_type}: {message}")
            if attempt < POLL_MAX_ATTEMPTS - 1:
                time.sleep(POLL_INTERVAL_SECONDS)

        raise TempProjectError(f"Timed out waiting for {action} job '{job_id}' of project '{self.temp_project_location}'")

    @staticmethod
    def _safe_json(response: Response) -> JsonDict:
        """Parse a response body as a JSON object, returning {} for non-JSON or non-object bodies.

        Returns:
            JsonDict: The parsed object, or an empty dict if the body is not a JSON object
        """
        try:
            parsed: JsonValue = response.json()
        except ValueError:
            # requests raises JSONDecodeError (a ValueError subclass) for HTML/empty bodies.
            return {}
        if isinstance(parsed, dict):
            return parsed
        return {}

    def _job_id_from_response(self, response: Response, action: str) -> str:
        """Extract the job id from an async 202 response body (jobsSinglePostResponse).

        Returns:
            str: The job identifier

        Raises:
            TempProjectError: If the body has no usable job id
        """
        body: JsonDict = self._safe_json(response)
        data: JsonValue = body.get("data")
        if isinstance(data, dict):
            job_id: JsonValue = data.get("id")
            if isinstance(job_id, str) and job_id:
                return job_id
        logger.error("Unexpected async %s response for project '%s': %s", action, self.temp_project_location, body)
        raise TempProjectError(f"Async {action} response for project '{self.temp_project_location}' carried no job id")

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

        logger.info("'%s' have been deleted in %.2f seconds", self.temp_project_location, time.time() - start_time)
