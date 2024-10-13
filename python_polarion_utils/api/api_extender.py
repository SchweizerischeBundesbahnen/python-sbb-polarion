"""API Extender Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionApiExtenderApi(PolarionGenericExtensionApi):
    """API Extender Polarion Extension API"""

    def __init__(self, polarion_connection):
        super().__init__("api-extender", polarion_connection)

    def save_custom_field(self, project_id, key, value):
        """save project custom field"""
        data = {"value": value}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/projects/{project_id}/keys/{key}", data=data)

    def get_custom_field(self, project_id, key):
        """get project custom field"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}/keys/{key}")

    def delete_custom_field(self, project_id, key):
        """delete project custom field"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/projects/{project_id}/keys/{key}")

    def save_record(self, key, value):
        """save global record"""
        data = {"value": value}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/records/{key}", data=data)

    def get_record(self, key):
        """get global record"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/records/{key}")

    def delete_record(self, key):
        """delete global record"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/records/{key}")
