"""Diff Tool Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionDiffToolApi(PolarionGenericExtensionApi):
    """Diff Tool Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("diff-tool", polarion_connection)

    def convert_html(self, html, orientation="landscape", paper_size="A4"):
        """POST Returns requested HTML converted to PDF"""
        headers = {"Accept": "*/*", "Content-Type": "text/html"}
        params = {"orientation": orientation, "paperSize": paper_size}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/conversion/html-to-pdf", data=html, headers=headers, params=params)

    def diff_documents(self, data):
        """Gets difference of two live documents"""
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/diff/documents", data=data)

    def diff_workitems(self, data):
        """Gets difference of two workitems"""
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/diff/workitems", data=data)

    def diff_html(self, html1, html2):
        """Gets difference of two strings which contain HTML tags"""
        files = {"html1": html1, "html2": html2}
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/diff/html", files=files)

    def diff_text(self, text1, text2):
        """Gets difference of two strings which contain plain text"""
        files = {"text1": text1, "text2": text2}
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/diff/text", files=files)

    def merge_workitems(self, data):
        """Merge workItems"""
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/merge/workitems", data=data)

    def get_documents_in_space(self, project_id, space_id):
        """Gets list of documents located in specified space of specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents")

    def get_document_revisions(self, project_id, space_id, document_name):
        """Gets list of revisions for the document located in specified space of specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/revisions")

    def get_spaces(self, project_id):
        """Gets list of spaces (folders) located in specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/spaces")

    def get_all_workitem_fields(self, project_id):
        """Gets full list of all general and custom fields configured for all kind of work items in specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/workitem-fields")

    def get_all_workitem_statuses(self, project_id):
        """Gets list of all statuses configured for all kind of work items in specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/workitem-statuses")

    def save_settings(self, data, name="Default", scope=None):
        """save settings for diff-tool"""
        return super()._save_settings("diff", data, name=name, scope=scope)

    def delete_settings(self, name, scope=None):
        """delete diff-tool settings"""
        return super()._delete_settings("diff", name=name, scope=scope)
