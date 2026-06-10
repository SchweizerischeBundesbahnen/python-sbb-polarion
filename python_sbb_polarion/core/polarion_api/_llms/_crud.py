"""LLMs (Large Language Models) operations mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.core.polarion_api._base import PAGE_NUMBER, PAGE_SIZE, BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import JsonDict


class LlmsMixin(BaseMixin):
    """LLMs operations.

    Provides methods for listing Large Language Models and generating chat completions.
    New in Polarion 2606.
    """

    @restapi_endpoint(
        method="GET",
        path="/llms",
        query_params={
            PAGE_SIZE: "page_size",
            PAGE_NUMBER: "page_number",
        },
        response_type="json",
    )
    def get_llms(
        self,
        page_size: int | None = None,
        page_number: int | None = None,
    ) -> Response:
        """Get list of available Large Language Models (LLMs).

        Args:
            page_size: Number of items per page
            page_number: Page number (1-based)

        Returns:
            Response: List of LLMs from API
        """
        url: str = f"{self.base_url}/llms"
        params: dict[str, str] = {}
        if page_size is not None:
            params[PAGE_SIZE] = str(page_size)
        if page_number is not None:
            params[PAGE_NUMBER] = str(page_number)
        return self.polarion_connection.api_request_get(url, params=params or None)

    @restapi_endpoint(
        method="POST",
        path="/llms/actions/generateCompletion",
        body_param="data",
        required_params=["__request_body__"],
        response_type="json",
    )
    def generate_completion(
        self,
        data: JsonDict,
    ) -> Response:
        """Generate a chat completion using a Large Language Model (LLM).

        Args:
            data: Completion request data in JSON:API format

        Returns:
            Response: Generated completion from API
        """
        url: str = f"{self.base_url}/llms/actions/generateCompletion"
        return self.polarion_connection.api_request_post(url, data=data)
