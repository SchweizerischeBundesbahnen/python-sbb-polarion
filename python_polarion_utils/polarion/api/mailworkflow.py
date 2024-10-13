"""Mail Workflow Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionMailWorkflowApi(PolarionGenericExtensionApi):
    """Mail Workflow Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("mailworkflow", polarion_connection)
