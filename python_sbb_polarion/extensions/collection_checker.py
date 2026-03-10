"""Collection Checker Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._collection_checker import ChecksMixin, CollectionsMixin
from python_sbb_polarion.extensions._collection_checker._types import ReportFormat


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


__all__ = ["PolarionCollectionCheckerApi", "ReportFormat"]


class PolarionCollectionCheckerApi(
    ChecksMixin,
    CollectionsMixin,
    PolarionGenericExtensionApi,
):
    """Collection Checker Polarion Extension API

    This class combines all collection checker functionality through mixins:
    - ChecksMixin: Check operations (start, cancel, get status, reports)
    - CollectionsMixin: Collection listing
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("collection-checker", polarion_connection)
