"""Mail Workflow Polarion Extension API"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionMailWorkflowApi(PolarionGenericExtensionApi):
    """Mail Workflow Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("mailworkflow", polarion_connection)
