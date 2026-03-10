"""DOCX Exporter Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi
from python_sbb_polarion.extensions._docx_exporter import (
    ConfigurationMixin,
    ConversionMixin,
    SettingsMixin,
    TestRunAttachmentsMixin,
    UtilityMixin,
)
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
    from python_sbb_polarion.core.base import PolarionRestApiConnection


# Re-export for public API
__all__ = [
    "CommentsRenderType",
    "ConverterJobStatus",
    "DocumentType",
    "Language",
    "Orientation",
    "PaperSize",
    "PolarionDocxExporterApi",
    "WebhookAuthType",
]


class PolarionDocxExporterApi(
    ConversionMixin,
    SettingsMixin,
    ConfigurationMixin,
    TestRunAttachmentsMixin,
    UtilityMixin,
    PolarionGenericExtensionSettingsApi,
    PolarionGenericExtensionApi,
):
    """DOCX Exporter Polarion Extension API

    This class combines all DOCX exporter functionality through mixins:
    - ConversionMixin: HTML to DOCX conversion, async jobs, document conversion
    - SettingsMixin: Localization and style package settings
    - ConfigurationMixin: Configuration checks (CORS, DLE, Pandoc, etc.)
    - TestRunAttachmentsMixin: Test run attachments management
    - UtilityMixin: Collections, document info, webhooks, project name
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("docx-exporter", polarion_connection)
