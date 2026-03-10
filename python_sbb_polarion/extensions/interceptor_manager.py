"""Interceptor Manager Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._interceptor_manager import HookSettingsMixin, HooksMixin


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


class PolarionInterceptorManagerApi(
    HookSettingsMixin,
    HooksMixin,
    PolarionGenericExtensionApi,
):
    """Interceptor Manager Polarion Extension API

    This class combines all interceptor manager functionality through mixins:
    - HookSettingsMixin: Hook settings operations
    - HooksMixin: Hooks list operations
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("interceptor-manager", polarion_connection)
