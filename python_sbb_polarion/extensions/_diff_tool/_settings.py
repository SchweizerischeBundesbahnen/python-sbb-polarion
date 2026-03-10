"""Diff Tool settings mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class SettingsMixin(BaseMixin):
    """Settings operations.

    Note: This mixin requires PolarionGenericExtensionSettingsApi methods
    to be available via multiple inheritance.
    """

    if TYPE_CHECKING:

        def save_setting(self, feature: str, data: JsonDict, name: str = "Default", scope: str | None = None) -> Response: ...
        def delete_setting(self, feature: str, name: str, scope: str | None = None) -> Response: ...
        def get_setting_content(self, feature: str, name: str = "Default", scope: str | None = None, revision: str | None = None) -> Response: ...

    def save_diff_settings(self, data: JsonDict, name: str = "Default", scope: str | None = None) -> Response:
        """Save settings for diff-tool feature (convenience wrapper for save_setting)

        Returns:
            Response: Settings data from the parent class method
        """
        return self.save_setting("diff", data, name=name, scope=scope)

    def delete_diff_settings(self, name: str, scope: str | None = None) -> Response:
        """Delete diff-tool settings (convenience wrapper for delete_setting)

        Returns:
            Response: Deletion response from the parent class method
        """
        return self.delete_setting("diff", name=name, scope=scope)

    def get_diff_settings(self, name: str = "Default", scope: str | None = None, revision: str | None = None) -> Response:
        """Get diff-tool settings (convenience wrapper for get_setting_content)

        Returns:
            Response: Settings data from the parent class method
        """
        return self.get_setting_content("diff", name=name, scope=scope, revision=revision)
