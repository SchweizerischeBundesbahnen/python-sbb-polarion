"""Unit tests for REST API endpoint annotations."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING, cast

from python_sbb_polarion.core.annotations import RestApiEndpoint, restapi_endpoint


if TYPE_CHECKING:
    from python_sbb_polarion.types import JsonDict


class TestRestApiEndpoint(unittest.TestCase):
    """Test RestApiEndpoint dataclass."""

    def test_minimal_initialization(self) -> None:
        """Test dataclass with only required fields."""
        endpoint = RestApiEndpoint(method="GET", path="/api/test")

        self.assertEqual(endpoint.method, "GET")
        self.assertEqual(endpoint.path, "/api/test")
        self.assertEqual(endpoint.path_params, {})
        self.assertEqual(endpoint.query_params, {})
        self.assertIsNone(endpoint.body_param)
        self.assertEqual(endpoint.multipart_fields, {})
        self.assertEqual(endpoint.header_params, {})
        self.assertEqual(endpoint.helper_params, [])
        self.assertEqual(endpoint.required_params, [])
        self.assertIsNone(endpoint.response_type)
        self.assertFalse(endpoint.deprecated)

    def test_full_initialization(self) -> None:
        """Test dataclass with all fields specified."""
        endpoint = RestApiEndpoint(
            method="POST",
            path="/api/projects/{projectId}/items",
            path_params={"projectId": "project_id"},
            query_params={"limit": "limit", "offset": "offset"},
            body_param="data",
            multipart_fields={"file": "file_content"},
            header_params={"X-Revision": "revision"},
            helper_params=["file_path"],
            required_params=["projectId"],
            response_type="json",
            deprecated=True,
        )

        self.assertEqual(endpoint.method, "POST")
        self.assertEqual(endpoint.path, "/api/projects/{projectId}/items")
        self.assertEqual(endpoint.path_params, {"projectId": "project_id"})
        self.assertEqual(endpoint.query_params, {"limit": "limit", "offset": "offset"})
        self.assertEqual(endpoint.body_param, "data")
        self.assertEqual(endpoint.multipart_fields, {"file": "file_content"})
        self.assertEqual(endpoint.header_params, {"X-Revision": "revision"})
        self.assertEqual(endpoint.helper_params, ["file_path"])
        self.assertEqual(endpoint.required_params, ["projectId"])
        self.assertEqual(endpoint.response_type, "json")
        self.assertTrue(endpoint.deprecated)


class TestRestApiEndpointDecorator(unittest.TestCase):
    """Test restapi_endpoint decorator."""

    def _get_metadata(self, func: object) -> RestApiEndpoint:
        """Get RestApiEndpoint metadata from decorated function."""
        return cast("RestApiEndpoint", getattr(func, "__restapi_endpoint__"))  # noqa: B009

    def test_minimal_decorator(self) -> None:
        """Test decorator with only required parameters."""

        @restapi_endpoint(method="GET", path="/api/test")
        def get_test() -> None:
            return None

        self.assertTrue(hasattr(get_test, "__restapi_endpoint__"))
        metadata: RestApiEndpoint = self._get_metadata(get_test)
        self.assertEqual(metadata.method, "GET")
        self.assertEqual(metadata.path, "/api/test")
        self.assertEqual(metadata.path_params, {})
        self.assertEqual(metadata.query_params, {})

    def test_method_uppercasing(self) -> None:
        """Test that HTTP method is uppercased."""

        @restapi_endpoint(method="post", path="/api/test")
        def create_test() -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(create_test)
        self.assertEqual(metadata.method, "POST")

    def test_with_path_params(self) -> None:
        """Test decorator with path parameters."""

        @restapi_endpoint(
            method="GET",
            path="/api/projects/{projectId}/items/{itemId}",
            path_params={"projectId": "project_id", "itemId": "item_id"},
        )
        def get_item(project_id: str, item_id: str) -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(get_item)
        self.assertEqual(metadata.path_params, {"projectId": "project_id", "itemId": "item_id"})

    def test_with_query_params(self) -> None:
        """Test decorator with query parameters."""

        @restapi_endpoint(
            method="GET",
            path="/api/items",
            query_params={"maxResults": "max_results", "offset": "offset"},
        )
        def list_items(max_results: int | None = None, offset: int | None = None) -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(list_items)
        self.assertEqual(metadata.query_params, {"maxResults": "max_results", "offset": "offset"})

    def test_with_body_param(self) -> None:
        """Test decorator with body parameter."""

        @restapi_endpoint(method="POST", path="/api/items", body_param="item_data")
        def create_item(item_data: JsonDict) -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(create_item)
        self.assertEqual(metadata.body_param, "item_data")

    def test_with_multipart_fields(self) -> None:
        """Test decorator with multipart fields for file upload."""

        @restapi_endpoint(
            method="POST",
            path="/api/upload",
            multipart_fields={"file": "file_content", "metadata": "meta"},
        )
        def upload_file(file_content: bytes, meta: JsonDict) -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(upload_file)
        self.assertEqual(metadata.multipart_fields, {"file": "file_content", "metadata": "meta"})

    def test_with_header_params(self) -> None:
        """Test decorator with header parameters."""

        @restapi_endpoint(
            method="GET",
            path="/api/data",
            header_params={"X-Revision": "revision", "X-Scope": "scope"},
        )
        def get_data(revision: str | None = None, scope: str | None = None) -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(get_data)
        self.assertEqual(metadata.header_params, {"X-Revision": "revision", "X-Scope": "scope"})

    def test_with_helper_params(self) -> None:
        """Test decorator with helper parameters not from OpenAPI spec."""

        @restapi_endpoint(
            method="POST",
            path="/api/export",
            helper_params=["file_path", "overwrite"],
        )
        def export_data(file_path: str, overwrite: bool = False) -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(export_data)
        self.assertEqual(metadata.helper_params, ["file_path", "overwrite"])

    def test_with_required_params(self) -> None:
        """Test decorator with required parameters list."""

        @restapi_endpoint(
            method="POST",
            path="/api/projects/{projectId}/documents/{documentName}",
            path_params={"projectId": "project_id", "documentName": "document_name"},
            required_params=["projectId", "documentName"],
        )
        def create_document(project_id: str, document_name: str) -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(create_document)
        self.assertEqual(metadata.required_params, ["projectId", "documentName"])

    def test_with_response_type(self) -> None:
        """Test decorator with response type hint."""

        @restapi_endpoint(method="GET", path="/api/file", response_type="binary")
        def get_file() -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(get_file)
        self.assertEqual(metadata.response_type, "binary")

    def test_with_deprecated(self) -> None:
        """Test decorator with deprecated flag."""

        @restapi_endpoint(method="GET", path="/api/old", deprecated=True)
        def get_old() -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(get_old)
        self.assertTrue(metadata.deprecated)

    def test_full_decorator(self) -> None:
        """Test decorator with all parameters specified."""

        @restapi_endpoint(
            method="post",
            path="/api/projects/{projectId}/templates/{templateId}",
            path_params={"projectId": "project_id", "templateId": "template_id"},
            query_params={"force": "force_update"},
            body_param="template_data",
            multipart_fields={"attachment": "file_content"},
            header_params={"X-Request-Id": "request_id"},
            helper_params=["local_file_path"],
            required_params=["projectId", "templateId"],
            response_type="json",
            deprecated=True,
        )
        def upload_template(
            project_id: str,
            template_id: str,
            template_data: JsonDict,
            file_content: bytes,
            request_id: str | None = None,
            force_update: bool = False,
            local_file_path: str | None = None,
        ) -> None:
            return None

        metadata: RestApiEndpoint = self._get_metadata(upload_template)
        self.assertEqual(metadata.method, "POST")
        self.assertEqual(metadata.path, "/api/projects/{projectId}/templates/{templateId}")
        self.assertEqual(metadata.path_params, {"projectId": "project_id", "templateId": "template_id"})
        self.assertEqual(metadata.query_params, {"force": "force_update"})
        self.assertEqual(metadata.body_param, "template_data")
        self.assertEqual(metadata.multipart_fields, {"attachment": "file_content"})
        self.assertEqual(metadata.header_params, {"X-Request-Id": "request_id"})
        self.assertEqual(metadata.helper_params, ["local_file_path"])
        self.assertEqual(metadata.required_params, ["projectId", "templateId"])
        self.assertEqual(metadata.response_type, "json")
        self.assertTrue(metadata.deprecated)

    def test_function_preserved(self) -> None:
        """Test that the decorated function is preserved and callable."""

        @restapi_endpoint(method="GET", path="/api/test")
        def sample_function(value: int) -> int:
            return value * 2

        # Function should still be callable
        result: int = sample_function(5)
        self.assertEqual(result, 10)

        # Function should have metadata attached
        self.assertTrue(hasattr(sample_function, "__restapi_endpoint__"))


if __name__ == "__main__":
    unittest.main()
