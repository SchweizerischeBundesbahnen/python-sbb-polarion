"""Requirements Inspector Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionRequirementsInspectorApi(PolarionGenericExtensionApi):
    """Requirements Inspector Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("requirements-inspector", polarion_connection)
