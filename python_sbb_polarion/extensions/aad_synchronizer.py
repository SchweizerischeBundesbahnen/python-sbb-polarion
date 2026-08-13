"""AAD Synchronizer Polarion Extension API"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionAadSynchronizerApi(PolarionGenericExtensionApi):
    """AAD Synchronizer Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("aad-synchronizer", polarion_connection)
