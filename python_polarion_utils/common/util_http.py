"""
common implementation for HTTP connections

"""

import base64

import requests


class HttpConnection:
    """HTTP connection"""

    def __init__(self, **kwargs):
        self.host = kwargs.get("url", "")
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
            print("WARNING: this type of authorization is not secure --> please consider to generate an access token instead")
            __auth = base64.b64encode(f"{__username}:{__password}".encode()).decode("utf-8")
            self.__authorization_headers = {"Authorization": f"Basic {__auth}"}

        self.__default_connection_headers = {"Content-Type": __default_content_type, "Accept": __default_accept}
        self.__default_connection_headers.update(self.__authorization_headers)

        self.request_session = requests.Session()
        self.request_session.trust_env = __trust_env

        self.__requests_error_occurred = False

    def get_requests_error_occurred(self):
        """in case a request error returns True and reset the state

        :return:
        """
        if self.__requests_error_occurred:
            self.__reset_requests_error_occurred()
            return True
        return False

    def __set_requests_error_occurred(self):
        self.__requests_error_occurred = True

    def __reset_requests_error_occurred(self):
        self.__requests_error_occurred = False

    def __api_request(self, request_type, api_url, **kwargs):
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
            if response.status_code // 100 != 2:  # Consider any status other than 2xx as an error
                self.__set_requests_error_occurred()
                if print_error:
                    print(f"Error: Unexpected response: '{response}'")
                    print(f"Error: Response header: '{response.headers}'")
                    print(f"Error: Response content: '{response.content}'")
                    print(f"Error: Request header: '{response.request.headers}'")
        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            print(f"Error: {e}")

        return response

    def set_print_error(self, print_error):
        """print error or not"""
        self.__print_error = print_error

    def __create_request_headers(self, headers=None, files=None):
        if headers:
            headers.update(self.__authorization_headers)
            effective_headers = headers
        else:
            effective_headers = self.__default_connection_headers
            if files:
                effective_headers.pop("Content-Type", "")  # Content-Type should be omitted if multipart/form-data is used
        return effective_headers

    def api_request_get(self, api_url, **kwargs):
        """GET request"""
        return self.__api_request("GET", api_url, **kwargs)

    def api_request_patch(self, api_url, **kwargs):
        """PATCH request"""
        return self.__api_request("PATCH", api_url, **kwargs)

    def api_request_put(self, api_url, **kwargs):
        """PUT request"""
        return self.__api_request("PUT", api_url, **kwargs)

    def api_request_post(self, api_url, **kwargs):
        """POST request"""
        return self.__api_request("POST", api_url, **kwargs)

    def api_request_delete(self, api_url, **kwargs):
        """DELETE request"""
        return self.__api_request("DELETE", api_url, **kwargs)
