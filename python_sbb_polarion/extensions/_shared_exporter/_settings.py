"""Shared settings operations mixin for PDF and DOCX exporters.

This module provides methods for managing exporter settings:
localization and style packages.
"""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict, JsonList


class SharedExporterSettingsMixin(BaseMixin):
    """Shared settings operations for exporters.

    This mixin provides methods for:
    - Localization settings (upload/download XLIFF)
    - Style package weights and suitable names
    - Convenience wrappers for style package settings

    Note: This mixin requires PolarionGenericExtensionSettingsApi methods
    (get_setting_names, get_setting_content, save_setting, delete_setting)
    to be available via multiple inheritance.
    """

    # Type hints for methods from PolarionGenericExtensionSettingsApi (declared for type checkers only)
    if TYPE_CHECKING:

        def get_setting_names(self, feature: str, scope: str | None = None) -> Response: ...
        def get_setting_content(self, feature: str, name: str = "Default", scope: str | None = None, revision: str | None = None) -> Response: ...
        def save_setting(self, feature: str, data: JsonDict, name: str = "Default", scope: str | None = None) -> Response: ...
        def delete_setting(self, feature: str, name: str, scope: str | None = None) -> Response: ...

    # =========================================================================
    # Localization Settings
    # =========================================================================

    @restapi_endpoint(
        method="POST",
        path="/api/settings/localization/upload",
        query_params={
            "language": "language",
            "scope": "scope",
        },
        multipart_fields={
            "file": "file_content",
        },
        helper_params=["xliff_file_path"],
        required_params=[],
        response_type="json",
    )
    def upload_localization_settings(self, xliff_file_path: str, language: str, scope: str) -> Response:
        """Upload XLIFF and parse it on server, as result JSON will be returned.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/localization/upload"
        params: dict[str, str] = {
            "language": language,
        }
        if scope:
            params["scope"] = scope

        file_path: pathlib.Path = pathlib.Path(xliff_file_path)
        file_content: str = file_path.read_text(encoding="utf-8")

        files: FilesDict = {
            "file": (file_path.name, file_content),
        }
        return self.polarion_connection.api_request_post(url, files=files, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/settings/localization/names/{name}/download",
        path_params={
            "name": "name",
        },
        query_params={
            "language": "language",
            "scope": "scope",
            "revision": "revision",
        },
        required_params=["name"],
        response_type="binary",
    )
    def download_localization_settings(self, language: str, name: str = "Default", scope: str | None = None, revision: str | None = None) -> Response:
        """Download XLIFF for provided language.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/localization/names/{name}/download"
        params: dict[str, str] = {
            "language": language,
        }
        if scope:
            params["scope"] = scope
        if revision:
            params["revision"] = revision

        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.XML,
        }
        return self.polarion_connection.api_request_get(url, headers=headers, params=params)

    # =========================================================================
    # Style Package - Weights and Suitable Names
    # =========================================================================

    @restapi_endpoint(
        method="POST",
        path="/api/settings/style-package/suitable-names",
        body_param="data",
        required_params=["__request_body__"],
        response_type="json",
    )
    def find_suitable_style_package_names(self, data: JsonList) -> Response:
        """Get list of style packages suitable for a document in the provided project & scope.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/style-package/suitable-names"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/settings/style-package/weights",
        query_params={
            "scope": "scope",
        },
        required_params=[],
        response_type="json",
    )
    def get_style_package_weights(self, scope: str) -> Response:
        """Get full list of available style packages for the specific scope with the weight information.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/style-package/weights"
        params: dict[str, str] = {
            "scope": scope,
        }
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="POST",
        path="/api/settings/style-package/weights",
        body_param="data",
        required_params=["__request_body__"],
        response_type="json",
    )
    def save_style_package_weights(self, data: JsonList) -> Response:
        """Update weight information for the provided style packages.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/settings/style-package/weights"
        return self.polarion_connection.api_request_post(url, data=data)

    # =========================================================================
    # Convenience Methods for Style Package Settings
    # =========================================================================

    def get_style_packages_names(self, scope: str | None = None) -> Response:
        """Get style-package names in specified scope (convenience wrapper for get_setting_names).

        Returns:
            Response: Response object from the API call
        """
        return self.get_setting_names("style-package", scope=scope)

    def get_style_package(self, name: str, scope: str | None = None, revision: str | None = None) -> Response:
        """Get style-package content by name in specified scope (convenience wrapper for get_setting_content).

        Returns:
            Response: Response object from the API call
        """
        return self.get_setting_content("style-package", name=name, scope=scope, revision=revision)

    def save_style_package(self, name: str, data: JsonDict, scope: str | None = None) -> Response:
        """Save style-package content by name in specified scope (convenience wrapper for save_setting).

        Returns:
            Response: Response object from the API call
        """
        return self.save_setting("style-package", data, name=name, scope=scope)

    def delete_style_package(self, name: str, scope: str | None = None) -> Response:
        """Delete style-package by name in specified scope (convenience wrapper for delete_setting).

        Returns:
            Response: Response object from the API call
        """
        return self.delete_setting("style-package", name=name, scope=scope)
