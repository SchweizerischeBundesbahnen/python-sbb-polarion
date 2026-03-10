"""Unit tests for TestContainersHelper."""

from __future__ import annotations

import os
import unittest
from http import HTTPStatus
from unittest.mock import Mock, patch

from python_sbb_polarion.extensions.admin_utility import PolarionAdminUtilityApi
from python_sbb_polarion.testing.testcontainers_helper import (
    ArtifactInfo,
    ContainerSetupError,
    MavenError,
    PolarionContainerParameters,
    PolarionStartupError,
    TestContainersHelper,
)
from python_sbb_polarion.types import MediaType


class TestExceptionClasses(unittest.TestCase):
    """Test custom exception classes."""

    def test_container_setup_error(self) -> None:
        """Test ContainerSetupError can be raised and caught."""
        # Act & Assert
        with self.assertRaises(ContainerSetupError) as context:
            raise ContainerSetupError("Container setup failed")

        self.assertEqual(str(context.exception), "Container setup failed")
        self.assertIsInstance(context.exception, Exception)

    def test_polarion_startup_error(self) -> None:
        """Test PolarionStartupError can be raised and caught."""
        # Act & Assert
        with self.assertRaises(PolarionStartupError) as context:
            raise PolarionStartupError("Polarion failed to start")

        self.assertEqual(str(context.exception), "Polarion failed to start")
        self.assertIsInstance(context.exception, Exception)

    def test_maven_error(self) -> None:
        """Test MavenError can be raised and caught."""
        # Act & Assert
        with self.assertRaises(MavenError) as context:
            raise MavenError("Maven command failed")

        self.assertEqual(str(context.exception), "Maven command failed")
        self.assertIsInstance(context.exception, Exception)


class TestArtifactInfo(unittest.TestCase):
    """Test ArtifactInfo dataclass."""

    def test_artifact_info_creation(self) -> None:
        """Test ArtifactInfo dataclass creation."""
        # Act
        artifact = ArtifactInfo(group_id="com.example", artifact_id="my-artifact", version="1.0.0")

        # Assert
        self.assertEqual(artifact.group_id, "com.example")
        self.assertEqual(artifact.artifact_id, "my-artifact")
        self.assertEqual(artifact.version, "1.0.0")


class TestPolarionContainerParameters(unittest.TestCase):
    """Test PolarionContainerParameters dataclass."""

    def test_polarion_container_parameters_creation(self) -> None:
        """Test PolarionContainerParameters dataclass creation."""
        # Arrange
        artifacts: list[ArtifactInfo] = [ArtifactInfo("group", "artifact", "1.0")]

        # Act
        params: PolarionContainerParameters = PolarionContainerParameters(
            polarion_image_name="polarion:latest",
            weasyprint_service_image_name="weasyprint:latest",
            extension_version="2.0.0",
            additional_bundles=artifacts,
            admin_utility_version="3.0.0",
        )

        # Assert
        self.assertEqual(params.polarion_image_name, "polarion:latest")
        self.assertEqual(params.weasyprint_service_image_name, "weasyprint:latest")
        self.assertEqual(params.extension_version, "2.0.0")
        self.assertEqual(params.additional_bundles, artifacts)
        self.assertEqual(params.admin_utility_version, "3.0.0")


class TestTestContainersHelperGetParameter(unittest.TestCase):
    """Test TestContainersHelper.get_parameter method."""

    @patch.dict("os.environ", {"TEST_VAR": "env_value"})
    def test_get_parameter_from_env(self) -> None:
        """Test get_parameter returns environment variable when available."""
        # Act
        result: str | None = TestContainersHelper.get_parameter("TEST_VAR", "arg_value")

        # Assert
        self.assertEqual(result, "env_value")

    @patch.dict("os.environ", {}, clear=True)
    def test_get_parameter_from_arg(self) -> None:
        """Test get_parameter returns argument when env variable not available."""
        # Act
        result: str | None = TestContainersHelper.get_parameter("TEST_VAR", "arg_value")

        # Assert
        self.assertEqual(result, "arg_value")

    @patch.dict("os.environ", {}, clear=True)
    def test_get_parameter_returns_none(self) -> None:
        """Test get_parameter returns None when both env and arg are None."""
        # Act
        result: str | None = TestContainersHelper.get_parameter("TEST_VAR", None)

        # Assert
        self.assertIsNone(result)


class TestTestContainersHelperParseAdditionalBundles(unittest.TestCase):
    """Test TestContainersHelper.parse_additional_bundles method."""

    def test_parse_additional_bundles_single(self) -> None:
        """Test parse_additional_bundles with single bundle."""
        # Act
        result: list[ArtifactInfo] | None = TestContainersHelper.parse_additional_bundles("com.example:artifact:1.0.0")

        # Assert
        self.assertIsNotNone(result)
        assert result is not None  # Type narrowing
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].group_id, "com.example")
        self.assertEqual(result[0].artifact_id, "artifact")
        self.assertEqual(result[0].version, "1.0.0")

    def test_parse_additional_bundles_multiple(self) -> None:
        """Test parse_additional_bundles with multiple bundles."""
        # Act
        result: list[ArtifactInfo] | None = TestContainersHelper.parse_additional_bundles("com.example:artifact1:1.0.0,org.test:artifact2:2.0.0")

        # Assert
        self.assertIsNotNone(result)
        assert result is not None  # Type narrowing
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].group_id, "com.example")
        self.assertEqual(result[0].artifact_id, "artifact1")
        self.assertEqual(result[0].version, "1.0.0")
        self.assertEqual(result[1].group_id, "org.test")
        self.assertEqual(result[1].artifact_id, "artifact2")
        self.assertEqual(result[1].version, "2.0.0")

    def test_parse_additional_bundles_none(self) -> None:
        """Test parse_additional_bundles with None input."""
        # Act
        result: list[ArtifactInfo] | None = TestContainersHelper.parse_additional_bundles(None)

        # Assert
        self.assertIsNone(result)


class TestTestContainersHelperGetMavenLocation(unittest.TestCase):
    """Test TestContainersHelper.get_maven_location method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.shutil.which")
    def test_get_maven_location_found(self, mock_which: Mock) -> None:
        """Test get_maven_location returns Maven path when found."""
        # Arrange
        mock_which.return_value = "/usr/local/bin/mvn"

        # Act
        result: str = TestContainersHelper.get_maven_location()

        # Assert
        self.assertEqual(result, "/usr/local/bin/mvn")
        mock_which.assert_called_once_with("mvn")

    @patch("python_sbb_polarion.testing.testcontainers_helper.shutil.which")
    def test_get_maven_location_not_found(self, mock_which: Mock) -> None:
        """Test get_maven_location raises MavenError when Maven not found."""
        # Arrange
        mock_which.return_value = None

        # Act & Assert
        with self.assertRaises(MavenError) as context:
            TestContainersHelper.get_maven_location()

        self.assertIn("Maven is not available", str(context.exception))


class TestTestContainersHelperGetLatestArtifactVersion(unittest.TestCase):
    """Test TestContainersHelper.get_latest_artifact_version method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_maven_repo_location")
    @patch("python_sbb_polarion.testing.testcontainers_helper.pathlib.Path")
    def test_get_latest_artifact_version_sorts_correctly(self, mock_path_class: Mock, mock_get_repo: Mock) -> None:
        """Test get_latest_artifact_version returns highest version."""
        # Arrange
        mock_get_repo.return_value = "/home/user/.m2/repository"

        # Mock directory structure with items that have .name attribute
        mock_artifact_path = Mock()
        mock_item1: Mock
        mock_item2: Mock
        mock_item3: Mock
        mock_item4: Mock
        mock_item1, mock_item2, mock_item3, mock_item4 = Mock(), Mock(), Mock(), Mock()
        mock_item1.name, mock_item2.name, mock_item3.name, mock_item4.name = "1.0.0", "1.2.0", "2.0.0", "1.10.0"
        mock_artifact_path.iterdir.return_value = [mock_item1, mock_item2, mock_item3, mock_item4]

        # Mock Path to support chained / operations: Path(repo) / group / artifact
        mock_group_path = Mock()
        mock_group_path.__truediv__ = Mock(return_value=mock_artifact_path)

        mock_repo_path = Mock()
        mock_repo_path.__truediv__ = Mock(return_value=mock_group_path)
        mock_path_class.return_value = mock_repo_path

        # Act
        result: str = TestContainersHelper.get_latest_artifact_version("com.example", "artifact")

        # Assert
        self.assertEqual(result, "2.0.0")

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_maven_repo_location")
    @patch("python_sbb_polarion.testing.testcontainers_helper.pathlib.Path")
    def test_get_latest_artifact_version_handles_snapshot(self, mock_path_class: Mock, mock_get_repo: Mock) -> None:
        """Test get_latest_artifact_version handles SNAPSHOT versions."""
        # Arrange
        mock_get_repo.return_value = "/home/user/.m2/repository"

        # Mock directory structure with items that have .name attribute
        mock_artifact_path = Mock()
        mock_item1: Mock
        mock_item2: Mock
        mock_item3: Mock
        mock_item1, mock_item2, mock_item3 = Mock(), Mock(), Mock()
        mock_item1.name, mock_item2.name, mock_item3.name = "1.0.0", "2.0.0-SNAPSHOT", "1.5.0"
        mock_artifact_path.iterdir.return_value = [mock_item1, mock_item2, mock_item3]

        # Mock Path to support chained / operations: Path(repo) / group / artifact
        mock_group_path = Mock()
        mock_group_path.__truediv__ = Mock(return_value=mock_artifact_path)

        mock_repo_path = Mock()
        mock_repo_path.__truediv__ = Mock(return_value=mock_group_path)
        mock_path_class.return_value = mock_repo_path

        # Act
        result: str = TestContainersHelper.get_latest_artifact_version("com.example", "artifact")

        # Assert
        # "2.0.0-SNAPSHOT" should be first when sorted in reverse
        self.assertEqual(result, "2.0.0-SNAPSHOT")

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_maven_repo_location")
    @patch("python_sbb_polarion.testing.testcontainers_helper.pathlib.Path")
    def test_get_latest_artifact_version_filters_non_versions(self, mock_path_class: Mock, mock_get_repo: Mock) -> None:
        """Test get_latest_artifact_version filters out non-version directories."""
        # Arrange
        mock_get_repo.return_value = "/home/user/.m2/repository"

        # Mock directory structure with items that have .name attribute (including non-version items)
        mock_artifact_path = Mock()
        mock_item1: Mock
        mock_item2: Mock
        mock_item3: Mock
        mock_item4: Mock
        mock_item1, mock_item2, mock_item3, mock_item4 = Mock(), Mock(), Mock(), Mock()
        mock_item1.name, mock_item2.name, mock_item3.name, mock_item4.name = "1.0.0", "2.0.0", "maven-metadata.xml", "README"
        mock_artifact_path.iterdir.return_value = [mock_item1, mock_item2, mock_item3, mock_item4]

        # Mock Path to support chained / operations: Path(repo) / group / artifact
        mock_group_path = Mock()
        mock_group_path.__truediv__ = Mock(return_value=mock_artifact_path)

        mock_repo_path = Mock()
        mock_repo_path.__truediv__ = Mock(return_value=mock_group_path)
        mock_path_class.return_value = mock_repo_path

        # Act
        result: str = TestContainersHelper.get_latest_artifact_version("com.example", "artifact")

        # Assert
        self.assertEqual(result, "2.0.0")


class TestTestContainersHelperGetMavenRepoLocation(unittest.TestCase):
    """Test TestContainersHelper.get_maven_repo_location method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.subprocess.run")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_maven_location")
    @patch("python_sbb_polarion.testing.testcontainers_helper.pathlib.Path")
    def test_get_maven_repo_location_success(self, mock_path_class: Mock, mock_get_mvn: Mock, mock_run: Mock) -> None:
        """Test get_maven_repo_location returns repository path."""
        # Arrange
        mock_get_mvn.return_value = "/usr/local/bin/mvn"
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "/home/user/.m2/repository\n"
        mock_run.return_value = mock_result

        mock_path = Mock()
        mock_path.expanduser.return_value = "/home/user/.m2/repository"
        mock_path_class.return_value = mock_path

        # Act
        result: str = TestContainersHelper.get_maven_repo_location()

        # Assert
        self.assertEqual(result, "/home/user/.m2/repository")
        mock_run.assert_called_once()
        # Verify the command contains the Maven executable
        call_args: tuple[tuple[object, ...], dict[str, object]] = mock_run.call_args
        self.assertIn("/usr/local/bin/mvn", call_args[0][0])  # type: ignore[arg-type]

    @patch("python_sbb_polarion.testing.testcontainers_helper.subprocess.run")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_maven_location")
    def test_get_maven_repo_location_failure(self, mock_get_mvn: Mock, mock_run: Mock) -> None:
        """Test get_maven_repo_location raises MavenError on failure."""
        # Arrange
        mock_get_mvn.return_value = "/usr/local/bin/mvn"
        mock_result = Mock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        # Act & Assert
        with self.assertRaises(MavenError) as context:
            TestContainersHelper.get_maven_repo_location()

        self.assertIn("Cannot determine local maven repository", str(context.exception))
        self.assertIn("code: 1", str(context.exception))


class TestTestContainersHelperCopyDependency(unittest.TestCase):
    """Test TestContainersHelper.copy_dependency method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.subprocess.run")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_maven_location")
    def test_copy_dependency_success_with_version(self, mock_get_mvn: Mock, mock_run: Mock) -> None:
        """Test copy_dependency successfully copies artifact with version."""
        # Arrange
        mock_get_mvn.return_value = "/usr/bin/mvn"
        mock_result = Mock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        # Act
        TestContainersHelper.copy_dependency("/tmp/extensions", "com.example", "artifact", "1.0.0")

        # Assert
        mock_run.assert_called_once()
        call_args: list[str] = mock_run.call_args[0][0]
        self.assertIn("/usr/bin/mvn", call_args)
        self.assertIn("dependency:copy", call_args)
        self.assertIn("-Dartifact=com.example:artifact:1.0.0", call_args)
        self.assertIn("-DoutputDirectory=/tmp/extensions", call_args)

    @patch("python_sbb_polarion.testing.testcontainers_helper.subprocess.run")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_latest_artifact_version")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_maven_location")
    def test_copy_dependency_success_without_version(self, mock_get_mvn: Mock, mock_get_latest: Mock, mock_run: Mock) -> None:
        """Test copy_dependency gets latest version when version is None."""
        # Arrange
        mock_get_mvn.return_value = "/usr/bin/mvn"
        mock_get_latest.return_value = "2.0.0"
        mock_result = Mock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        # Act
        TestContainersHelper.copy_dependency("/tmp/extensions", "com.example", "artifact", None)

        # Assert
        mock_get_latest.assert_called_once_with("com.example", "artifact")
        mock_run.assert_called_once()
        call_args: list[str] = mock_run.call_args[0][0]
        self.assertIn("-Dartifact=com.example:artifact:2.0.0", call_args)

    @patch("python_sbb_polarion.testing.testcontainers_helper.subprocess.run")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_maven_location")
    def test_copy_dependency_failure(self, mock_get_mvn: Mock, mock_run: Mock) -> None:
        """Test copy_dependency raises MavenError on failure."""
        # Arrange
        mock_get_mvn.return_value = "/usr/bin/mvn"
        mock_result = Mock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        # Act & Assert
        with self.assertRaises(MavenError) as context:
            TestContainersHelper.copy_dependency("/tmp/extensions", "com.example", "artifact", "1.0.0")

        self.assertIn("Failed to copy artifact", str(context.exception))
        self.assertIn("com.example:artifact:1.0.0", str(context.exception))
        self.assertIn("code: 1", str(context.exception))


class TestTestContainersHelperGetParameters(unittest.TestCase):
    """Test TestContainersHelper.get_parameters method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_parameter")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.parse_additional_bundles")
    def test_get_parameters_all_set(self, mock_parse: Mock, mock_get_param: Mock) -> None:
        """Test get_parameters with all parameters set."""
        # Arrange
        mock_get_param.side_effect = ["polarion:latest", "weasyprint:latest", "1.0.0", "com.example:artifact:1.0", "3.0.0"]
        mock_parse.return_value = [ArtifactInfo("com.example", "artifact", "1.0")]

        args = Mock()
        args.tc_polarion_image_name = "polarion:latest"
        args.tc_weasyprint_service_image_name = "weasyprint:latest"
        args.tc_extension_version = "1.0.0"
        args.tc_additional_bundles = "com.example:artifact:1.0"
        args.tc_admin_utility_version = "3.0.0"

        # Act
        result: PolarionContainerParameters = TestContainersHelper.get_parameters(args)

        # Assert
        self.assertIsInstance(result, PolarionContainerParameters)
        self.assertEqual(result.polarion_image_name, "polarion:latest")
        self.assertEqual(result.weasyprint_service_image_name, "weasyprint:latest")
        self.assertEqual(result.extension_version, "1.0.0")
        self.assertEqual(result.admin_utility_version, "3.0.0")
        self.assertIsNotNone(result.additional_bundles)

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_parameter")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.parse_additional_bundles")
    def test_get_parameters_none_values(self, mock_parse: Mock, mock_get_param: Mock) -> None:
        """Test get_parameters with None values."""
        # Arrange
        mock_get_param.return_value = None
        mock_parse.return_value = None

        args = Mock()
        args.tc_polarion_image_name = None
        args.tc_weasyprint_service_image_name = None
        args.tc_extension_version = None
        args.tc_additional_bundles = None
        args.tc_admin_utility_version = None

        # Act
        result: PolarionContainerParameters = TestContainersHelper.get_parameters(args)

        # Assert
        self.assertEqual(result.polarion_image_name, "")
        self.assertEqual(result.weasyprint_service_image_name, "")
        self.assertEqual(result.extension_version, "")
        self.assertEqual(result.admin_utility_version, "")
        self.assertIsNone(result.additional_bundles)


class TestTestContainersHelperCheckDefaultActivationResponse(unittest.TestCase):
    """Test TestContainersHelper.check_default_activation_response method."""

    def test_check_default_activation_response_normal(self) -> None:
        """Test check_default_activation_response with normal JSON response."""
        # Arrange
        mock_response = Mock()
        mock_response.headers.get.return_value = MediaType.JSON
        mock_response.content = b'{"status": "ok"}'

        # Act - should not raise
        TestContainersHelper.check_default_activation_response(mock_response)

        # Assert - no exception raised

    def test_check_default_activation_response_plain_text_without_activated(self) -> None:
        """Test check_default_activation_response with plain text without 'activated'."""
        # Arrange
        mock_response = Mock()
        mock_response.headers.get.return_value = MediaType.PLAIN
        mock_response.content = b"Some plain text response"

        # Act - should not raise
        TestContainersHelper.check_default_activation_response(mock_response)

        # Assert - no exception raised

    def test_check_default_activation_response_raises_error(self) -> None:
        """Test check_default_activation_response raises PolarionStartupError."""
        # Arrange
        mock_response = Mock()
        mock_response.headers.get.return_value = "text/plain; charset=utf-8"
        mock_response.content = b'{"activated":true}'

        # Act & Assert
        with self.assertRaises(PolarionStartupError) as context:
            TestContainersHelper.check_default_activation_response(mock_response)

        self.assertIn("admin-utility extension is not available", str(context.exception))

    def test_check_default_activation_response_none_content_type(self) -> None:
        """Test check_default_activation_response with None content type."""
        # Arrange
        mock_response = Mock()
        mock_response.headers.get.return_value = None
        mock_response.content = b'{"activated":true}'

        # Act - should not raise
        TestContainersHelper.check_default_activation_response(mock_response)

        # Assert - no exception raised

    def test_check_default_activation_response_none_content(self) -> None:
        """Test check_default_activation_response with None content."""
        # Arrange
        mock_response = Mock()
        mock_response.headers.get.return_value = MediaType.PLAIN
        mock_response.content = None

        # Act - should not raise
        TestContainersHelper.check_default_activation_response(mock_response)

        # Assert - no exception raised


class TestTestContainersHelperCreateTestContainerIfRequired(unittest.TestCase):
    """Test TestContainersHelper.create_test_container_if_required method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.create_polarion_container")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.create_weasyprint_service_container")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.create_network")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_parameters")
    @patch("python_sbb_polarion.testing.testcontainers_helper.get_script_arguments")
    @patch.dict("os.environ", {}, clear=True)
    def test_create_test_container_with_both_images(self, mock_get_args: Mock, mock_get_params: Mock, mock_create_network: Mock, mock_create_weasyprint: Mock, mock_create_polarion: Mock) -> None:
        """Test create_test_container_if_required with both weasyprint and polarion images."""
        # Arrange
        mock_args = Mock()
        mock_get_args.return_value = mock_args

        params = PolarionContainerParameters(polarion_image_name="polarion:latest", weasyprint_service_image_name="weasyprint:latest", extension_version="1.0.0", additional_bundles=None, admin_utility_version="2.0.0")
        mock_get_params.return_value = params

        mock_create_weasyprint.return_value = "http://weasyprint:9080"
        mock_create_polarion.return_value = ("http://localhost:8080", "test-token")

        helper = TestContainersHelper()

        # Act
        helper.create_test_container_if_required("pdf-exporter")

        # Assert
        mock_create_network.assert_called_once_with("test-weasyprint-network")
        mock_create_weasyprint.assert_called_once_with(params)
        mock_create_polarion.assert_called_once_with("pdf-exporter", params, "http://weasyprint:9080")
        self.assertEqual(os.environ.get("APP_URL"), "http://localhost:8080")
        self.assertEqual(os.environ.get("APP_TOKEN"), "test-token")

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.create_polarion_container")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_parameters")
    @patch("python_sbb_polarion.testing.testcontainers_helper.get_script_arguments")
    @patch.dict("os.environ", {}, clear=True)
    def test_create_test_container_only_polarion(self, mock_get_args: Mock, mock_get_params: Mock, mock_create_polarion: Mock) -> None:
        """Test create_test_container_if_required with only polarion image."""
        # Arrange
        mock_args = Mock()
        mock_get_args.return_value = mock_args

        params = PolarionContainerParameters(polarion_image_name="polarion:latest", weasyprint_service_image_name="", extension_version="1.0.0", additional_bundles=None, admin_utility_version="2.0.0")
        mock_get_params.return_value = params

        mock_create_polarion.return_value = ("http://localhost:8080", "test-token")

        helper = TestContainersHelper()

        # Act
        helper.create_test_container_if_required("pdf-exporter")

        # Assert
        mock_create_polarion.assert_called_once_with("pdf-exporter", params, None)

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.get_parameters")
    @patch("python_sbb_polarion.testing.testcontainers_helper.get_script_arguments")
    def test_create_test_container_no_images(self, mock_get_args: Mock, mock_get_params: Mock) -> None:
        """Test create_test_container_if_required with no images."""
        # Arrange
        mock_args = Mock()
        mock_get_args.return_value = mock_args

        params = PolarionContainerParameters(polarion_image_name="", weasyprint_service_image_name="", extension_version="1.0.0", additional_bundles=None, admin_utility_version="2.0.0")
        mock_get_params.return_value = params

        helper = TestContainersHelper()

        # Act
        helper.create_test_container_if_required("pdf-exporter")

        # Assert - method completes without creating containers


class TestTestContainersHelperCreateWeasyprintServiceContainer(unittest.TestCase):
    """Test TestContainersHelper.create_weasyprint_service_container method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.DockerContainer")
    def test_create_weasyprint_service_container_success(self, mock_docker_container_class: Mock) -> None:
        """Test create_weasyprint_service_container creates and starts container."""
        # Arrange
        params = PolarionContainerParameters(polarion_image_name="", weasyprint_service_image_name="weasyprint:latest", extension_version="", additional_bundles=None, admin_utility_version="")

        mock_container = Mock()
        mock_wrapped = Mock()
        mock_wrapped.short_id = "abc123"
        mock_container.get_wrapped_container.return_value = mock_wrapped
        mock_container.with_bind_ports.return_value = mock_container
        mock_container.with_name.return_value = mock_container
        mock_docker_container_class.return_value = mock_container

        helper = TestContainersHelper()

        # Act
        result: str = helper.create_weasyprint_service_container(params)

        # Assert
        self.assertEqual(result, "http://test-weasyprint-service-container:9080")
        mock_container.start.assert_called_once()
        self.assertEqual(helper.weasyprint_service_container, mock_container)

    @patch("python_sbb_polarion.testing.testcontainers_helper.DockerContainer")
    def test_create_weasyprint_service_container_with_network(self, mock_docker_container_class: Mock) -> None:
        """Test create_weasyprint_service_container connects to network."""
        # Arrange
        params = PolarionContainerParameters(polarion_image_name="", weasyprint_service_image_name="weasyprint:latest", extension_version="", additional_bundles=None, admin_utility_version="")

        mock_container = Mock()
        mock_wrapped = Mock()
        mock_wrapped.short_id = "abc123"
        mock_container.get_wrapped_container.return_value = mock_wrapped
        mock_container.with_bind_ports.return_value = mock_container
        mock_container.with_name.return_value = mock_container
        mock_docker_container_class.return_value = mock_container

        mock_network = Mock()
        helper = TestContainersHelper()
        helper.network = mock_network

        # Act
        helper.create_weasyprint_service_container(params)

        # Assert
        mock_network.connect.assert_called_once_with("abc123")

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.tear_down")
    @patch("python_sbb_polarion.testing.testcontainers_helper.DockerContainer")
    def test_create_weasyprint_service_container_error(self, mock_docker_container_class: Mock, mock_tear_down: Mock) -> None:
        """Test create_weasyprint_service_container raises ContainerSetupError on failure."""
        # Arrange
        params = PolarionContainerParameters(polarion_image_name="", weasyprint_service_image_name="weasyprint:latest", extension_version="", additional_bundles=None, admin_utility_version="")

        mock_container = Mock()
        mock_container.with_bind_ports.return_value = mock_container
        mock_container.with_name.return_value = mock_container
        mock_container.start.side_effect = Exception("Docker error")
        mock_docker_container_class.return_value = mock_container

        helper = TestContainersHelper()

        # Act & Assert
        with self.assertRaises(ContainerSetupError) as context:
            helper.create_weasyprint_service_container(params)

        self.assertIn("Cannot setup Weasyprint Service container", str(context.exception))
        mock_tear_down.assert_called_once()


class TestTestContainersHelperCreatePolarionContainer(unittest.TestCase):
    """Test TestContainersHelper.create_polarion_container method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.time.sleep")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.setup_polarion_container")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.prepare_systest_extensions")
    @patch("python_sbb_polarion.testing.testcontainers_helper.DockerContainer")
    def test_create_polarion_container_success(self, mock_docker_container_class: Mock, mock_prepare: Mock, mock_setup: Mock, mock_sleep: Mock) -> None:
        """Test create_polarion_container creates and starts container."""
        # Arrange
        params = PolarionContainerParameters(polarion_image_name="polarion:latest", weasyprint_service_image_name="", extension_version="1.0.0", additional_bundles=None, admin_utility_version="2.0.0")

        mock_container = Mock()
        mock_wrapped = Mock()
        mock_wrapped.short_id = "pol123"
        mock_container.get_wrapped_container.return_value = mock_wrapped
        mock_container.get_exposed_port.return_value = "8080"
        mock_container.with_bind_ports.return_value = mock_container
        mock_container.with_name.return_value = mock_container
        mock_container.with_volume_mapping.return_value = mock_container
        mock_container.with_env.return_value = mock_container
        mock_docker_container_class.return_value = mock_container

        mock_setup.return_value = "test-token-abc"

        helper = TestContainersHelper()
        helper.systest_extensions_root = "/tmp/systest"

        # Act
        app_url: str
        token: str
        app_url, token = helper.create_polarion_container("pdf-exporter", params, None)

        # Assert
        self.assertEqual(app_url, "http://localhost:8080")
        self.assertEqual(token, "test-token-abc")
        mock_prepare.assert_called_once_with("pdf-exporter", params)
        mock_container.start.assert_called_once()
        mock_setup.assert_called_once_with("http://localhost:8080")
        self.assertEqual(helper.polarion_container, mock_container)

    @patch("python_sbb_polarion.testing.testcontainers_helper.time.sleep")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.setup_polarion_container")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.prepare_systest_extensions")
    @patch("python_sbb_polarion.testing.testcontainers_helper.DockerContainer")
    def test_create_polarion_container_with_weasyprint(self, mock_docker_container_class: Mock, mock_prepare: Mock, mock_setup: Mock, mock_sleep: Mock) -> None:
        """Test create_polarion_container with weasyprint endpoint."""
        # Arrange
        params = PolarionContainerParameters(polarion_image_name="polarion:latest", weasyprint_service_image_name="weasyprint:latest", extension_version="1.0.0", additional_bundles=None, admin_utility_version="2.0.0")

        mock_container = Mock()
        mock_wrapped = Mock()
        mock_wrapped.short_id = "pol123"
        mock_container.get_wrapped_container.return_value = mock_wrapped
        mock_container.get_exposed_port.return_value = "8080"
        mock_container.with_bind_ports.return_value = mock_container
        mock_container.with_name.return_value = mock_container
        mock_container.with_volume_mapping.return_value = mock_container
        mock_container.with_env.return_value = mock_container
        mock_docker_container_class.return_value = mock_container

        mock_setup.return_value = "test-token"

        helper = TestContainersHelper()
        helper.systest_extensions_root = "/tmp/systest"

        # Act
        helper.create_polarion_container("pdf-exporter", params, "http://weasyprint:9080")

        # Assert
        mock_container.with_env.assert_called_once_with("WEASYPRINT_SERVICE_ENDPOINT", "http://weasyprint:9080")

    @patch("python_sbb_polarion.testing.testcontainers_helper.time.sleep")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.setup_polarion_container")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.prepare_systest_extensions")
    @patch("python_sbb_polarion.testing.testcontainers_helper.DockerContainer")
    def test_create_polarion_container_with_network(self, mock_docker_container_class: Mock, mock_prepare: Mock, mock_setup: Mock, mock_sleep: Mock) -> None:
        """Test create_polarion_container connects to network when network is set."""
        # Arrange
        params = PolarionContainerParameters(polarion_image_name="polarion:latest", weasyprint_service_image_name="", extension_version="1.0.0", additional_bundles=None, admin_utility_version="2.0.0")

        mock_container = Mock()
        mock_wrapped = Mock()
        mock_wrapped.short_id = "pol456"
        mock_container.get_wrapped_container.return_value = mock_wrapped
        mock_container.get_exposed_port.return_value = "8080"
        mock_container.with_bind_ports.return_value = mock_container
        mock_container.with_name.return_value = mock_container
        mock_container.with_volume_mapping.return_value = mock_container
        mock_container.with_env.return_value = mock_container
        mock_docker_container_class.return_value = mock_container

        mock_setup.return_value = "test-token-net"

        mock_network = Mock()

        helper = TestContainersHelper()
        helper.systest_extensions_root = "/tmp/systest"
        helper.network = mock_network

        # Act
        app_url: str
        token: str
        app_url, token = helper.create_polarion_container("pdf-exporter", params, None)

        # Assert
        self.assertEqual(app_url, "http://localhost:8080")
        self.assertEqual(token, "test-token-net")
        mock_container.start.assert_called_once()
        mock_network.connect.assert_called_once_with("pol456")

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.tear_down")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.prepare_systest_extensions")
    @patch("python_sbb_polarion.testing.testcontainers_helper.DockerContainer")
    def test_create_polarion_container_error(self, mock_docker_container_class: Mock, mock_prepare: Mock, mock_tear_down: Mock) -> None:
        """Test create_polarion_container raises ContainerSetupError on failure."""
        # Arrange
        params = PolarionContainerParameters(polarion_image_name="polarion:latest", weasyprint_service_image_name="", extension_version="1.0.0", additional_bundles=None, admin_utility_version="2.0.0")

        mock_container = Mock()
        mock_container.with_bind_ports.return_value = mock_container
        mock_container.with_name.return_value = mock_container
        mock_container.with_volume_mapping.return_value = mock_container
        mock_container.start.side_effect = Exception("Docker error")
        mock_docker_container_class.return_value = mock_container

        helper = TestContainersHelper()
        helper.systest_extensions_root = "/tmp/systest"

        # Act & Assert
        with self.assertRaises(ContainerSetupError) as context:
            helper.create_polarion_container("pdf-exporter", params, None)

        self.assertIn("Cannot setup Polarion container", str(context.exception))
        mock_tear_down.assert_called_once()


class TestTestContainersHelperSetupPolarionContainer(unittest.TestCase):
    """Test TestContainersHelper.setup_polarion_container method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.issue_security_token")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.wait_for_start_and_activate")
    @patch("python_sbb_polarion.testing.testcontainers_helper.ExtensionApiFactory.get_extension_api_by_name")
    @patch("python_sbb_polarion.testing.testcontainers_helper.PolarionRestApiConnection")
    def test_setup_polarion_container_success(self, mock_connection_class: Mock, mock_factory: Mock, mock_wait: Mock, mock_issue_token: Mock) -> None:
        """Test setup_polarion_container returns security token."""
        # Arrange
        mock_connection = Mock()
        mock_connection_class.return_value = mock_connection

        mock_admin_api = Mock(spec=PolarionAdminUtilityApi)
        mock_factory.return_value = mock_admin_api

        mock_issue_token.return_value = "security-token-123"

        # Act
        result: str = TestContainersHelper.setup_polarion_container("http://localhost:8080")

        # Assert
        self.assertEqual(result, "security-token-123")
        mock_connection_class.assert_called_once_with(url="http://localhost:8080", username="admin", password="admin")
        mock_factory.assert_called_once_with(extension_name="admin-utility", polarion_connection=mock_connection)
        mock_wait.assert_called_once_with(mock_admin_api)
        mock_issue_token.assert_called_once_with(mock_admin_api)


class TestTestContainersHelperWaitForStartAndActivate(unittest.TestCase):
    """Test TestContainersHelper.wait_for_start_and_activate method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.time.sleep")
    @patch("python_sbb_polarion.testing.testcontainers_helper.time.time")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.check_default_activation_response")
    def test_wait_for_start_and_activate_success(self, mock_check: Mock, mock_time: Mock, mock_sleep: Mock) -> None:
        """Test wait_for_start_and_activate succeeds on first try."""
        # Arrange
        mock_time.side_effect = [0, 1]  # Start time, then 1 second later

        mock_admin_api = Mock()
        mock_connection = Mock()
        mock_admin_api.polarion_connection = mock_connection

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_admin_api.activate_trial_license.return_value = mock_response

        # Act
        TestContainersHelper.wait_for_start_and_activate(mock_admin_api)

        # Assert
        mock_check.assert_called_once_with(mock_response)
        mock_connection.set_print_error.assert_any_call(False)
        mock_connection.set_print_error.assert_any_call(True)

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.check_default_activation_response")
    @patch("python_sbb_polarion.testing.testcontainers_helper.time.sleep")
    @patch("python_sbb_polarion.testing.testcontainers_helper.time.time")
    def test_wait_for_start_and_activate_retries_on_503(self, mock_time: Mock, mock_sleep: Mock, mock_check: Mock) -> None:
        """Test wait_for_start_and_activate retries on 503."""
        # Arrange
        mock_time.side_effect = [0, 1, 2, 3]  # Simulating time progression

        mock_admin_api = Mock()
        mock_connection = Mock()
        mock_admin_api.polarion_connection = mock_connection

        mock_response_503 = Mock()
        mock_response_503.status_code = HTTPStatus.SERVICE_UNAVAILABLE

        mock_response_200 = Mock()
        mock_response_200.status_code = HTTPStatus.OK

        mock_admin_api.activate_trial_license.side_effect = [mock_response_503, mock_response_503, mock_response_200]

        # Act
        TestContainersHelper.wait_for_start_and_activate(mock_admin_api)

        # Assert
        self.assertEqual(mock_admin_api.activate_trial_license.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        mock_check.assert_called_once_with(mock_response_200)

    @patch("python_sbb_polarion.testing.testcontainers_helper.time.sleep")
    @patch("python_sbb_polarion.testing.testcontainers_helper.time.time")
    def test_wait_for_start_and_activate_raises_on_error_status(self, mock_time: Mock, mock_sleep: Mock) -> None:
        """Test wait_for_start_and_activate raises PolarionStartupError on non-200/503 status."""
        # Arrange
        mock_time.side_effect = [0, 1]

        mock_admin_api = Mock()
        mock_connection = Mock()
        mock_admin_api.polarion_connection = mock_connection

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_response.content = b"Internal server error"
        mock_admin_api.activate_trial_license.return_value = mock_response

        # Act & Assert
        with self.assertRaises(PolarionStartupError) as context:
            TestContainersHelper.wait_for_start_and_activate(mock_admin_api)

        self.assertIn("Polarion license activation failure", str(context.exception))
        self.assertIn("status = 500", str(context.exception))
        mock_connection.set_print_error.assert_any_call(True)  # Should be called in finally block

    @patch("python_sbb_polarion.testing.testcontainers_helper.time.sleep")
    @patch("python_sbb_polarion.testing.testcontainers_helper.time.time")
    def test_wait_for_start_and_activate_timeout(self, mock_time: Mock, mock_sleep: Mock) -> None:
        """Test wait_for_start_and_activate raises PolarionStartupError on timeout."""
        # Arrange - need multiple time values for while loop condition checking
        mock_time.side_effect = [0, 1, 2, 601]  # Final check shows timeout

        mock_admin_api = Mock()
        mock_connection = Mock()
        mock_admin_api.polarion_connection = mock_connection

        mock_response = Mock()
        mock_response.status_code = HTTPStatus.SERVICE_UNAVAILABLE
        mock_admin_api.activate_trial_license.return_value = mock_response

        # Act & Assert
        with self.assertRaises(PolarionStartupError) as context:
            TestContainersHelper.wait_for_start_and_activate(mock_admin_api)

        self.assertIn("Polarion start timeout", str(context.exception))
        mock_connection.set_print_error.assert_any_call(True)


class TestTestContainersHelperCreateHostExtensionsPath(unittest.TestCase):
    """Test TestContainersHelper.create_host_extensions_path method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.pathlib.Path")
    @patch("python_sbb_polarion.testing.testcontainers_helper.shutil.rmtree")
    @patch("python_sbb_polarion.testing.testcontainers_helper.tempfile.gettempdir")
    def test_create_host_extensions_path_creates_new_path(self, mock_gettempdir: Mock, mock_rmtree: Mock, mock_path_class: Mock) -> None:
        """Test create_host_extensions_path creates new directory."""
        # Arrange
        mock_gettempdir.return_value = "/tmp"
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = False
        mock_path_class.return_value = mock_path_instance

        helper = TestContainersHelper()

        # Act
        result: str = helper.create_host_extensions_path()

        # Assert
        self.assertEqual(result, "/tmp/systest/sbb-extensions/eclipse/plugins")
        self.assertEqual(helper.systest_extensions_root, "/tmp/systest")
        mock_rmtree.assert_not_called()
        mock_path_instance.mkdir.assert_called_once_with(parents=True)

    @patch("python_sbb_polarion.testing.testcontainers_helper.pathlib.Path")
    @patch("python_sbb_polarion.testing.testcontainers_helper.shutil.rmtree")
    @patch("python_sbb_polarion.testing.testcontainers_helper.tempfile.gettempdir")
    def test_create_host_extensions_path_removes_existing(self, mock_gettempdir: Mock, mock_rmtree: Mock, mock_path_class: Mock) -> None:
        """Test create_host_extensions_path removes existing directory first."""
        # Arrange
        mock_gettempdir.return_value = "/tmp"
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path_class.return_value = mock_path_instance

        helper = TestContainersHelper()

        # Act
        result: str = helper.create_host_extensions_path()

        # Assert
        self.assertEqual(result, "/tmp/systest/sbb-extensions/eclipse/plugins")
        mock_rmtree.assert_called_once_with("/tmp/systest/sbb-extensions/eclipse/plugins")
        mock_path_instance.mkdir.assert_called_once_with(parents=True)


class TestTestContainersHelperIssueSecurityToken(unittest.TestCase):
    """Test TestContainersHelper.issue_security_token method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.timedelta")
    @patch("python_sbb_polarion.testing.testcontainers_helper.datetime")
    def test_issue_security_token_success(self, mock_datetime_class: Mock, mock_timedelta_class: Mock) -> None:
        """Test issue_security_token creates security token."""
        # Arrange
        from datetime import timedelta as real_timedelta

        mock_now = Mock()
        mock_future = Mock()
        mock_future.strftime.return_value = "2024-01-01T12:05:00Z"
        mock_now.__add__ = Mock(return_value=mock_future)
        mock_datetime_class.now.return_value = mock_now
        mock_timedelta_class.return_value = real_timedelta(minutes=5)

        mock_admin_api = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"token": "test-token-123"}
        mock_admin_api.create_token.return_value = mock_response

        # Act
        result: str = TestContainersHelper.issue_security_token(mock_admin_api)

        # Assert
        self.assertEqual(result, "test-token-123")
        mock_admin_api.create_token.assert_called_once()


class TestTestContainersHelperCreateNetwork(unittest.TestCase):
    """Test TestContainersHelper.create_network method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.docker.from_env")
    def test_create_network_success(self, mock_docker: Mock) -> None:
        """Test create_network creates Docker network."""
        # Arrange
        mock_client = Mock()
        mock_network = Mock()
        mock_client.networks.create.return_value = mock_network
        mock_docker.return_value = mock_client

        helper = TestContainersHelper()

        # Act
        helper.create_network("test-network")

        # Assert
        self.assertEqual(helper.network, mock_network)
        mock_client.networks.create.assert_called_once_with("test-network", driver="bridge")


class TestTestContainersHelperTearDown(unittest.TestCase):
    """Test TestContainersHelper.tear_down method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.shutil.rmtree")
    @patch("python_sbb_polarion.testing.testcontainers_helper.pathlib.Path")
    def test_tear_down_cleans_all_resources(self, mock_path_class: Mock, mock_rmtree: Mock) -> None:
        """Test tear_down stops containers and removes resources."""
        # Arrange
        helper = TestContainersHelper()

        mock_weasyprint_container = Mock()
        mock_weasyprint_wrapped = Mock()
        mock_weasyprint_container.get_wrapped_container.return_value = mock_weasyprint_wrapped
        helper.weasyprint_service_container = mock_weasyprint_container

        mock_polarion_container = Mock()
        mock_polarion_wrapped = Mock()
        mock_polarion_container.get_wrapped_container.return_value = mock_polarion_wrapped
        helper.polarion_container = mock_polarion_container

        mock_network = Mock()
        helper.network = mock_network

        helper.systest_extensions_root = "/tmp/systest"
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path_class.return_value = mock_path_instance

        # Act
        helper.tear_down()

        # Assert
        mock_weasyprint_container.stop.assert_called_once()
        mock_polarion_container.stop.assert_called_once()
        mock_rmtree.assert_called_once_with("/tmp/systest")
        mock_network.remove.assert_called_once()

    def test_tear_down_handles_none_containers(self) -> None:
        """Test tear_down handles None containers gracefully."""
        # Arrange
        helper = TestContainersHelper()
        helper.weasyprint_service_container = None
        helper.polarion_container = None
        helper.network = None
        helper.systest_extensions_root = None

        # Act - should not raise
        helper.tear_down()

        # Assert - no exception raised


class TestTestContainersHelperPrepareSystemTestExtensions(unittest.TestCase):
    """Test TestContainersHelper.prepare_systest_extensions method."""

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.copy_dependency")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.create_host_extensions_path")
    def test_prepare_systest_extensions_without_additional_bundles(self, mock_create_path: Mock, mock_copy: Mock) -> None:
        """Test prepare_systest_extensions copies required extensions."""
        # Arrange
        mock_create_path.return_value = "/tmp/systest/plugins"

        params = PolarionContainerParameters(
            polarion_image_name="polarion:latest",
            weasyprint_service_image_name="",
            extension_version="1.0.0",
            additional_bundles=None,
            admin_utility_version="2.0.0",
        )

        helper = TestContainersHelper()

        # Act
        helper.prepare_systest_extensions("pdf-exporter", params)

        # Assert
        self.assertEqual(mock_copy.call_count, 2)
        mock_copy.assert_any_call("/tmp/systest/plugins", "ch.sbb.polarion.extensions", "ch.sbb.polarion.extension.pdf-exporter", "1.0.0")
        mock_copy.assert_any_call("/tmp/systest/plugins", "ch.sbb.polarion.extensions", "ch.sbb.polarion.extension.admin-utility", "2.0.0")

    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.copy_dependency")
    @patch("python_sbb_polarion.testing.testcontainers_helper.TestContainersHelper.create_host_extensions_path")
    def test_prepare_systest_extensions_with_additional_bundles(self, mock_create_path: Mock, mock_copy: Mock) -> None:
        """Test prepare_systest_extensions includes additional bundles."""
        # Arrange
        mock_create_path.return_value = "/tmp/systest/plugins"

        additional: list[ArtifactInfo] = [ArtifactInfo("com.example", "extra-bundle", "3.0.0")]
        params: PolarionContainerParameters = PolarionContainerParameters(
            polarion_image_name="polarion:latest",
            weasyprint_service_image_name="",
            extension_version="1.0.0",
            additional_bundles=additional,
            admin_utility_version="2.0.0",
        )

        helper = TestContainersHelper()

        # Act
        helper.prepare_systest_extensions("pdf-exporter", params)

        # Assert
        self.assertEqual(mock_copy.call_count, 3)
        mock_copy.assert_any_call("/tmp/systest/plugins", "com.example", "extra-bundle", "3.0.0")


if __name__ == "__main__":
    unittest.main()
