"""Unit tests for GenericTestCase."""

from __future__ import annotations

import unittest
from http import HTTPStatus
from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi, PolarionRestApiConnection
from python_sbb_polarion.testing.generic_test_case import GenericTestCase


if TYPE_CHECKING:
    from python_sbb_polarion.types import JsonDict


class MockExtensionApi(PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi):
    """Mock extension API with both base and settings functionality for testing."""


class TestGenericTestCase(unittest.TestCase):
    """Test GenericTestCase class."""

    @patch("python_sbb_polarion.testing.generic_test_case.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.generic_test_case.PolarionApiV1")
    @patch("python_sbb_polarion.testing.generic_test_case.get_script_arguments")
    @patch.dict("os.environ", {"APP_URL": "https://example.com", "APP_TOKEN": "test-token"})
    def test_create_extension_api_with_env_vars(self, mock_get_args: Mock, mock_polarion_api_v1: Mock, mock_factory: Mock) -> None:
        """Test create_extension_api with environment variables."""
        # Arrange
        mock_args = SimpleNamespace(app_url=None, app_token=None)
        mock_get_args.return_value = mock_args

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_factory.return_value = mock_api

        # Act
        result: PolarionGenericExtensionApi = GenericTestCase.create_extension_api("pdf-exporter")

        # Assert
        self.assertEqual(result, mock_api)
        mock_factory.assert_called_once()
        call_kwargs: dict[str, object] = mock_factory.call_args[1]
        self.assertEqual(call_kwargs["extension_name"], "pdf-exporter")
        self.assertIsInstance(call_kwargs["polarion_connection"], PolarionRestApiConnection)
        mock_polarion_api_v1.assert_called_once()

    @patch("python_sbb_polarion.testing.generic_test_case.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.generic_test_case.PolarionApiV1")
    @patch("python_sbb_polarion.testing.generic_test_case.get_script_arguments")
    @patch.dict("os.environ", {}, clear=True)
    def test_create_extension_api_with_args(self, mock_get_args: Mock, mock_polarion_api_v1: Mock, mock_factory: Mock) -> None:
        """Test create_extension_api with script arguments."""
        # Arrange
        mock_args = SimpleNamespace(app_url="https://polarion.example.com", app_token="arg-token")
        mock_get_args.return_value = mock_args

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_factory.return_value = mock_api

        # Act
        result: PolarionGenericExtensionApi = GenericTestCase.create_extension_api("admin-utility")

        # Assert
        self.assertEqual(result, mock_api)
        mock_factory.assert_called_once()
        call_kwargs: dict[str, object] = mock_factory.call_args[1]
        self.assertEqual(call_kwargs["extension_name"], "admin-utility")
        mock_polarion_api_v1.assert_called_once()

    @patch.dict("os.environ", {"TEST_PARAM": "env_value"})
    def test_get_parameter_from_env(self) -> None:
        """Test get_parameter returns environment variable when available."""
        # Act
        result: str = GenericTestCase.get_parameter("TEST_PARAM", "arg_value")

        # Assert
        self.assertEqual(result, "env_value")

    @patch.dict("os.environ", {}, clear=True)
    def test_get_parameter_from_arg(self) -> None:
        """Test get_parameter returns argument when env variable not available."""
        # Act
        result: str = GenericTestCase.get_parameter("TEST_PARAM", "arg_value")

        # Assert
        self.assertEqual(result, "arg_value")

    @patch.dict("os.environ", {}, clear=True)
    def test_get_parameter_returns_none(self) -> None:
        """Test get_parameter returns None when both env and arg are None."""
        # Act
        result: str | None = GenericTestCase.get_parameter("TEST_PARAM", None)

        # Assert
        self.assertIsNone(result)

    @patch("python_sbb_polarion.testing.generic_test_case.get_script_arguments")
    @patch.dict("os.environ", {}, clear=True)
    def test_check_mandatory_parameters_missing_url(self, mock_get_args: Mock) -> None:
        """Test __check_mandatory_parameters raises ValueError when URL is missing."""
        # Arrange
        mock_args = SimpleNamespace(app_url=None, app_token="token")
        mock_get_args.return_value = mock_args

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            GenericTestCase.create_extension_api("test")

        self.assertIn("app_url", str(context.exception))
        self.assertIn("not provided", str(context.exception))

    @patch("python_sbb_polarion.testing.generic_test_case.get_script_arguments")
    @patch.dict("os.environ", {"APP_URL": "https://example.com"}, clear=True)
    def test_check_mandatory_parameters_missing_token(self, mock_get_args: Mock) -> None:
        """Test __check_mandatory_parameters raises ValueError when token is missing."""
        # Arrange
        mock_args = SimpleNamespace(app_url=None, app_token=None)
        mock_get_args.return_value = mock_args

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            GenericTestCase.create_extension_api("test")

        self.assertIn("app_token", str(context.exception))
        self.assertIn("not provided", str(context.exception))

    def test_run_test_get_version_success(self) -> None:
        """Test run_test_get_version with successful response."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "bundleVendor": "SBB AG",
            "bundleVersion": "1.2.3",
            "bundleBuildTimestamp": "2024-10-23 12:34",
            "bundleName": "ch.sbb.polarion.extension.pdf-exporter",
            "automaticModuleName": "ch.sbb.polarion.extension.pdf_exporter",
            "bundleBuildTimestampDigitsOnly": "202410231234",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "pdf-exporter"
        mock_api.get_version.return_value = mock_response
        test_case.extension_api = mock_api

        # Act
        result: JsonDict = test_case.run_test_get_version()

        # Assert
        self.assertEqual(result["bundleVendor"], "SBB AG")
        self.assertEqual(result["bundleVersion"], "1.2.3")
        mock_api.get_version.assert_called_once()

    def test_run_test_get_version_validates_bundle_vendor(self) -> None:
        """Test run_test_get_version validates bundleVendor is 'SBB AG'."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "bundleVendor": "Other Vendor",
            "bundleVersion": "1.2.3",
            "bundleBuildTimestamp": "2024-10-23 12:34",
            "bundleName": "test",
            "automaticModuleName": "ch.sbb.polarion.extension.test",
            "bundleBuildTimestampDigitsOnly": "202410231234",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "test"
        mock_api.get_version.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_version()

    def test_run_test_get_version_validates_version_format(self) -> None:
        """Test run_test_get_version validates version format."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "bundleVendor": "SBB AG",
            "bundleVersion": "invalid",
            "bundleBuildTimestamp": "2024-10-23 12:34",
            "bundleName": "test",
            "automaticModuleName": "ch.sbb.polarion.extension.test",
            "bundleBuildTimestampDigitsOnly": "202410231234",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "test"
        mock_api.get_version.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_version()

    def test_run_test_get_version_validates_automatic_module_name(self) -> None:
        """Test run_test_get_version validates automatic module name."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "bundleVendor": "SBB AG",
            "bundleVersion": "1.2.3",
            "bundleBuildTimestamp": "2024-10-23 12:34",
            "bundleName": "test",
            "automaticModuleName": "wrong.module.name",
            "bundleBuildTimestampDigitsOnly": "202410231234",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "test"
        mock_api.get_version.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_version()

    def test_run_test_get_version_validates_timestamp_format(self) -> None:
        """Test run_test_get_version validates timestamp format."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "bundleVendor": "SBB AG",
            "bundleVersion": "1.2.3",
            "bundleBuildTimestamp": "invalid-timestamp",
            "bundleName": "test",
            "automaticModuleName": "ch.sbb.polarion.extension.test",
            "bundleBuildTimestampDigitsOnly": "202410231234",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "test"
        mock_api.get_version.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_version()

    def test_run_test_get_version_validates_timestamp_digits_only(self) -> None:
        """Test run_test_get_version validates timestamp digits only format."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "bundleVendor": "SBB AG",
            "bundleVersion": "1.2.3",
            "bundleBuildTimestamp": "2024-10-23 12:34",
            "bundleName": "test",
            "automaticModuleName": "ch.sbb.polarion.extension.test",
            "bundleBuildTimestampDigitsOnly": "invalid",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "test"
        mock_api.get_version.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_version()

    def test_run_test_get_version_validates_status_code(self) -> None:
        """Test run_test_get_version validates status code is 200."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.get_version.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_version()

    @patch("python_sbb_polarion.testing.generic_test_case.HttpConnection")
    def test_run_test_get_version_with_invalid_token(self, mock_http_connection_class: Mock) -> None:
        """Test run_test_get_version_with_invalid_token handles 401 error."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.UNAUTHORIZED

        mock_http_conn = Mock()
        mock_http_conn.api_request_get.return_value = mock_response
        mock_http_connection_class.return_value = mock_http_conn

        mock_api = Mock()
        mock_api.extension_name = "pdf-exporter"
        mock_api.polarion_connection.host = "https://example.com"
        test_case.extension_api = mock_api

        # Act
        test_case.run_test_get_version_with_invalid_token()

        # Assert
        mock_http_connection_class.assert_called_once_with(url="https://example.com", token="invalid token")
        mock_http_conn.api_request_get.assert_called_once_with("/polarion/pdf-exporter/rest/api/version", print_error=False)

    @patch("python_sbb_polarion.testing.generic_test_case.HttpConnection")
    def test_run_test_get_version_with_invalid_token_assertion(self, mock_http_connection_class: Mock) -> None:
        """Test run_test_get_version_with_invalid_token asserts 401 status."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK  # Wrong status code

        mock_http_conn = Mock()
        mock_http_conn.api_request_get.return_value = mock_response
        mock_http_connection_class.return_value = mock_http_conn

        mock_api = Mock()
        mock_api.extension_name = "test"
        mock_api.polarion_connection.host = "https://example.com"
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_version_with_invalid_token()

    def test_run_test_get_context_success(self) -> None:
        """Test run_test_get_context with successful response."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "baseUrl": "/polarion/pdf-exporter",
            "extensionContext": "pdf-exporter",
            "restUrl": "/polarion/pdf-exporter/rest",
            "swaggerUiUrl": "/polarion/pdf-exporter/rest/swagger",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "pdf-exporter"
        mock_api.get_context.return_value = mock_response
        test_case.extension_api = mock_api

        # Act
        result: JsonDict = test_case.run_test_get_context()

        # Assert
        self.assertEqual(result["baseUrl"], "/polarion/pdf-exporter")
        self.assertEqual(result["extensionContext"], "pdf-exporter")
        self.assertEqual(result["restUrl"], "/polarion/pdf-exporter/rest")
        self.assertEqual(result["swaggerUiUrl"], "/polarion/pdf-exporter/rest/swagger")
        mock_api.get_context.assert_called_once()

    def test_run_test_get_context_validates_status_code(self) -> None:
        """Test run_test_get_context validates status code is 200."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.get_context.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_context()

    def test_run_test_get_context_validates_base_url(self) -> None:
        """Test run_test_get_context validates baseUrl."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "baseUrl": "/wrong/path",
            "extensionContext": "pdf-exporter",
            "restUrl": "/polarion/pdf-exporter/rest",
            "swaggerUiUrl": "/polarion/pdf-exporter/rest/swagger",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "pdf-exporter"
        mock_api.get_context.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_context()

    def test_run_test_get_context_validates_extension_context(self) -> None:
        """Test run_test_get_context validates extensionContext."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "baseUrl": "/polarion/pdf-exporter",
            "extensionContext": "wrong-extension",
            "restUrl": "/polarion/pdf-exporter/rest",
            "swaggerUiUrl": "/polarion/pdf-exporter/rest/swagger",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "pdf-exporter"
        mock_api.get_context.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_context()

    def test_run_test_get_context_validates_rest_url(self) -> None:
        """Test run_test_get_context validates restUrl."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "baseUrl": "/polarion/pdf-exporter",
            "extensionContext": "pdf-exporter",
            "restUrl": "/wrong/rest",
            "swaggerUiUrl": "/polarion/pdf-exporter/rest/swagger",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "pdf-exporter"
        mock_api.get_context.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_context()

    def test_run_test_get_context_validates_swagger_url(self) -> None:
        """Test run_test_get_context validates swaggerUiUrl."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "baseUrl": "/polarion/pdf-exporter",
            "extensionContext": "pdf-exporter",
            "restUrl": "/polarion/pdf-exporter/rest",
            "swaggerUiUrl": "/wrong/swagger",
        }

        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "pdf-exporter"
        mock_api.get_context.return_value = mock_response
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(AssertionError):
            test_case.run_test_get_context()

    def test_api_method_raises_value_error(self) -> None:
        """Test api method raises ValueError (abstract method)."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            test_case.api()

        self.assertIn("Unknown extension API", str(context.exception))

    def test_init_settings(self) -> None:
        """Test _init_settings initializes settings with defaults."""
        from http import HTTPStatus

        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]

        mock_defaults_response = Mock()
        mock_defaults_response.json.return_value = {"default": "value"}

        mock_save_response = Mock()
        mock_save_response.status_code = HTTPStatus.NO_CONTENT

        mock_api = Mock(spec=MockExtensionApi)
        mock_api.get_setting_default_content.return_value = mock_defaults_response
        mock_api.save_setting.return_value = mock_save_response
        test_case.extension_api = mock_api

        # Act
        test_case._init_settings(feature="test_feature")

        # Assert
        mock_api.get_setting_default_content.assert_called_once_with(feature="test_feature")
        mock_api.save_setting.assert_called_once_with(feature="test_feature", scope=None, data={"default": "value"})

    def test_init_settings_with_custom_scope(self) -> None:
        """Test _init_settings with custom scope parameter."""
        from http import HTTPStatus

        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]

        mock_defaults_response = Mock()
        mock_defaults_response.json.return_value = {"default": "value"}

        mock_save_response = Mock()
        mock_save_response.status_code = HTTPStatus.NO_CONTENT

        mock_api = Mock(spec=MockExtensionApi)
        mock_api.get_setting_default_content.return_value = mock_defaults_response
        mock_api.save_setting.return_value = mock_save_response
        test_case.extension_api = mock_api

        # Act
        test_case._init_settings(feature="test_feature", scope="project")

        # Assert
        mock_api.save_setting.assert_called_once_with(feature="test_feature", scope="project", data={"default": "value"})

    def test_init_settings_raises_type_error_for_non_settings_api(self) -> None:
        """Test _init_settings raises TypeError when extension doesn't support settings."""
        # Arrange
        test_case = GenericTestCase()  # type: ignore[abstract]

        # Use base API without settings mixin
        mock_api = Mock(spec=PolarionGenericExtensionApi)
        mock_api.extension_name = "test-extension"
        test_case.extension_api = mock_api

        # Act & Assert
        with self.assertRaises(TypeError) as context:
            test_case._init_settings(feature="test_feature")

        self.assertIn("does not support settings", str(context.exception))
        self.assertIn("test-extension", str(context.exception))

    def test_setup_class(self) -> None:
        """Test setUpClass configures logging."""
        # Act
        GenericTestCase.setUpClass()

        # Assert - logging was configured (no exception means success)

    @patch.dict("os.environ", {"INT_PARAM": "not_an_int"})
    def test_get_parameter_type_conversion_failure(self) -> None:
        """Test get_parameter returns script argument when type conversion fails."""
        # Act - env has "not_an_int" but script_argument_value is int
        result: int = GenericTestCase.get_parameter("INT_PARAM", 42)

        # Assert - returns original script argument since "not_an_int" can't convert to int
        self.assertEqual(result, 42)

    @patch("python_sbb_polarion.testing.generic_test_case.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.generic_test_case.PolarionApiV1")
    @patch("python_sbb_polarion.testing.generic_test_case.get_script_arguments")
    @patch.dict("os.environ", {"APP_URL": "https://example.com", "APP_TOKEN": "test-token"})
    def test_polarion_api_method(self, mock_get_args: Mock, mock_polarion_api_v1: Mock, mock_factory: Mock) -> None:
        """Test polarion_api returns the internal PolarionApiV1 instance."""
        # Arrange
        mock_args = SimpleNamespace(app_url=None, app_token=None)
        mock_get_args.return_value = mock_args

        mock_api = Mock(spec=MockExtensionApi)
        mock_factory.return_value = mock_api

        mock_polarion_api_v1_instance = Mock()
        mock_polarion_api_v1.return_value = mock_polarion_api_v1_instance

        # Act - create extension API first to initialize polarion_api()
        GenericTestCase.create_extension_api("pdf-exporter")
        test_case = GenericTestCase()  # type: ignore[abstract]
        result: object = test_case.polarion_api()

        # Assert - polarion_api() returns PolarionApiV1
        self.assertEqual(result, mock_polarion_api_v1_instance)


if __name__ == "__main__":
    unittest.main()
