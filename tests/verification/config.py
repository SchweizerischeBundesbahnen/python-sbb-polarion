"""
Configuration and constants for extension API verification tests.
"""

import logging
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv


# Configure logger for this module
logger = logging.getLogger(__name__)


# =============================================================================
# Load .env file if exists (optional - for local development convenience)
# =============================================================================

_env_file = Path(__file__).parent.parent.parent / ".env"
if _env_file.exists():
    load_dotenv(_env_file)
    logger.info("Loaded environment variables from %s", _env_file)


# =============================================================================
# Configuration Constants
# =============================================================================

GITHUB_ORG = "SchweizerischeBundesbahnen"
REPO_PREFIX = "ch.sbb.polarion.extension"
OPENAPI_BRANCH = "main"  # Try 'main' first, fallback to 'master'
OPENAPI_PATH = "docs/openapi.json"
REQUEST_TIMEOUT = 10  # seconds
# Extensions to skip in GitHub-based verification (source code tests)
SKIP_EXTENSIONS_GITHUB: list[str] = []

# Extensions to skip in live Polarion verification (deployed instance tests)
SKIP_EXTENSIONS_LIVE: list[str] = [
    # Add extension names here if they should be skipped in live tests
]
VALIDATE_PARAMETERS = os.environ.get("VALIDATE_PARAMETERS", "true").lower() == "true"

# Default Polarion URL for live testing
DEFAULT_APP_URL = "https://polarion.example.com"


# =============================================================================
# Authentication
# =============================================================================

# Authentication Configuration
# Primary (Polarion - deployed extensions):
# - APP_URL: Polarion instance URL (default: https://polarion.example.com)
# - APP_TOKEN: Bearer token for Polarion API access
#
# Fallback (GitHub - source code):
# - GITHUB_TOKEN: Personal Access Token for private GitHub repos
#   (Or use 'gh auth login' - token will be auto-detected via 'gh auth token')


def _get_github_token() -> str | None:
    """Get GitHub token from environment or gh CLI."""
    # First try environment variable
    token: str | None = os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    # Fallback to gh CLI if available
    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5, check=False)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return None


GITHUB_TOKEN = _get_github_token()


# =============================================================================
# Extension Mapping
# =============================================================================

# Extension mapping: Python module name -> GitHub repo name (kebab-case)
EXTENSION_MAPPING: dict[str, str] = {
    "aad_synchronizer": "aad-synchronizer",
    "admin_utility": "admin-utility",
    "api_extender": "api-extender",
    "collection_checker": "collection-checker",
    "cucumber": "cucumber",
    "diff_tool": "diff-tool",
    "dms_doc_connector": "dms-doc-connector",
    "dms_wi_connector": "dms-wi-connector",
    "docx_exporter": "docx-exporter",
    "excel_importer": "excel-importer",
    "fake_services": "fake-services",
    "interceptor_manager": "interceptor-manager",
    "json_editor": "json-editor",
    "mailworkflow": "mailworkflow",
    "pdf_exporter": "pdf-exporter",
    "requirements_inspector": "requirements-inspector",
    "strictdoc_exporter": "strictdoc-exporter",
    "test_data": "test-data",
    "xml_repair": "xml-repair",
}

# Base methods inherited from PolarionGenericExtensionApi that should be excluded
BASE_API_METHODS: set[str] = {
    "get_context",
    "get_version",
    "get_swagger",
    "get_openapi",
}
