"""JSON Editor Polarion Extension API"""

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection

ACCEPT_TEXT = {"Accept": "text/plain"}


class PolarionJsonEditorApi(PolarionGenericExtensionApi):
    """JSON Editor Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "json-editor")

    def get_attachment(self, project_id: str, workitem_id: str, attachment_id: str) -> Response | None:
        """Get attachment content"""
        url = f"{self.rest_api_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}/content"
        return self.polarion_connection.api_request_get(url, headers=ACCEPT_TEXT)

    def create_attachment(self, project_id: str, workitem_id: str, file_name: str) -> Response | None:
        """Create an attachment"""
        url = f"{self.rest_api_url}/projects/{project_id}/workitems/{workitem_id}/attachments"
        return self.polarion_connection.api_request_post(url, headers=ACCEPT_TEXT, files={"fileName": file_name})

    def update_attachment(self, project_id: str, workitem_id: str, attachment_id: str, content) -> Response | None:
        """Update attachment content"""
        url = f"{self.rest_api_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_patch(url, headers=ACCEPT_TEXT, files={"content": content})
