"""DOCX Exporter configuration operations mixin.

This module provides DOCX-specific configuration methods.
Common methods are inherited from SharedExporterConfigurationMixin.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._shared_exporter import SharedExporterConfigurationMixin


if TYPE_CHECKING:
    from requests import Response


class ConfigurationMixin(SharedExporterConfigurationMixin):
    """DOCX Exporter configuration operations.

    Common methods inherited from SharedExporterConfigurationMixin:
    - check_cors_config() - Check CORS configuration
    - check_default_settings(scope) - Check default settings
    - check_dle_toolbar_config() - Check DLE toolbar configuration
    - check_document_properties_pane_config(scope) - Check document properties pane

    DOCX-specific methods:
    - check_pandoc() - Check Pandoc configuration
    """

    # =========================================================================
    # Configuration Checks (DOCX-specific)
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/configuration/pandoc",
        required_params=[],
        response_type="json",
    )
    def check_pandoc(self) -> Response:
        """Check Pandoc configuration.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/configuration/pandoc"
        return self.polarion_connection.api_request_get(url)
