"""Excel Importer Polarion Extension API"""

import os

from .generic import PolarionGenericExtensionApi


class PolarionExcelImporterApi(PolarionGenericExtensionApi):
    """Excel Importer Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("excel-importer", polarion_connection)

    def import_excel_sheet(self, project_id, excel_file_path):
        """import Excel sheet"""
        url = f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/import"

        with open(excel_file_path, "rb") as excel_content:
            files = {"file": (os.path.basename(excel_file_path), excel_content)}

            headers = {"Accept": "application/json"}
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    def get_workitem_types(self, project_id):
        """get workitem types for selected project"""
        return self.polarion_connection.api_request_get(f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/workitem_types")

    def get_workitem_fields(self, project_id, workitem_type):
        """get workitem fields for selected project and workitem type"""
        return self.polarion_connection.api_request_get(f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/workitem_types/{workitem_type}/fields")

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
