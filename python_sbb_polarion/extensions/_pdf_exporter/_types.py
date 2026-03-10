"""PDF Exporter specific types and enums."""

from enum import StrEnum


class PdfVariant(StrEnum):
    """PDF/A and PDF/UA variants for PDF export.

    See: ch.sbb.polarion.extension.pdf_exporter.rest.model.conversion.PdfVariant
    """

    PDF_A_1A = "PDF_A_1A"
    PDF_A_1B = "PDF_A_1B"
    PDF_A_2A = "PDF_A_2A"
    PDF_A_2B = "PDF_A_2B"
    PDF_A_2U = "PDF_A_2U"
    PDF_A_3A = "PDF_A_3A"
    PDF_A_3B = "PDF_A_3B"
    PDF_A_3U = "PDF_A_3U"
    PDF_A_4E = "PDF_A_4E"
    PDF_A_4F = "PDF_A_4F"
    PDF_A_4U = "PDF_A_4U"
    PDF_UA_1 = "PDF_UA_1"
    PDF_UA_2 = "PDF_UA_2"


class ImageDensity(StrEnum):
    """Quality of PNG images converted from SVG.

    See: ch.sbb.polarion.extension.pdf_exporter.rest.model.conversion.ImageDensity
    """

    DPI_96 = "DPI_96"
    DPI_192 = "DPI_192"
    DPI_300 = "DPI_300"
    DPI_600 = "DPI_600"
