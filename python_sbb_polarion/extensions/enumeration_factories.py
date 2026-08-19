"""Custom Enumeration Factories Polarion Extension API"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionEnumerationFactoriesApi(PolarionGenericExtensionApi):
    """Custom Enumeration Factories Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("enumerationfactories", polarion_connection, automatic_module_name="com.polarion.alm.custom.enumerationfactories")
