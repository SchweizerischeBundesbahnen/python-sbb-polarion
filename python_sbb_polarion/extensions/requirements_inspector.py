"""Requirements Inspector Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._requirements_inspector import InspectionMixin


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


class PolarionRequirementsInspectorApi(
    InspectionMixin,
    PolarionGenericExtensionApi,
):
    """Requirements Inspector Polarion Extension API

    This class combines all requirements inspector functionality through mixins:
    - InspectionMixin: Workitem inspection operations
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("requirements-inspector", polarion_connection)
