"""PDF Exporter Polarion Extension API

This module provides the main API class for the PDF Exporter extension.
The implementation is split into mixins for better organization:
- ConversionMixin: PDF conversion operations (HTML, Jobs, Documents)
- SettingsMixin: Settings operations (Cover Page, Localization, Style Package)
- ConfigurationMixin: Configuration checks
- TestRunAttachmentsMixin: Test run attachments
- UtilityMixin: Collections, document info, webhooks, project info
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi, PolarionRestApiConnection
from python_sbb_polarion.extensions._base import ExportPermissionMixin, RolesMixin
from python_sbb_polarion.extensions._pdf_exporter import (
    ConfigurationMixin,
    ConversionMixin,
    SettingsMixin,
    TestRunAttachmentsMixin,
    UtilityMixin,
)
from python_sbb_polarion.extensions._pdf_exporter._types import PdfVariant, deprecated_type
from python_sbb_polarion.extensions._shared_exporter_types import (
    CommentsRenderType,
    ConverterJobStatus,
    DocumentType,
    Language,
    Orientation,
    PaperSize,
    WebhookAuthType,
)


if TYPE_CHECKING:
    from python_sbb_polarion.extensions._pdf_exporter._types import ImageDensity


# Re-export for public API
__all__ = [
    "CommentsRenderType",
    "ConverterJobStatus",
    "DocumentType",
    "Language",
    "Orientation",
    "PaperSize",
    "PdfVariant",
    "PolarionPdfExporterApi",
    "WebhookAuthType",
]


def __getattr__(name: str) -> type[ImageDensity]:
    """Resolve the deprecated ImageDensity, with a DeprecationWarning."""
    return deprecated_type(__name__, name)


class PolarionPdfExporterApi(
    ExportPermissionMixin,
    RolesMixin,
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
