"""Hooks Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionHooksApi(PolarionGenericExtensionApi):
    """Hooks Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("hooks", polarion_connection)

    def get_hooks(self):
        """get all registered hooks"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/hooks")

    def get_settings(self, feature, name="Default", scope=None):
        """get settings for provided feature"""
        return super()._get_settings(feature, name=name, scope=scope)

    def save_settings(self, feature, data, name="Default", scope=None):
        """save settings for provided feature"""
        return super()._save_settings(feature, data, name=name, scope=scope)

    def get_settings_defaults(self, feature):
        """get default settings for provided feature"""
        return super()._get_settings_defaults(feature)

    def get_settings_revisions(self, feature, name="Default", scope=None):
        """get settings revisions for provided feature"""
        return super()._get_settings_revisions(feature, name=name, scope=scope)
