import logging
from pathlib import Path
from typing import TYPE_CHECKING

from python_sbb_polarion.testing import GenericTestCase
from python_sbb_polarion.testing.project_template_uploader import ProjectTemplateUploader
from python_sbb_polarion.testing.temp_project import TempProject


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.extensions import PolarionTestDataApi


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class PolarionProjectManager:
    """Manages download and creation of temporary Polarion project templates."""

    def __init__(self, template_dir: str | Path = "./test-data/project-template") -> None:
        """
        Initialize the Polarion Project Manager.

        Args:
            template_dir: Directory to store project templates.
        """
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Using template directory: %s", self.template_dir.resolve())

    def download_project(
        self,
        project_id: str,
        project_group: str | None = None,
        output_filename: str | None = None,
    ) -> Path:
        """
        Download a project template from Polarion.

        Args:
            project_id: The ID of the project to download.
            project_group: Optional project group identifier.
            output_filename: Optional custom output filename (without extension).

        Returns:
            Path to the downloaded template file.

        Raises:
            ValueError: If the response content is empty.
        """
        filename: str = output_filename or f"{project_id}_remote"
        output_path: Path = self.template_dir / f"{filename}.zip"

        logger.info("Downloading project '%s' to '%s'...", project_id, output_path)

        try:
            test_data_api: PolarionTestDataApi = GenericTestCase.create_extension_api("test-data")
            response: Response = test_data_api.download_project_template(
                project_id=project_id,
                project_group=project_group,
            )

            response.raise_for_status()

            if not response.content:
                raise ValueError(f"Empty content received for project '{project_id}'")

            output_path.write_bytes(response.content)
        except Exception:
            logger.exception("Failed to download project '%s'", project_id)
            raise
        else:
            logger.info("Successfully downloaded project '%s' (%d bytes)", project_id, len(response.content))
            return output_path

    @staticmethod
    def _find_first_zip_file() -> Path:
        """
        Find the first zip file in the current directory.

        Returns:
            Path to the first zip file found.

        Raises:
            FileNotFoundError: If no zip files are found in the current directory.
        """
        current_dir: Path = Path("test-data/project-template")
        zip_files: list[Path] = list(current_dir.glob("*.zip"))

        if not zip_files:
            logger.error("No zip files found in current directory")
            raise FileNotFoundError("No zip files found in current directory")

        logger.info("No template path provided, using first zip file found: %s", zip_files[0])
        return zip_files[0]

    @staticmethod
    def create_project(
        template_path: str | Path | None,
        template_id: str = "custom_project_template_for_st",
        project_id: str = "elibrary",
        project_name: str = "E-Library",
    ) -> TempProject:
        """
        Create a temporary Polarion project from a template.

        Args:
            template_path: Path to the project template zip file.
            project_id: ID for the temporary project.
            project_name: Display name for the temporary project.
            template_id: Template identifier.

        Returns:
            TempProject instance.

        Raises:
            FileNotFoundError: If template file does not exist.
        """
        if template_path is None:
            template_path = PolarionProjectManager._find_first_zip_file()

        template_file = Path(template_path)

        if not template_file.is_file():
            logger.error("Template file not found: %s", template_path)
            raise FileNotFoundError(f"No such file or directory: '{template_path}'")

        logger.info("Creating temporary project '%s' from template '%s'...", project_id, template_path)

        try:
            temp_project = TempProject(
                project_id=project_id,
                project_name=project_name,
                template_id=template_id,
                template_location=template_file,
            )
        except Exception:
            logger.exception("Failed to create project from template '%s'", template_path)
            raise
        else:
            logger.info("Successfully created temporary project: %s", temp_project.temp_project_id)
            return temp_project

    @staticmethod
    def upload_template(template_path: str | Path | None, template_id: str = "custom_project_template_for_st") -> None:
        if template_path is None:
            template_path = PolarionProjectManager._find_first_zip_file()

        test_data_api: PolarionTestDataApi = GenericTestCase.create_extension_api("test-data")
        uploader: ProjectTemplateUploader = ProjectTemplateUploader(test_data_api=test_data_api)
        uploader.upload_template(template_id=template_id, template_location=Path(template_path))
