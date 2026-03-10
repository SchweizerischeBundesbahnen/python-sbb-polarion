"""Documents branching operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class DocumentsBranchingMixin(BaseMixin):
    """Documents branching operations.

    Provides methods for document branching and merging.
    """

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/actions/branch",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "revision": "revision",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def branch_document(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        data: JsonDict,
        revision: str | None = None,
    ) -> Response:
        """Create a branch of the document.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            data: Branch configuration data
            revision: Specific revision to branch from

        Returns:
            Response: Branch result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/branch"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_post(url, data=data, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/all/documents/actions/branch",
        body_param="data",
        response_type="json",
    )
    def branch_documents(self, data: JsonDict) -> Response:
        """Create branches of multiple documents (global operation).

        Args:
            data: Branch configuration data for multiple documents

        Returns:
            Response: Branch results from API
        """
        url: str = f"{self.base_url}/all/documents/actions/branch"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/actions/copy",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        query_params={
            "revision": "revision",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def copy_document(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        data: JsonDict,
        revision: str | None = None,
    ) -> Response:
        """Create a copy of the document.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            data: Copy configuration data
            revision: Specific revision to copy from

        Returns:
            Response: Copy result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/copy"
        params: dict[str, str] = {}
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_post(url, data=data, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/actions/mergeFromMaster",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def merge_document_from_master(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        data: JsonDict,
    ) -> Response:
        """Merge Master Work Item changes to the specified Branched Document.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            data: Merge configuration data

        Returns:
            Response: Merge result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/mergeFromMaster"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/spaces/{spaceId}/documents/{documentName}/actions/mergeToMaster",
        path_params={
            "projectId": "project_id",
            "spaceId": "space_id",
            "documentName": "document_name",
        },
        body_param="data",
        required_params=["projectId", "spaceId", "documentName"],
        response_type="json",
    )
    def merge_document_to_master(
        self,
        project_id: str,
        space_id: str,
        document_name: str,
        data: JsonDict,
    ) -> Response:
        """Merge Work Item changes from specified Branched Document to Master.

        Args:
            project_id: Project identifier
            space_id: Space identifier
            document_name: Document name
            data: Merge configuration data

        Returns:
            Response: Merge result from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/mergeToMaster"
        return self.polarion_connection.api_request_post(url, data=data)
