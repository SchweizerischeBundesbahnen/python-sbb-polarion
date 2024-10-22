"""Diff Tool Polarion Extension API"""

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionDiffToolApi(PolarionGenericExtensionApi):
    """Diff Tool Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "diff-tool")

    def convert_html(self, html: str, orientation: str = "landscape", paper_size: str = "A4") -> Response | None:
        """POST Returns requested HTML converted to PDF"""
        headers = {"Accept": "*/*", "Content-Type": "text/html"}
        params = {"orientation": orientation, "paperSize": paper_size}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/conversion/html-to-pdf", data=html, headers=headers, params=params)

    def diff_documents(self, data) -> Response | None:
        """Gets difference of two live documents"""
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/diff/documents", data=data)

    def diff_workitems(self, data) -> Response | None:
        """Gets difference of two workitems"""
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/diff/workitems", data=data)

    def diff_html(self, html1: str, html2: str) -> Response | None:
        """Gets difference of two strings which contain HTML tags"""
        files = {"html1": html1, "html2": html2}
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/diff/html", files=files)

    def diff_text(self, text1: str, text2: str) -> Response | None:
        """Gets difference of two strings which contain plain text"""
        files = {"text1": text1, "text2": text2}
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/diff/text", files=files)

    def merge_workitems(self, data) -> Response | None:
        """Merge workItems"""
        return self.polarion_connection.api_request_post(f"{self.rest_api_url}/merge/workitems", data=data)

    def get_documents_in_space(self, project_id: str, space_id: str) -> Response | None:
        """Gets list of documents located in specified space of specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents")

    def get_document_revisions(self, project_id: str, space_id: str, document_name: str) -> Response | None:
        """Gets list of revisions for the document located in specified space of specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/revisions")

    def get_spaces(self, project_id: str) -> Response | None:
        """Gets list of spaces (folders) located in specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/spaces")

    def get_all_workitem_fields(self, project_id: str) -> Response | None:
        """Gets full list of all general and custom fields configured for all kind of work items in specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/workitem-fields")

    def get_all_workitem_statuses(self, project_id: str) -> Response | None:
        """Gets list of all statuses configured for all kind of work items in specified project"""
        return self.polarion_connection.api_request_get(f"{self.rest_api_url}/projects/{project_id}/workitem-statuses")

    def save_settings(self, data, name: str = "Default", scope: str | None = None) -> Response | None:
        """save settings for diff-tool"""
        return super()._save_settings("diff", data, name=name, scope=scope)

    def delete_settings(self, name: str, scope: str | None = None) -> Response | None:
        """delete diff-tool settings"""
        return super()._delete_settings("diff", name=name, scope=scope)
