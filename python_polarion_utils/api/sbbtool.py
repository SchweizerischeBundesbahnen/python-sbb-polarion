"""SBB Tool Polarion Extension API"""

import os
from typing import NamedTuple

from .generic import PolarionGenericExtensionApi

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

    def __init__(self, polarion_connection):
        super().__init__("sbbtool", polarion_connection)

    def find_regex_matches_in_string(self, text, regex):
        """find regex matches in the string"""
        url = f"{self.rest_api_url}/find-regex-matches-in-string"
        files = {"text": text, "regex": regex}
        return self.polarion_connection.api_request_post(url, files=files)

    def diff_html(self, html1, html2):
        """compare html"""
        url = f"{self.rest_api_url}/diff-html"
        files = {"html1": html1, "html2": html2}
        return self.polarion_connection.api_request_post(url, headers=ACCEPT_XML, files=files)

    def diff_text(self, text1, text2):
        """compare text"""
        url = f"{self.rest_api_url}/diff-text"
        files = {"text1": text1, "text2": text2}
        return self.polarion_connection.api_request_post(url, headers=ACCEPT_XML, files=files)

    def sort_map(self, shuffled, ascending):
        """sort map"""
        url = f"{self.rest_api_url}/sort-map?ascending={ascending}"
        return self.polarion_connection.api_request_post(url, data=shuffled)

    def xlsx_from_html_table(self, html_table, file_name):
        """create Excel file from html table"""
        url = f"{self.rest_api_url}/xlsx-from-html-table"
        files = {"htmlTable": html_table, "fileName": file_name}
        headers = {"Accept": "application/octet-stream"}
        return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    def html_table_from_list(self, source_list):
        """create from html table from list"""
        url = f"{self.rest_api_url}/html-table-from-list"
        return self.polarion_connection.api_request_post(url, headers=ACCEPT_HTML, data=source_list)

    def attach_table(self, project_id, params: AttachTableParams):
        """attach table as an attachment"""
        url = f"{self.rest_api_url}/projects/{project_id}/attach-table"
        return self.polarion_connection.api_request_post(url, data=params._asdict())

    def tables_from_attachments(self, project_id, object_type, object_id):
        """create tables from attachments"""
        url = f"{self.rest_api_url}/projects/{project_id}/tables-from-attachments"
        data = {"objectType": object_type, "objectId": object_id}
        return self.polarion_connection.api_request_post(url, data=data)

    def htmls_from_attachments(self, project_id, object_type, object_id):
        """create html tables from attachments"""
        url = f"{self.rest_api_url}/projects/{project_id}/htmls-from-attachments"
        data = {"objectType": object_type, "objectId": object_id}
        return self.polarion_connection.api_request_post(url, data=data)

    def list_from_xlsx(self, excel_file_path):
        """list from xlsx"""
        url = f"{self.rest_api_url}/list-from-xlsx"
        with open(excel_file_path, "rb") as content:
            files = {"file": (os.path.basename(excel_file_path), content)}
            return self.polarion_connection.api_request_post(url, files=files)

    def html_from_xlsx(self, excel_file_path):
        """html from xlsx"""
        url = f"{self.rest_api_url}/html-from-xlsx"
        with open(excel_file_path, "rb") as content:
            files = {"file": (os.path.basename(excel_file_path), content)}
            return self.polarion_connection.api_request_post(url, headers=ACCEPT_HTML, files=files)
