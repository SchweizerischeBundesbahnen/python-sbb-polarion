"""AzureAD Sync to Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionAadSynchronizerApi(PolarionGenericExtensionApi):
    """AzureAD Sync to Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("aad-synchronizer", polarion_connection)
