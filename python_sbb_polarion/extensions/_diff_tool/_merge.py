"""Diff Tool merge operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class MergeMixin(BaseMixin):
    """Merge operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/merge/documents",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_document_workitems(self, data: JsonDict) -> Response:
        """Merge workItems from different documents

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/documents"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/merge/documents-fields",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_documents_fields(self, data: JsonDict) -> Response:
        """Merge fields values from one live document into another

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/documents-fields"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/merge/documents-content",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_documents_content(self, data: JsonDict) -> Response:
        """Merge content from one live document into another

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/documents-content"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/merge/workitems",
        body_param="data",
        required_params=["__request_body__"],
    )
    def merge_detached_workitems(self, data: JsonDict) -> Response:
        """Merge workItems out of documents scope

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/merge/workitems"
        return self.polarion_connection.api_request_post(url, data=data)
