"""PDF Exporter Polarion Extension API"""

import os
from enum import Enum

from .generic import PolarionGenericExtensionApi


class DocumentType(str, Enum):
    """Document type"""

    LIVE_DOC = "LIVE_DOC"
    LIVE_REPORT = "LIVE_REPORT"
    TEST_RUN = "TEST_RUN"
    WIKI_PAGE = "WIKI_PAGE"


class PolarionPdfExporterApi(PolarionGenericExtensionApi):
    """PDF Exporter Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("pdf-exporter", polarion_connection)

    def convert(self, export_params):
        """POST Returns requested Polarion's document converted to PDF"""
        headers = {"Accept": "application/pdf", "Content-Type": "application/json"}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/convert", data=export_params, headers=headers)

    def prepared_html_content(self, export_params):
        """POST Returns requested Polarion's document as HTML which can be used later for PDF generation"""
        headers = {"Accept": "text/html", "Content-Type": "application/json"}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/prepared-html-content", data=export_params, headers=headers)

    def start_pdf_converter_job(self, export_params):
        """POST Starts asynchronous conversion job of Polarion's document to PDF"""
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/convert/jobs", data=export_params, headers=headers)

    def get_pdf_converter_job_status(self, job_id):
        """Get conversion job status"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/convert/jobs/{job_id}", allow_redirects=False)

    def get_pdf_converter_job_result(self, job_id):
        """Get conversion result"""
        headers = {"Accept": "application/pdf", "Content-Type": "application/json"}
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/convert/jobs/{job_id}/result", headers=headers)

    def get_all_pdf_converter_jobs(self):
        """Get all jobs"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/convert/jobs/")

    def convert_html(self, html, orientation="portrait", paper_size="A4", filename="html-to-pdf.pdf"):
        """POST Returns requested HTML converted to PDF"""
        headers = {"Accept": "*/*", "Content-Type": "text/html"}
        params = {"orientation": orientation, "paperSize": paper_size, "fileName": filename}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/convert/html", data=html, headers=headers, params=params)

    def validate(self, export_params, max_results=6):
        """POST Validates if requested Polarion's document been converted to PDF doesn't contain pages which content exceeds page's width"""
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/validate?max-results={max_results}", data=export_params)

    def settings_localization_download(self, language, name="Default", scope=None, revision=None):
        """GET Downloads XLIFF for provided language"""
        url = f"/{self.rest_api_url}/settings/localization/names/{name}/download?language={language}"
        if scope:
            url += f"&scope={scope}"
        if revision:
            url += f"&revision={revision}"

        headers = {"Accept": "application/xml"}
        return self.polarion_connection.api_request_get(url, headers=headers)

    def settings_localization_upload(self, xliff_file_path, language, scope):
        """POST Uploads XLIFF and parse it on server, as result JSON will be returned"""
        url = f"/{self.rest_api_url}/settings/localization/upload?language={language}"
        if scope:
            url += f"&scope={scope}"

        with open(xliff_file_path, encoding="utf-8") as xliff_content:
            files = {"file": (os.path.basename(xliff_file_path), xliff_content)}

            return self.polarion_connection.api_request_post(url, files=files)

    def check_nested_lists(self, export_params):
        """POST Checks if requested Polarion's document contains nested lists"""
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/checknestedlists", data=export_params)

    def get_settings(self, feature, name="Default", scope=None):
        """get settings for provided feature"""
        return super()._get_settings(feature, name=name, scope=scope)

    def save_settings(self, feature, data, name="Default", scope=None):
        """save settings for provided feature"""
        return super()._save_settings(feature, data, name=name, scope=scope)

    def get_settings_defaults(self, feature):
        """get default settings for provided feature"""
        return super()._get_settings_defaults(feature)

    def get_settings_revisions(self, feature, name="Default", scope=None):
        """get settings revisions for provided feature"""
        return super()._get_settings_revisions(feature, name=name, scope=scope)

    def get_document_filename(self, data):
        """get filename for converted document"""
        headers = {"Accept": "text/plain"}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/export-filename", headers=headers, data=data)

    def get_webhooks_status(self):
        """get status of webhooks"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/webhooks/status")

    def get_project_name(self, project_id):
        """get name of requested project"""
        headers = {"Accept": "text/plain"}
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}/name", headers=headers)

    def get_document_language(self, project_id, space_id, document_name, revision=None):
        """get language of requested document"""
        url = f"/{self.rest_api_url}/document-language?projectId={project_id}&spaceId={space_id}&documentName={document_name}"
        if revision:
            url += f"&revision={revision}"

        headers = {"Accept": "text/plain"}
        return self.polarion_connection.api_request_get(url, headers=headers)

    def get_link_role_names(self, scope):
        """get names of link-roles from requested scope"""

        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/link-role-names?scope={scope}")
