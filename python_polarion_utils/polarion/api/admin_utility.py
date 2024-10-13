"""Admin Utility Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionAdminUtilityApi(PolarionGenericExtensionApi):
    """Admin Utility Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("admin-utility", polarion_connection)

    def activate_trial_license(self):
        """activate trial license"""
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/licenses/trial/activation")

    def create_security_token(self, name, expires_date):
        """create security token"""
        data = {"name": name, "expiresOn": expires_date}
        response = self.polarion_connection.api_request_post(f"/{self.rest_api_url}/tokens", data=data)
        return response.json()["token"]

    def get_project(self, project_id):
        """get project info"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}")

    def create_project(self, project_id, project_name, template_id):
        """create project from specified project template"""
        data = {"projectId": project_id, "projectName": project_name, "templateId": template_id}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/projects", data=data)

    def delete_project(self, project_id):
        """delete project info"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/projects/{project_id}")

    def create_token(self, name, expires_on):
        """create access token"""
        data = {"name": name, "expiresOn": expires_on}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/tokens", data=data)

    def delete_token(self, token_id):
        """delete token"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/tokens/{token_id}")

    def delete_all_tokens(self):
        """delete all tokens"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/tokens")

    def create_test_run_template(self, project_id, template_id):
        """create test run template"""
        data = {"templateId": template_id}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/projects/{project_id}/test-run-templates", data=data)

    def delete_module(self, project_id, space_id, module_id):
        """delete module"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{module_id}")

    def create_collection(self, project_id, collection_name):
        """create collection"""
        url = f"/{self.rest_api_url}/projects/{project_id}/collections"
        return self.polarion_connection.api_request_post(url, data={"collectionName": collection_name})

    def delete_collection(self, project_id, collection_id):
        """delete collection"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/projects/{project_id}/collections/{collection_id}")

    def add_to_collection(self, project_id, collection_id, module_id):
        """add an element to the collection"""
        url = f"/{self.rest_api_url}/projects/{project_id}/collections/{collection_id}/modules"
        return self.polarion_connection.api_request_post(url, data={"moduleId": module_id})

    def create_wiki_page(self, space_id, name, project_id=None):
        """create new wiki page"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += f"/spaces/{space_id}/wiki"
        return self.polarion_connection.api_request_post(url, data={"name": name})

    def delete_wiki_page(self, space_id, name, project_id=None):
        """Delete wiki page"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += f"/spaces/{space_id}/wiki/{name}"
        return self.polarion_connection.api_request_delete(url)

    def create_live_report(self, space_id, name, content_type, content, project_id=None):
        """create new live report"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += f"/spaces/{space_id}/report"
        data = {"name": name, "contentType": content_type, "content": content}
        return self.polarion_connection.api_request_post(url, data=data)

    def delete_live_report(self, space_id, name, project_id=None):
        """Delete live report"""
        url = f"/{self.rest_api_url}"
        if project_id:
            url += f"/projects/{project_id}"

        url += f"/spaces/{space_id}/report/{name}"
        return self.polarion_connection.api_request_delete(url)

    def set_custom_field_type(self, field_id, field_name, field_type, field_description=None, is_required=False, project_id=None, work_item_type=None):
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
