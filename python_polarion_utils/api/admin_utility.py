"""Admin Utility Extension API"""

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionAdminUtilityApi(PolarionGenericExtensionApi):
    """Admin Utility Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "admin-utility")

    def activate_trial_license(self) -> Response | None:
        """activate trial license"""
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/licenses/trial/activation")

    def create_security_token(self, name: str, expires_date: str) -> str | None:
        """create security token"""
        data = {"name": name, "expiresOn": expires_date}
        response = self.polarion_connection.api_request_post(f"/{self.rest_api_url}/tokens", data=data)
        return response.json()["token"] if response else None

    def get_project(self, project_id: str) -> Response | None:
        """get project info"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}")

    def create_project(self, project_id: str, project_name: str, template_id: str) -> Response | None:
        """create project from specified project template"""
        data = {"projectId": project_id, "projectName": project_name, "templateId": template_id}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/projects", data=data)

    def delete_project(self, project_id: str) -> Response | None:
        """delete project info"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/projects/{project_id}")

    def create_token(self, name: str, expires_on: str) -> Response | None:
        """create access token"""
        data = {"name": name, "expiresOn": expires_on}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/tokens", data=data)

    def delete_token(self, token_id: str) -> Response | None:
        """delete token"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/tokens/{token_id}")

    def delete_all_tokens(self) -> Response | None:
        """delete all tokens"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/tokens")

    def create_test_run_template(self, project_id: str, template_id: str) -> Response | None:
        """create test run template"""
        data = {"templateId": template_id}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/projects/{project_id}/test-run-templates", data=data)

    def delete_module(self, project_id: str, space_id: str, module_id: str) -> Response | None:
        """delete module"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{module_id}")

    def create_collection(self, project_id: str, collection_name: str) -> Response | None:
        """create collection"""
        url = f"/{self.rest_api_url}/projects/{project_id}/collections"
        return self.polarion_connection.api_request_post(url, data={"collectionName": collection_name})

    def delete_collection(self, project_id: str, collection_id: str) -> Response | None:
        """delete collection"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/projects/{project_id}/collections/{collection_id}")

    def add_to_collection(self, project_id: str, collection_id: str, module_id: str) -> Response | None:
        """add an element to the collection"""
        url = f"/{self.rest_api_url}/projects/{project_id}/collections/{collection_id}/modules"
        return self.polarion_connection.api_request_post(url, data={"moduleId": module_id})

    def create_wiki_page(self, space_id: str, name: str, project_id: str | None = None) -> Response | None:
        """create new wiki page"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += f"/spaces/{space_id}/wiki"
        return self.polarion_connection.api_request_post(url, data={"name": name})

    def delete_wiki_page(self, space_id: str, name: str, project_id: str | None = None) -> Response | None:
        """Delete wiki page"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += f"/spaces/{space_id}/wiki/{name}"
        return self.polarion_connection.api_request_delete(url)

    def create_live_report(self, space_id: str, name: str, content_type: str, content: str, project_id: str | None = None) -> Response | None:
        """create new live report"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += f"/spaces/{space_id}/report"
        data = {"name": name, "contentType": content_type, "content": content}
        return self.polarion_connection.api_request_post(url, data=data)

    def delete_live_report(self, space_id: str, name: str, project_id: str | None = None) -> Response | None:
        """Delete live report"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += f"/spaces/{space_id}/report/{name}"
        return self.polarion_connection.api_request_delete(url)

    def set_custom_field_type(self, field_id: str, field_name: str, field_type: str, field_description: str | None = None, is_required: bool = False, project_id: str | None = None, work_item_type: str | None = None) -> Response | None:
        """create new live report"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += "/custom-fields"
        data = {
            "workItemType": work_item_type,
            "customFields": [{"id": field_id, "name": field_name, "type": field_type, "description": field_description, "isRequired": is_required}],
        }
        return self.polarion_connection.api_request_put(url, data=data)
