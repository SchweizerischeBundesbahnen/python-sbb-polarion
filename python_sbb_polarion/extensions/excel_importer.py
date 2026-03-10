"""Excel Importer Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi
from python_sbb_polarion.extensions._excel_importer import ExcelToolMixin, ImportMixin, SettingsMixin, WorkItemsMixin
from python_sbb_polarion.extensions._excel_importer._excel_tool import AttachTableParams


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


__all__ = ["AttachTableParams", "PolarionExcelImporterApi"]


class PolarionExcelImporterApi(
    ExcelToolMixin,
    ImportMixin,
    WorkItemsMixin,
    SettingsMixin,
    PolarionGenericExtensionSettingsApi,
    PolarionGenericExtensionApi,
):
    """Excel Importer Polarion Extension API

    This class combines all Excel importer functionality through mixins:
    - ExcelToolMixin: Excel tool operations (export, attach table)
    - ImportMixin: Import jobs and direct import
    - WorkItemsMixin: Work item types and fields
    - SettingsMixin: Mapping settings management
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("excel-importer", polarion_connection)
