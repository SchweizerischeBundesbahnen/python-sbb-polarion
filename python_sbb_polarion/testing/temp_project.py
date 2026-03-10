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
    from requests import Response

    from python_sbb_polarion.extensions.admin_utility import PolarionAdminUtilityApi
    from python_sbb_polarion.extensions.test_data import PolarionTestDataApi
    from python_sbb_polarion.types import SparseFields


logger = logging.getLogger(__name__)


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

        self._upload_project_template(transform_links)
        self._create_temp_project()

    def get_temp_project_id(self) -> str:
        return self.temp_project_id

    def _create_temp_project(self) -> None:
        admin_utility_api: PolarionAdminUtilityApi = GenericTestCase.create_extension_api("admin-utility")

        logger.debug(
            "Creating project with id '%s' and name '%s' for template with id '%s'",
            self.temp_project_id,
            self.temp_project_name,
            self.temp_project_template_id,
        )

        start_time: float = time.time()
        response: Response = admin_utility_api.create_project(
            project_id=self.temp_project_id,
            project_name=self.temp_project_name,
            template_id=self.temp_project_template_id,
        )

        if response.status_code == HTTPStatus.OK:
            logger.info(
                "'%s' have been created in %.2f seconds",
                self.temp_project_id,
                time.time() - start_time,
            )
        elif response.status_code == HTTPStatus.BAD_REQUEST and f"Project id '{self.temp_project_id}' clashes with existing project id '{self.temp_project_id}'." in response.text:
            logger.info("'%s' already exists... nothing to do", self.temp_project_id)
        else:
            logger.error("Error during creation project '%s'", self.temp_project_id)
            logger.debug("Response status: %s", response.status_code)
            logger.debug("Response headers: %s", response.headers)
            logger.debug("Response content: %s", response.content)
            sys.exit(-1)

    def _upload_project_template(self, transform_links: SparseFields | None = None) -> None:
        if self.temp_project_template_location is None:
            logger.warning("Template location is not configured. Skipping upload.")
            return

        test_data_api: PolarionTestDataApi = GenericTestCase.create_extension_api("test-data")
        uploader: ProjectTemplateUploader = ProjectTemplateUploader(test_data_api=test_data_api)
        uploader.upload_template(
            template_id=self.temp_project_template_id,
            template_location=self.temp_project_template_location,
            transform_links=transform_links,
        )

    def tear_down(self) -> None:
        # Delete the temporary project after testing
        admin_utility_api: PolarionAdminUtilityApi = GenericTestCase.create_extension_api("admin-utility")

        start_time: float = time.time()
        response: Response = admin_utility_api.delete_project(project_id=self.temp_project_id)

        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info("'%s' have been deleted in %.2f seconds", self.temp_project_id, time.time() - start_time)
        else:
            logger.error("Error during deletion project '%s'", self.temp_project_id)
            logger.debug("Response status: %s", response.status_code)
            logger.debug("Response headers: %s", response.headers)
            logger.debug("Response content: %s", response.content)
            sys.exit(-1)
