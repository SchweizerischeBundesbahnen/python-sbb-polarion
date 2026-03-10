"""
common implementation for HTTP connections

"""

import base64
import json
import logging
from collections.abc import Mapping
from typing import TypedDict, Unpack

from requests import Response, Session, exceptions

from python_sbb_polarion.types import AuthScheme, FileUpload, Header, JsonValue, MediaType


logger = logging.getLogger(__name__)


class HttpConnectionConfig(TypedDict, total=False):
    """Configuration parameters for HttpConnection."""

    url: str
    username: str
    password: str
    token: str
    api_key: str
    content_type: str
    accept: str
    trust_env: bool
    print_error: bool


class HttpRequestParams(TypedDict, total=False):
    """Parameters for HTTP requests."""

    data: Mapping[str, JsonValue] | dict[str, JsonValue] | list[JsonValue] | str | bool  # Can be JSON dict, list, str for raw data, or bool
    payload: str | bytes
    params: Mapping[str, str | JsonValue] | dict[str, JsonValue] | dict[str, str] | None  # Query parameters can be str or other JSON values
    headers: dict[str, str] | dict[Header, str] | dict[Header, MediaType]
    files: FileUpload | None  # File uploads in requests library format
    print_error: bool
    allow_redirects: bool


class HttpConnection:
    """HTTP connection"""

    def __init__(self, **kwargs: Unpack[HttpConnectionConfig]) -> None:
        self.host: str = kwargs.get("url", "")
        username: str = kwargs.get("username", "")
        password: str = kwargs.get("password", "")
        token: str = kwargs.get("token", "")
        api_key: str = kwargs.get("api_key", "")
        default_content_type: str = kwargs.get("content_type", MediaType.JSON)
        default_accept: str = kwargs.get("accept", MediaType.JSON)
        trust_env: bool = kwargs.get("trust_env", False)  # if False .netrc support will be disabled
        self.__print_error: bool = kwargs.get("print_error", True)

        if token:
            self.__authorization_headers = {Header.AUTHORIZATION: f"{AuthScheme.BEARER} {token}"}
        elif api_key:
            self.__authorization_headers = {Header.X_API_KEY: api_key}
        else:
            logger.warning("this type of authorization is not secure --> please consider to generate an access token instead")
            credentials: bytes = f"{username}:{password}".encode()
            auth: str = base64.b64encode(credentials).decode("utf-8")
            self.__authorization_headers = {Header.AUTHORIZATION: f"{AuthScheme.BASIC} {auth}"}

        self.__default_connection_headers = {
            Header.CONTENT_TYPE: default_content_type,
            Header.ACCEPT: default_accept,
        }
        self.__default_connection_headers.update(self.__authorization_headers)

        self.request_session = Session()
        self.request_session.trust_env = trust_env

        self.__requests_error_occurred = False

    def get_requests_error_occurred(self) -> bool:
        """In case a request error returns True and reset the state

        Returns:
            bool: True if a request error occurred, False otherwise
        """
        if self.__requests_error_occurred:
            self.__reset_requests_error_occurred()
            return True
        return False

    def __set_requests_error_occurred(self) -> None:
        self.__requests_error_occurred = True

    def __reset_requests_error_occurred(self) -> None:
        self.__requests_error_occurred = False

    def __api_request(self, request_type: str, api_url: str, **kwargs: Unpack[HttpRequestParams]) -> Response:
        """Request handler for all request types

        :param request_type: GET, POST, PUT, PATCH, DELETE, etc
        :param api_url:

        Returns:
            Response: Response object from the HTTP request (always returned, even for 4xx/5xx status codes)

        Raises:
            exceptions.RequestException: Network/connection errors (timeout, SSL, connection refused, etc.)
        """
        data: Mapping[str, JsonValue] | dict[str, JsonValue] | list[JsonValue] | str | bool | None = kwargs.get("data")
        payload: str | bytes | None = kwargs.get("payload")
        params: Mapping[str, str | JsonValue] | dict[str, JsonValue] | dict[str, str] | None = kwargs.get("params")
        headers: dict[str, str] | dict[Header, str] | dict[Header, MediaType] | None = kwargs.get("headers")
        files: FileUpload | None = kwargs.get("files")
        print_error: bool = kwargs.get("print_error", self.__print_error)
        allow_redirects: bool = kwargs.get("allow_redirects", True)

        url: str = f"{self.host}{api_url}"
        effective_headers: Mapping[str, str] = self.__create_request_headers(headers, files)

        # Convert Mapping to dict for requests library compatibility
        headers_dict: dict[str, str] = dict(effective_headers)

        # Convert params - requests expects simple str/int/float values, convert JsonValue to str
        params_dict: dict[str, str] | None = None
        if params:
            params_dict = {}
            for key, value in params.items():
                # Convert complex types to strings
                if isinstance(value, (dict, list)):
                    params_dict[key] = json.dumps(value)
                elif value is None:
                    params_dict[key] = ""
                else:
                    params_dict[key] = str(value)

        # Handle data parameter - convert Mapping to dict for JSON serialization
        json_data: dict[str, JsonValue] | list[JsonValue] | str | bool | None = None
        if isinstance(data, Mapping):
            json_data = dict(data)
        elif isinstance(data, (list, str, bool)):
            json_data = data

        try:
            response: Response = self.request_session.request(
                request_type,
                url=url,
                headers=headers_dict,
                params=params_dict,
                json=json_data,
                data=payload,
                files=files,
                verify=True,
                allow_redirects=allow_redirects,
            )
            # Log non-2xx responses for debugging, but still return them
            if response.status_code // 100 != 2:
                self.__set_requests_error_occurred()
                if print_error:
                    logger.warning("Non-2xx response received: %s %s", response.status_code, response.reason)
                    logger.debug("Response header: %s", response.headers)
                    logger.debug("Response content: %s", response.content)
        except exceptions.RequestException:
            # Log and re-raise network/connection errors (timeout, SSL, connection refused, etc.)
            logger.exception("Request exception occurred")
            raise

        return response

    def set_print_error(self, print_error: bool) -> None:
        """Print error or not"""
        self.__print_error = print_error

    def __create_request_headers(self, headers: dict[str, str] | dict[Header, str] | dict[Header, MediaType] | None = None, files: FileUpload | None = None) -> dict[str, str]:
        if headers:
            # Convert Header enum keys to strings for compatibility
            effective_headers: dict[str, str] = {str(k): str(v) for k, v in headers.items()}
            effective_headers.update({str(k): str(v) for k, v in self.__authorization_headers.items()})
        else:
            effective_headers = {str(k): str(v) for k, v in self.__default_connection_headers.items()}
            if files:
                effective_headers.pop(Header.CONTENT_TYPE, "")  # Content-Type should be omitted if multipart/form-data is used
        return effective_headers

    def api_request_get(self, api_url: str, **kwargs: Unpack[HttpRequestParams]) -> Response:
        """Perform GET request.

        Returns:
            Response: Response object from the GET request
        """
        return self.__api_request("GET", api_url, **kwargs)

    def api_request_patch(self, api_url: str, **kwargs: Unpack[HttpRequestParams]) -> Response:
        """Perform PATCH request.

        Returns:
            Response: Response object from the PATCH request
        """
        return self.__api_request("PATCH", api_url, **kwargs)

    def api_request_put(self, api_url: str, **kwargs: Unpack[HttpRequestParams]) -> Response:
        """Perform PUT request.

        Returns:
            Response: Response object from the PUT request
        """
        return self.__api_request("PUT", api_url, **kwargs)

    def api_request_post(self, api_url: str, **kwargs: Unpack[HttpRequestParams]) -> Response:
        """Perform POST request.

        Returns:
            Response: Response object from the POST request
        """
        return self.__api_request("POST", api_url, **kwargs)

    def api_request_delete(self, api_url: str, **kwargs: Unpack[HttpRequestParams]) -> Response:
        """Perform DELETE request.

        Returns:
            Response: Response object from the DELETE request
        """
        return self.__api_request("DELETE", api_url, **kwargs)
