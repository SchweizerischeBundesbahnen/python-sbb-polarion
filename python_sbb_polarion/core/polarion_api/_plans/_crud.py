"""Plans CRUD operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict, SparseFields


class PlansMixin(BaseMixin):
    """Plans operations.

    Provides methods for managing plans and their relationships.
    """

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/plans",
        path_params={
            "projectId": "project_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "query": "query",
            "sort": "sort",
            "revision": "revision",
            "templates": "templates",
        },
        required_params=["projectId"],
        response_type="json",
    )
    def get_plans(
        self,
        project_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        query: str | None = None,
        sort: str | None = None,
        revision: str | None = None,
        templates: str | None = None,
    ) -> Response:
        """Get list of plans.

        Args:
            project_id: Project identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            query: Lucene query string
            sort: Sort specification
            revision: Specific revision
            templates: Filter by templates

        Returns:
            Response: List of plans from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if query:
            params["query"] = query
        if sort:
            params["sort"] = sort
        if revision:
            params["revision"] = revision
        if templates:
            params["templates"] = templates
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/plans/{planId}",
        path_params={
            "projectId": "project_id",
            "planId": "plan_id",
        },
        query_params={
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "planId"],
        response_type="json",
    )
    def get_plan(
        self,
        project_id: str,
        plan_id: str,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get a specific plan.

        Args:
            project_id: Project identifier
            plan_id: Plan identifier
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Plan data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans/{plan_id}"
        params: dict[str, str] = {}
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/plans",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def create_plans(self, project_id: str, data: JsonDict) -> Response:
        """Create plans.

        Args:
            project_id: Project identifier
            data: Plans data in JSON:API format

        Returns:
            Response: Created plans data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/plans/{planId}",
        path_params={
            "projectId": "project_id",
            "planId": "plan_id",
        },
        body_param="data",
        required_params=["projectId", "planId"],
        response_type="json",
    )
    def update_plan(
        self,
        project_id: str,
        plan_id: str,
        data: JsonDict,
    ) -> Response:
        """Update a plan.

        Args:
            project_id: Project identifier
            plan_id: Plan identifier
            data: Plan data in JSON:API format

        Returns:
            Response: Updated plan data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans/{plan_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/plans",
        path_params={
            "projectId": "project_id",
        },
        body_param="data",
        required_params=["projectId"],
        response_type="json",
    )
    def delete_plans(self, project_id: str, data: JsonDict) -> Response:
        """Delete plans.

        Args:
            project_id: Project identifier
            data: Plans to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans"
        return self.polarion_connection.api_request_delete(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/plans/{planId}",
        path_params={
            "projectId": "project_id",
            "planId": "plan_id",
        },
        required_params=["projectId", "planId"],
        response_type="json",
    )
    def delete_plan(self, project_id: str, plan_id: str) -> Response:
        """Delete a specific plan.

        Args:
            project_id: Project identifier
            plan_id: Plan identifier

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans/{plan_id}"
        return self.polarion_connection.api_request_delete(url)

    # Plan Relationships

    @restapi_endpoint(
        method="GET",
        path="/projects/{projectId}/plans/{planId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "planId": "plan_id",
            "relationshipId": "relationship_id",
        },
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
            "fields": "fields",
            "include": "include",
            "revision": "revision",
        },
        required_params=["projectId", "planId", "relationshipId"],
        response_type="json",
    )
    def get_plan_relationships(
        self,
        project_id: str,
        plan_id: str,
        relationship_id: str,
        page_size: int | None = None,
        page_number: int | None = None,
        fields: SparseFields | None = None,
        include: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Get plan relationships.

        Args:
            project_id: Project identifier
            plan_id: Plan identifier
            relationship_id: Relationship identifier
            page_size: Number of items per page
            page_number: Page number (0-based)
            fields: JSON:API sparse fieldsets dict (e.g., {"workitems": "@all"})
            include: Include related resources
            revision: Specific revision

        Returns:
            Response: Relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        self._add_sparse_fields(params, fields)
        if include:
            params["include"] = include
        if revision:
            params["revision"] = revision
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/projects/{projectId}/plans/{planId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "planId": "plan_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "planId", "relationshipId"],
        response_type="json",
    )
    def create_plan_relationships(
        self,
        project_id: str,
        plan_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Create plan relationships.

        Args:
            project_id: Project identifier
            plan_id: Plan identifier
            relationship_id: Relationship identifier
            data: Relationships data in JSON:API format

        Returns:
            Response: Created relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_post(url, data=data)

    @restapi_endpoint(
        method="PATCH",
        path="/projects/{projectId}/plans/{planId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "planId": "plan_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "planId", "relationshipId"],
        response_type="json",
    )
    def update_plan_relationships(
        self,
        project_id: str,
        plan_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Update plan relationships.

        Args:
            project_id: Project identifier
            plan_id: Plan identifier
            relationship_id: Relationship identifier
            data: Relationships data in JSON:API format

        Returns:
            Response: Updated relationships data from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_patch(url, data=data)

    @restapi_endpoint(
        method="DELETE",
        path="/projects/{projectId}/plans/{planId}/relationships/{relationshipId}",
        path_params={
            "projectId": "project_id",
            "planId": "plan_id",
            "relationshipId": "relationship_id",
        },
        body_param="data",
        required_params=["projectId", "planId", "relationshipId"],
        response_type="json",
    )
    def delete_plan_relationships(
        self,
        project_id: str,
        plan_id: str,
        relationship_id: str,
        data: JsonDict,
    ) -> Response:
        """Delete plan relationships.

        Args:
            project_id: Project identifier
            plan_id: Plan identifier
            relationship_id: Relationship identifier
            data: Relationships to delete in JSON:API format

        Returns:
            Response: Response from API
        """
        url: str = f"{self.base_url}/projects/{project_id}/plans/{plan_id}/relationships/{relationship_id}"
        return self.polarion_connection.api_request_delete(url, data=data)
