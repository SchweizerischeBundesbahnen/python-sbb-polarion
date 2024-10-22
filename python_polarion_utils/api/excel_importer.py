"""Excel Importer Polarion Extension API"""

from pathlib import Path

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionExcelImporterApi(PolarionGenericExtensionApi):
    """Excel Importer Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "excel-importer")

    def import_excel_sheet(self, project_id: str, excel_file_path: str) -> Response | None:
        """import Excel sheet"""
        url = f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/import"

        with Path(excel_file_path).open(mode="rb") as excel_content:
            files = {"file": (Path(excel_file_path).name, excel_content)}

            headers = {"Accept": "application/json"}
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    def get_workitem_types(self, project_id: str) -> Response | None:
        """get workitem types for selected project"""
        return self.polarion_connection.api_request_get(f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/workitem_types")

    def get_workitem_fields(self, project_id: str, workitem_type: str) -> Response | None:
        """get workitem fields for selected project and workitem type"""
        return self.polarion_connection.api_request_get(f"/polarion/{self.extension_name}/rest/api/projects/{project_id}/workitem_types/{workitem_type}/fields")

    def get_settings(self, feature: str, name: str = "Default", scope: str | None = None) -> Response | None:
        """get settings for provided feature"""
        return super()._get_settings(feature, name=name, scope=scope)

    def save_settings(self, feature: str, data, name: str = "Default", scope: str | None = None) -> Response | None:
        """save settings for provided feature"""
        return super()._save_settings(feature, data, name=name, scope=scope)

    def get_settings_defaults(self, feature: str) -> Response | None:
        """get default settings for provided feature"""
        return super()._get_settings_defaults(feature)

    def get_settings_revisions(self, feature: str, name: str = "Default", scope: str | None = None) -> Response | None:
        """get settings revisions for provided feature"""
        return super()._get_settings_revisions(feature, name=name, scope=scope)
