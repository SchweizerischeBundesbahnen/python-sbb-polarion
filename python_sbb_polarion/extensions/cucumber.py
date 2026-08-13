"""Cucumber Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._cucumber import ExportMixin, FeaturesMixin, ImportMixin


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


class PolarionCucumberApi(
    FeaturesMixin,
    ExportMixin,
    ImportMixin,
    PolarionGenericExtensionApi,
):
    """Cucumber Polarion Extension API

    This class combines all cucumber functionality through mixins:
    - FeaturesMixin: Feature operations (save, get, jira fields)
    - ExportMixin: Export test features
    - ImportMixin: Import cucumber/junit test results
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("cucumber", polarion_connection)
