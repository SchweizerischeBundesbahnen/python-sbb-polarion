from __future__ import annotations

import hashlib
import logging
import shutil
import sys
import tempfile
import zipfile
from http import HTTPStatus
from pathlib import Path, PurePath
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.extensions.test_data import PolarionTestDataApi

logger = logging.getLogger(__name__)


class ProjectTemplateUploader:
    """Handles uploading and managing Polarion project templates.

    Args:
        test_data_api: PolarionTestDataApi instance for API calls
    """

    def __init__(self, test_data_api: PolarionTestDataApi) -> None:
        self._test_data_api: PolarionTestDataApi = test_data_api

    @staticmethod
    def calculate_folder_hash(folder_path: Path) -> str:
        """Calculate SHA-512 hash of a folder's contents.

        Args:
            folder_path: Path to folder

        Returns:
            Hex-encoded SHA-512 hash of all files in folder
        """
        hash_sha512: hashlib._Hash = hashlib.sha512()

        # Get all files sorted by relative path for consistent hashing
        files: list[Path] = sorted(folder_path.rglob("*"))

        for file_path in files:
            if file_path.is_file():
                # Include relative path in hash for structure consistency
                rel_path: PurePath = file_path.relative_to(folder_path)
                hash_sha512.update(str(rel_path).encode("utf-8"))

                # Include file contents
                with file_path.open("rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha512.update(chunk)

        return hash_sha512.hexdigest()

    @staticmethod
    def zip_folder(folder_path: Path) -> Path:
        """Zip a folder and its contents to a temporary file.

        Args:
            folder_path: Path to folder to zip

        Returns:
            Path to created temporary zip file
        """
        if not folder_path.is_dir():
            logger.error("Path '%s' is not a directory", folder_path)
            sys.exit(1)

        with tempfile.NamedTemporaryFile(
            suffix=".zip",
            delete=False,
            mode="wb",
        ) as temp_file:
            output_zip_path: Path = Path(temp_file.name)

        logger.info("Zipping folder '%s' to '%s'...", folder_path, output_zip_path)

        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder_path.rglob("*"):
                if file_path.is_file():
                    # Create relative path for archive
                    file_name: PurePath = file_path.relative_to(folder_path)
                    zipf.write(file_path, file_name)
                    logger.debug("Added '%s' to zip", file_name)

        logger.info("Zip file created successfully: '%s'", output_zip_path)
        return output_zip_path

    @staticmethod
    def transform_workitem_links(folder_path: Path, link_mapping: dict[str, str]) -> None:
        """Transform links in all workitem.xml files by replacing strings according to mapping.
        Used to transform links to other projects (e.g. template has a link to the project "template_project_id"
        but at runtime it should point to "project_id_42" - in this case mapping like {"template_project_id": "project_id_42"}
        must be used).

        Args:
            folder_path: Path to folder containing workitem.xml files
            link_mapping: Mapping of old values to new values for replacement
        """
        workitem_files: list[Path] = list(folder_path.rglob("workitem.xml"))
        logger.info("Found %d workitem.xml files to transform", len(workitem_files))

        for workitem_file in workitem_files:
            content: str = workitem_file.read_text(encoding="utf-8")
            original_content: str = content

            for old_value, new_value in link_mapping.items():
                content = content.replace(old_value, new_value)

            if content != original_content:
                workitem_file.write_text(content, encoding="utf-8")
                logger.debug("Transformed links in '%s'", workitem_file)

    def upload_template(self, template_id: str, template_location: Path, transform_links: dict[str, str] | None = None) -> None:
        """Upload project template if it differs from server version.

        Args:
            template_id: Template identifier
            template_location: Absolute path to template folder
            transform_links: Optional mapping for link transformation e.g. {"old_project_id": "new_project_id"}
        """
        if not template_location.exists():
            logger.error("Template folder '%s' doesn't exist", template_location)
            sys.exit(1)

        zip_path: Path | None = None
        temp_folder: Path | None = None

        try:
            # Determine working folder - use temp copy if links need transformation
            if transform_links:
                temp_folder = Path(tempfile.mkdtemp())
                working_folder: Path = temp_folder / template_location.name
                logger.info("Copying template to temp folder for link transformation...")
                shutil.copytree(template_location, working_folder)
                self.transform_workitem_links(working_folder, transform_links)
            else:
                working_folder = template_location

            # Calculate hash from folder contents
            local_hash: str = self.calculate_folder_hash(folder_path=working_folder)

            response: Response = self._test_data_api.get_template_hash(template_id=template_id)

            if response.status_code == HTTPStatus.OK and local_hash == response.text:
                logger.info("Template '%s' is up-to-date. Skipping upload.", template_id)
                return

            logger.info("Template '%s' differs. Uploading new version...", template_id)

            zip_path = self.zip_folder(working_folder)

            response = self._test_data_api.save_project_template(
                template_id=template_id,
                file_path=zip_path,
                template_hash=local_hash,
            )

            if response.status_code == HTTPStatus.CREATED:
                logger.info("Template '%s' uploaded successfully", template_id)
            else:
                logger.error("Failed to upload template '%s'", template_id)
                sys.exit(1)
        finally:
            # Clean up temporary zip file if it was created
            if zip_path is not None and zip_path.exists():
                logger.debug("Cleaning up temporary zip file: '%s'", zip_path)
                zip_path.unlink()
            # Clean up temporary folder if it was created
            if temp_folder is not None and temp_folder.exists():
                logger.debug("Cleaning up temporary folder: '%s'", temp_folder)
                shutil.rmtree(temp_folder)
