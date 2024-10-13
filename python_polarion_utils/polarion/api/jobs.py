"""Jobs Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionJobsApi(PolarionGenericExtensionApi):
    """Jobs Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("jobs", polarion_connection)
