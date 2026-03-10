"""Shared types and enums for exporter extensions (PDF, DOCX, etc.)."""

from enum import StrEnum


class DocumentType(StrEnum):
    """Document type for export operations.

    Used by PDF Exporter, DOCX Exporter, and other document export extensions.
    """

    LIVE_DOC = "LIVE_DOC"
    LIVE_REPORT = "LIVE_REPORT"
    TEST_RUN = "TEST_RUN"
    WIKI_PAGE = "WIKI_PAGE"


class Orientation(StrEnum):
    """Page orientation for document export.

    See: ch.sbb.polarion.extension.pdf_exporter.rest.model.conversion.Orientation
    """

    PORTRAIT = "PORTRAIT"
    LANDSCAPE = "LANDSCAPE"


class PaperSize(StrEnum):
    """Standard paper sizes supported by CSS @page/size.

    See: ch.sbb.polarion.extension.pdf_exporter.rest.model.conversion.PaperSize
    https://developer.mozilla.org/en-US/docs/Web/CSS/@page/size
    """

    A5 = "A5"
    A4 = "A4"
    A3 = "A3"
    B5 = "B5"
    B4 = "B4"
    JIS_B5 = "JIS_B5"
    JIS_B4 = "JIS_B4"
    LETTER = "LETTER"
    LEGAL = "LEGAL"
    LEDGER = "LEDGER"


class Language(StrEnum):
    """Supported languages for localization settings.

    See: ch.sbb.polarion.extension.pdf_exporter.rest.model.settings.localization.Language
    """

    EN = "EN"
    DE = "DE"
    FR = "FR"
    IT = "IT"


class ConverterJobStatus(StrEnum):
    """Status of the converter job.

    Used by PDF Exporter and DOCX Exporter for async conversion jobs.
    """

    IN_PROGRESS = "IN_PROGRESS"
    SUCCESSFULLY_FINISHED = "SUCCESSFULLY_FINISHED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class CommentsRenderType(StrEnum):
    """Type of comments to render in document export.

    Used by PDF Exporter and DOCX Exporter.
    """

    OPEN = "OPEN"
    ALL = "ALL"


class WebhookAuthType(StrEnum):
    """Authentication type for webhooks.

    Used by PDF Exporter and DOCX Exporter.
    """

    BEARER_TOKEN = "BEARER_TOKEN"  # noqa: S105
    BASIC_AUTH = "BASIC_AUTH"
