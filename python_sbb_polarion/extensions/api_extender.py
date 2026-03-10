"""API Extender Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi
from python_sbb_polarion.extensions._api_extender import CustomFieldsMixin, RecordsMixin, RegexMixin


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


class PolarionApiExtenderApi(
    CustomFieldsMixin,
    RecordsMixin,
    RegexMixin,
    PolarionGenericExtensionSettingsApi,
    PolarionGenericExtensionApi,
):
    """API Extender Polarion Extension API

    This class combines all API extender functionality through mixins:
    - CustomFieldsMixin: Project custom fields operations
    - RecordsMixin: Global records operations
    - RegexMixin: Regex tool operations
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("api-extender", polarion_connection)
