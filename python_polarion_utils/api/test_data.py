"""Test data Polarion Extension API"""

from requests import Response  # type: ignore

from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection


class PolarionTestDataApi(PolarionGenericExtensionApi):
    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__(polarion_connection, "test-data")

    def generate_large_document(self, project_id: str, space_id: str, document_name: str, quantity: int | None = None) -> Response | None:
        """Generate test live document"""
        url = f"/{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}"
        if quantity:
            url += f"?quantity={quantity}"

        headers = {"Accept": "text/plain"}
        return self.polarion_connection.api_request_post(url, headers=headers)

    def change_work_item_descriptions(self, project_id: str, space_id: str, document_name: str, interval: int | None = None) -> Response | None:
        """Update workitem descriptions in specified document"""
        url = f"/{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/change-wi-descriptions"
        if interval:
            url += f"?interval={interval}"

        headers = {"Accept": "text/plain"}
        return self.polarion_connection.api_request_patch(url, headers=headers)
