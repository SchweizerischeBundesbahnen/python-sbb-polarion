"""Polarion Extension API Factory"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Literal, overload

from python_sbb_polarion.extensions.aad_synchronizer import PolarionAadSynchronizerApi
from python_sbb_polarion.extensions.admin_utility import PolarionAdminUtilityApi
from python_sbb_polarion.extensions.api_extender import PolarionApiExtenderApi
from python_sbb_polarion.extensions.collection_checker import PolarionCollectionCheckerApi
from python_sbb_polarion.extensions.cucumber import PolarionCucumberApi
from python_sbb_polarion.extensions.diff_tool import PolarionDiffToolApi
from python_sbb_polarion.extensions.dms_doc_connector import PolarionDmsDocConnectorApi
from python_sbb_polarion.extensions.dms_wi_connector import PolarionDmsWiConnectorApi
from python_sbb_polarion.extensions.docx_exporter import PolarionDocxExporterApi
from python_sbb_polarion.extensions.excel_importer import PolarionExcelImporterApi
from python_sbb_polarion.extensions.fake_services import PolarionFakeServicesApi
from python_sbb_polarion.extensions.interceptor_manager import PolarionInterceptorManagerApi
from python_sbb_polarion.extensions.json_editor import PolarionJsonEditorApi
from python_sbb_polarion.extensions.mailworkflow import PolarionMailWorkflowApi
from python_sbb_polarion.extensions.pdf_exporter import PolarionPdfExporterApi
from python_sbb_polarion.extensions.requirements_inspector import PolarionRequirementsInspectorApi
from python_sbb_polarion.extensions.strictdoc_exporter import PolarionStrictDocExporterApi
from python_sbb_polarion.extensions.test_data import PolarionTestDataApi
from python_sbb_polarion.extensions.xml_repair import PolarionXmlRepairApi


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionRestApiConnection


class ExtensionApiFactory:
    """Extension API Factory"""

    __extension_api_classes: ClassVar[dict[str, type[PolarionGenericExtensionApi]]] = {
        "aad-synchronizer": PolarionAadSynchronizerApi,
        "admin-utility": PolarionAdminUtilityApi,
        "api-extender": PolarionApiExtenderApi,
        "collection-checker": PolarionCollectionCheckerApi,
        "cucumber": PolarionCucumberApi,
        "diff-tool": PolarionDiffToolApi,
        "dms-doc-connector": PolarionDmsDocConnectorApi,
        "dms-wi-connector": PolarionDmsWiConnectorApi,
        "excel-importer": PolarionExcelImporterApi,
        "fake-services": PolarionFakeServicesApi,
        "interceptor-manager": PolarionInterceptorManagerApi,
        "json-editor": PolarionJsonEditorApi,
        "mailworkflow": PolarionMailWorkflowApi,
        "pdf-exporter": PolarionPdfExporterApi,
        "docx-exporter": PolarionDocxExporterApi,
        "requirements-inspector": PolarionRequirementsInspectorApi,
        "strictdoc-exporter": PolarionStrictDocExporterApi,
        "test-data": PolarionTestDataApi,
        "xml-repair": PolarionXmlRepairApi,
    }

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["aad-synchronizer"], polarion_connection: PolarionRestApiConnection) -> PolarionAadSynchronizerApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["admin-utility"], polarion_connection: PolarionRestApiConnection) -> PolarionAdminUtilityApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["api-extender"], polarion_connection: PolarionRestApiConnection) -> PolarionApiExtenderApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["collection-checker"], polarion_connection: PolarionRestApiConnection) -> PolarionCollectionCheckerApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["cucumber"], polarion_connection: PolarionRestApiConnection) -> PolarionCucumberApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["diff-tool"], polarion_connection: PolarionRestApiConnection) -> PolarionDiffToolApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["dms-doc-connector"], polarion_connection: PolarionRestApiConnection) -> PolarionDmsDocConnectorApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["dms-wi-connector"], polarion_connection: PolarionRestApiConnection) -> PolarionDmsWiConnectorApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["excel-importer"], polarion_connection: PolarionRestApiConnection) -> PolarionExcelImporterApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["fake-services"], polarion_connection: PolarionRestApiConnection) -> PolarionFakeServicesApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["interceptor-manager"], polarion_connection: PolarionRestApiConnection) -> PolarionInterceptorManagerApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["json-editor"], polarion_connection: PolarionRestApiConnection) -> PolarionJsonEditorApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["mailworkflow"], polarion_connection: PolarionRestApiConnection) -> PolarionMailWorkflowApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["pdf-exporter"], polarion_connection: PolarionRestApiConnection) -> PolarionPdfExporterApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["docx-exporter"], polarion_connection: PolarionRestApiConnection) -> PolarionDocxExporterApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["requirements-inspector"], polarion_connection: PolarionRestApiConnection) -> PolarionRequirementsInspectorApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["strictdoc-exporter"], polarion_connection: PolarionRestApiConnection) -> PolarionStrictDocExporterApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["test-data"], polarion_connection: PolarionRestApiConnection) -> PolarionTestDataApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: Literal["xml-repair"], polarion_connection: PolarionRestApiConnection) -> PolarionXmlRepairApi: ...

    @overload
    @classmethod
    def get_extension_api_by_name(cls, extension_name: str, polarion_connection: PolarionRestApiConnection) -> PolarionGenericExtensionApi: ...

    @classmethod
    def get_extension_api_by_name(cls, extension_name: str, polarion_connection: PolarionRestApiConnection) -> PolarionGenericExtensionApi:
        """Get extension api object for provided extension name

        Raises:
            ValueError: If extension name is invalid

        Returns:
            PolarionGenericExtensionApi: Extension API instance
        """
        api_class: type[PolarionGenericExtensionApi] | None = cls.__extension_api_classes.get(extension_name)
        if api_class:
            # Extension subclasses have different __init__ signature than base class
            # They only take polarion_connection (extension_name is hardcoded)
            return api_class(polarion_connection)  # type: ignore[call-arg, arg-type]
        raise ValueError("Invalid extension name")
