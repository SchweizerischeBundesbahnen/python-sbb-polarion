"""Hooks Polarion Extension API"""

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionHooksApi(PolarionGenericExtensionApi):
    """Hooks Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "hooks")

    def get_hooks(self) -> Response | None:
        """get all registered hooks"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/hooks")

    def get_settings(self, feature: str, name: str = "Default", scope: str | None = None) -> Response | None:
        """get settings for provided feature"""
        return super()._get_settings(feature, name=name, scope=scope)

    def save_settings(self, feature: str, data, name: str = "Default", scope: str | None = None) -> Response | None:
        """save settings for provided feature"""
        return super()._save_settings(feature, data, name=name, scope=scope)

    def get_settings_defaults(self, feature: str) -> Response | None:
        """get default settings for provided feature"""
        return super()._get_settings_defaults(feature)

    def get_settings_revisions(self, feature: str, name: str = "Default", scope: str | None = None) -> Response | None:
        """get settings revisions for provided feature"""
        return super()._get_settings_revisions(feature, name=name, scope=scope)
