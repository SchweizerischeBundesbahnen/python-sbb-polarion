"""XML Repair repair operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class RepairMixin(BaseMixin):
    """Repair operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/baselines",
        query_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_baselines(self, project_id: str) -> Response:
        """Gets list of baselines for the given project

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] = {
            "projectId": project_id,
        }
        url: str = f"{self.rest_api_url}/baselines"
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/work-item-types",
        query_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_work_item_types(self, project_id: str) -> Response:
        """Gets list of work item types for the given project

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] = {
            "projectId": project_id,
        }
        url: str = f"{self.rest_api_url}/work-item-types"
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/document-types",
        query_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_document_types(self, project_id: str) -> Response:
        """Gets list of document types for the given project

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] = {
            "projectId": project_id,
        }
        url: str = f"{self.rest_api_url}/document-types"
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/link-roles",
        query_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_link_roles(self, project_id: str) -> Response:
        """Gets list of work item link roles for the given project

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] = {
            "projectId": project_id,
        }
        url: str = f"{self.rest_api_url}/link-roles"
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="GET",
        path="/api/repairers",
        query_params={
            "entityType": "entity_type",
        },
        required_params=["entityType"],
    )
    def get_repairers(self, entity_type: str) -> Response:
        """Gets list of repairers for specified entity type

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] = {}
        if entity_type:
            params["entityType"] = entity_type
        url: str = f"{self.rest_api_url}/repairers"
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/api/scan",
        body_param="scan_params",
        naming_ok=True,
    )
    def scan(self, scan_params: JsonDict) -> Response:
        """Scans entities for XML issues

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/scan"
        return self.polarion_connection.api_request_post(url, data=scan_params)

    @restapi_endpoint(
        method="POST",
        path="/api/repair",
        body_param="repair_params",
        naming_ok=True,
    )
    def repair(self, repair_params: JsonDict) -> Response:
        """Repairs XML issues identified by scan

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/repair"
        return self.polarion_connection.api_request_post(url, data=repair_params)

    @restapi_endpoint(
        method="POST",
        path="/api/scan/jobs",
        body_param="scan_params",
        required_params=["__request_body__"],
    )
    def start_scan_job(self, scan_params: JsonDict) -> Response:
        """Starts an asynchronous scan of entities for XML issues

        Returns:
            Response: Response object from the API call, the job URI in its Location header
        """
        url: str = f"{self.rest_api_url}/scan/jobs"
        return self.polarion_connection.api_request_post(url, data=scan_params)

    @restapi_endpoint(
        method="GET",
        path="/api/scan/jobs/{id}",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
    )
    def get_scan_job_status(self, job_id: str) -> Response:
        """Gets the status of a scan job, without following the redirect to its result

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/scan/jobs/{job_id}"
        return self.polarion_connection.api_request_get(url, allow_redirects=False)

    @restapi_endpoint(
        method="GET",
        path="/api/scan/jobs/{id}/result",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
        response_type="json",
    )
    def get_scan_job_result(self, job_id: str) -> Response:
        """Gets the result of a scan job

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/scan/jobs/{job_id}/result"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/scan/jobs/{id}/stop",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
        naming_ok=True,
    )
    def stop_scan_job(self, job_id: str) -> Response:
        """Stops a running scan job, which still finishes with the items scanned so far

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/scan/jobs/{job_id}/stop"
        return self.polarion_connection.api_request_post(url)

    @restapi_endpoint(
        method="POST",
        path="/api/repair/jobs",
        body_param="repair_params",
        required_params=["__request_body__"],
    )
    def start_repair_job(self, repair_params: JsonDict) -> Response:
        """Starts an asynchronous repair of XML issues, all of them in one transaction

        Returns:
            Response: Response object from the API call, the job URI in its Location header
        """
        url: str = f"{self.rest_api_url}/repair/jobs"
        return self.polarion_connection.api_request_post(url, data=repair_params)

    @restapi_endpoint(
        method="GET",
        path="/api/repair/jobs/{id}",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
    )
    def get_repair_job_status(self, job_id: str) -> Response:
        """Gets the status of a repair job, without following the redirect to its result

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/repair/jobs/{job_id}"
        return self.polarion_connection.api_request_get(url, allow_redirects=False)

    @restapi_endpoint(
        method="GET",
        path="/api/repair/jobs/{id}/result",
        path_params={
            "id": "job_id",
        },
        required_params=["id"],
        response_type="json",
    )
    def get_repair_job_result(self, job_id: str) -> Response:
        """Gets the result of a repair job

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/repair/jobs/{job_id}/result"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/entities",
        query_params={
            "projectId": "project_id",
            "entityType": "entity_type",
            "entitySubtype": "entity_subtype",
        },
        required_params=["projectId", "entityType"],
        response_type="json",
    )
    def list_entities(self, project_id: str, entity_type: str, entity_subtype: str | None = None) -> Response:
        """List entities of a project by type, optionally narrowed by subtype.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/entities"
        params: dict[str, str] = {
            "projectId": project_id,
            "entityType": entity_type,
        }
        if entity_subtype:
            params["entitySubtype"] = entity_subtype
        return self.polarion_connection.api_request_get(url, params=params)
