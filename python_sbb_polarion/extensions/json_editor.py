"""JSON Editor Polarion Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._json_editor import WorkItemAttachmentsMixin


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


__all__ = ["PolarionJsonEditorApi"]


class PolarionJsonEditorApi(
    WorkItemAttachmentsMixin,
    PolarionGenericExtensionApi,
):
    """JSON Editor Polarion Extension API

    This class combines all JSON editor functionality through mixins:
    - WorkItemAttachmentsMixin: Work item attachment operations (create, update, get)
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("json-editor", polarion_connection)
