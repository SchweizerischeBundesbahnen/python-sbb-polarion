"""Wiki Velocity Context Polarion Extension API"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionVContextApi(PolarionGenericExtensionApi):
    """Wiki Velocity Context Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("vcontext", polarion_connection, automatic_module_name="com.polarion.alm.extension.vcontext")
