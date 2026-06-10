"""REST API endpoint annotations for explicit OpenAPI mapping.

This module provides decorators for explicitly mapping Python methods to REST API endpoints,
enabling precise validation against OpenAPI specifications without relying on method name heuristics.
"""

import functools
import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, TypeVar


F = TypeVar("F", bound=Callable[..., Any])


def deprecated_method(replacement: str) -> Callable[[F], F]:
    """Mark a method as deprecated in favour of a standard Polarion REST API v1 method.

    Emits a ``DeprecationWarning`` (pointing at the caller) when the wrapped method is
    invoked, and records the replacement on the function as ``__deprecated_replacement__``
    for documentation and tooling. The original signature and any other attributes
    (e.g. ``__restapi_endpoint__``) are preserved via ``functools.wraps``.

    Args:
        replacement: Human-readable replacement, e.g. "PolarionApiV1.create_project"

    Returns:
        Decorator that wraps the method to emit the warning before delegating to it
    """

    def decorator(func: F) -> F:
        message: str = f"{func.__qualname__} is deprecated and will be removed in a future major release; use {replacement} instead."

        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        wrapper.__deprecated_replacement__ = replacement  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator


@dataclass
class RestApiEndpoint:
    """Metadata describing REST API endpoint mapping.

    Stores complete information about how a Python method maps to a REST API endpoint,
    including HTTP method, path, parameter mappings, and helper parameters.

    Attributes:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE)
        path: API endpoint path with {placeholders} for path parameters
        path_params: Mapping of OpenAPI path parameter names to Python parameter names
        query_params: Mapping of OpenAPI query parameter names to Python parameter names
        body_param: Name of Python parameter containing request body (for JSON requests)
        multipart_fields: Mapping of OpenAPI multipart field names to Python parameter names
        header_params: Mapping of OpenAPI header names to Python parameter names
        helper_params: List of Python parameter names that are helpers (not from OpenAPI spec)
        required_params: List of OpenAPI parameter names that are required
        response_type: Expected response type hint ("json" | "text" | "binary")
        deprecated: Whether this endpoint is deprecated in the OpenAPI spec
        naming_ok: Suppress naming suggestions - method name is intentionally non-standard

    Example:
        RestApiEndpoint(
            method="POST",
            path="/api/projects/{projectId}/documents/{documentName}",
            path_params={"projectId": "project_id", "documentName": "document_name"},
            query_params={"quantity": "quantity"},
            required_params=["projectId", "documentName"],
            response_type="text"
        )
    """

    method: str
    path: str
    path_params: dict[str, str] = field(default_factory=dict)
    query_params: dict[str, str] = field(default_factory=dict)
    body_param: str | None = None
    multipart_fields: dict[str, str] = field(default_factory=dict)
    header_params: dict[str, str] = field(default_factory=dict)
    helper_params: list[str] = field(default_factory=list)
    required_params: list[str] = field(default_factory=list)
    response_type: str | None = None
    deprecated: bool = False
    naming_ok: bool = False


def restapi_endpoint(
    method: str,
    path: str,
    *,
    path_params: dict[str, str] | None = None,
    query_params: dict[str, str] | None = None,
    body_param: str | None = None,
    multipart_fields: dict[str, str] | None = None,
    header_params: dict[str, str] | None = None,
    helper_params: list[str] | None = None,
    required_params: list[str] | None = None,
    response_type: str | None = None,
    deprecated: bool = False,
    naming_ok: bool = False,
) -> Callable[[F], F]:
    """Annotate Python method as REST API endpoint with explicit parameter mapping.

    This decorator explicitly declares how a Python method maps to a REST API endpoint,
    enabling precise validation against OpenAPI specifications. It eliminates the need
    for method name heuristics by providing complete mapping information.

    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE)
        path: API endpoint path with {placeholders} for path parameters
            Example: "/api/projects/{projectId}/documents/{documentName}"
        path_params: Mapping of OpenAPI path parameter names to Python parameter names
            Example: {"projectId": "project_id", "documentName": "document_name"}
        query_params: Mapping of OpenAPI query parameter names to Python parameter names
            Example: {"maxResults": "max_results", "offset": "offset"}
        body_param: Name of Python parameter containing request body (for JSON requests)
            Example: "export_params" for a parameter that contains the entire JSON body
        multipart_fields: Mapping of OpenAPI multipart field names to Python parameter names
            Used for file uploads. Example: {"file": "file_content"}
        header_params: Mapping of OpenAPI header names to Python parameter names
            Example: {"X-Revision": "revision", "X-Scope": "scope"}
        helper_params: List of Python parameter names that are NOT from OpenAPI spec
            These are implementation helpers (e.g., file paths, internal flags)
            Example: ["file_path"] - accepts local file path, not in API spec
        required_params: List of OpenAPI parameter names that are required
            Used to validate that required parameters don't have default values
            Example: ["projectId", "documentName"]
        response_type: Expected response type ("json" | "text" | "binary")
            Optional hint for documentation and validation
        deprecated: Whether this endpoint is deprecated in OpenAPI spec
        naming_ok: Suppress naming suggestions for this method
            Use when method name is intentionally non-standard but correct for the use case

    Returns:
        Decorated function with __restapi_endpoint__ attribute containing metadata

    Examples:
        Simple GET with path parameters:
        >>> @restapi_endpoint(
        ...     method="GET",
        ...     path="/api/projects/{projectId}/items/{itemId}",
        ...     path_params={"projectId": "project_id", "itemId": "item_id"},
        ...     required_params=["projectId", "itemId"],
        ... )
        ... def get_item(self, project_id: str, item_id: str) -> Response: ...

        POST with path and query parameters:
        >>> @restapi_endpoint(
        ...     method="POST",
        ...     path="/api/projects/{projectId}/documents/{documentName}",
        ...     path_params={"projectId": "project_id", "documentName": "document_name"},
        ...     query_params={"quantity": "quantity"},
        ...     required_params=["projectId", "documentName"],
        ...     response_type="text",
        ... )
        ... def create_document(self, project_id: str, document_name: str, quantity: int | None = None): ...

        POST with JSON body:
        >>> @restapi_endpoint(method="POST", path="/api/convert", body_param="export_params", response_type="binary")
        ... def convert(self, export_params: JsonDict) -> Response: ...

        POST with file upload and helper parameter:
        >>> @restapi_endpoint(
        ...     method="POST",
        ...     path="/api/templates/{templateId}/{templateHash}",
        ...     path_params={"templateId": "template_id", "templateHash": "template_hash"},
        ...     multipart_fields={"file": "file_content"},
        ...     helper_params=["file_path"],  # Not in OpenAPI, Python-only helper
        ...     required_params=["templateId", "templateHash"],
        ...     response_type="json",
        ... )
        ... def upload_template(self, template_id: str, file_path: str, template_hash: str): ...

        GET with header parameters:
        >>> @restapi_endpoint(
        ...     method="GET", path="/api/data", header_params={"X-Revision": "revision"}, query_params={"scope": "scope"}
        ... )
        ... def get_data(self, revision: str | None = None, scope: str | None = None): ...
    """

    def decorator(func: F) -> F:
        # Create and attach metadata to function
        metadata = RestApiEndpoint(
            method=method.upper(),
            path=path,
            path_params=path_params or {},
            query_params=query_params or {},
            body_param=body_param,
            multipart_fields=multipart_fields or {},
            header_params=header_params or {},
            helper_params=helper_params or [],
            required_params=required_params or [],
            response_type=response_type,
            deprecated=deprecated,
            naming_ok=naming_ok,
        )
        func.__restapi_endpoint__ = metadata  # type: ignore[attr-defined]
        return func

    return decorator
