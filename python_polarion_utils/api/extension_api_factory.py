"""Polarion Extension API Factory"""

from python_polarion_utils.api.aad_synchronizer import PolarionAadSynchronizerApi
from python_polarion_utils.api.admin_utility import PolarionAdminUtilityApi
from python_polarion_utils.api.api_extender import PolarionApiExtenderApi
from python_polarion_utils.api.collection_checker import PolarionCollectionCheckerApi
from python_polarion_utils.api.cucumber import PolarionCucumberApi
from python_polarion_utils.api.diff_tool import PolarionDiffToolApi
from python_polarion_utils.api.dms_doc_connector import PolarionDmsDocConnectorApi
from python_polarion_utils.api.dms_wi_connector import PolarionDmsWiConnectorApi
from python_polarion_utils.api.excel_importer import PolarionExcelImporterApi
from python_polarion_utils.api.generic import PolarionApiExtensionName, PolarionGenericExtensionApi, PolarionRestApiConnection
from python_polarion_utils.api.hooks import PolarionHooksApi
from python_polarion_utils.api.jobs import PolarionJobsApi
from python_polarion_utils.api.json_editor import PolarionJsonEditorApi
from python_polarion_utils.api.mailworkflow import PolarionMailWorkflowApi
from python_polarion_utils.api.pdf_exporter import PolarionPdfExporterApi
from python_polarion_utils.api.requirements_inspector import PolarionRequirementsInspectorApi
from python_polarion_utils.api.sbbtool import PolarionSBBToolApi
from python_polarion_utils.api.test_data import PolarionTestDataApi


class ExtensionApiFactory:
    """Extension API Factory"""

    __extension_api_classes: dict[PolarionApiExtensionName, type[PolarionGenericExtensionApi]] = {
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
        "requirements-inspector": PolarionRequirementsInspectorApi,
        "sbbtool": PolarionSBBToolApi,
        "test-data": PolarionTestDataApi,
        "generic": PolarionGenericExtensionApi,
    }

    @classmethod
    def get_extension_api_by_name(cls, extension_name: PolarionApiExtensionName, polarion_connection: PolarionRestApiConnection) -> PolarionGenericExtensionApi:
        """get extension api object for provided extension name"""
        api_class = cls.__extension_api_classes.get(extension_name)
        if api_class:
            return api_class(polarion_connection)
        raise ValueError("Invalid extension name")
