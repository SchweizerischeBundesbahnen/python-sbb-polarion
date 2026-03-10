"""Shared configuration mixin for PDF and DOCX exporters.

This module provides common configuration check methods shared between exporters.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class SharedExporterConfigurationMixin(BaseMixin):
    """Shared configuration operations.

    This mixin provides common methods for:
    - CORS configuration check
    - Default settings check
    - DLE toolbar configuration check
    - Document properties pane configuration check
    """

    # =========================================================================
    # Configuration Checks (Shared)
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/configuration/cors-config",
        required_params=[],
        response_type="json",
    )
    def check_cors_config(self) -> Response:
        """Check CORS configuration.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/configuration/cors-config"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/configuration/default-settings",
        query_params={
            "scope": "scope",
        },
        required_params=[],
        response_type="json",
    )
    def check_default_settings(self, scope: str | None = None) -> Response:
        """Check default settings configuration.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/configuration/default-settings"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/api/configuration/dle-toolbar-config",
        required_params=[],
        response_type="json",
    )
    def check_dle_toolbar_config(self) -> Response:
        """Check DLE toolbar configuration.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/configuration/dle-toolbar-config"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/configuration/document-properties-pane-config",
        query_params={
            "scope": "scope",
        },
        required_params=[],
        response_type="json",
    )
    def check_document_properties_pane_config(self, scope: str | None = None) -> Response:
        """Check document properties pane configuration.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/configuration/document-properties-pane-config"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_get(url, params=params or None)
