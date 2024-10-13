"""Collection Checker Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionCollectionCheckerApi(PolarionGenericExtensionApi):
    """Collection Checker Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("collection-checker", polarion_connection)

    def get_checks(self, project_id, days_interval=1, page=1, count=20):
        """get checks list"""
        url = f"/{self.rest_api_url}/projects/{project_id}/checks?"
        url += f"&daysInterval={days_interval}"
        url += f"&page={page}"
        url += f"&count={count}"

        return self.polarion_connection.api_request_get(url)

    def get_check(self, project_id, check_id):
        """get check for provided id"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}/checks/{check_id}")

    def get_linkroles(self, project_id):
        """get project link roles"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}/linkroles")

    def get_check_json_report(self, project_id, check_id):
        """get check repost in JSON format"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}/checks/{check_id}/report?format=JSON")

    def get_check_text_log(self, project_id, check_id):
        """get check log as text"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}/checks/{check_id}/report?format=TXT")

    def get_collections(self, project_id):
        """get all collections within the project"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}/collections")

    def cancel_check(self, project_id, check_id):
        """cancel check"""
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/projects/{project_id}/checks/{check_id}/cancel")

    def start_check(self, project_id, collection_id, **kwargs):
        """start new check"""
        default_check_options = {
            "ignoreLinkRoles": None,
            "ignoreCopyingLinkRoles": None,
            "ignoreWorkItemIsContainedInMultipleRevisionsErrors": False,
            "ignoreLinkOutOfCollectionWithSpecificRevisionErrors": False,
        }
        check_options = {**default_check_options, **kwargs}

        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/projects/{project_id}/collections/{collection_id}/checks", data=check_options)
