"""Quality Analysis Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionQualityAnalysisApi(PolarionGenericExtensionApi):
    """Quality Analysis Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("qualityanalysis", polarion_connection)
