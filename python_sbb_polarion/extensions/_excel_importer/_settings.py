"""Excel Importer settings mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict

MAPPINGS_FEATURE = "mappings"


class SettingsMixin(BaseMixin):
    """Settings and mappings operations.

    Note: This mixin requires PolarionGenericExtensionSettingsApi methods
    to be available via multiple inheritance.
    """

    if TYPE_CHECKING:

        def get_setting_content(self, feature: str, name: str = "Default", scope: str | None = None, revision: str | None = None) -> Response: ...
        def save_setting(self, feature: str, data: JsonDict, name: str = "Default", scope: str | None = None) -> Response: ...
        def delete_setting(self, feature: str, name: str, scope: str | None = None) -> Response: ...
        def get_setting_default_content(self, feature: str) -> Response: ...
        def get_setting_revisions(self, feature: str, name: str = "Default", scope: str | None = None) -> Response: ...
        def get_setting_names(self, feature: str, scope: str | None = None) -> Response: ...
        def rename_setting(self, feature: str, name: str, new_name: str, scope: str | None = None) -> Response: ...

    def get_mapping(self, name: str = "Default", scope: str | None = None, revision: str | None = None) -> Response:
        """Get mapping by name for the provided scope (convenience wrapper for get_setting_content)

        Returns:
            Response: Mapping data from the parent class method
        """
        return self.get_setting_content(MAPPINGS_FEATURE, name=name, scope=scope, revision=revision)

    def save_mapping(self, data: JsonDict, name: str = "Default", scope: str | None = None) -> Response:
        """Save mapping by name for the provided scope (convenience wrapper for save_setting)

        Returns:
            Response: Mapping data from the parent class method
        """
        return self.save_setting(MAPPINGS_FEATURE, data, name=name, scope=scope)

    def delete_mapping(self, name: str = "Default", scope: str | None = None) -> Response:
        """Delete mapping by name for the provided scope (convenience wrapper for delete_setting)

        Returns:
            Response: Deletion response from the parent class method
        """
        return self.delete_setting(MAPPINGS_FEATURE, name=name, scope=scope)

    def get_default_mapping(self) -> Response:
        """Get default mapping (convenience wrapper for get_setting_default_content)

        Returns:
            Response: Default mapping from the parent class method
        """
        return self.get_setting_default_content(MAPPINGS_FEATURE)

    def get_mapping_revisions(self, name: str = "Default", scope: str | None = None) -> Response:
        """Get mapping revisions by name for the provided scope (convenience wrapper for get_setting_revisions)

        Returns:
            Response: Revisions data from the parent class method
        """
        return self.get_setting_revisions(MAPPINGS_FEATURE, name=name, scope=scope)

    def get_mapping_names(self, scope: str | None = None) -> Response:
        """GET Returns list of mapping names (convenience wrapper for get_setting_names)

        Returns:
            Response: Response object from the API call
        """
        return self.get_setting_names(MAPPINGS_FEATURE, scope=scope)

    def rename_mapping(self, name: str, new_name: str, scope: str | None = None) -> Response:
        """POST Rename specified mapping (convenience wrapper for rename_setting)

        Returns:
            Response: Response object from the API call
        """
        return self.rename_setting(MAPPINGS_FEATURE, name=name, new_name=new_name, scope=scope)
