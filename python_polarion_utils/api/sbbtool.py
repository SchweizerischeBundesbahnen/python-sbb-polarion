"""SBB Tool Polarion Extension API"""

from pathlib import Path
from typing import NamedTuple

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection

ACCEPT_HTML = {"Accept": "text/html"}
ACCEPT_XML = {"Accept": "application/xml"}


class AttachTableParams(NamedTuple):
    """Definition of parameters for attach_table API call"""

    objectType: str
    objectId: str
    htmlTable: str
    fileName: str
    fileTitle: str


class PolarionSBBToolApi(PolarionGenericExtensionApi):
    """SBB Tool Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "sbbtool")

    def find_regex_matches_in_string(self, text: str, regex: str) -> Response | None:
        """find regex matches in the string"""
        url = f"{self.rest_api_url}/find-regex-matches-in-string"
        files = {"text": text, "regex": regex}
        return self.polarion_connection.api_request_post(url, files=files)

    def diff_html(self, html1: str, html2: str) -> Response | None:
        """compare html"""
        url = f"{self.rest_api_url}/diff-html"
        files = {"html1": html1, "html2": html2}
        return self.polarion_connection.api_request_post(url, headers=ACCEPT_XML, files=files)

    def diff_text(self, text1: str, text2: str) -> Response | None:
        """compare text"""
        url = f"{self.rest_api_url}/diff-text"
        files = {"text1": text1, "text2": text2}
        return self.polarion_connection.api_request_post(url, headers=ACCEPT_XML, files=files)

    def sort_map(self, shuffled, ascending: bool) -> Response | None:
        """sort map"""
        url = f"{self.rest_api_url}/sort-map?ascending={ascending}"
        return self.polarion_connection.api_request_post(url, data=shuffled)

    def xlsx_from_html_table(self, html_table, file_name: str) -> Response | None:
        """create Excel file from html table"""
        url = f"{self.rest_api_url}/xlsx-from-html-table"
        files = {"htmlTable": html_table, "fileName": file_name}
        headers = {"Accept": "application/octet-stream"}
        return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    def html_table_from_list(self, source_list) -> Response | None:
        """create from html table from list"""
        url = f"{self.rest_api_url}/html-table-from-list"
        return self.polarion_connection.api_request_post(url, headers=ACCEPT_HTML, data=source_list)

    def attach_table(self, project_id: str, params: AttachTableParams) -> Response | None:
        """attach table as an attachment"""
        url = f"{self.rest_api_url}/projects/{project_id}/attach-table"
        return self.polarion_connection.api_request_post(url, data=params._asdict())

    def tables_from_attachments(self, project_id: str, object_type: str, object_id: str) -> Response | None:
        """create tables from attachments"""
        url = f"{self.rest_api_url}/projects/{project_id}/tables-from-attachments"
        data = {"objectType": object_type, "objectId": object_id}
        return self.polarion_connection.api_request_post(url, data=data)

    def htmls_from_attachments(self, project_id: str, object_type: str, object_id: str) -> Response | None:
        """create html tables from attachments"""
        url = f"{self.rest_api_url}/projects/{project_id}/htmls-from-attachments"
        data = {"objectType": object_type, "objectId": object_id}
        return self.polarion_connection.api_request_post(url, data=data)

    def list_from_xlsx(self, excel_file_path: str) -> Response | None:
        """list from xlsx"""
        url = f"{self.rest_api_url}/list-from-xlsx"
        with Path(excel_file_path).open("rb") as content:
            files = {"file": (Path(excel_file_path).name, content)}
            return self.polarion_connection.api_request_post(url, files=files)

    def html_from_xlsx(self, excel_file_path: str) -> Response | None:
        """html from xlsx"""
        url = f"{self.rest_api_url}/html-from-xlsx"
        with Path(excel_file_path).open("rb") as content:
            files = {"file": (Path(excel_file_path).name, content)}
            return self.polarion_connection.api_request_post(url, headers=ACCEPT_HTML, files=files)
