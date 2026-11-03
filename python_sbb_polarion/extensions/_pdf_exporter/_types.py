"""PDF Exporter specific types and enums."""

import warnings
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

    Deprecated: weasyprint-service 70.0.8 and later draws SVG as vector and ignores it.
    The next major release removes it.

    See: ch.sbb.polarion.extension.pdf_exporter.rest.model.conversion.ImageDensity
    """

    DPI_96 = "DPI_96"
    DPI_192 = "DPI_192"
    DPI_300 = "DPI_300"
    DPI_600 = "DPI_600"


IMAGE_DENSITY_DEPRECATION: str = "ImageDensity is deprecated and will be removed in a future major release; weasyprint-service 70.0.8 and later ignores it."


def deprecated_type(module_name: str, name: str) -> type[ImageDensity]:
    """Resolve a deprecated type of a module, for its ``__getattr__``.

    Emits a ``DeprecationWarning`` that points at the code which reads the name.

    Args:
        module_name: Name of the module that resolves the name
        name: Name that is read from the module

    Returns:
        The deprecated type

    Raises:
        AttributeError: If the module has no such deprecated type
    """
    if name == "ImageDensity":
        warnings.warn(IMAGE_DENSITY_DEPRECATION, DeprecationWarning, stacklevel=3)
        return ImageDensity
    raise AttributeError(f"module {module_name!r} has no attribute {name!r}")
