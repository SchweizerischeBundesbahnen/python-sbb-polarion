"""Test data Polarion Extension API"""

from .generic import PolarionGenericExtensionApi


class PolarionTestDataApi(PolarionGenericExtensionApi):
    def __init__(self, polarion_connection):
        super().__init__("test-data", polarion_connection)

    def generate_large_document(self, project_id, space_id, document_name, quantity=None):
        """Generate test live document"""
        url = f"/{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}"
        if quantity:
            url += f"?quantity={quantity}"

        headers = {"Accept": "text/plain"}
        return self.polarion_connection.api_request_post(url, headers=headers)

    def change_work_item_descriptions(self, project_id, space_id, document_name, interval=None):
        """Update workitem descriptions in specified document"""
        url = f"/{self.rest_api_url}/projects/{project_id}/spaces/{space_id}/documents/{document_name}/change-wi-descriptions"
        if interval:
            url += f"?interval={interval}"

        headers = {"Accept": "text/plain"}
        return self.polarion_connection.api_request_patch(url, headers=headers)
