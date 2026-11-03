"""StrictDoc Exporter Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi
from python_sbb_polarion.extensions._base import RolesMixin
from python_sbb_polarion.extensions._strictdoc_exporter import ExportMixin


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


class PolarionStrictDocExporterApi(
    RolesMixin,
    ExportMixin,
    PolarionGenericExtensionSettingsApi,
    PolarionGenericExtensionApi,
):
    """StrictDoc Exporter Polarion Extension API

    This class combines all StrictDoc exporter functionality through mixins:
    - RolesMixin: Roles available for the extension
    - ExportMixin: Live document export operations and the bulk export widget
    - PolarionGenericExtensionSettingsApi: Generic settings endpoints
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("strictdoc-exporter", polarion_connection)
