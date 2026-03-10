"""
Parameter extraction utilities for extension API verification.
"""

from typing import Any


def extract_endpoint_parameters(operation: dict[str, Any]) -> dict[str, Any]:
    """
    Extract parameters from OpenAPI operation.

    Args:
        operation: OpenAPI operation object (e.g., from spec['paths']['/api/endpoint']['get'])

    Returns:
        Dictionary with:
        - path_params: List of path parameter names (e.g., ['id', 'projectId'])
        - query_params: List of query parameter names (e.g., ['scope', 'revision'])
        - body_schema: Request body schema (if present), or None
        - required_params: Set of required parameter names (e.g., {'id', 'projectId'})
        - all_params: Set of all parameter names (for easier comparison)
    """
    path_params: list[str] = []
    query_params: list[str] = []
    required_params: set[str] = set()

    # Extract parameters from 'parameters' list
    for param in operation.get("parameters", []):
        param_name: str = param.get("name")
        param_in: str = param.get("in")  # path, query, header, cookie
        is_required: bool = param.get("required", False)

        if param_in == "path":
            path_params.append(param_name)
        elif param_in == "query":
            query_params.append(param_name)

        if is_required:
            required_params.add(param_name)

    # Extract request body (if present)
    body_schema: dict[str, Any] | None = None
    request_body: dict[str, Any] | None = operation.get("requestBody")
    if request_body is not None:
        body_schema = request_body.get("content", {})
        # Mark as required if specified
        if request_body.get("required", False):
            required_params.add("__request_body__")  # Special marker for body

    # Combine all parameter names
    all_params: set[str] = set(path_params + query_params)

    return {
        "path_params": path_params,
        "query_params": query_params,
        "body_schema": body_schema,
        "required_params": required_params,
        "all_params": all_params,
    }
