"""OpenText Fake Content Server management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict, JsonDict


class OpenTextMixin(BaseMixin):
    """OpenText Fake Content Server management operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/opentext/api/v1/auth",
        body_param="data",
        helper_params=["username", "password"],
        required_params=[],
    )
    def authenticate(self, username: str, password: str) -> Response:
        """Authenticate to DMS

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/api/v1/auth"
        data: JsonDict = {
            "username": username,
            "password": password,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="POST",
        path="/api/opentext/api/v1/nodes",
        multipart_fields={
            "type": "type",
            "parent_id": "parent_id",
            "name": "name",
            "file": "file",
        },
        header_params={
            "OTCSTICKET": "ticket",
        },
        required_params=["OTCSTICKET"],
        response_type="json",
    )
    def write_file_to_container(self, ticket: str, type_param: str, parent_id: str, name: str, file: bytes) -> Response:
        """Write a file into DMS container

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/api/v1/nodes"
        headers: dict[str, str] = {
            "OTCSTICKET": ticket,
        }
        files: FilesDict = {
            "type": ("type.txt", type_param),
            "parent_id": ("parent_id.txt", parent_id),
            "name": ("name.txt", name),
            "file": ("file.pdf", file),
        }
        return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    @restapi_endpoint(
        method="POST",
        path="/api/opentext/api/v2/nodes/{nodeId}/versions/{version}/promote",
        path_params={
            "nodeId": "nodeId",
            "version": "version",
        },
        header_params={
            "OTCSTICKET": "ticket",
        },
        required_params=["OTCSTICKET", "nodeId", "version"],
        response_type="json",
    )
    def promote_version(self, ticket: str, node_id: str, version: str) -> Response:
        """Promote a version of a DMS node

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/api/v2/nodes/{node_id}/versions/{version}/promote"
        headers: dict[str, str] = {
            "OTCSTICKET": ticket,
        }
        return self.polarion_connection.api_request_post(url, headers=headers)

    @restapi_endpoint(
        method="POST",
        path="/api/opentext/api/v1/nodes/{nodeId}/versions",
        path_params={
            "nodeId": "nodeId",
        },
        multipart_fields={
            "add_major_version": "add_major_version",
            "file": "file",
        },
        header_params={
            "OTCSTICKET": "ticket",
        },
        required_params=["OTCSTICKET", "nodeId"],
        response_type="json",
    )
    def write_new_file_version(self, ticket: str, node_id: str, add_major_version: str, file: bytes) -> Response:
        """Write a new file version

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/api/v1/nodes/{node_id}/versions"
        headers: dict[str, str] = {
            "OTCSTICKET": ticket,
        }
        files: FilesDict = {
            "add_major_version": ("add_major_version.txt", add_major_version),
            "file": ("file.pdf", file),
        }
        return self.polarion_connection.api_request_post(url, headers=headers, files=files)

    @restapi_endpoint(
        method="GET",
        path="/api/opentext/api/v1/nodes/{nodeId}/output",
        path_params={
            "nodeId": "nodeId",
        },
        query_params={
            "destination": "destination",
            "name": "name",
            "containerid": "container_id",
            "filename": "filename",
        },
        header_params={
            "OTCSTICKET": "ticket",
        },
        required_params=["OTCSTICKET", "nodeId", "name", "filename"],
        response_type="json",
    )
    def get_output_from_webreport_node_execution(self, ticket: str, node_id: str, destination: str, name: str, container_id: str, filename: str) -> Response:
        """Run a WebReport

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/api/v1/nodes/{node_id}/output"
        headers: dict[str, str] = {
            "OTCSTICKET": ticket,
        }
        params: dict[str, str] = {
            "destination": destination,
            "name": name,
            "containerid": container_id,
            "filename": filename,
        }
        return self.polarion_connection.api_request_get(url, headers=headers, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/opentext/manage/users",
        required_params=[],
        response_type="json",
    )
    def get_dms_users(self) -> Response:
        """Get all DMS users

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/manage/users"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/opentext/manage/users",
        query_params={
            "username": "username",
            "password": "password",
        },
        required_params=["username", "password"],
    )
    def add_dms_user(self, username: str, password: str) -> Response:
        """Add a new DMS user

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/manage/users"
        params: dict[str, str] = {
            "username": username,
            "password": password,
        }
        return self.polarion_connection.api_request_post(url, params=params)

    @restapi_endpoint(
        method="DELETE",
        path="/api/opentext/manage/users/{username}",
        path_params={
            "username": "username",
        },
        required_params=["username"],
    )
    def delete_dms_user(self, username: str) -> Response:
        """Delete DMS user

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/manage/users/{username}"
        return self.polarion_connection.api_request_delete(url)

    @restapi_endpoint(
        method="GET",
        path="/api/opentext/manage/uploads",
        query_params={
            "ticket": "ticket",
        },
        required_params=[],
        response_type="json",
    )
    def get_dms_uploads(self, ticket: str | None = None) -> Response:
        """Get all executed DMS uploads

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] | None = {"ticket": ticket} if ticket else None
        url: str = f"{self.rest_api_url}/opentext/manage/uploads"
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="DELETE",
        path="/api/opentext/manage/uploads",
        query_params={
            "ticket": "ticket",
        },
        required_params=[],
    )
    def delete_dms_uploads(self, ticket: str | None = None) -> Response:
        """POST Delete all executed DMS uploads

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] | None = {"ticket": ticket} if ticket else None
        url: str = f"{self.rest_api_url}/opentext/manage/uploads"
        return self.polarion_connection.api_request_delete(url, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/opentext/manage/containers",
        query_params={
            "ticket": "ticket",
        },
        required_params=[],
        response_type="json",
    )
    def get_dms_containers(self, ticket: str | None = None) -> Response:
        """Get all created DMS containers

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] | None = {"ticket": ticket} if ticket else None
        url: str = f"{self.rest_api_url}/opentext/manage/containers"
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="DELETE",
        path="/api/opentext/manage/containers",
        query_params={
            "ticket": "ticket",
        },
        required_params=[],
    )
    def delete_dms_containers(self, ticket: str | None = None) -> Response:
        """Delete all created DMS containers

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] | None = {"ticket": ticket} if ticket else None
        url: str = f"{self.rest_api_url}/opentext/manage/containers"
        return self.polarion_connection.api_request_delete(url, params=params)

    @restapi_endpoint(
        method="DELETE",
        path="/api/opentext/manage/tickets",
        query_params={
            "ticket": "ticket",
        },
        required_params=[],
    )
    def delete_tickets(self, ticket: str | None = None) -> Response:
        """Delete ticket(s)

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] | None = {"ticket": ticket} if ticket else None
        url: str = f"{self.rest_api_url}/opentext/manage/tickets"
        return self.polarion_connection.api_request_delete(url, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/opentext/manage/tickets",
        required_params=[],
        response_type="json",
    )
    def get_dms_tickets(self) -> Response:
        """Get all DMS tickets

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/opentext/manage/tickets"
        return self.polarion_connection.api_request_get(url)

    def get_dms_ticket_for_user(self, username: str) -> str | None:
        """Retrieve registered ticket for the specified username

        Returns:
            Response: Response object from the API call
        """
        result: str | None = self.get_dms_tickets().json().get(username)
        return result
