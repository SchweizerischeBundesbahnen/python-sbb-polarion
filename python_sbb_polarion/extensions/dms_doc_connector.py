"""DMS Doc Connector Polarion Extension API"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi, PolarionRestApiConnection


class PolarionDmsDocConnectorApi(PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi):
    """DMS Doc Connector Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("dms-doc-connector", polarion_connection)
