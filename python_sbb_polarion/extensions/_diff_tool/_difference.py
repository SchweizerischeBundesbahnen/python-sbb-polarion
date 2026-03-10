"""Diff Tool difference operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict


class DifferenceMixin(BaseMixin):
    """Difference operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/diff/collections",
        body_param="data",
        helper_params=["collection1_project_id", "collection1_id", "collection2_project_id", "collection2_id"],
        required_params=["__request_body__"],
    )
    def diff_collections(self, collection1_project_id: str, collection1_id: str, collection2_project_id: str, collection2_id: str) -> Response:
        """Gets difference of two live document collections

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/collections"
        data: JsonDict = {
            "leftCollection": {
                "id": collection1_id,
                "name": "any",
                "projectId": collection1_project_id,
                "projectName": "any",
            },
            "rightCollection": {
                "id": collection2_id,
                "name": "any",
                "projectId": collection2_project_id,
                "projectName": "any",
            },
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/diff/detached-workitems",
        body_param="data",
        required_params=["__request_body__"],
    )
    def diff_detached_workitems(self, data: JsonDict) -> Response:
        """Gets difference of two WorkItems not necessarily contained in a document

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/detached-workitems"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/diff/document-workitems",
        body_param="data",
        required_params=["__request_body__"],
    )
    def diff_document_workitems(self, data: JsonDict) -> Response:
        """Gets difference of two workitems from different documents

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/document-workitems"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/diff/documents",
        body_param="data",
        required_params=["__request_body__"],
    )
    def diff_documents(self, data: JsonDict) -> Response:
        """Gets difference of two live documents

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/documents"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/diff/documents-fields",
        body_param="data",
        required_params=["__request_body__"],
    )
    def diff_documents_fields(self, data: JsonDict) -> Response:
        """Gets difference of fields for two live documents

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/documents-fields"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/diff/documents-content",
        body_param="data",
        required_params=["__request_body__"],
    )
    def diff_documents_content(self, data: JsonDict) -> Response:
        """Gets difference of content for two live documents

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/documents-content"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/diff/html",
        multipart_fields={
            "html1": "html1",
            "html2": "html2",
        },
    )
    def diff_html(self, html1: str, html2: str) -> Response:
        """Gets difference of two strings which contain HTML tags

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/html"
        files: FilesDict = {
            "html1": html1,
            "html2": html2,
        }
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="POST",
        path="/api/diff/text",
        multipart_fields={
            "text1": "text1",
            "text2": "text2",
        },
    )
    def diff_text(self, text1: str, text2: str) -> Response:
        """Gets difference of two strings which contain plain text

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/text"
        files: FilesDict = {
            "text1": text1,
            "text2": text2,
        }
        return self.polarion_connection.api_request_post(url, files=files)

    @restapi_endpoint(
        method="POST",
        path="/api/diff/workitems-pairs",
        body_param="data",
        required_params=["__request_body__"],
    )
    def find_workitems_pairs(self, data: JsonDict) -> Response:
        """Finds pairs to specified WorkItems, for later diff

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/diff/workitems-pairs"
        return self.polarion_connection.api_request_post(url, data=data)
