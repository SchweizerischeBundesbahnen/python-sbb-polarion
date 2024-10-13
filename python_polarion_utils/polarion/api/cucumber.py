"""Cucumber Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionCucumberApi(PolarionGenericExtensionApi):
    """Cucumber Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("cucumber", polarion_connection)

    def save_feature(self, project_id, workitem_id, title, content):
        """save feature"""
        filename = f"{workitem_id}.feature"
        data = {"projectId": project_id, "workItemId": workitem_id, "title": title, "filename": filename, "content": content}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/feature", data=data)

    def get_feature(self, project_id, workitem_id):
        """get feature"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/feature/{project_id}/{workitem_id}")

    def get_jira_fields(self, project_id):
        """get jira fields"""
        headers = {"Accept": "application/json", "projectId": project_id}
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/2/field", headers=headers)

    def export_test(self, keys: str = None, filter_query: str = None, fz: bool = True):
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

    def import_cucumber_test_results_multipart(self, info_file_path, result_file_path):
        """import cucumber test results"""
        url = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/cucumber/multipart"

        with open(info_file_path, encoding="utf-8") as info_content, open(result_file_path, encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files = {"info": ("cucumber-info.json", info_content, "application/json"), "result": ("cucumber-result.json", result_content, "application/json")}

            headers = {"Accept": "application/json"}
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    def import_junit_test_results(self, parameters, result_file_path):
        """import JUnit test results"""
        url = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/junit?"

        for key, value in parameters.items():
            url += f"&{key}={value}"

        with open(result_file_path, encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files = {"file": ("result.json", result_content, "application/json")}

            headers = {"Accept": "application/json"}
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    def import_junit_test_results_multipart(self, info_file_path, result_file_path):
        """import JUnit test results"""
        url = f"/polarion/{self.extension_name}/rest/raven/1.0/import/execution/junit/multipart"

        with open(info_file_path, encoding="utf-8") as info_content, open(result_file_path, encoding="utf-8") as result_content:
            # Multipart media type in cucumber REST API must be supported to be compatible with X-Ray Jenkins plugin
            files = {"info": ("info.json", info_content, "application/json"), "file": ("result.json", result_content, "application/json")}

            headers = {"Accept": "application/json"}
            return self.polarion_connection.api_request_post(url, headers=headers, files=files)
