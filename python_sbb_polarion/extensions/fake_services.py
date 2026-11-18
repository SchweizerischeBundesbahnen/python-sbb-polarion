"""Fake Services Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._fake_services import (
    OpenTextMixin,
    WebhookMixin,
)


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


__all__ = ["PolarionFakeServicesApi"]


class PolarionFakeServicesApi(
    OpenTextMixin,
    WebhookMixin,
    PolarionGenericExtensionApi,
):
    """Fake Services Polarion Extension API

    This class combines all admin utility functionality through mixins:
    - OpenTextMixin: OpenText Fake Content Server management operations
    - WebhookMixin: Fake export webhook operations
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("fake-services", polarion_connection)
