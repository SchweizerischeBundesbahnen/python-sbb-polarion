"""Polarion Extension API Factory"""

from .aad_synchronizer import PolarionAadSynchronizerApi
from .admin_utility import PolarionAdminUtilityApi
from .api_extender import PolarionApiExtenderApi
from .collection_checker import PolarionCollectionCheckerApi
from .cucumber import PolarionCucumberApi
from .diff_tool import PolarionDiffToolApi
from .dms_doc_connector import PolarionDmsDocConnectorApi
from .dms_wi_connector import PolarionDmsWiConnectorApi
from .excel_importer import PolarionExcelImporterApi
from .generic import PolarionGenericExtensionApi
from .hooks import PolarionHooksApi
from .jobs import PolarionJobsApi
from .json_editor import PolarionJsonEditorApi
from .mailworkflow import PolarionMailWorkflowApi
from .pdf_exporter import PolarionPdfExporterApi
from .qualityanalysis import PolarionQualityAnalysisApi
from .sbbtool import PolarionSBBToolApi
from .test_data import PolarionTestDataApi


class ExtensionApiFactory:  # pylint: disable=R0903
    """Extension API Factory"""

    __extension_api_classes = {
        "aad-synchronizer": PolarionAadSynchronizerApi,
        "admin-utility": PolarionAdminUtilityApi,
        "api-extender": PolarionApiExtenderApi,
        "collection-checker": PolarionCollectionCheckerApi,
        "cucumber": PolarionCucumberApi,
        "diff-tool": PolarionDiffToolApi,
        "dms-doc-connector": PolarionDmsDocConnectorApi,
        "dms-wi-connector": PolarionDmsWiConnectorApi,
        "excel-importer": PolarionExcelImporterApi,
        "hooks": PolarionHooksApi,
        "jobs": PolarionJobsApi,
        "json-editor": PolarionJsonEditorApi,
        "mailworkflow": PolarionMailWorkflowApi,
        "pdf-exporter": PolarionPdfExporterApi,
        "qualityanalysis": PolarionQualityAnalysisApi,
        "sbbtool": PolarionSBBToolApi,
        "test-data": PolarionTestDataApi,
        "generic": PolarionGenericExtensionApi,
    }

    @classmethod
    def get_extension_api_by_name(cls, extension_name, polarion_connection):
        """get extension api object for provided extension name"""
        api_class = cls.__extension_api_classes.get(extension_name)
        if api_class:
            return api_class(polarion_connection)
        raise ValueError("Invalid extension name")
