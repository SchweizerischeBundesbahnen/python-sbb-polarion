"""Generic Polarion Test Case"""

import logging
import os
import unittest
from abc import abstractmethod

from python_polarion_utils.api.extension_api_factory import ExtensionApiFactory
from python_polarion_utils.api.generic import PolarionGenericExtensionApi, PolarionRestApiConnection
from python_polarion_utils.api.polarion_api import PolarionApi
from python_polarion_utils.common.util_argparse import get_script_arguments
from python_polarion_utils.common.util_http import HttpConnection


class GenericTestCase(unittest.TestCase):
    """Generic Polarion Test Case with common code for system tests"""

    extension_api: PolarionGenericExtensionApi = None
    _polarion_api: PolarionApi = None
    logger = logging.getLogger("GenericTestCase")

    @classmethod
    def setUpClass(cls):
        GenericTestCase.extension_api = GenericTestCase.create_extension_api("generic")

    @classmethod
    def create_extension_api(cls, extension_name):
        """Create extension API using provided extension name. If omitted try to detect it based on repo name."""
        app_url, app_token = cls.__get_parameters()
        polarion_connection = PolarionRestApiConnection(url=app_url, token=app_token)
        cls._polarion_api = PolarionApi(polarion_connection)
        return ExtensionApiFactory.get_extension_api_by_name(extension_name=extension_name, polarion_connection=polarion_connection)

    @classmethod
    def __get_parameters(cls):
        args = get_script_arguments(None)
        app_url = cls.get_parameter("APP_URL", args.app_url)
        app_token = cls.get_parameter("APP_TOKEN", args.app_token)
        cls.__check_mandatory_parameters(app_url, app_token)
        return app_url, app_token

    @staticmethod
    def get_parameter(env_param_name, script_argument_value):
        param = os.environ.get(env_param_name)
        if not param:
            param = script_argument_value
        return param

    @classmethod
    def __check_mandatory_parameters(cls, app_url, app_token):
        if app_url is None:
            raise ValueError("'app_url' is not provided: use --app_url or APP_URL env variable")
        if app_token is None:
            raise ValueError("'app_token' is not provided: use --app_token or APP_TOKEN env variable")

    def run_test_get_version(self):
        """Method code for testing GET /version endpoint."""
        # Act
        response = self.extension_api.get_version()

        # Assert
        self.assertEqual(response.status_code, 200)

        json = response.json()

        bundle_vendor = json["bundleVendor"]
        bundle_version = json["bundleVersion"]
        bundle_build_timestamp = json["bundleBuildTimestamp"]
        bundle_name = json["bundleName"]
        automatic_module_name = json["automaticModuleName"]
        bundle_build_timestamp_digits_only = json["bundleBuildTimestampDigitsOnly"]

        self.logger.info(f"Bundle name: '{bundle_name}'")
        self.logger.info(f"Automatic module name: '{automatic_module_name}'")
        self.logger.info(f"Bundle version: '{bundle_version}'")
        self.logger.info(f"Bundle Build timestamp: '{bundle_build_timestamp}'")

        self.assertEqual(bundle_vendor, "SBB AG")
        self.assertEqual(automatic_module_name, f"ch.sbb.polarion.extension.{self.extension_api.extension_name.replace('-', '_')}")
        self.assertRegex(bundle_version, r"^\d+\.\d+\.\d+$")
        self.assertRegex(bundle_build_timestamp, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
        self.assertRegex(bundle_build_timestamp_digits_only, r"^\d{4}\d{2}\d{2}\d{2}\d{2}$")

        return json

    def run_test_get_version_with_invalid_token(self):
        """Method code for testing GET /version endpoint with invalid token."""
        # Act
        extension_url = f"/polarion/{self.extension_api.extension_name}/rest/api/version"
        http_connection = HttpConnection(url=self.extension_api.polarion_connection.host, token="invalid token")  # noqa: S106
        response = http_connection.api_request_get(extension_url, print_error=False)

        # Assert
        self.assertEqual(response.status_code, 401)

    def run_test_get_context(self):
        """Method code for testing GET /context endpoint."""
        # Act
        response = self.extension_api.get_context()

        # Assert
        self.assertEqual(response.status_code, 200)

        json = response.json()

        self.assertEqual(json["baseUrl"], f"/polarion/{self.extension_api.extension_name}")
        self.assertEqual(json["extensionContext"], self.extension_api.extension_name)
        self.assertEqual(json["restUrl"], f"/polarion/{self.extension_api.extension_name}/rest")
        self.assertEqual(json["swaggerUiUrl"], f"/polarion/{self.extension_api.extension_name}/rest/swagger")

        return json

    @abstractmethod
    def api(self):
        """Casting to extension API"""
        raise ValueError("Unknown extension API")
