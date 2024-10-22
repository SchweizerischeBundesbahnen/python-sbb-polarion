"""Cucumber Polarion Extension API"""

from pathlib import Path

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionCucumberApi(PolarionGenericExtensionApi):
    """Cucumber Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "cucumber")

    def save_feature(self, project_id: str, workitem_id: str, title: str, content) -> Response | None:
        """save feature"""
        filename = f"{workitem_id}.feature"
        data = {"projectId": project_id, "workItemId": workitem_id, "title": title, "filename": filename, "content": content}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/feature", data=data)

    def get_feature(self, project_id: str, workitem_id: str) -> Response | None:
        """get feature"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/feature/{project_id}/{workitem_id}")

    def get_jira_fields(self, project_id: str) -> Response | None:
        """get jira fields"""
        headers = {"Accept": "application/json", "projectId": project_id}
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/2/field", headers=headers)

    def export_test(self, keys: str | None = None, filter_query: str | None = None, fz: bool = True) -> Response | None:
        """
        export features
        keys -- list of workitem ids -- example "elibrary/EL-4;elibrary/EL-5"
        filter_query -- polarion query to find workitems
        fz -- if true -- zip files with all found features, if false -- first found feature
        """
        url = f"/polarion/{self.extension_name}/rest/raven/1.0/export/test?"
        if keys:
            url += f"keys={keys}"
        elif filter_query:
            url += f"keys={filter_query}"
        url += f"&fz={str(fz).lower()}"

        headers = {"Accept": "application/octet-stream"}
        return self.polarion_connection.api_request_get(url, headers=headers)

    def import_cucumber_test_results_multipart(self, info_file_path: str, result_file_path: str) -> Response | None:
        """import cucumber test results"""
        url = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/cucumber/multipart"

        with Path(info_file_path).open(encoding="utf-8") as info_content, Path(result_file_path).open(encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files = {"info": ("cucumber-info.json", info_content, "application/json"), "result": ("cucumber-result.json", result_content, "application/json")}

            headers = {"Accept": "application/json"}
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    def import_junit_test_results(self, parameters: dict[str, str], result_file_path: str) -> Response | None:
        """import JUnit test results"""
        url = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/junit?"

        for key, value in parameters.items():
            url += f"&{key}={value}"

        with Path(result_file_path).open(encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files = {"file": ("result.json", result_content, "application/json")}

            headers = {"Accept": "application/json"}
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    def import_junit_test_results_multipart(self, info_file_path: str, result_file_path: str) -> Response | None:
        """import JUnit test results"""
        url = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/junit/multipart"

        with Path(info_file_path).open(encoding="utf-8") as info_content, Path(result_file_path).open(encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files = {"info": ("info.json", info_content, "application/json"), "file": ("result.json", result_content, "application/json")}

            headers = {"Accept": "application/json"}
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)
