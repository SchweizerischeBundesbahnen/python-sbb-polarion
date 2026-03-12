"""
OpenAPI specification fetching and parsing utilities.
"""

import inspect
import logging
import os
import re
from functools import lru_cache
from http import HTTPStatus
from typing import Any

import requests

from python_sbb_polarion.types import AuthScheme, Header, MediaType

from .config import (
    GITHUB_ORG,
    GITHUB_TOKEN,
    OPENAPI_BRANCH,
    OPENAPI_PATH,
    REPO_PREFIX,
    REQUEST_TIMEOUT,
)


logger = logging.getLogger(__name__)


class OpenAPIFetchError(Exception):
    """Exception raised when OpenAPI spec cannot be fetched."""


# =============================================================================
# OpenAPI Spec Fetching
# =============================================================================


@lru_cache(maxsize=32)
def fetch_openapi_spec(extension_name: str, repo_name: str) -> dict[str, Any] | None:
    """
    Fetch OpenAPI spec from GitHub (primary) or Polarion (experimental).

    Tries sources in order:
    1. GitHub repository (source code) - WORKING, source of truth
    2. Polarion deployed instance (if POLARION_TOKEN set) - EXPERIMENTAL, needs investigation

    Note: Polarion endpoints currently return Microsoft SSO login pages even with
    valid Bearer token. URL format needs investigation. GitHub is reliable source.

    Args:
        extension_name: Python extension name (e.g., 'pdf_exporter')
        repo_name: Repository name (e.g., 'pdf-exporter')

    Returns:
        OpenAPI specification as dictionary, or None if not found

    Raises:
        requests.exceptions.RequestException: If repository host is unreachable
    """
    # Try GitHub first (source code - reliable)
    spec: dict[str, Any] | None = _fetch_from_github(repo_name)
    if spec is not None:
        return spec

    # Experimental: Try Polarion (needs investigation - currently returns HTML login pages)
    return _fetch_from_polarion(repo_name)


def _fetch_from_polarion(extension_name: str) -> dict[str, Any] | None:
    """
    Fetch OpenAPI spec from deployed Polarion instance (FUTURE - not yet implemented).

    Future endpoint format (to be implemented):
        https://polarion.example.com/polarion/{extension-name}/rest/api/openapi.json

    Example:
        https://polarion.example.com/polarion/pdf-exporter/rest/api/openapi.json

    Note: This endpoint is not yet implemented on Polarion. When available, this will
    become the primary source for verification (deployed extensions = production reality).

    Args:
        extension_name: Extension name (e.g., 'pdf-exporter')

    Returns:
        OpenAPI specification as dictionary, or None if not available
    """
    polarion_url: str = os.environ.get("POLARION_URL", "https://polarion.example.com")
    token: str | None = os.environ.get("POLARION_TOKEN")

    if not token:
        return None  # No token, skip Polarion

    # Future endpoint format (not yet implemented)
    url: str = f"{polarion_url}/polarion/{extension_name}/rest/api/openapi.json"
    headers: dict[str, str] = {
        Header.AUTHORIZATION: f"{AuthScheme.BEARER} {token}",
    }

    try:
        response: requests.Response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code == HTTPStatus.OK:
            logger.info("Fetched OpenAPI spec from Polarion: %s", url)
            result: dict[str, Any] = response.json()
            return result
        # Expected: 404 (not yet implemented) or other errors
        logger.debug("Polarion endpoint not yet available (status %d): %s", response.status_code, url)
        return None
    except requests.exceptions.RequestException as e:
        # Network errors or endpoint not available yet
        logger.debug("Polarion fetch skipped (%s): %s", e.__class__.__name__, url)
        return None


def _fetch_from_github(repo_name: str) -> dict[str, Any] | None:
    """
    Fetch OpenAPI spec from GitHub (public or private).

    Args:
        repo_name: GitHub repository name (e.g., 'pdf-exporter')

    Returns:
        OpenAPI specification as dictionary, or None if not found
    """
    headers: dict[str, str] = {}
    if GITHUB_TOKEN:
        headers[Header.AUTHORIZATION] = f"token {GITHUB_TOKEN}"

    # Try main branch first, then master
    for branch in [OPENAPI_BRANCH, "master"]:
        url: str = f"https://raw.githubusercontent.com/{GITHUB_ORG}/{REPO_PREFIX}.{repo_name}/{branch}/{OPENAPI_PATH}"
        try:
            response: requests.Response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code == HTTPStatus.OK:
                logger.info("Fetched OpenAPI spec from GitHub: %s", url)
                result: dict[str, Any] = response.json()
                return result
            if response.status_code == HTTPStatus.NOT_FOUND:
                continue  # Try next branch
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # If it's a 404, try the next branch
            if hasattr(e, "response") and e.response is not None and e.response.status_code == HTTPStatus.NOT_FOUND:
                continue
            # For other errors, re-raise
            raise
    logger.warning("GitHub fetch failed: No OpenAPI spec found for %s", repo_name)
    return None


def fetch_openapi_from_polarion_live(extension_name: str, app_url: str, token: str) -> dict[str, Any]:
    """
    Fetch OpenAPI spec directly from a live Polarion instance.

    Args:
        extension_name: Extension name in kebab-case (e.g., 'pdf-exporter')
        app_url: Base Polarion URL (e.g., 'https://polarion.example.com')
        token: Bearer token for authentication

    Returns:
        OpenAPI specification as dictionary

    Raises:
        OpenAPIFetchError: If OpenAPI spec cannot be fetched (with descriptive message)
        requests.exceptions.RequestException: If connection fails
    """
    url: str = f"{app_url}/polarion/{extension_name}/rest/api/openapi.json"
    headers: dict[str, str] = {
        Header.AUTHORIZATION: f"{AuthScheme.BEARER} {token}",
    }

    logger.info("Fetching OpenAPI spec from: %s", url)
    response: requests.Response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

    msg: str
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        msg = f"Authentication failed (HTTP 401): Cannot authorize to {url}. Check APP_TOKEN."
        logger.warning(msg)
        raise OpenAPIFetchError(msg)

    if response.status_code == HTTPStatus.FORBIDDEN:
        msg = f"Access denied (HTTP 403): No permission to access {url}"
        logger.warning(msg)
        raise OpenAPIFetchError(msg)

    if response.status_code == HTTPStatus.NOT_FOUND:
        msg = f"Not found (HTTP 404): OpenAPI spec not available at {url}"
        logger.warning(msg)
        raise OpenAPIFetchError(msg)

    if response.status_code == HTTPStatus.OK:
        content_type: str = response.headers.get(Header.CONTENT_TYPE, "")
        if MediaType.JSON in content_type or "text/json" in content_type:
            logger.info("Successfully fetched OpenAPI spec from Polarion")
            result: dict[str, Any] = response.json()
            return result
        # Check if it's HTML (login page redirect)
        if MediaType.HTML in content_type:
            msg = f"Received HTML instead of JSON from {url} - possibly SSO login page redirect"
            logger.warning(msg)
            raise OpenAPIFetchError(msg)
        # Try to parse as JSON anyway
        try:
            result2: dict[str, Any] = response.json()
            return result2
        except requests.exceptions.JSONDecodeError as err:
            msg = f"Response from {url} is not valid JSON (Content-Type: {content_type})"
            logger.warning(msg)
            raise OpenAPIFetchError(msg) from err

    msg = f"Failed to fetch OpenAPI spec: HTTP {response.status_code} from {url}"
    logger.warning(msg)
    raise OpenAPIFetchError(msg)


# =============================================================================
# Python Method Extraction
# =============================================================================


def extract_python_methods(module_name: str) -> set[str]:
    """
    Extract all public method names from a Python extension module.

    Args:
        module_name: Python module name (e.g., 'pdf_exporter')

    Returns:
        Set of public method names (excluding base class methods)
    """
    # Import the extension module
    module_path: str = f"python_sbb_polarion.extensions.{module_name}"
    try:
        # Dynamic import
        import importlib

        module: Any = importlib.import_module(module_path)
    except ImportError:
        return set()

    # Find the API class (should be PolarionXxxApi)
    # We need to find the class that is defined in THIS module, not imported base classes
    api_class: type[Any] | None = None
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Check if the class is defined in this module (not imported)
        if obj.__module__ == module_path and name.startswith("Polarion") and name.endswith("Api"):
            api_class = obj
            break

    if not api_class:
        return set()

    # Extract public methods (not starting with _)
    # Use inspect.getmembers with inspect.ismethod on an instance to get all methods including inherited
    # But we only care about methods defined in the extension class itself, not the base class
    methods: set[str] = set()
    for name in dir(api_class):
        if name.startswith("_"):
            continue
        # Check if it's a callable method
        attr: Any = getattr(api_class, name, None)
        if callable(attr):
            methods.add(name)

    return methods


def extract_annotated_methods(module_name: str) -> dict[str, Any]:
    """
    Extract methods with @restapi_endpoint annotations from a Python extension module.

    This function looks for methods decorated with @restapi_endpoint and extracts
    their metadata for validation against OpenAPI specifications.

    IMPORTANT: This function searches for annotated methods in the entire class hierarchy,
    including base classes (e.g., PolarionGenericExtensionSettingsApi). This allows
    extensions to inherit annotated methods without needing to override them.

    Args:
        module_name: Python module name (e.g., 'pdf_exporter')

    Returns:
        Dictionary mapping method names to their RestApiEndpoint metadata
        Format: {method_name: {"method": "POST", "path": "/api/...", "metadata": RestApiEndpoint}}
        Returns empty dict if no annotated methods found
    """
    module_path: str = f"python_sbb_polarion.extensions.{module_name}"
    try:
        import importlib

        module: Any = importlib.import_module(module_path)
    except ImportError:
        return {}

    # Find the API class
    api_class: type[Any] | None = None
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module_path and name.startswith("Polarion") and name.endswith("Api"):
            api_class = obj
            break

    if not api_class:
        return {}

    # Extract methods with @restapi_endpoint annotations
    # IMPORTANT: Only extract methods that are DIRECTLY defined in the extension class
    # or have annotations DIRECTLY on the extension class's method (not inherited annotations)
    annotated_methods: dict[str, Any] = {}

    for name in dir(api_class):
        if name.startswith("_"):
            continue

        attr: Any = getattr(api_class, name, None)
        if not callable(attr) or not hasattr(attr, "__restapi_endpoint__"):
            continue

        metadata: Any = attr.__restapi_endpoint__
        annotated_methods[name] = {
            "method": metadata.method,
            "path": metadata.path,
            "metadata": metadata,
            "func": attr,
        }

    return annotated_methods


def extract_unannotated_api_methods(module_name: str) -> list[str]:
    """
    Extract methods from extension class that look like API methods but lack @restapi_endpoint.

    This helps detect when annotations are accidentally removed from convenience methods.

    Args:
        module_name: Python module name (e.g., 'pdf_exporter')

    Returns:
        List of method names that should probably have @restapi_endpoint but don't
    """
    # API method name prefixes that suggest the method maps to an endpoint
    API_PREFIXES: tuple[str, ...] = (
        "get_",
        "create_",
        "delete_",
        "update_",
        "save_",
        "find_",
        "upload_",
        "download_",
        "export_",
        "import_",
        "convert_",
        "start_",
        "cancel_",
        "check_",
        "validate_",
        "receive_",
        "persist_",
        "clear_",
        "rename_",
        "diff_",
        "merge_",
    )

    module_path: str = f"python_sbb_polarion.extensions.{module_name}"
    try:
        import importlib

        module: Any = importlib.import_module(module_path)
    except ImportError:
        return []

    # Find the API class
    api_class: type[Any] | None = None
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module_path and name.startswith("Polarion") and name.endswith("Api"):
            api_class = obj
            break

    if not api_class:
        return []

    # Get methods defined directly in the extension class (not inherited)
    own_methods: set[str] = set(api_class.__dict__.keys())

    unannotated_api_methods: list[str] = []
    for name in own_methods:
        if name.startswith("_"):
            continue

        attr: Any = getattr(api_class, name, None)
        if not callable(attr):
            continue

        # Check if method name suggests it's an API method
        if not any(name.startswith(prefix) for prefix in API_PREFIXES):
            continue

        # Check if method has @restapi_endpoint
        if hasattr(attr, "__restapi_endpoint__"):
            continue

        # Skip wrapper methods (methods that just delegate to another method)
        # Detected by "wrapper" in docstring
        docstring: str = getattr(attr, "__doc__", "") or ""
        if "wrapper" in docstring.lower():
            continue

        # Method looks like API but lacks annotation
        unannotated_api_methods.append(name)

    return unannotated_api_methods


# =============================================================================
# Annotation Validation
# =============================================================================


# Mapping from api_request_* method names to HTTP methods
API_REQUEST_METHOD_MAP: dict[str, str] = {
    "api_request_get": "GET",
    "api_request_post": "POST",
    "api_request_put": "PUT",
    "api_request_patch": "PATCH",
    "api_request_delete": "DELETE",
}


def validate_implementation_http_method(method_func: Any, annotated_method: str) -> str | None:
    """
    Validate that the actual api_request_* call in method body matches the annotated HTTP method.

    Analyzes the source code of the method to find api_request_* calls and verifies
    they match the HTTP method declared in @restapi_endpoint annotation.

    Args:
        method_func: The actual method function object
        annotated_method: The HTTP method from @restapi_endpoint annotation (e.g., "GET", "POST")

    Returns:
        Error message if mismatch found, None if valid or cannot be determined
    """
    try:
        source: str = inspect.getsource(method_func)
    except (OSError, TypeError):
        # Cannot get source code (e.g., built-in, C extension)
        return None

    # Find all api_request_* calls in the source
    found_methods: list[str] = []
    for api_method, http_method in API_REQUEST_METHOD_MAP.items():
        # Match patterns like: .api_request_get( or polarion_connection.api_request_get(
        if re.search(rf"\.{api_method}\s*\(", source):
            found_methods.append(http_method)

    if not found_methods:
        # No api_request_* calls found - might be a wrapper method
        return None

    # Check if any found method doesn't match the annotation
    mismatched: list[str] = [m for m in found_methods if m != annotated_method]

    if mismatched:
        return f"HTTP method implementation mismatch: annotation declares {annotated_method}, but method body calls api_request_{mismatched[0].lower()}()"

    return None


def validate_annotation_against_openapi(_method_name: str, annotation_data: dict[str, Any], openapi_endpoint: dict[str, Any]) -> list[str]:
    """
    Validate that method annotation matches OpenAPI endpoint specification.

    Args:
        method_name: Name of the Python method
        annotation_data: Dict with "method", "path", "metadata" keys from @restapi_endpoint
        openapi_endpoint: OpenAPI endpoint dict with "method", "path", "parameters" keys

    Returns:
        List of validation error messages (empty if valid)
    """
    issues: list[str] = []
    metadata: Any = annotation_data["metadata"]

    # 1. Validate HTTP method matches
    if openapi_endpoint["method"] != metadata.method:
        issues.append(f"HTTP method mismatch: OpenAPI={openapi_endpoint['method']}, annotation={metadata.method}")

    # 2. Validate path matches
    if openapi_endpoint["path"] != metadata.path:
        issues.append(f"Path mismatch: OpenAPI={openapi_endpoint['path']}, annotation={metadata.path}")

    openapi_params: dict[str, Any] = openapi_endpoint.get("parameters", {})

    # 3. Validate all OpenAPI path parameters are mapped
    openapi_path_params: set[str] = set(openapi_params.get("path_params", []))
    annotated_path_params: set[str] = set(metadata.path_params.keys())

    missing_path: set[str] = openapi_path_params - annotated_path_params
    if missing_path:
        issues.append(f"Missing path parameter mappings: {missing_path}")

    extra_path: set[str] = annotated_path_params - openapi_path_params
    if extra_path:
        issues.append(f"Extra path parameters in annotation: {extra_path}")

    # 4. Validate all OpenAPI query parameters are mapped
    openapi_query_params: set[str] = set(openapi_params.get("query_params", []))
    annotated_query_params: set[str] = set(metadata.query_params.keys())

    missing_query: set[str] = openapi_query_params - annotated_query_params
    if missing_query:
        issues.append(f"Missing query parameter mappings: {missing_query}")

    extra_query: set[str] = annotated_query_params - openapi_query_params
    if extra_query:
        issues.append(f"Extra query parameters in annotation: {extra_query}")

    # 5. Validate required parameters are marked correctly
    openapi_required: set[str] = set(openapi_params.get("required_params", []))
    annotated_required: set[str] = set(metadata.required_params)

    # Handle __request_body__ special marker:
    # - __request_body__ is a synthetic marker indicating a request body is expected
    # - If annotation has body_param or multipart_fields, the body is handled correctly
    # - Remove from both sets to avoid false positives in either direction
    if metadata.body_param or metadata.multipart_fields:
        openapi_required -= {"__request_body__"}
        annotated_required -= {"__request_body__"}

    missing_required: set[str] = openapi_required - annotated_required
    if missing_required:
        issues.append(f"Required parameters not marked in annotation: {missing_required}")

    extra_required: set[str] = annotated_required - openapi_required
    if extra_required:
        issues.append(f"Parameters marked as required but optional in OpenAPI: {extra_required}")

    return issues


# =============================================================================
# OpenAPI Endpoint Extraction
# =============================================================================


def extract_api_endpoints(openapi_spec: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Extract REST endpoints from OpenAPI specification.

    Args:
        openapi_spec: OpenAPI specification dictionary

    Returns:
        List of endpoint dictionaries with 'path', 'method', 'operation_id', 'summary', and 'parameters'
    """
    from .parameter_utils import extract_endpoint_parameters

    if not openapi_spec or "paths" not in openapi_spec:
        return []

    endpoints: list[dict[str, Any]] = []
    for path, path_item in openapi_spec["paths"].items():
        for method, operation in path_item.items():
            # Skip non-HTTP methods
            if method.upper() not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
                continue

            endpoint: dict[str, Any] = {
                "path": path,
                "method": method.upper(),
                "operation_id": operation.get("operationId", ""),
                "summary": operation.get("summary", ""),
                "parameters": extract_endpoint_parameters(operation),
            }
            endpoints.append(endpoint)

    return endpoints


# =============================================================================
# Method Name Generation
# =============================================================================


def endpoint_to_method_name(path: str, method: str, operation_id: str = "") -> str:
    """
    Convert REST endpoint path+method to expected Python method name.

    Args:
        path: REST API path (e.g., '/api/convert')
        method: HTTP method (e.g., 'GET', 'POST')
        operation_id: OpenAPI operation ID (if available)

    Returns:
        Expected Python method name (e.g., 'convert', 'get_status')
    """
    # If operation_id is provided and looks like a Python method name, use it
    if operation_id:
        # Convert camelCase to snake_case
        operation_id = re.sub(r"(?<!^)(?=[A-Z])", "_", operation_id).lower()
        return operation_id

    # Remove base path and leading/trailing slashes
    path = re.sub(r"^/?(polarion/[^/]+/)?rest/api/?", "", path)
    path = path.strip("/")

    # Replace path parameters with generic names
    path = re.sub(r"\{[^}]+\}", "id", path)

    # Convert path to snake_case
    parts: list[str] = path.split("/")
    parts = [re.sub(r"[-\s]+", "_", part.lower()) for part in parts if part]

    # Add method prefix for non-standard verbs
    if method in ["POST", "PUT", "PATCH"] and len(parts) > 0:
        # Check if the last part suggests an action
        last_part: str = parts[-1]
        if last_part not in ["jobs", "status", "result"]:
            # For POST/PUT/PATCH, typically the last part is the action
            pass
    elif method == "GET" and len(parts) > 1:
        # For GET, prepend 'get_' if not already descriptive
        if not any(verb in parts[0] for verb in ["get", "fetch", "list", "find"]):
            parts = ["get"] + parts
    elif method == "DELETE":
        parts = ["delete"] + parts

    return "_".join(parts)


def generate_method_variations(path: str, method: str, operation_id: str = "") -> list[str]:
    """
    Generate multiple possible Python method name variations for an endpoint.

    This accounts for different naming conventions used across extensions.

    Args:
        path: REST API path
        method: HTTP method
        operation_id: OpenAPI operation ID

    Returns:
        List of possible method name variations
    """
    variations: list[str] = []

    # Primary method name from operation_id or path
    primary_name: str = endpoint_to_method_name(path, method, operation_id)
    variations.append(primary_name)

    # Remove common prefixes/suffixes for variations
    for prefix in ["get_", "post_", "put_", "delete_", "create_", "update_"]:
        if primary_name.startswith(prefix):
            without_prefix: str = primary_name[len(prefix) :]
            if without_prefix:  # Make sure we don't add empty string
                variations.append(without_prefix)

    # Handle special cases based on operation_id if available
    if operation_id:
        # Convert camelCase to snake_case (handle acronyms like CORS properly)
        # First insert underscore before sequences of capitals followed by lowercase
        step1: str = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", operation_id)
        # Then insert underscore before capital letters
        snake_case: str = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", step1).lower()
        variations.append(snake_case)

        # Try without common verb prefixes from operation_id
        for verb in ["get", "create", "update", "delete", "post", "put", "patch", "fetch", "read", "save", "remove", "check", "convert", "upload"]:
            if snake_case.startswith(verb + "_"):
                variations.append(snake_case[len(verb) + 1 :])
                # Also try with different prefix
                if verb == "check":
                    variations.append(f"get_{snake_case[len(verb) + 1 :]}")
                    variations.append(f"validate_{snake_case[len(verb) + 1 :]}")

        # Try without common suffix patterns (e.g., "convertHtmlToPdf" -> "convert_html")
        for suffix_pattern in ["_to_pdf", "_to_docx", "_to_html", "_to_xml"]:
            if snake_case.endswith(suffix_pattern):
                without_suffix: str = snake_case[: -len(suffix_pattern)]
                variations.append(without_suffix)

    # Generate full path-based method name (e.g., "settings_localization_upload")
    # This handles cases where methods are named after the full endpoint path
    path_parts: list[str] = [p for p in path.split("/") if p and not p.startswith("{") and p != "api"]
    if len(path_parts) >= 2:
        # Join all path parts with underscores (e.g., ["settings", "localization", "upload"] -> "settings_localization_upload")
        full_path_name: str = "_".join(p.replace("-", "_") for p in path_parts)
        variations.append(full_path_name)

        # Also try with HTTP method prefix for full path names
        if method == "GET":
            variations.append(f"get_{full_path_name}")
        elif method == "POST":
            variations.append(f"post_{full_path_name}")
            variations.append(f"create_{full_path_name}")
        elif method == "PUT":
            variations.append(f"save_{full_path_name}")
            variations.append(f"update_{full_path_name}")
        elif method == "DELETE":
            variations.append(f"delete_{full_path_name}")

    # Extract the last meaningful part of path as a simple method name
    if path_parts:
        last_part: str = path_parts[-1].replace("-", "_")
        variations.append(last_part)
        # Also try with method prefix
        if method == "GET":
            variations.append(f"get_{last_part}")
        elif method == "POST":
            variations.append(f"post_{last_part}")
            variations.append(f"create_{last_part}")
            variations.append(f"start_{last_part}")
        elif method == "DELETE":
            variations.append(f"delete_{last_part}")
        elif method == "PUT":
            variations.append(f"save_{last_part}")
            variations.append(f"update_{last_part}")

    # Handle job-related endpoints
    if "job" in primary_name and method == "POST":
        variations.extend(
            [
                primary_name.replace("post_", "start_"),
                primary_name.replace("post_", "create_"),
                primary_name.replace("create_", "start_"),
            ]
        )

    # Handle status/result endpoints
    if "status" in path.lower():
        base_status: str = primary_name.replace("get_", "").replace("_status", "")
        variations.extend([f"{base_status}_status", f"get_{base_status}_status", f"{base_status}_job_status"])
    if "result" in path.lower():
        base_result: str = primary_name.replace("get_", "").replace("_result", "")
        variations.extend([f"{base_result}_result", f"get_{base_result}_result", f"{base_result}_job_result"])

    # Clean up and remove duplicates, empty strings
    variations = [v for v in variations if v and not v.startswith("_")]
    return list(set(variations))


# =============================================================================
# PolarionApiV1 Method Extraction
# =============================================================================


def extract_polarion_api_v1_annotated_methods() -> dict[str, Any]:
    """
    Extract methods with @restapi_endpoint annotations from PolarionApiV1.

    This function looks for methods decorated with @restapi_endpoint and extracts
    their metadata for validation against polarion-openapi.json.

    Returns:
        Dictionary mapping method names to their RestApiEndpoint metadata
        Format: {method_name: {"method": "POST", "path": "/projects/...", "metadata": RestApiEndpoint}}
        Returns empty dict if no annotated methods found
    """
    try:
        from python_sbb_polarion.core.polarion_api import PolarionApiV1
    except ImportError:
        return {}

    annotated_methods: dict[str, Any] = {}

    for name in dir(PolarionApiV1):
        if name.startswith("_"):
            continue

        attr: Any = getattr(PolarionApiV1, name, None)
        if not callable(attr) or not hasattr(attr, "__restapi_endpoint__"):
            continue

        metadata: Any = attr.__restapi_endpoint__
        annotated_methods[name] = {
            "method": metadata.method,
            "path": metadata.path,
            "metadata": metadata,
            "func": attr,
        }

    return annotated_methods


def extract_polarion_api_v1_unannotated_methods() -> list[str]:
    """
    Extract public methods from PolarionApiV1 that lack @restapi_endpoint.

    All public methods in PolarionApiV1 should have @restapi_endpoint annotation
    since they all correspond to OpenAPI spec endpoints.

    Returns:
        List of method names that are missing @restapi_endpoint
    """
    try:
        from python_sbb_polarion.core.polarion_api import PolarionApiV1
    except ImportError:
        return []

    unannotated_methods: list[str] = []

    for name in dir(PolarionApiV1):
        if name.startswith("_"):
            continue

        attr: Any = getattr(PolarionApiV1, name, None)
        if not callable(attr):
            continue

        # Check if method has @restapi_endpoint
        if hasattr(attr, "__restapi_endpoint__"):
            continue

        unannotated_methods.append(name)

    return unannotated_methods
