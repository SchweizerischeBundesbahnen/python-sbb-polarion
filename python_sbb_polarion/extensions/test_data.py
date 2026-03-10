"""Test data Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._test_data import DocumentsMixin, TemplatesMixin


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


class PolarionTestDataApi(
    DocumentsMixin,
    TemplatesMixin,
    PolarionGenericExtensionApi,
):
    """Test Data Polarion Extension API

    This class combines all test data functionality through mixins:
    - DocumentsMixin: Document operations with generated workitems
    - TemplatesMixin: Template hash and upload operations
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("test-data", polarion_connection)
