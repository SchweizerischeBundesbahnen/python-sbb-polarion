"""DMS WI Connector Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionDmsWiConnectorApi(PolarionGenericExtensionApi):
    """DMS WI Connector Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("dms-wi-connector", polarion_connection)

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
