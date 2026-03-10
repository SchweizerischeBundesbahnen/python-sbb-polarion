"""DMS WI Connector Polarion Extension API"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi, PolarionRestApiConnection


class PolarionDmsWiConnectorApi(PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi):
    """DMS WI Connector Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("dms-wi-connector", polarion_connection)
