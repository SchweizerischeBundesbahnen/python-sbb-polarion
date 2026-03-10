import argparse
import logging
import sys
from argparse import _SubParsersAction
from typing import TYPE_CHECKING

from python_sbb_polarion.polarion_project_manager.project_manager import PolarionProjectManager


if TYPE_CHECKING:
    from pathlib import Path

    from python_sbb_polarion.testing import TempProject

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the argument parser.

    Returns:
        argparse.ArgumentParser: Configured CLI parser.
    """
    parser = argparse.ArgumentParser(
        description=("Polarion Project Template Manager - Download and create project templates."),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--template-dir",
        default="./test-data/project-template",
        help="Directory to store project templates (default: ./test-data/project-template)",
    )

    subparsers: _SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Download command
    download_parser: argparse.ArgumentParser = subparsers.add_parser("download", help="Download a project template by its ID")
    download_parser.add_argument("--project_id", required=True, help="Project ID")
    download_parser.add_argument("--project_group", required=False)
    download_parser.add_argument("--output", required=False)

    # Download command
    upload_parser: argparse.ArgumentParser = subparsers.add_parser("upload_template", help="Upload a project template")
    upload_parser.add_argument("--template_id", default="custom_project_template_for_st")
    upload_parser.add_argument("--template_path", required=False)

    # Create command
    create_parser: argparse.ArgumentParser = subparsers.add_parser("create", help="Create a temporary project from a template")
    create_parser.add_argument("--project_id", required=True)
    create_parser.add_argument("--project_name", default="E-Library")
    create_parser.add_argument("--template_id", default="custom_project_template_for_st")
    create_parser.add_argument("--template_path", required=False)

    return parser


def main() -> None:
    parser: argparse.ArgumentParser = build_parser()
    args: argparse.Namespace = parser.parse_args()

    manager: PolarionProjectManager = PolarionProjectManager(template_dir=args.template_dir)

    try:
        if args.command == "download":
            output_path: Path = manager.download_project(
                project_id=args.project_id,
                project_group=args.project_group,
                output_filename=args.output,
            )
            logger.info("Downloaded to: %s", output_path)
        elif args.command == "upload_template":
            manager.upload_template(
                template_id=args.template_id,
                template_path=args.template_path,
            )
            logger.info("Uploaded template: %s", args.template_id)
        elif args.command == "create":
            temp_project: TempProject = manager.create_project(
                template_path=args.template_path,
                template_id=args.template_id,
                project_id=args.project_id,
                project_name=args.project_name,
            )
            logger.info("Created project: %s", temp_project.temp_project_id)

    except FileNotFoundError as e:
        logger.critical("File not found: %s", e)
        sys.exit(2)
    except Exception as e:
        logger.critical("An unhandled error occurred: %s", e)
        sys.exit(1)
