"""PDF Exporter Polarion Extension API

This module provides the main API class for the PDF Exporter extension.
The implementation is split into mixins for better organization:
- ConversionMixin: PDF conversion operations (HTML, Jobs, Documents)
- SettingsMixin: Settings operations (Cover Page, Localization, Style Package)
- ConfigurationMixin: Configuration checks
- TestRunAttachmentsMixin: Test run attachments
- UtilityMixin: Collections, document info, webhooks, project info
"""

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi, PolarionRestApiConnection
from python_sbb_polarion.extensions._pdf_exporter import (
    ConfigurationMixin,
    ConversionMixin,
    SettingsMixin,
    TestRunAttachmentsMixin,
    UtilityMixin,
)
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


# Re-export for public API
__all__ = [
    "CommentsRenderType",
    "ConverterJobStatus",
    "DocumentType",
    "ImageDensity",
    "Language",
    "Orientation",
    "PaperSize",
    "PdfVariant",
    "PolarionPdfExporterApi",
    "WebhookAuthType",
]


class PolarionPdfExporterApi(
    ConversionMixin,
    SettingsMixin,
    ConfigurationMixin,
    TestRunAttachmentsMixin,
    UtilityMixin,
    PolarionGenericExtensionSettingsApi,
    PolarionGenericExtensionApi,
):
    """PDF Exporter Polarion Extension API

    This class combines all PDF Exporter functionality through mixins:
    - ConversionMixin: convert_html, convert, validate, job management
    - SettingsMixin: cover page, localization, style package weights, convenience wrappers
    - ConfigurationMixin: configuration checks
    - TestRunAttachmentsMixin: test run attachments
    - UtilityMixin: collections, document info, webhooks, project name
    - PolarionGenericExtensionSettingsApi: generic settings CRUD
    - PolarionGenericExtensionApi: base extension functionality
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("pdf-exporter", polarion_connection)
