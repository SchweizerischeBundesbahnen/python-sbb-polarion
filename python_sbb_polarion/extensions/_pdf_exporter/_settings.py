"""PDF Exporter settings operations mixin.

This module provides PDF-specific settings methods (cover pages).
Common settings functionality is inherited from SharedSettingsMixin.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._shared_exporter import SharedExporterSettingsMixin


if TYPE_CHECKING:
    from requests import Response


class SettingsMixin(SharedExporterSettingsMixin):
    """PDF Exporter settings operations.

    This mixin provides PDF-specific methods for:
    - Cover page template management

    Common methods inherited from SharedSettingsMixin:
    - Localization settings (upload/download XLIFF)
    - Style package weights and suitable names
    - Convenience wrappers for style package settings
    """

    # =========================================================================
    # Cover Page Settings (PDF-specific)
    # =========================================================================

    @restapi_endpoint(
        method="GET",
        path="/api/settings/cover-page/templates",
        required_params=[],
        response_type="json",
    )
    def get_cover_page_template_names(self) -> Response:
        """Get cover page template names.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/cover-page/templates"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/settings/cover-page/templates/{template}",
        path_params={
            "template": "template",
        },
        query_params={
            "scope": "scope",
        },
        required_params=["template"],
        response_type="json",
    )
    def persist_cover_page_template(self, template: str, scope: str | None = None) -> Response:
        """Persist cover page template in specified scope.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/cover-page/templates/{template}"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_post(url, params=params or None)

    @restapi_endpoint(
        method="DELETE",
        path="/api/settings/cover-page/names/{name}/images",
        path_params={
            "name": "name",
        },
        query_params={
            "scope": "scope",
        },
        required_params=["name"],
        response_type="json",
    )
    def delete_cover_page_images(self, name: str, scope: str | None = None) -> Response:
        """Delete cover page images by name in specified scope.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/cover-page/names/{name}/images"
        params: dict[str, str] = {}
        if scope:
            params["scope"] = scope
        return self.polarion_connection.api_request_delete(url, params=params or None)
