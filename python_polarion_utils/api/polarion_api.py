"""Polarion builtin REST API used for system tests"""

import json
from pathlib import Path

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionApi(PolarionGenericExtensionApi):
    """Polarion builtin REST API used for system tests"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        self.polarion_connection = polarion_connection
        self.base_url = "/polarion/rest/v1"

    def get_workitem(self, project_id: str, workitem_id: str) -> Response | None:
        """get polarion workitem"""
        url = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}"
        return self.polarion_connection.api_request_get(url)

    def create_workitem(self, project_id: str, attributes: list[str]) -> Response | None:
        """create polarion workitem"""
        url = f"{self.base_url}/projects/{project_id}/workitems"
        if "type" not in attributes:
            raise KeyError("Attribute 'type' is required")
        data = {
            "data": [
                {
                    "type": "workitems",
                    "attributes": attributes,
                }
            ]
        }
        return self.polarion_connection.api_request_post(url, data=data)

    def delete_workitem(self, project_id: str, workitem_id: str) -> Response | None:
        """delete polarion workitem"""
        url = f"{self.base_url}/projects/{project_id}/workitems"
        data = {"data": [{"type": "workitems", "id": workitem_id}]}
        return self.polarion_connection.api_request_delete(url, data=data)

    def get_attachments(self, project_id: str, workitem_id: str) -> Response | None:
        """get polarion attachments"""
        url = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments"
        return self.polarion_connection.api_request_get(url)

    def create_wi_attachment(self, project_id: str, workitem_id: str, file_path: str, attributes: list[str]) -> Response | None:
        """create polarion attachment"""
        url = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments"
        resource = {"data": [{"type": "workitem_attachments", "attributes": attributes}]}
        with Path(file_path).open("rb") as content:
            files = {"resource": json.dumps(resource), "files": (Path(file_path).name, content)}
            return self.polarion_connection.api_request_post(url, files=files)

    def delete_attachment(self, project_id: str, workitem_id: str, attachment_id: str) -> Response | None:
        """delete polarion attachment"""
        url = f"{self.base_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_delete(url)

    def create_module(self, project_id: str, space_id: str, attributes: list[str]) -> Response | None:
        """create polarion module"""
        url = f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents"
        if "type" not in attributes:
            raise KeyError("Attribute 'type' is required")
        if "moduleName" not in attributes:
            raise KeyError("Attribute 'moduleName' is required")
        data = {"data": [{"type": "documents", "attributes": attributes}]}
        return self.polarion_connection.api_request_post(url, data=data)

    def copy_document(self, project_id: str, space_id: str, document_name: str, data) -> Response | None:
        """Copy live document"""
        return self.polarion_connection.api_request_post(f"{self.base_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/actions/copy", data=data)
