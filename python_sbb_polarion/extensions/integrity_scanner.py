"""Integrity Scanner Polarion Extension API"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionRestApiConnection
from python_sbb_polarion.extensions._integrity_scanner import IntegrityScannerMixin


class PolarionIntegrityScannerApi(IntegrityScannerMixin, PolarionGenericExtensionApi):
    """Integrity Scanner Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("integrity-scanner", polarion_connection)
