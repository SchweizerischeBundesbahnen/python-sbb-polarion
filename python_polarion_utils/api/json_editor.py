"""JSON Editor Polarion Extension API"""

from .generic import PolarionGenericExtensionApi

ACCEPT_TEXT = {"Accept": "text/plain"}


class PolarionJsonEditorApi(PolarionGenericExtensionApi):
    """JSON Editor Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("json-editor", polarion_connection)

    def get_attachment(self, project_id, workitem_id, attachment_id):
        """Get attachment content"""
        url = f"{self.rest_api_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}/content"
        return self.polarion_connection.api_request_get(url, headers=ACCEPT_TEXT)

    def create_attachment(self, project_id, workitem_id, file_name):
        """Create an attachment"""
        url = f"{self.rest_api_url}/projects/{project_id}/workitems/{workitem_id}/attachments"
        return self.polarion_connection.api_request_post(url, headers=ACCEPT_TEXT, files={"fileName": file_name})

    def update_attachment(self, project_id, workitem_id, attachment_id, content):
        """Update attachment content"""
        url = f"{self.rest_api_url}/projects/{project_id}/workitems/{workitem_id}/attachments/{attachment_id}"
        return self.polarion_connection.api_request_patch(url, headers=ACCEPT_TEXT, files={"content": content})
