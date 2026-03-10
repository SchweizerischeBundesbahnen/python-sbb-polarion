"""Generic Polarion Test Case"""

from __future__ import annotations

import logging
import os
import re
import unittest
from abc import abstractmethod
from http import HTTPStatus
from typing import TYPE_CHECKING, Literal, TypeVar, overload

from python_sbb_polarion.core import PolarionApiV1
from python_sbb_polarion.core.base import PolarionGenericExtensionApi, PolarionGenericExtensionSettingsApi, PolarionRestApiConnection
from python_sbb_polarion.core.factory import ExtensionApiFactory
from python_sbb_polarion.util.argparse import get_script_arguments
from python_sbb_polarion.util.http import HttpConnection


if TYPE_CHECKING:
    import argparse

    from requests import Response

    from python_sbb_polarion.extensions.aad_synchronizer import PolarionAadSynchronizerApi
    from python_sbb_polarion.extensions.admin_utility import PolarionAdminUtilityApi
    from python_sbb_polarion.extensions.api_extender import PolarionApiExtenderApi
    from python_sbb_polarion.extensions.collection_checker import PolarionCollectionCheckerApi
    from python_sbb_polarion.extensions.cucumber import PolarionCucumberApi
    from python_sbb_polarion.extensions.diff_tool import PolarionDiffToolApi
    from python_sbb_polarion.extensions.dms_doc_connector import PolarionDmsDocConnectorApi
    from python_sbb_polarion.extensions.dms_wi_connector import PolarionDmsWiConnectorApi
    from python_sbb_polarion.extensions.docx_exporter import PolarionDocxExporterApi
    from python_sbb_polarion.extensions.excel_importer import PolarionExcelImporterApi
    from python_sbb_polarion.extensions.fake_services import PolarionFakeServicesApi
    from python_sbb_polarion.extensions.interceptor_manager import PolarionInterceptorManagerApi
    from python_sbb_polarion.extensions.json_editor import PolarionJsonEditorApi
    from python_sbb_polarion.extensions.mailworkflow import PolarionMailWorkflowApi
    from python_sbb_polarion.extensions.pdf_exporter import PolarionPdfExporterApi
    from python_sbb_polarion.extensions.requirements_inspector import PolarionRequirementsInspectorApi
    from python_sbb_polarion.extensions.strictdoc_exporter import PolarionStrictDocExporterApi
    from python_sbb_polarion.extensions.test_data import PolarionTestDataApi
    from python_sbb_polarion.extensions.xml_repair import PolarionXmlRepairApi
    from python_sbb_polarion.types import JsonDict, JsonValue


logger = logging.getLogger(__name__)


class GenericTestCase(unittest.TestCase):
    """Generic Polarion Test Case with common code for system tests"""

    extension_api: PolarionGenericExtensionApi
    __polarion_api: PolarionApiV1

    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["aad-synchronizer"]) -> PolarionAadSynchronizerApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["admin-utility"]) -> PolarionAdminUtilityApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["api-extender"]) -> PolarionApiExtenderApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["collection-checker"]) -> PolarionCollectionCheckerApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["cucumber"]) -> PolarionCucumberApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["diff-tool"]) -> PolarionDiffToolApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["dms-doc-connector"]) -> PolarionDmsDocConnectorApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["dms-wi-connector"]) -> PolarionDmsWiConnectorApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["excel-importer"]) -> PolarionExcelImporterApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["fake-services"]) -> PolarionFakeServicesApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["interceptor-manager"]) -> PolarionInterceptorManagerApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["json-editor"]) -> PolarionJsonEditorApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["mailworkflow"]) -> PolarionMailWorkflowApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["pdf-exporter"]) -> PolarionPdfExporterApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["docx-exporter"]) -> PolarionDocxExporterApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["requirements-inspector"]) -> PolarionRequirementsInspectorApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["strictdoc-exporter"]) -> PolarionStrictDocExporterApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["test-data"]) -> PolarionTestDataApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: Literal["xml-repair"]) -> PolarionXmlRepairApi: ...

    @overload
    @classmethod
    def create_extension_api(cls, extension_name: str) -> PolarionGenericExtensionApi: ...

    @classmethod
    def create_extension_api(cls, extension_name: str) -> PolarionGenericExtensionApi:
        """Create extension API using provided extension name. If omitted try to detect it based on repo name.

        Returns:
            PolarionGenericExtensionApi: Configured extension API instance
        """
        app_url: str
        app_token: str
        app_url, app_token = cls.__get_parameters()
        polarion_connection = PolarionRestApiConnection(url=app_url, token=app_token)
        cls.__polarion_api = PolarionApiV1(polarion_connection)
        return ExtensionApiFactory.get_extension_api_by_name(extension_name=extension_name, polarion_connection=polarion_connection)

    @classmethod
    def __get_parameters(cls) -> tuple[str, str]:
        args: argparse.Namespace = get_script_arguments()

        app_url: str | None = cls.get_parameter("APP_URL", args.app_url)
        if app_url is None:
            raise ValueError("'app_url' is not provided: use --app_url or APP_URL env variable")

        app_token: str | None = cls.get_parameter("APP_TOKEN", args.app_token)
        if app_token is None:
            raise ValueError("'app_token' is not provided: use --app_token or APP_TOKEN env variable")

        return app_url, app_token

    T = TypeVar("T")

    @staticmethod
    @overload
    def get_parameter(env_param_name: str, script_argument_value: None = None) -> str | None: ...
    @staticmethod
    @overload
    def get_parameter(env_param_name: str, script_argument_value: T) -> T: ...

    @staticmethod
    def get_parameter(env_param_name: str, script_argument_value: T | None = None) -> T | str | None:
        env_value: str | None = os.environ.get(env_param_name)

        if env_value is None:
            return script_argument_value

        if script_argument_value is None:
            return env_value

        try:
            return type(script_argument_value)(env_value)  # type: ignore[call-arg]
        except Exception:
            return script_argument_value

    def run_test_get_version(self) -> JsonDict:
        """Method code for testing GET /version endpoint.

        Returns:
            JsonDict: Version information JSON
        """
        # Ensure extension_api is initialized
        assert self.extension_api is not None

        # Act
        response: Response = self.extension_api.get_version()

        # Assert
        assert response.status_code == HTTPStatus.OK

        json: JsonDict = response.json()

        bundle_vendor: JsonValue = json["bundleVendor"]
        bundle_version: JsonValue = json["bundleVersion"]
        bundle_build_timestamp: JsonValue = json["bundleBuildTimestamp"]
        bundle_name: JsonValue = json["bundleName"]
        automatic_module_name: JsonValue = json["automaticModuleName"]
        bundle_build_timestamp_digits_only: JsonValue = json["bundleBuildTimestampDigitsOnly"]

        # Type narrowing - ensure values are strings
        assert isinstance(bundle_version, str)
        assert isinstance(bundle_build_timestamp, str)
        assert isinstance(bundle_build_timestamp_digits_only, str)

        logger.info("Bundle name: '%s', Automatic module name: '%s', Bundle version: '%s', Bundle Build timestamp: '%s'", bundle_name, automatic_module_name, bundle_version, bundle_build_timestamp)

        assert bundle_vendor == "SBB AG"
        assert automatic_module_name == f"ch.sbb.polarion.extension.{self.extension_api.extension_name.replace('-', '_')}"
        assert re.match(r"^\d+\.\d+\.\d+$", bundle_version)
        assert re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", bundle_build_timestamp)
        assert re.match(r"^\d{4}\d{2}\d{2}\d{2}\d{2}$", bundle_build_timestamp_digits_only)

        return json

    def run_test_get_version_with_invalid_token(self) -> None:
        """Method code for testing GET /version endpoint with invalid token."""
        # Ensure extension_api is initialized
        assert self.extension_api is not None

        # Act
        extension_url: str = f"/polarion/{self.extension_api.extension_name}/rest/api/version"
        # S106: Hardcoded test token is acceptable for testing invalid authentication
        http_connection: HttpConnection = HttpConnection(url=self.extension_api.polarion_connection.host, token="invalid token")  # noqa: S106
        response: Response = http_connection.api_request_get(extension_url, print_error=False)

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def run_test_get_context(self) -> JsonDict:
        """Method code for testing GET /context endpoint.

        Returns:
            JsonDict: Context information JSON
        """
        # Ensure extension_api is initialized
        assert self.extension_api is not None

        # Act
        response: Response = self.extension_api.get_context()

        # Assert
        assert response.status_code == HTTPStatus.OK

        json: JsonDict = response.json()

        assert json["baseUrl"] == f"/polarion/{self.extension_api.extension_name}"
        assert json["extensionContext"] == self.extension_api.extension_name
        assert json["restUrl"] == f"/polarion/{self.extension_api.extension_name}/rest"
        assert json["swaggerUiUrl"] == f"/polarion/{self.extension_api.extension_name}/rest/swagger"

        return json

    def _init_settings(self, feature: str, scope: str | None = None) -> None:
        """Initialize settings with default values to prevent clashes with default Repository settings

        Raises:
            TypeError: If extension API does not support settings (missing PolarionGenericExtensionSettingsApi mixin)
        """
        # Ensure extension_api is initialized
        assert self.extension_api is not None

        # Check if extension has settings API (mixin)
        if not isinstance(self.extension_api, PolarionGenericExtensionSettingsApi):
            raise TypeError(f"Extension API '{self.extension_api.extension_name}' does not support settings (missing PolarionGenericExtensionSettingsApi mixin)")

        default_settings: Response = self.extension_api.get_setting_default_content(feature=feature)
        save_response: Response = self.extension_api.save_setting(feature=feature, scope=scope, data=default_settings.json())
        assert save_response.status_code == HTTPStatus.NO_CONTENT

    @abstractmethod
    def api(self) -> PolarionGenericExtensionApi:
        """Casting to extension API

        Raises:
            ValueError: Always raised - method must be implemented by subclass
        """
        raise ValueError("Unknown extension API")

    def polarion_api(self) -> PolarionApiV1:
        return self.__polarion_api
