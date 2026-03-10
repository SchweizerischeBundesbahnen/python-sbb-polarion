"""Requirements Inspector inspection mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class InspectionMixin(BaseMixin):
    """Inspection operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/inspect/workitems",
        body_param="data",
        required_params=["__request_body__"],
        response_type="json",
    )
    def inspect_workitems(self, data: JsonDict) -> Response:
        """Inspect multiple workitems for quality issues

        Args:
            data: Request body containing inspection parameters:
                - ids (list[str]): Workitem identifiers to inspect
                - projectId (str): Project identifier
                - inspectFields (list[str], optional): Specific fields to analyze
                - ignoreInspectTitle (bool, optional): Skip title inspection
                - addMissingLanguage (bool, optional): Auto-detect language

        Returns:
            Response: Response object containing array of WorkItemResponse objects
                with quality metrics (language, smells, complexity, etc.)
        """
        url: str = f"{self.rest_api_url}/inspect/workitems"
        return self.polarion_connection.api_request_post(url, data=data)
