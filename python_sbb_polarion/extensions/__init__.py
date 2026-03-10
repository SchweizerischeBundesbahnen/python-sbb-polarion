"""Polarion Extension Clients Module

This module contains client interfaces for SBB Polarion extensions.
Each module corresponds to a specific Polarion extension from:
https://github.com/SchweizerischeBundesbahnen/ch.sbb.polarion.extension.*
"""

from python_sbb_polarion.extensions._collection_checker._types import ReportFormat
from python_sbb_polarion.extensions._pdf_exporter._types import ImageDensity, PdfVariant
from python_sbb_polarion.extensions._shared_exporter_types import (
    CommentsRenderType,
    ConverterJobStatus,
    DocumentType,
    Language,
    Orientation,
    PaperSize,
    WebhookAuthType,
)
from python_sbb_polarion.extensions.aad_synchronizer import PolarionAadSynchronizerApi
from python_sbb_polarion.extensions.admin_utility import PolarionAdminUtilityApi
from python_sbb_polarion.extensions.api_extender import PolarionApiExtenderApi
from python_sbb_polarion.extensions.collection_checker import PolarionCollectionCheckerApi
from python_sbb_polarion.extensions.cucumber import PolarionCucumberApi
from python_sbb_polarion.extensions.diff_tool import PolarionDiffToolApi
from python_sbb_polarion.extensions.dms_doc_connector import PolarionDmsDocConnectorApi
from python_sbb_polarion.extensions.dms_wi_connector import PolarionDmsWiConnectorApi
from python_sbb_polarion.extensions.docx_exporter import PolarionDocxExporterApi
from python_sbb_polarion.extensions.excel_importer import AttachTableParams, PolarionExcelImporterApi
from python_sbb_polarion.extensions.fake_services import PolarionFakeServicesApi
from python_sbb_polarion.extensions.interceptor_manager import PolarionInterceptorManagerApi
from python_sbb_polarion.extensions.json_editor import PolarionJsonEditorApi
from python_sbb_polarion.extensions.mailworkflow import PolarionMailWorkflowApi
from python_sbb_polarion.extensions.pdf_exporter import PolarionPdfExporterApi
from python_sbb_polarion.extensions.requirements_inspector import PolarionRequirementsInspectorApi
from python_sbb_polarion.extensions.strictdoc_exporter import PolarionStrictDocExporterApi
from python_sbb_polarion.extensions.test_data import PolarionTestDataApi
from python_sbb_polarion.extensions.xml_repair import PolarionXmlRepairApi


__all__ = [
    "AttachTableParams",
    "CommentsRenderType",
    "ConverterJobStatus",
    "DocumentType",
    "ImageDensity",
    "Language",
    "Orientation",
    "PaperSize",
    "PdfVariant",
    "PolarionAadSynchronizerApi",
    "PolarionAdminUtilityApi",
    "PolarionApiExtenderApi",
    "PolarionCollectionCheckerApi",
    "PolarionCucumberApi",
    "PolarionDiffToolApi",
    "PolarionDmsDocConnectorApi",
    "PolarionDmsWiConnectorApi",
    "PolarionDocxExporterApi",
    "PolarionExcelImporterApi",
    "PolarionFakeServicesApi",
    "PolarionInterceptorManagerApi",
    "PolarionJsonEditorApi",
    "PolarionMailWorkflowApi",
    "PolarionPdfExporterApi",
    "PolarionRequirementsInspectorApi",
    "PolarionStrictDocExporterApi",
    "PolarionTestDataApi",
    "PolarionXmlRepairApi",
    "ReportFormat",
    "WebhookAuthType",
]
