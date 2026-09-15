"""PDF Exporter configuration operations mixin.

This module provides PDF-specific configuration methods.
Common methods are inherited from SharedExporterConfigurationMixin.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._shared_exporter import SharedExporterConfigurationMixin


if TYPE_CHECKING:
    from requests import Response


class ConfigurationMixin(SharedExporterConfigurationMixin):
    """PDF Exporter configuration operations.

    Common methods inherited from SharedExporterConfigurationMixin:
    - check_cors_config() - Check CORS configuration
    - check_default_settings(scope) - Check default settings
    - check_dle_toolbar_config() - Check DLE toolbar configuration
    - check_document_properties_pane_config(scope) - Check document properties pane

    PDF-specific methods:
    - check_live_report_config() - Check live report configuration
    - check_weasyprint() - Check weasyprint configuration
    - check_bulk_processing() - Check bulk processing service configuration
    - get_bulk_processing_service_status() - Check bulk processing service availability
    """

    # =========================================================================
    # Configuration Checks (PDF-specific)
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/configuration/live-report-config",
        required_params=[],
        response_type="json",
    )
    def check_live_report_config(self) -> Response:
        """Check live report configuration.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/configuration/live-report-config"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/configuration/weasyprint",
        required_params=[],
        response_type="json",
    )
    def check_weasyprint(self) -> Response:
        """Check weasyprint configuration.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/configuration/weasyprint"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/configuration/bulk-processing",
        required_params=[],
        response_type="json",
    )
    def check_bulk_processing(self) -> Response:
        """Check bulk processing service configuration.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/configuration/bulk-processing"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/bulk-processing/status",
        required_params=[],
        response_type="json",
    )
    def get_bulk_processing_service_status(self) -> Response:
        """Check if the bulk processing service is available.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/bulk-processing/status"
        return self.polarion_connection.api_request_get(url)
