"""API Extender Polarion Extension API"""

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionApiExtenderApi(PolarionGenericExtensionApi):
    """API Extender Polarion Extension API"""

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "api-extender")

    def save_custom_field(self, project_id: str, key: str, value: str) -> Response | None:
        """save project custom field"""
        data = {"value": value}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/projects/{project_id}/keys/{key}", data=data)

    def get_custom_field(self, project_id: str, key: str) -> Response | None:
        """get project custom field"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/projects/{project_id}/keys/{key}")

    def delete_custom_field(self, project_id: str, key: str) -> Response | None:
        """delete project custom field"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/projects/{project_id}/keys/{key}")

    def save_record(self, key: str, value: str) -> Response | None:
        """save global record"""
        data = {"value": value}
        return self.polarion_connection.api_request_post(f"/{self.rest_api_url}/records/{key}", data=data)

    def get_record(self, key: str) -> Response | None:
        """get global record"""
        return self.polarion_connection.api_request_get(f"/{self.rest_api_url}/records/{key}")

    def delete_record(self, key: str) -> Response | None:
        """delete global record"""
        return self.polarion_connection.api_request_delete(f"/{self.rest_api_url}/records/{key}")
