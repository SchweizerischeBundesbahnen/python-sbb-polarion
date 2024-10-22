"""Requirements Inspector Polarion Extension API"""

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionRequirementsInspectorApi(PolarionGenericExtensionApi):
    """Requirements Inspector Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "requirements-inspector")
