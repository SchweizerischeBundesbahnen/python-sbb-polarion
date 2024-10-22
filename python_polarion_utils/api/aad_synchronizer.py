"""AzureAD Sync to Polarion Extension API"""

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionAadSynchronizerApi(PolarionGenericExtensionApi):
    """AzureAD Sync to Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "aad-synchronizer")
