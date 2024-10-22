"""Mail Workflow Polarion Extension API"""

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionMailWorkflowApi(PolarionGenericExtensionApi):
    """Mail Workflow Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "mailworkflow")
