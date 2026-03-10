"""
CLI entry point for extension API verification tests.

Usage:
    # Run GitHub-based tests (default)
    uv run python -m tests.verification

    # Run live Polarion tests for all extensions
    export APP_TOKEN='your-token'
    uv run python -m tests.verification --live

    # Run live test for single extension
    uv run python -m tests.verification --live --extension pdf-exporter

    # Run live test with custom URL
    uv run python -m tests.verification --live --app_url https://polarion.example.com --app_token 'token' --extension pdf-exporter

    # Run method naming validation
    uv run python -m tests.verification --naming
    uv run python -m tests.verification --naming --extension pdf-exporter
    uv run python -m tests.verification --naming --verbose  # Include OK methods

    # List available extensions
    uv run python -m tests.verification --list
"""

import argparse
import logging
import os
import sys
import unittest

from .config import DEFAULT_APP_URL, EXTENSION_MAPPING
from .method_naming import ExtensionNamingReport, format_naming_report, validate_extension_naming
from .test_github import GitHubAPIVerificationTest
from .test_polarion_live import PolarionLiveAPIVerificationTest


logger = logging.getLogger(__name__)


def run_naming_validation(extension: str | None = None, verbose: bool = False, json_output: bool = False) -> bool:
    """
    Run method naming validation for extension(s).

    Args:
        extension: Extension name (kebab-case) or None for all
        verbose: Include OK methods in output
        json_output: Output as JSON instead of text

    Returns:
        True if all validations passed (no errors), False otherwise
    """
    import json

    from .method_naming import format_naming_report_json

    extensions_to_check: list[str]

    if extension:
        # Convert kebab-case to snake_case
        extension_snake: str = extension.replace("-", "_")

        if extension_snake not in EXTENSION_MAPPING and extension not in EXTENSION_MAPPING.values():
            logger.error("Unknown extension '%s'", extension)
            logger.info("Available extensions: %s", ", ".join(sorted(EXTENSION_MAPPING.values())))
            return False

        # Use snake_case for internal lookup
        if extension_snake in EXTENSION_MAPPING:
            extensions_to_check = [extension_snake]
        else:
            # Find by repo name
            extensions_to_check = [k for k, v in EXTENSION_MAPPING.items() if v == extension]
    else:
        extensions_to_check = list(EXTENSION_MAPPING.keys())

    all_passed: bool = True
    all_reports: list[ExtensionNamingReport] = []

    for ext in sorted(extensions_to_check):
        report: ExtensionNamingReport = validate_extension_naming(ext)
        all_reports.append(report)

        if report.error_count > 0:
            all_passed = False

    if json_output:
        output: dict[str, object] = {
            "extensions": [format_naming_report_json(r) for r in all_reports],
            "summary": {
                "total_extensions": len(all_reports),
                "total_methods": sum(len(r.results) for r in all_reports),
                "total_errors": sum(r.error_count for r in all_reports),
                "total_warnings": sum(r.warning_count for r in all_reports),
                "total_suggestions": sum(r.suggestion_count for r in all_reports),
            },
        }
        logger.info(json.dumps(output, indent=2))
    else:
        for report in all_reports:
            logger.info(format_naming_report(report, verbose=verbose))

        # Overall summary
        logger.info("\n%s", "=" * 80)
        logger.info("Overall Summary")
        logger.info("=" * 80)
        logger.info("Extensions checked: %d", len(all_reports))
        logger.info("Total methods:      %d", sum(len(r.results) for r in all_reports))
        logger.info("Total errors:       %d", sum(r.error_count for r in all_reports))
        logger.info("Total warnings:     %d", sum(r.warning_count for r in all_reports))
        logger.info("Total suggestions:  %d", sum(r.suggestion_count for r in all_reports))

    return all_passed


def run_live_verification(extension: str | None = None, app_url: str | None = None, app_token: str | None = None) -> None:
    """
    Run live Polarion API verification from command line.

    Args:
        extension: Extension name (kebab-case, e.g., 'pdf-exporter') or None for all
        app_url: Polarion URL or None to use APP_URL env var
        app_token: Bearer token or None to use APP_TOKEN env var
    """
    # Set environment variables if provided
    if app_url:
        os.environ["APP_URL"] = app_url
    if app_token:
        os.environ["APP_TOKEN"] = app_token

    # Validate token is available
    token: str | None = os.environ.get("APP_TOKEN")
    if not token:
        logger.error("APP_TOKEN is required. Set it via environment variable or --app_token argument.")
        logger.info("Usage:")
        logger.info("  export APP_TOKEN='your-token-here'")
        logger.info("  uv run python -m tests.verification --live --extension pdf-exporter")
        logger.info("Or:")
        logger.info("  uv run python -m tests.verification --live --app_token 'your-token' --extension pdf-exporter")
        return

    if extension:
        # Convert kebab-case to snake_case for test lookup
        extension_snake: str = extension.replace("-", "_")

        # Validate extension exists
        if extension_snake not in EXTENSION_MAPPING and extension not in EXTENSION_MAPPING.values():
            logger.error("Unknown extension '%s'", extension)
            logger.info("Available extensions: %s", ", ".join(sorted(EXTENSION_MAPPING.values())))
            return

        # Run single test
        test_name: str = f"test_{extension_snake}_completeness_live"
        suite: unittest.TestSuite = unittest.TestSuite()
        suite.addTest(PolarionLiveAPIVerificationTest(test_name))
        runner: unittest.TextTestRunner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    else:
        # Run all live tests
        loader: unittest.TestLoader = unittest.TestLoader()
        suite2: unittest.TestSuite = loader.loadTestsFromTestCase(PolarionLiveAPIVerificationTest)
        runner2: unittest.TextTestRunner = unittest.TextTestRunner(verbosity=2)
        runner2.run(suite2)


def run_github_verification(extension: str | None = None) -> bool:
    """
    Run GitHub-based API verification from command line.

    Args:
        extension: Extension name (kebab-case, e.g., 'pdf-exporter') or None for all

    Returns:
        True if all tests passed, False otherwise
    """
    if extension:
        # Convert kebab-case to snake_case for test lookup
        extension_snake: str = extension.replace("-", "_")

        # Validate extension exists
        if extension_snake not in EXTENSION_MAPPING and extension not in EXTENSION_MAPPING.values():
            logger.error("Unknown extension '%s'", extension)
            logger.info("Available extensions: %s", ", ".join(sorted(EXTENSION_MAPPING.values())))
            return False

        # Run single test
        test_name: str = f"test_{extension_snake}_completeness"
        suite: unittest.TestSuite = unittest.TestSuite()
        suite.addTest(GitHubAPIVerificationTest(test_name))
        runner: unittest.TextTestRunner = unittest.TextTestRunner(verbosity=2)
        result: unittest.result.TestResult = runner.run(suite)
        return result.wasSuccessful()
    # Run all GitHub tests
    loader: unittest.TestLoader = unittest.TestLoader()
    suite2: unittest.TestSuite = loader.loadTestsFromTestCase(GitHubAPIVerificationTest)
    runner2: unittest.TextTestRunner = unittest.TextTestRunner(verbosity=2)
    result2: unittest.result.TestResult = runner2.run(suite2)
    return result2.wasSuccessful()


def main() -> None:
    """Main CLI entry point."""
    # Configure logging for CLI output
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(
        description="Extension API Verification Tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run GitHub-based tests (default)
  uv run python -m tests.verification

  # Run GitHub test for single extension
  uv run python -m tests.verification --extension pdf-exporter

  # Run live Polarion tests for all extensions
  export APP_TOKEN='your-token'
  uv run python -m tests.verification --live

  # Run live test for single extension
  uv run python -m tests.verification --live --extension pdf-exporter

  # Run live test with custom URL
  uv run python -m tests.verification --live --app_url https://polarion.example.com --app_token 'token' --extension pdf-exporter

  # Run method naming validation
  uv run python -m tests.verification --naming
  uv run python -m tests.verification --naming --extension pdf-exporter
  uv run python -m tests.verification --naming --verbose
  uv run python -m tests.verification --naming --json

  # List available extensions
  uv run python -m tests.verification --list
        """,
    )
    parser.add_argument("--live", action="store_true", help="Run tests against live Polarion instance")
    parser.add_argument("--naming", action="store_true", help="Run method naming validation")
    parser.add_argument("--app_url", type=str, default=None, help=f"Polarion URL (default: {DEFAULT_APP_URL})")
    parser.add_argument("--app_token", type=str, default=None, help="Polarion Bearer token (or set APP_TOKEN env var)")
    parser.add_argument("--extension", "-e", type=str, default=None, help="Single extension to test (kebab-case, e.g., 'pdf-exporter')")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output (include OK methods in naming report)")
    parser.add_argument("--json", action="store_true", help="Output as JSON (for naming validation)")
    parser.add_argument("--list", action="store_true", help="List available extensions")

    args: argparse.Namespace = parser.parse_args()

    if args.list:
        logger.info("Available extensions:")
        for python_name, repo_name in sorted(EXTENSION_MAPPING.items()):
            logger.info("  %s (module: %s)", repo_name.ljust(25), python_name)
    elif args.naming:
        success: bool = run_naming_validation(extension=args.extension, verbose=args.verbose, json_output=args.json)
        if not success:
            sys.exit(1)
    elif args.live:
        run_live_verification(extension=args.extension, app_url=args.app_url, app_token=args.app_token)
    else:
        success2: bool = run_github_verification(extension=args.extension)
        if not success2:
            sys.exit(1)


if __name__ == "__main__":
    main()
