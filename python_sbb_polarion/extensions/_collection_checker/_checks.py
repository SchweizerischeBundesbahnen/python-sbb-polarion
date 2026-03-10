"""Collection Checker checks mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.extensions._collection_checker._types import ReportFormat


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, JsonList


class ChecksMixin(BaseMixin):
    """Check operations."""

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/checks",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            "daysInterval": "days_interval",
            "page": "page",
            "count": "count",
        },
        required_params=["projectId"],
    )
    def get_checks(self, project_id: str, days_interval: int = 1, page: int = 1, count: int = 20) -> Response:
        """Get checks list

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/checks"
        params: dict[str, str] = {
            "daysInterval": str(days_interval),
            "page": str(page),
            "count": str(count),
        }
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/checks/{checkId}/cancel",
        path_params={
            "projectId": "project_id",
            "checkId": "check_id",
        },
        required_params=["projectId", "checkId"],
    )
    def cancel_check(self, project_id: str, check_id: str) -> Response:
        """Cancel check

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/checks/{check_id}/cancel"
        return self.polarion_connection.api_request_post(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/checks/{checkId}",
        path_params={
            "projectId": "project_id",
            "checkId": "check_id",
        },
        required_params=["projectId", "checkId"],
    )
    def get_check(self, project_id: str, check_id: str) -> Response:
        """Get check for provided id

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/checks/{check_id}"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="POST",
        path="/api/projects/{projectId}/collections/{collectionId}/checks",
        path_params={
            "projectId": "project_id",
            "collectionId": "collection_id",
        },
        body_param="kwargs",
        required_params=["projectId", "collectionId"],
    )
    def start_check(
        self,
        project_id: str,
        collection_id: str,
        ignore_link_roles: list[str] | None = None,
        ignore_copying_link_roles: list[str] | None = None,
        ignore_multiple_revisions_errors: bool = False,
        ignore_link_out_of_collection_errors: bool = False,
    ) -> Response:
        """Start new check

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/collections/{collection_id}/checks"

        # Convert list[str] to JsonList for type compatibility
        ignore_link_roles_json: JsonList | None = None
        if ignore_link_roles:
            ignore_link_roles_json = list(ignore_link_roles)

        ignore_copying_link_roles_json: JsonList | None = None
        if ignore_copying_link_roles:
            ignore_copying_link_roles_json = list(ignore_copying_link_roles)

        data: JsonDict = {
            "ignoreLinkRoles": ignore_link_roles_json,
            "ignoreCopyingLinkRoles": ignore_copying_link_roles_json,
            "ignoreWorkItemIsContainedInMultipleRevisionsErrors": ignore_multiple_revisions_errors,
            "ignoreLinkOutOfCollectionWithSpecificRevisionErrors": ignore_link_out_of_collection_errors,
        }
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/linkroles",
        path_params={
            "projectId": "project_id",
        },
        required_params=["projectId"],
    )
    def get_linkroles(self, project_id: str) -> Response:
        """Get project link roles

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/linkroles"
        return self.polarion_connection.api_request_get(url)

    @restapi_endpoint(
        method="GET",
        path="/api/projects/{projectId}/checks/{checkId}/report",
        path_params={
            "projectId": "project_id",
            "checkId": "check_id",
        },
        query_params={
            "format": "report_format",
        },
        required_params=["projectId", "checkId"],
    )
    def get_check_report(self, project_id: str, check_id: str, report_format: ReportFormat = ReportFormat.JSON) -> Response:
        """Get check report in specified format

        Args:
            project_id: Project ID
            check_id: Check ID
            report_format: Report format - ReportFormat.JSON or ReportFormat.TXT

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/projects/{project_id}/checks/{check_id}/report"
        params: dict[str, str] = {
            "format": report_format,
        }
        return self.polarion_connection.api_request_get(url, params=params or None)

    def get_check_json_report(self, project_id: str, check_id: str) -> Response:
        """Get check report in JSON format (wrapper for get_check_report with format=JSON)

        Returns:
            Response: Response object from the API call
        """
        return self.get_check_report(project_id, check_id, report_format=ReportFormat.JSON)

    def get_check_text_log(self, project_id: str, check_id: str) -> Response:
        """Get check log as text (wrapper for get_check_report with format=TXT)

        Returns:
            Response: Response object from the API call
        """
        return self.get_check_report(project_id, check_id, report_format=ReportFormat.TXT)
