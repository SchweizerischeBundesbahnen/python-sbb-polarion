"""Fake export webhook management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlencode

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response

    from python_sbb_polarion.types import FilesDict


WEBHOOK_RESPOND_PATH = "/polarion/fake-services/rest/api/webhook/respond"


class WebhookMixin(BaseMixin):
    """Fake export webhook operations.

    The PDF and the DOCX exporter send a webhook the same request, so one fake answers both. The answer is chosen
    by the query of the URL stored in the webhooks configuration, which :meth:`webhook_respond_path` builds.
    """

    @staticmethod
    def webhook_respond_path(
        key: str,
        status: int | None = None,
        body: str | None = None,
        body_size: int | None = None,
        delay_millis: int | None = None,
        append: str | None = None,
    ) -> str:
        """Build the path of the fake webhook, with the query which decides how it answers.

        The path is absolute within the server and carries no host: Polarion calls the webhook itself, so the
        caller prefixes the address that Polarion reaches its own server under, which is not necessarily the one
        the tests use.

        Args:
            key: the bucket the calls are recorded in, so parallel cases do not read each other's calls
            status: the status to answer with, 200 where it is not given
            body: the body to answer a refusal with
            body_size: the length of a generated body, used where no body is given
            delay_millis: how long the webhook holds its answer back
            append: markup inserted before </body> of the HTML the webhook answers with

        Returns:
            str: the path and query to store as the URL of a webhook
        """
        query: dict[str, str] = {"key": key}
        if status is not None:
            query["status"] = str(int(status))
        if body is not None:
            query["body"] = body
        if body_size is not None:
            query["bodySize"] = str(int(body_size))
        if delay_millis is not None:
            query["delayMillis"] = str(int(delay_millis))
        if append is not None:
            query["append"] = append
        return f"{WEBHOOK_RESPOND_PATH}?{urlencode(query)}"

    @restapi_endpoint(
        method="POST",
        path="/api/webhook/respond",
        query_params={
            "key": "key",
            "status": "status",
            "body": "body",
            "bodySize": "body_size",
            "delayMillis": "delay_millis",
            "append": "append",
        },
        multipart_fields={
            "exportParams": "export_params",
            "html": "html",
        },
        required_params=[],
        response_type="text",
        # The endpoint is a webhook, not a resource: a call creates nothing
        naming_ok=True,
    )
    def call_webhook(
        self,
        html: str,
        export_params: str = "{}",
        key: str | None = None,
        status: int | None = None,
        body: str | None = None,
        body_size: int | None = None,
        delay_millis: int | None = None,
        append: str | None = None,
    ) -> Response:
        """Call the fake webhook the way an exporter does.

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/webhook/respond"
        params: dict[str, str] = {}
        if key is not None:
            params["key"] = key
        if status is not None:
            params["status"] = str(int(status))
        if body is not None:
            params["body"] = body
        if body_size is not None:
            params["bodySize"] = str(int(body_size))
        if delay_millis is not None:
            params["delayMillis"] = str(int(delay_millis))
        if append is not None:
            params["append"] = append
        files: FilesDict = {
            "exportParams": ("exportParams.json", export_params),
            "html": ("html.html", html),
        }
        return self.polarion_connection.api_request_post(url, params=params or None, files=files)

    @restapi_endpoint(
        method="GET",
        path="/api/webhook/manage/calls",
        query_params={
            "key": "key",
        },
        required_params=[],
        response_type="json",
    )
    def get_webhook_calls(self, key: str | None = None) -> Response:
        """Get the calls the fake webhook recorded

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] | None = {"key": key} if key else None
        url: str = f"{self.rest_api_url}/webhook/manage/calls"
        return self.polarion_connection.api_request_get(url, params=params)

    @restapi_endpoint(
        method="DELETE",
        path="/api/webhook/manage/calls",
        query_params={
            "key": "key",
        },
        required_params=[],
    )
    def delete_webhook_calls(self, key: str | None = None) -> Response:
        """Delete the calls the fake webhook recorded

        Returns:
            Response: Response object from the API call
        """
        params: dict[str, str] | None = {"key": key} if key else None
        url: str = f"{self.rest_api_url}/webhook/manage/calls"
        return self.polarion_connection.api_request_delete(url, params=params)
