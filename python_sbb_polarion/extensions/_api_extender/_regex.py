"""API Extender regex mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict


class RegexMixin(BaseMixin):
    """Regex tool operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/regex-tool/find-matches",
        body_param="form_data",
        required_params=[],
        response_type="json",
    )
    def find_matches(self, text: str, regex: str) -> Response:
        """Find regex matches in the string

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/regex-tool/find-matches"
        files: FilesDict = {
            "text": text,
            "regex": regex,
        }
        return self.polarion_connection.api_request_post(url, files=files)
