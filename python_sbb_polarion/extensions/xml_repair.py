"""DMS Doc Connector Polarion Extension API"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi, PolarionRestApiConnection
from python_sbb_polarion.extensions._xml_repair import RepairMixin


class PolarionXmlRepairApi(RepairMixin, PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi):
    """XML Repair Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("xml-repair", polarion_connection)
