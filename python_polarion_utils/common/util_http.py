"""
common implementation for HTTP connections

"""

import base64
import logging
import re
from enum import Enum
from typing import Any, Literal, NotRequired, TypeAlias, TypedDict, Unpack

import requests  # type: ignore
from requests import Response  # type: ignore


class StatusCodeClass(Enum):
    SUCCESSFUL = re.compile(r"^2\d\d$")
    REDIRECT = re.compile(r"^3\d\d$")
    CLIENT_ERROR = re.compile(r"^4\d\d$")
    SERVER_ERROR = re.compile(r"^5\d\d$")


class StatusCode(Enum):
    OK = 200
    INTERNAL_SERVER_ERROR = 503


class HttpConnectionParams(TypedDict):
    url: str
    username: NotRequired[str]
    password: NotRequired[str]
    token: NotRequired[str]
    api_key: NotRequired[str]
    content_type: NotRequired[str]
    accept: NotRequired[str]
    trust_env: NotRequired[bool]
    print_error: NotRequired[bool]


RequestType: TypeAlias = Literal["GET", "POST", "PATCH", "PUT", "DELETE"]


class OptionalApiRequestParams(TypedDict):
    data: NotRequired[Any]
    files: NotRequired[Any]
    params: NotRequired[dict[str, str]]
    headers: NotRequired[dict[str, str]]
    print_error: NotRequired[bool]
    allow_redirects: NotRequired[bool]


class HttpConnection:
    """HTTP connection"""

    def __init__(self, **kwargs: Unpack[HttpConnectionParams]) -> None:
        self.host = kwargs.get("url", "")
        self.logger = logging.getLogger("python-polarion-utils-http")
        __username = kwargs.get("username", "")
        __password = kwargs.get("password", "")
        __token = kwargs.get("token", "")
        __api_key = kwargs.get("api_key", "")
        __default_content_type = kwargs.get("content_type", "application/json")
        __default_accept = kwargs.get("accept", "application/json")
        __trust_env = kwargs.get("trust_env", False)  # if False .netrc support will be disabled
        self.__print_error = kwargs.get("print_error", True)

        if __token:
            self.__authorization_headers = {"Authorization": f"Bearer {__token}"}
        elif __api_key:
            self.__authorization_headers = {"X-API-Key": __api_key}
        else:
            self.logger.warning("This type of authorization is not secure --> please consider to generate an access token instead")
            __auth = base64.b64encode(f"{__username}:{__password}".encode()).decode("utf-8")
            self.__authorization_headers = {"Authorization": f"Basic {__auth}"}

        self.__default_connection_headers = {"Content-Type": __default_content_type, "Accept": __default_accept}
        self.__default_connection_headers.update(self.__authorization_headers)

        self.request_session = requests.Session()
        self.request_session.trust_env = __trust_env

        self.__requests_error_occurred = False

    def get_requests_error_occurred(self) -> bool:
        """in case a request error returns True and reset the state

        :return:
        """
        if self.__requests_error_occurred:
            self.__reset_requests_error_occurred()
            return True
        return False

    def __set_requests_error_occurred(self) -> None:
        self.__requests_error_occurred = True

    def __reset_requests_error_occurred(self) -> None:
        self.__requests_error_occurred = False

    def __api_request(self, request_type: RequestType, api_url: str, **kwargs: Unpack[OptionalApiRequestParams]) -> Response | None:
        """request handler for all request types

        :param request_type: GET, POST, PUT, PATCH, DELETE, etc
        :param api_url:
        :return: response
        """
        data = kwargs.get("data")
        params = kwargs.get("params")
        headers = kwargs.get("headers")
        files = kwargs.get("files")
        print_error = kwargs.get("print_error", self.__print_error)
        allow_redirects = kwargs.get("allow_redirects", True)

        response = None

        url = f"{self.host}{api_url}"
        effective_headers = self.__create_request_headers(headers, files)

        try:
            response = self.request_session.request(
                request_type,
                url=url,
                headers=effective_headers,
                params=params,
                json=data,
                files=files,
                verify=True,
                allow_redirects=allow_redirects,
            )
            if StatusCodeClass.SUCCESSFUL.value.match(str(response.status_code)) is not None:  # Consider any status other than 2xx as an error
                self.__set_requests_error_occurred()
                if print_error:
                    self.logger.error(f"Unexpected response: '{response}'")
                    self.logger.error(f"Response header: '{response.headers}'")
                    self.logger.error(f"Response content: '{response.content}'")
                    self.logger.error(f"Request header: '{response.request.headers}'")
        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            self.logger.error(e)

        return response

    def set_print_error(self, print_error: bool) -> None:
        """print error or not"""
        self.__print_error = print_error

    def __create_request_headers(self, headers: dict[str, str] | None = None, files: dict[str, str] | None = None) -> dict[str, str]:
        if headers:
            headers.update(self.__authorization_headers)
            effective_headers = headers
        else:
            effective_headers = self.__default_connection_headers
            if files:
                effective_headers.pop("Content-Type", "")  # Content-Type should be omitted if multipart/form-data is used
        return effective_headers

    def api_request_get(self, api_url: str, **kwargs: Unpack[OptionalApiRequestParams]) -> Response | None:
        """GET request"""
        return self.__api_request("GET", api_url, **kwargs)

    def api_request_patch(self, api_url: str, **kwargs: Unpack[OptionalApiRequestParams]) -> Response | None:
        """PATCH request"""
        return self.__api_request("PATCH", api_url, **kwargs)

    def api_request_put(self, api_url: str, **kwargs: Unpack[OptionalApiRequestParams]) -> Response | None:
        """PUT request"""
        return self.__api_request("PUT", api_url, **kwargs)

    def api_request_post(self, api_url: str, **kwargs: Unpack[OptionalApiRequestParams]) -> Response | None:
        """POST request"""
        return self.__api_request("POST", api_url, **kwargs)

    def api_request_delete(self, api_url: str, **kwargs: Unpack[OptionalApiRequestParams]) -> Response | None:
        """DELETE request"""
        return self.__api_request("DELETE", api_url, **kwargs)
