"""Diff Tool Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi
from python_sbb_polarion.extensions._diff_tool import (
    ConversionMixin,
    DifferenceMixin,
    MergeMixin,
    SettingsMixin,
    UtilityMixin,
)
from python_sbb_polarion.extensions._shared_exporter_types import Orientation, PaperSize


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


# Re-export for public API
__all__ = ["Orientation", "PaperSize", "PolarionDiffToolApi"]


class PolarionDiffToolApi(
    ConversionMixin,
    DifferenceMixin,
    MergeMixin,
    SettingsMixin,
    UtilityMixin,
    PolarionGenericExtensionSettingsApi,
    PolarionGenericExtensionApi,
):
    """Diff Tool Polarion Extension API

    This class combines all diff tool functionality through mixins:
    - ConversionMixin: HTML to PDF conversion
    - DifferenceMixin: Diff operations for documents, workitems, collections
    - MergeMixin: Merge operations
    - SettingsMixin: Diff settings management
    - UtilityMixin: Spaces, documents, workitem fields, queue statistics
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("diff-tool", polarion_connection)
