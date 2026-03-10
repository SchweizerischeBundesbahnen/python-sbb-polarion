"""Cucumber export mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin
from python_sbb_polarion.types import Header, MediaType


if TYPE_CHECKING:
    from requests import Response


class ExportMixin(BaseMixin):
    """Export operations."""

    if TYPE_CHECKING:
        extension_name: str

    @restapi_endpoint(
        method="GET",
        path="/raven/1.0/export/test",
        query_params={
            "keys": "keys",
            "filter": "filter_query",
            "fz": "fz",
        },
        response_type="binary",
    )
    def export_test(self, keys: str | None = None, filter_query: str | None = None, fz: bool = True) -> Response:
        """
        Export features
        keys -- list of workitem ids -- example "elibrary/EL-4;elibrary/EL-5"
        filter_query -- polarion query to find workitems
        fz -- if true -- zip files with all found features, if false -- first found feature

        Returns:
            Response: Response object from the API call
        """
        url: str = f"/polarion/{self.extension_name}/rest/raven/1.0/export/test"
        params: dict[str, str] = {
            "fz": str(fz).lower(),
        }
        if keys:
            params["keys"] = keys
        elif filter_query:
            params["keys"] = filter_query

        headers: dict[str, str] = {
            Header.ACCEPT: MediaType.OCTET_STREAM,
        }
        return self.polarion_connection.api_request_get(url, headers=headers, params=params or None)
