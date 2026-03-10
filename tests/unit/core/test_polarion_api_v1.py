"""Unit tests for PolarionApiV1 - complete coverage of all 212 methods."""

from __future__ import annotations

import unittest
from typing import TYPE_CHECKING
from unittest.mock import MagicMock


if TYPE_CHECKING:
    from python_sbb_polarion.types import JsonDict


class TestPolarionApiV1Init(unittest.TestCase):
    """Test PolarionApiV1 initialization."""

    def test_init_sets_connection(self) -> None:
        """Test that __init__ sets polarion_connection."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        mock_connection: MagicMock = MagicMock()
        api: PolarionApiV1 = PolarionApiV1(mock_connection)
        self.assertEqual(api.polarion_connection, mock_connection)

    def test_init_sets_base_url(self) -> None:
        """Test that __init__ sets base_url."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        mock_connection: MagicMock = MagicMock()
        api: PolarionApiV1 = PolarionApiV1(mock_connection)
        self.assertEqual(api.base_url, "/polarion/rest/v1")


# =============================================================================
# Workitems CRUD Tests (11 methods)
# =============================================================================


class TestWorkitemsCrud(unittest.TestCase):
    """Test workitems CRUD operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_workitems(self) -> None:
        """Test get_workitems method."""
        self.api.get_workitems("project1")
        self.mock_connection.api_request_get.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems", call_args[0][0])

    def test_get_workitems_with_pagination(self) -> None:
        """Test get_workitems with pagination parameters."""
        self.api.get_workitems("project1", page_size=50, page_number=2)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "2")

    def test_get_workitem(self) -> None:
        """Test get_workitem method."""
        self.api.get_workitem("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123", call_args[0][0])

    def test_get_workitem_with_fields(self) -> None:
        """Test get_workitem with fields parameter."""
        self.api.get_workitem("project1", "WI-123", fields={"workitems": "id,title"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,title")

    def test_create_workitems(self) -> None:
        """Test create_workitems method."""
        data: JsonDict = {
            "data": [{"type": "workitems"}],
        }
        self.api.create_workitems("project1", data)
        self.mock_connection.api_request_post.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems", call_args[0][0])

    def test_update_workitem(self) -> None:
        """Test update_workitem method."""
        attributes: JsonDict = {
            "title": "Updated Title",
        }
        self.api.update_workitem("project1", "WI-123", attributes)
        self.mock_connection.api_request_patch.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123", call_args[0][0])
        # Verify attributes are wrapped in JSON:API format
        sent_data: JsonDict = call_args[1]["data"]  # type: ignore[assignment]
        self.assertEqual(sent_data["data"]["type"], "workitems")  # type: ignore[index,call-overload]
        self.assertEqual(sent_data["data"]["id"], "project1/WI-123")  # type: ignore[index,call-overload]
        self.assertEqual(sent_data["data"]["attributes"], attributes)  # type: ignore[index,call-overload]

    def test_update_workitems(self) -> None:
        """Test update_workitems method."""
        data: JsonDict = {
            "data": [{"type": "workitems"}],
        }
        self.api.update_workitems("project1", data)
        self.mock_connection.api_request_patch.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems", call_args[0][0])

    def test_delete_workitems(self) -> None:
        """Test delete_workitems method."""
        data: JsonDict = {
            "data": [{"type": "workitems", "id": "WI-123"}],
        }
        self.api.delete_workitems("project1", data)
        self.mock_connection.api_request_delete.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems", call_args[0][0])

    def test_get_all_workitems(self) -> None:
        """Test get_all_workitems method."""
        self.api.get_all_workitems()
        self.mock_connection.api_request_get.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/workitems", call_args[0][0])

    def test_update_all_workitems(self) -> None:
        """Test update_all_workitems method."""
        data: JsonDict = {
            "data": [{"type": "workitems"}],
        }
        self.api.update_all_workitems(data)
        self.mock_connection.api_request_patch.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/workitems", call_args[0][0])

    def test_delete_all_workitems(self) -> None:
        """Test delete_all_workitems method."""
        data: JsonDict = {
            "data": [{"type": "workitems"}],
        }
        self.api.delete_all_workitems(data)
        self.mock_connection.api_request_delete.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/workitems", call_args[0][0])

    def test_move_workitem_to_document(self) -> None:
        """Test move_workitem_to_document method."""
        data: JsonDict = {
            "data": {"type": "documents"},
        }
        self.api.move_workitem_to_document("project1", "WI-123", data)
        self.mock_connection.api_request_post.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/actions/moveToDocument", call_args[0][0])

    def test_move_workitem_from_document(self) -> None:
        """Test move_workitem_from_document method."""
        data: JsonDict = {
            "targetSpace": "space1",
        }
        self.api.move_workitem_from_document("project1", "WI-123", data)
        self.mock_connection.api_request_post.assert_called_once()
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/actions/moveFromDocument", call_args[0][0])


# =============================================================================
# Workitems Attachments Tests (6 methods)
# =============================================================================


class TestWorkitemsAttachments(unittest.TestCase):
    """Test workitems attachments operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_workitem_attachments(self) -> None:
        """Test get_workitem_attachments method."""
        self.api.get_workitem_attachments("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/attachments", call_args[0][0])

    def test_get_workitem_attachment(self) -> None:
        """Test get_workitem_attachment method."""
        self.api.get_workitem_attachment("project1", "WI-123", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/attachments/att-1", call_args[0][0])

    def test_get_workitem_attachment_content(self) -> None:
        """Test get_workitem_attachment_content method."""
        self.api.get_workitem_attachment_content("project1", "WI-123", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/attachments/att-1/content", call_args[0][0])

    def test_create_workitem_attachments(self) -> None:
        """Test create_workitem_attachments method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("test.txt", b"content"),
        }
        self.api.create_workitem_attachments("project1", "WI-123", files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/attachments", call_args[0][0])

    def test_update_workitem_attachment(self) -> None:
        """Test update_workitem_attachment method."""
        data: JsonDict = {
            "data": {"type": "workitem_attachments"},
        }
        self.api.update_workitem_attachment("project1", "WI-123", "att-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123/attachments/att-1", call_args[0][0])

    def test_delete_workitem_attachment(self) -> None:
        """Test delete_workitem_attachment method."""
        self.api.delete_workitem_attachment("project1", "WI-123", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/attachments/att-1", call_args[0][0])


# =============================================================================
# Workitems Comments Tests (4 methods)
# =============================================================================


class TestWorkitemsComments(unittest.TestCase):
    """Test workitems comments operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_workitem_comments(self) -> None:
        """Test get_workitem_comments method."""
        self.api.get_workitem_comments("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/comments", call_args[0][0])

    def test_get_workitem_comment(self) -> None:
        """Test get_workitem_comment method."""
        self.api.get_workitem_comment("project1", "WI-123", "comment-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/comments/comment-1", call_args[0][0])

    def test_create_workitem_comments(self) -> None:
        """Test create_workitem_comments method."""
        data: JsonDict = {
            "data": [{"type": "workitem_comments"}],
        }
        self.api.create_workitem_comments("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/comments", call_args[0][0])

    def test_update_workitem_comment(self) -> None:
        """Test update_workitem_comment method."""
        data: JsonDict = {
            "data": {"type": "workitem_comments"},
        }
        self.api.update_workitem_comment("project1", "WI-123", "comment-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123/comments/comment-1", call_args[0][0])


# =============================================================================
# Workitems Links Tests (14 methods)
# =============================================================================


class TestWorkitemsLinks(unittest.TestCase):
    """Test workitems links operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_linked_workitems(self) -> None:
        """Test get_linked_workitems method."""
        self.api.get_linked_workitems("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedworkitems", call_args[0][0])

    def test_get_linked_workitem(self) -> None:
        """Test get_linked_workitem method."""
        self.api.get_linked_workitem("project1", "WI-123", "role1", "project2", "WI-456")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedworkitems/role1/project2/WI-456", call_args[0][0])

    def test_create_linked_workitems(self) -> None:
        """Test create_linked_workitems method."""
        data: JsonDict = {
            "data": [{"type": "linkedworkitems"}],
        }
        self.api.create_linked_workitems("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedworkitems", call_args[0][0])

    def test_update_linked_workitem(self) -> None:
        """Test update_linked_workitem method."""
        data: JsonDict = {
            "data": {"type": "linkedworkitems"},
        }
        self.api.update_linked_workitem("project1", "WI-123", "role1", "project2", "WI-456", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedworkitems/role1/project2/WI-456", call_args[0][0])

    def test_delete_linked_workitems(self) -> None:
        """Test delete_linked_workitems method."""
        data: JsonDict = {
            "data": [{"type": "linkedworkitems"}],
        }
        self.api.delete_linked_workitems("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedworkitems", call_args[0][0])

    def test_delete_linked_workitem(self) -> None:
        """Test delete_linked_workitem method."""
        self.api.delete_linked_workitem("project1", "WI-123", "role1", "project2", "WI-456")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedworkitems/role1/project2/WI-456", call_args[0][0])

    def test_get_externally_linked_workitems(self) -> None:
        """Test get_externally_linked_workitems method."""
        self.api.get_externally_linked_workitems("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/externallylinkedworkitems", call_args[0][0])

    def test_get_externally_linked_workitem(self) -> None:
        """Test get_externally_linked_workitem method."""
        self.api.get_externally_linked_workitem("project1", "WI-123", "role1", "host.com", "project2", "WI-456")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/externallylinkedworkitems/role1/host.com/project2/WI-456", call_args[0][0])

    def test_create_externally_linked_workitems(self) -> None:
        """Test create_externally_linked_workitems method."""
        data: JsonDict = {
            "data": [{"type": "externallylinkedworkitems"}],
        }
        self.api.create_externally_linked_workitems("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/externallylinkedworkitems", call_args[0][0])

    def test_delete_externally_linked_workitems(self) -> None:
        """Test delete_externally_linked_workitems method."""
        data: JsonDict = {
            "data": [{"type": "externallylinkedworkitems"}],
        }
        self.api.delete_externally_linked_workitems("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/externallylinkedworkitems", call_args[0][0])

    def test_delete_externally_linked_workitem(self) -> None:
        """Test delete_externally_linked_workitem method."""
        self.api.delete_externally_linked_workitem("project1", "WI-123", "role1", "host.com", "project2", "WI-456")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/externallylinkedworkitems/role1/host.com/project2/WI-456", call_args[0][0])

    def test_get_oslc_resources(self) -> None:
        """Test get_oslc_resources method."""
        self.api.get_oslc_resources("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedoslcresources", call_args[0][0])

    def test_create_oslc_resources(self) -> None:
        """Test create_oslc_resources method."""
        data: JsonDict = {
            "data": [{"type": "linkedoslcresources"}],
        }
        self.api.create_oslc_resources("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedoslcresources", call_args[0][0])

    def test_delete_oslc_resources(self) -> None:
        """Test delete_oslc_resources method."""
        data: JsonDict = {
            "data": [{"type": "linkedoslcresources"}],
        }
        self.api.delete_oslc_resources("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/linkedoslcresources", call_args[0][0])


# =============================================================================
# Workitems Approvals Tests (7 methods)
# =============================================================================


class TestWorkitemsApprovals(unittest.TestCase):
    """Test workitems approvals operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_workitem_approvals(self) -> None:
        """Test get_workitem_approvals method."""
        self.api.get_workitem_approvals("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/approvals", call_args[0][0])

    def test_get_workitem_approval(self) -> None:
        """Test get_workitem_approval method."""
        self.api.get_workitem_approval("project1", "WI-123", "user1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/approvals/user1", call_args[0][0])

    def test_create_workitem_approvals(self) -> None:
        """Test create_workitem_approvals method."""
        data: JsonDict = {
            "data": [{"type": "workitem_approvals"}],
        }
        self.api.create_workitem_approvals("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/approvals", call_args[0][0])

    def test_update_workitem_approval(self) -> None:
        """Test update_workitem_approval method."""
        data: JsonDict = {
            "data": {"type": "workitem_approvals"},
        }
        self.api.update_workitem_approval("project1", "WI-123", "user1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123/approvals/user1", call_args[0][0])

    def test_update_workitem_approvals(self) -> None:
        """Test update_workitem_approvals method."""
        data: JsonDict = {
            "data": [{"type": "workitem_approvals"}],
        }
        self.api.update_workitem_approvals("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123/approvals", call_args[0][0])

    def test_delete_workitem_approval(self) -> None:
        """Test delete_workitem_approval method."""
        self.api.delete_workitem_approval("project1", "WI-123", "user1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/approvals/user1", call_args[0][0])

    def test_delete_workitem_approvals(self) -> None:
        """Test delete_workitem_approvals method."""
        data: JsonDict = {
            "data": [{"type": "workitem_approvals"}],
        }
        self.api.delete_workitem_approvals("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/approvals", call_args[0][0])


# =============================================================================
# Workitems Test Steps Tests (9 methods)
# =============================================================================


class TestWorkitemsTestSteps(unittest.TestCase):
    """Test workitems test steps operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_test_steps(self) -> None:
        """Test get_test_steps method."""
        self.api.get_test_steps("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/teststeps", call_args[0][0])

    def test_get_test_step(self) -> None:
        """Test get_test_step method."""
        self.api.get_test_step("project1", "WI-123", 1)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/teststeps/1", call_args[0][0])

    def test_create_test_steps(self) -> None:
        """Test create_test_steps method."""
        data: JsonDict = {
            "data": [{"type": "teststeps"}],
        }
        self.api.create_test_steps("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/teststeps", call_args[0][0])

    def test_update_test_step(self) -> None:
        """Test update_test_step method."""
        data: JsonDict = {
            "data": {"type": "teststeps"},
        }
        self.api.update_test_step("project1", "WI-123", 1, data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123/teststeps/1", call_args[0][0])

    def test_update_test_steps(self) -> None:
        """Test update_test_steps method."""
        data: JsonDict = {
            "data": [{"type": "teststeps"}],
        }
        self.api.update_test_steps("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123/teststeps", call_args[0][0])

    def test_delete_test_step(self) -> None:
        """Test delete_test_step method."""
        self.api.delete_test_step("project1", "WI-123", 1)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/teststeps/1", call_args[0][0])

    def test_delete_test_steps(self) -> None:
        """Test delete_test_steps method."""
        data: JsonDict = {
            "data": [{"type": "teststeps"}],
        }
        self.api.delete_test_steps("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/teststeps", call_args[0][0])

    def test_get_workitem_test_parameter_definitions(self) -> None:
        """Test get_workitem_test_parameter_definitions method."""
        self.api.get_workitem_test_parameter_definitions("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/testparameterdefinitions", call_args[0][0])

    def test_get_workitem_test_parameter_definition(self) -> None:
        """Test get_workitem_test_parameter_definition method."""
        self.api.get_workitem_test_parameter_definition("project1", "WI-123", "param-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/testparameterdefinitions/param-1", call_args[0][0])


# =============================================================================
# Workitems Work Records Tests (5 methods)
# =============================================================================


class TestWorkitemsWorkRecords(unittest.TestCase):
    """Test workitems work records operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_work_records(self) -> None:
        """Test get_work_records method."""
        self.api.get_work_records("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/workrecords", call_args[0][0])

    def test_get_work_record(self) -> None:
        """Test get_work_record method."""
        self.api.get_work_record("project1", "WI-123", "record-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/workrecords/record-1", call_args[0][0])

    def test_create_work_records(self) -> None:
        """Test create_work_records method."""
        data: JsonDict = {
            "data": [{"type": "workrecords"}],
        }
        self.api.create_work_records("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/workrecords", call_args[0][0])

    def test_delete_work_record(self) -> None:
        """Test delete_work_record method."""
        self.api.delete_work_record("project1", "WI-123", "record-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/workrecords/record-1", call_args[0][0])

    def test_delete_work_records(self) -> None:
        """Test delete_work_records method."""
        data: JsonDict = {
            "data": [{"type": "workrecords"}],
        }
        self.api.delete_work_records("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/workrecords", call_args[0][0])


# =============================================================================
# Workitems Relationships Tests (4 methods)
# =============================================================================


class TestWorkitemsRelationships(unittest.TestCase):
    """Test workitems relationships operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_workitem_relationships(self) -> None:
        """Test get_workitem_relationships method."""
        self.api.get_workitem_relationships("project1", "WI-123", "assignee")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/relationships/assignee", call_args[0][0])

    def test_create_workitem_relationships(self) -> None:
        """Test create_workitem_relationships method."""
        data: JsonDict = {
            "data": [{"type": "users"}],
        }
        self.api.create_workitem_relationships("project1", "WI-123", "assignee", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/relationships/assignee", call_args[0][0])

    def test_update_workitem_relationships(self) -> None:
        """Test update_workitem_relationships method."""
        data: JsonDict = {
            "data": [{"type": "users"}],
        }
        self.api.update_workitem_relationships("project1", "WI-123", "assignee", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/workitems/WI-123/relationships/assignee", call_args[0][0])

    def test_delete_workitem_relationships(self) -> None:
        """Test delete_workitem_relationships method."""
        data: JsonDict = {
            "data": [{"type": "users"}],
        }
        self.api.delete_workitem_relationships("project1", "WI-123", "assignee", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/workitems/WI-123/relationships/assignee", call_args[0][0])


# =============================================================================
# Workitems Enums Tests (3 methods)
# =============================================================================


class TestWorkitemsEnums(unittest.TestCase):
    """Test workitems enum operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_workitems_available_enum_options(self) -> None:
        """Test get_workitems_available_enum_options method."""
        self.api.get_workitems_available_enum_options("project1", "status")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/fields/status/actions/getAvailableOptions", call_args[0][0])

    def test_get_workitem_available_enum_options(self) -> None:
        """Test get_workitem_available_enum_options method."""
        self.api.get_workitem_available_enum_options("project1", "WI-123", "status")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/fields/status/actions/getAvailableOptions", call_args[0][0])

    def test_get_workitem_current_enum_options(self) -> None:
        """Test get_workitem_current_enum_options method."""
        self.api.get_workitem_current_enum_options("project1", "WI-123", "status")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/fields/status/actions/getCurrentOptions", call_args[0][0])

    def test_get_workitem_available_enum_options_with_params(self) -> None:
        """Test get_workitem_available_enum_options with optional parameters."""
        self.api.get_workitem_available_enum_options("project1", "WI-123", "status", page_size=50, page_number=2, revision="1234")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "2")
        self.assertEqual(params["revision"], "1234")

    def test_get_workitem_current_enum_options_with_params(self) -> None:
        """Test get_workitem_current_enum_options with optional parameters."""
        self.api.get_workitem_current_enum_options("project1", "WI-123", "status", page_size=25, page_number=1, revision="5678")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "25")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["revision"], "5678")

    def test_get_workitems_available_enum_options_with_params(self) -> None:
        """Test get_workitems_available_enum_options with optional parameters."""
        self.api.get_workitems_available_enum_options("project1", "status", page_size=100, page_number=3, type_filter="task")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "100")
        self.assertEqual(params["page[number]"], "3")
        self.assertEqual(params["type"], "task")

    def test_get_workitem_relationships_with_params(self) -> None:
        """Test get_workitem_relationships with optional parameters."""
        self.api.get_workitem_relationships("project1", "WI-123", "assignee", page_size=10, page_number=0, fields={"workitems": "id,name"}, include="user", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "user")
        self.assertEqual(params["revision"], "rev1")

    def test_get_workitem_feature_selections(self) -> None:
        """Test get_workitem_feature_selections method."""
        self.api.get_workitem_feature_selections("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/featureselections", call_args[0][0])

    def test_get_workitem_feature_selections_with_params(self) -> None:
        """Test get_workitem_feature_selections with optional parameters."""
        self.api.get_workitem_feature_selections("project1", "WI-123", page_size=20, page_number=1, fields={"featureselections": "id"}, include="target", revision="rev2")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[featureselections]"], "id")
        self.assertEqual(params["include"], "target")
        self.assertEqual(params["revision"], "rev2")

    def test_get_workitem_feature_selection(self) -> None:
        """Test get_workitem_feature_selection method."""
        self.api.get_workitem_feature_selection("project1", "WI-123", "type1", "project2", "WI-456")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/featureselections/type1/project2/WI-456", call_args[0][0])

    def test_get_workitem_feature_selection_with_params(self) -> None:
        """Test get_workitem_feature_selection with optional parameters."""
        self.api.get_workitem_feature_selection("project1", "WI-123", "type1", "project2", "WI-456", fields={"featureselections": "id,type"}, include="source", revision="rev3")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[featureselections]"], "id,type")
        self.assertEqual(params["include"], "source")
        self.assertEqual(params["revision"], "rev3")


# =============================================================================
# Workitems Workflow Actions Tests (1 method)
# =============================================================================


class TestWorkitemsWorkflowActions(unittest.TestCase):
    """Test workitems workflow actions operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_workflow_actions(self) -> None:
        """Test get_workflow_actions method."""
        self.api.get_workflow_actions("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/actions", call_args[0][0])


# =============================================================================
# Testruns CRUD Tests (7 methods)
# =============================================================================


class TestTestrunsCrud(unittest.TestCase):
    """Test testruns CRUD operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_testruns(self) -> None:
        """Test get_testruns method."""
        self.api.get_testruns("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns", call_args[0][0])

    def test_get_testrun(self) -> None:
        """Test get_testrun method."""
        self.api.get_testrun("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1", call_args[0][0])

    def test_create_testruns(self) -> None:
        """Test create_testruns method."""
        data: JsonDict = {
            "data": [{"type": "testruns"}],
        }
        self.api.create_testruns("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns", call_args[0][0])

    def test_update_testrun(self) -> None:
        """Test update_testrun method."""
        data: JsonDict = {
            "data": {"type": "testruns"},
        }
        self.api.update_testrun("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1", call_args[0][0])

    def test_update_testruns(self) -> None:
        """Test update_testruns method."""
        data: JsonDict = {
            "data": [{"type": "testruns"}],
        }
        self.api.update_testruns("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns", call_args[0][0])

    def test_delete_testruns(self) -> None:
        """Test delete_testruns method."""
        data: JsonDict = {
            "data": [{"type": "testruns"}],
        }
        self.api.delete_testruns("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns", call_args[0][0])

    def test_get_testrun_workflow_actions(self) -> None:
        """Test get_testrun_workflow_actions method."""
        self.api.get_testrun_workflow_actions("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/actions", call_args[0][0])

    def test_get_testruns_with_params(self) -> None:
        """Test get_testruns with optional parameters."""
        self.api.get_testruns("project1", page_size=50, page_number=2, fields={"testruns": "id,title"}, include="author", query="status:open", sort="created", revision="rev1", templates="true")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "2")
        self.assertEqual(params["fields[testruns]"], "id,title")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["query"], "status:open")
        self.assertEqual(params["sort"], "created")
        self.assertEqual(params["revision"], "rev1")
        self.assertEqual(params["templates"], "true")

    def test_get_testrun_with_params(self) -> None:
        """Test get_testrun with optional parameters."""
        self.api.get_testrun("project1", "TR-1", fields={"testruns": "id,status"}, include="records", revision="rev2")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[testruns]"], "id,status")
        self.assertEqual(params["include"], "records")
        self.assertEqual(params["revision"], "rev2")

    def test_update_testrun_with_workflow_action(self) -> None:
        """Test update_testrun with workflow_action parameter."""
        data: JsonDict = {
            "data": {"type": "testruns"},
        }
        self.api.update_testrun("project1", "TR-1", data, workflow_action="complete")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["workflowAction"], "complete")

    def test_update_testruns_with_workflow_action(self) -> None:
        """Test update_testruns with workflow_action parameter."""
        data: JsonDict = {
            "data": [{"type": "testruns"}],
        }
        self.api.update_testruns("project1", data, workflow_action="approve")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["workflowAction"], "approve")

    def test_delete_testrun(self) -> None:
        """Test delete_testrun method."""
        self.api.delete_testrun("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1", call_args[0][0])

    def test_get_testrun_workflow_actions_with_params(self) -> None:
        """Test get_testrun_workflow_actions with optional parameters."""
        self.api.get_testrun_workflow_actions("project1", "TR-1", page_size=10, page_number=0, revision="rev3")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["revision"], "rev3")

    def test_export_tests_to_excel(self) -> None:
        """Test export_tests_to_excel method."""
        self.api.export_tests_to_excel("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/actions/exportTestsToExcel", call_args[0][0])

    def test_export_tests_to_excel_with_params(self) -> None:
        """Test export_tests_to_excel with optional parameters."""
        self.api.export_tests_to_excel("project1", "TR-1", query="status:passed", sort_by="name", template="default", revision="rev4")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["query"], "status:passed")
        self.assertEqual(params["sortBy"], "name")
        self.assertEqual(params["template"], "default")
        self.assertEqual(params["revision"], "rev4")


# =============================================================================
# Testruns Attachments Tests (6 methods)
# =============================================================================


class TestTestrunsAttachments(unittest.TestCase):
    """Test testruns attachments operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_testrun_attachments(self) -> None:
        """Test get_testrun_attachments method."""
        self.api.get_testrun_attachments("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/attachments", call_args[0][0])

    def test_get_testrun_attachment(self) -> None:
        """Test get_testrun_attachment method."""
        self.api.get_testrun_attachment("project1", "TR-1", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/attachments/att-1", call_args[0][0])

    def test_get_testrun_attachment_content(self) -> None:
        """Test get_testrun_attachment_content method."""
        self.api.get_testrun_attachment_content("project1", "TR-1", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/attachments/att-1/content", call_args[0][0])

    def test_create_testrun_attachments(self) -> None:
        """Test create_testrun_attachments method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("test.txt", b"content"),
        }
        self.api.create_testrun_attachments("project1", "TR-1", files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/attachments", call_args[0][0])

    def test_update_testrun_attachment(self) -> None:
        """Test update_testrun_attachment method."""
        data: JsonDict = {
            "data": {"type": "testrun_attachments"},
        }
        self.api.update_testrun_attachment("project1", "TR-1", "att-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/attachments/att-1", call_args[0][0])

    def test_delete_testrun_attachment(self) -> None:
        """Test delete_testrun_attachment method."""
        self.api.delete_testrun_attachment("project1", "TR-1", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/attachments/att-1", call_args[0][0])

    def test_get_testrun_attachments_with_params(self) -> None:
        """Test get_testrun_attachments with optional parameters."""
        self.api.get_testrun_attachments("project1", "TR-1", page_size=25, page_number=1, fields={"testrun_attachments": "id,filename"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "25")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[testrun_attachments]"], "id,filename")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_get_testrun_attachment_with_params(self) -> None:
        """Test get_testrun_attachment with optional parameters."""
        self.api.get_testrun_attachment("project1", "TR-1", "att-1", fields={"testrun_attachments": "id,size"}, include="testrun", revision="rev2")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[testrun_attachments]"], "id,size")
        self.assertEqual(params["include"], "testrun")
        self.assertEqual(params["revision"], "rev2")

    def test_get_testrun_attachment_content_with_revision(self) -> None:
        """Test get_testrun_attachment_content with revision parameter."""
        self.api.get_testrun_attachment_content("project1", "TR-1", "att-1", revision="rev3")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev3")

    def test_delete_testrun_attachments(self) -> None:
        """Test delete_testrun_attachments method."""
        data: JsonDict = {
            "data": [{"type": "testrun_attachments", "id": "att-1"}],
        }
        self.api.delete_testrun_attachments("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/attachments", call_args[0][0])


# =============================================================================
# Testruns Comments Tests (4 methods)
# =============================================================================


class TestTestrunsComments(unittest.TestCase):
    """Test testruns comments operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_testrun_comments(self) -> None:
        """Test get_testrun_comments method."""
        self.api.get_testrun_comments("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/comments", call_args[0][0])

    def test_get_testrun_comment(self) -> None:
        """Test get_testrun_comment method."""
        self.api.get_testrun_comment("project1", "TR-1", "comment-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/comments/comment-1", call_args[0][0])

    def test_create_testrun_comments(self) -> None:
        """Test create_testrun_comments method."""
        data: JsonDict = {
            "data": [{"type": "testrun_comments"}],
        }
        self.api.create_testrun_comments("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/comments", call_args[0][0])

    def test_update_testrun_comment(self) -> None:
        """Test update_testrun_comment method."""
        data: JsonDict = {
            "data": {"type": "testrun_comments"},
        }
        self.api.update_testrun_comment("project1", "TR-1", "comment-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/comments/comment-1", call_args[0][0])

    def test_get_testrun_comments_with_params(self) -> None:
        """Test get_testrun_comments with optional parameters."""
        self.api.get_testrun_comments("project1", "TR-1", page_size=20, page_number=0, fields={"testrun_comments": "id,text"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[testrun_comments]"], "id,text")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_get_testrun_comment_with_params(self) -> None:
        """Test get_testrun_comment with optional parameters."""
        self.api.get_testrun_comment("project1", "TR-1", "comment-1", fields={"testrun_comments": "id,created"}, include="testrun", revision="rev2")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[testrun_comments]"], "id,created")
        self.assertEqual(params["include"], "testrun")
        self.assertEqual(params["revision"], "rev2")

    def test_update_testrun_comments(self) -> None:
        """Test update_testrun_comments method."""
        data: JsonDict = {
            "data": [{"type": "testrun_comments", "id": "c1"}],
        }
        self.api.update_testrun_comments("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/comments", call_args[0][0])


# =============================================================================
# Testruns Records Tests (13 methods)
# =============================================================================


class TestTestrunsRecords(unittest.TestCase):
    """Test testruns records operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_test_records(self) -> None:
        """Test get_test_records method."""
        self.api.get_test_records("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords", call_args[0][0])

    def test_get_test_record(self) -> None:
        """Test get_test_record method."""
        self.api.get_test_record("project1", "TR-1", "project1", "TC-1", 0)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0", call_args[0][0])

    def test_create_test_records(self) -> None:
        """Test create_test_records method."""
        data: JsonDict = {
            "data": [{"type": "testrecords"}],
        }
        self.api.create_test_records("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords", call_args[0][0])

    def test_update_test_records(self) -> None:
        """Test update_test_records method."""
        data: JsonDict = {
            "data": [{"type": "testrecords"}],
        }
        self.api.update_test_records("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords", call_args[0][0])

    def test_get_test_record_attachments(self) -> None:
        """Test get_test_record_attachments method."""
        self.api.get_test_record_attachments("project1", "TR-1", "project1", "TC-1", 0)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/attachments", call_args[0][0])

    def test_get_test_record_attachment(self) -> None:
        """Test get_test_record_attachment method."""
        self.api.get_test_record_attachment("project1", "TR-1", "project1", "TC-1", 0, "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/attachments/att-1", call_args[0][0])

    def test_get_test_record_attachment_content(self) -> None:
        """Test get_test_record_attachment_content method."""
        self.api.get_test_record_attachment_content("project1", "TR-1", "project1", "TC-1", 0, "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/attachments/att-1/content", call_args[0][0])

    def test_create_test_record_attachments(self) -> None:
        """Test create_test_record_attachments method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("test.txt", b"content"),
        }
        self.api.create_test_record_attachments("project1", "TR-1", "project1", "TC-1", 0, files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/attachments", call_args[0][0])

    def test_update_test_record_attachment(self) -> None:
        """Test update_test_record_attachment method."""
        data: JsonDict = {
            "data": {"type": "testrecord_attachments"},
        }
        self.api.update_test_record_attachment("project1", "TR-1", "project1", "TC-1", 0, "att-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/attachments/att-1", call_args[0][0])

    def test_delete_test_record_attachment(self) -> None:
        """Test delete_test_record_attachment method."""
        self.api.delete_test_record_attachment("project1", "TR-1", "project1", "TC-1", 0, "att-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/attachments/att-1", call_args[0][0])

    def test_get_test_record_test_parameters(self) -> None:
        """Test get_test_record_test_parameters method."""
        self.api.get_test_record_test_parameters("project1", "TR-1", "project1", "TC-1", 0)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/testparameters", call_args[0][0])

    def test_get_test_record_test_parameter(self) -> None:
        """Test get_test_record_test_parameter method."""
        self.api.get_test_record_test_parameter("project1", "TR-1", "project1", "TC-1", 0, "param-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/testparameters/param-1", call_args[0][0])

    def test_delete_test_record_test_parameter(self) -> None:
        """Test delete_test_record_test_parameter method."""
        self.api.delete_test_record_test_parameter("project1", "TR-1", "project1", "TC-1", 0, "param-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/testparameters/param-1", call_args[0][0])

    def test_get_test_records_with_params(self) -> None:
        """Test get_test_records with optional parameters."""
        self.api.get_test_records("project1", "TR-1", page_size=50, page_number=1, fields={"testrecords": "id,result"}, include="testcase", revision="rev1", test_case_project_id="proj2", test_case_id="TC-1", test_result_id="0")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[testrecords]"], "id,result")
        self.assertEqual(params["include"], "testcase")
        self.assertEqual(params["revision"], "rev1")
        self.assertEqual(params["testCaseProjectId"], "proj2")
        self.assertEqual(params["testCaseId"], "TC-1")
        self.assertEqual(params["testResultId"], "0")

    def test_get_test_record_with_params(self) -> None:
        """Test get_test_record with optional parameters."""
        self.api.get_test_record("project1", "TR-1", "project1", "TC-1", 0, fields={"testrecords": "id,status"}, include="attachments", revision="rev2")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[testrecords]"], "id,status")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["revision"], "rev2")

    def test_update_test_record(self) -> None:
        """Test update_test_record method."""
        data: JsonDict = {
            "data": {"type": "testrecords"},
        }
        self.api.update_test_record("project1", "TR-1", "project1", "TC-1", 0, data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0", call_args[0][0])

    def test_delete_test_record(self) -> None:
        """Test delete_test_record method."""
        self.api.delete_test_record("project1", "TR-1", "project1", "TC-1", 0)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0", call_args[0][0])

    def test_get_test_record_attachments_with_params(self) -> None:
        """Test get_test_record_attachments with optional parameters."""
        self.api.get_test_record_attachments("project1", "TR-1", "project1", "TC-1", 0, page_size=20, page_number=0, fields={"testrecord_attachments": "id,name"}, include="author", revision="rev3")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[testrecord_attachments]"], "id,name")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev3")

    def test_get_test_record_attachment_with_params(self) -> None:
        """Test get_test_record_attachment with optional parameters."""
        self.api.get_test_record_attachment("project1", "TR-1", "project1", "TC-1", 0, "att-1", fields={"testrecord_attachments": "id,size"}, include="record", revision="rev4")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[testrecord_attachments]"], "id,size")
        self.assertEqual(params["include"], "record")
        self.assertEqual(params["revision"], "rev4")

    def test_get_test_record_attachment_content_with_revision(self) -> None:
        """Test get_test_record_attachment_content with revision parameter."""
        self.api.get_test_record_attachment_content("project1", "TR-1", "project1", "TC-1", 0, "att-1", revision="rev5")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev5")

    def test_delete_test_record_attachments(self) -> None:
        """Test delete_test_record_attachments method."""
        data: JsonDict = {
            "data": [{"type": "attachments", "id": "att-1"}],
        }
        self.api.delete_test_record_attachments("project1", "TR-1", "project1", "TC-1", 0, data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/attachments", call_args[0][0])

    def test_get_test_record_test_parameters_with_params(self) -> None:
        """Test get_test_record_test_parameters with optional parameters."""
        self.api.get_test_record_test_parameters("project1", "TR-1", "project1", "TC-1", 0, page_size=10, page_number=0, fields={"testparameters": "id,value"}, include="definition", revision="rev6")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[testparameters]"], "id,value")
        self.assertEqual(params["include"], "definition")
        self.assertEqual(params["revision"], "rev6")

    def test_get_test_record_test_parameter_with_params(self) -> None:
        """Test get_test_record_test_parameter with optional parameters."""
        self.api.get_test_record_test_parameter("project1", "TR-1", "project1", "TC-1", 0, "param-1", fields={"testparameters": "id,name"}, include="record", revision="rev7")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[testparameters]"], "id,name")
        self.assertEqual(params["include"], "record")
        self.assertEqual(params["revision"], "rev7")

    def test_create_test_record_test_parameters(self) -> None:
        """Test create_test_record_test_parameters method."""
        data: JsonDict = {
            "data": [{"type": "testparameters"}],
        }
        self.api.create_test_record_test_parameters("project1", "TR-1", "project1", "TC-1", 0, data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/testparameters", call_args[0][0])


# =============================================================================
# Testruns Step Results Tests (11 methods)
# =============================================================================


class TestTestrunsStepResults(unittest.TestCase):
    """Test testruns step results operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_test_step_results(self) -> None:
        """Test get_test_step_results method."""
        self.api.get_test_step_results("project1", "TR-1", "project1", "TC-1", 0)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults", call_args[0][0])

    def test_get_test_step_result(self) -> None:
        """Test get_test_step_result method."""
        self.api.get_test_step_result("project1", "TR-1", "project1", "TC-1", 0, 1)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults/1", call_args[0][0])

    def test_create_test_step_results(self) -> None:
        """Test create_test_step_results method."""
        data: JsonDict = {
            "data": [{"type": "teststepresults"}],
        }
        self.api.create_test_step_results("project1", "TR-1", "project1", "TC-1", 0, data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults", call_args[0][0])

    def test_update_test_step_result(self) -> None:
        """Test update_test_step_result method."""
        data: JsonDict = {
            "data": {"type": "teststepresults"},
        }
        self.api.update_test_step_result("project1", "TR-1", "project1", "TC-1", 0, 1, data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults/1", call_args[0][0])

    def test_update_test_step_results(self) -> None:
        """Test update_test_step_results method."""
        data: JsonDict = {
            "data": [{"type": "teststepresults"}],
        }
        self.api.update_test_step_results("project1", "TR-1", "project1", "TC-1", 0, data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults", call_args[0][0])

    def test_get_test_step_result_attachments(self) -> None:
        """Test get_test_step_result_attachments method."""
        self.api.get_test_step_result_attachments("project1", "TR-1", "project1", "TC-1", 0, 1)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults/1/attachments", call_args[0][0])

    def test_get_test_step_result_attachment(self) -> None:
        """Test get_test_step_result_attachment method."""
        self.api.get_test_step_result_attachment("project1", "TR-1", "project1", "TC-1", 0, 1, "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults/1/attachments/att-1", call_args[0][0])

    def test_get_test_step_result_attachment_content(self) -> None:
        """Test get_test_step_result_attachment_content method."""
        self.api.get_test_step_result_attachment_content("project1", "TR-1", "project1", "TC-1", 0, 1, "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults/1/attachments/att-1/content", call_args[0][0])

    def test_create_test_step_result_attachments(self) -> None:
        """Test create_test_step_result_attachments method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("test.txt", b"content"),
        }
        self.api.create_test_step_result_attachments("project1", "TR-1", "project1", "TC-1", 0, 1, files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults/1/attachments", call_args[0][0])

    def test_update_test_step_result_attachment(self) -> None:
        """Test update_test_step_result_attachment method."""
        data: JsonDict = {
            "data": {"type": "teststepresult_attachments"},
        }
        self.api.update_test_step_result_attachment("project1", "TR-1", "project1", "TC-1", 0, 1, "att-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults/1/attachments/att-1", call_args[0][0])

    def test_delete_test_step_result_attachment(self) -> None:
        """Test delete_test_step_result_attachment method."""
        self.api.delete_test_step_result_attachment("project1", "TR-1", "project1", "TC-1", 0, 1, "att-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testrecords/project1/TC-1/0/teststepresults/1/attachments/att-1", call_args[0][0])


# =============================================================================
# Testruns Parameters Tests (9 methods)
# =============================================================================


class TestTestrunsParameters(unittest.TestCase):
    """Test testruns parameters operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_testrun_test_parameters(self) -> None:
        """Test get_testrun_test_parameters method."""
        self.api.get_testrun_test_parameters("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testparameters", call_args[0][0])

    def test_get_testrun_test_parameter(self) -> None:
        """Test get_testrun_test_parameter method."""
        self.api.get_testrun_test_parameter("project1", "TR-1", "param-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testparameters/param-1", call_args[0][0])

    def test_create_testrun_test_parameters(self) -> None:
        """Test create_testrun_test_parameters method."""
        data: JsonDict = {
            "data": [{"type": "testparameters"}],
        }
        self.api.create_testrun_test_parameters("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testparameters", call_args[0][0])

    def test_delete_testrun_test_parameters(self) -> None:
        """Test delete_testrun_test_parameters method."""
        data: JsonDict = {
            "data": [{"type": "testparameters"}],
        }
        self.api.delete_testrun_test_parameters("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testparameters", call_args[0][0])

    def test_get_testrun_test_parameter_definitions(self) -> None:
        """Test get_testrun_test_parameter_definitions method."""
        self.api.get_testrun_test_parameter_definitions("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testparameterdefinitions", call_args[0][0])

    def test_get_testrun_test_parameter_definition(self) -> None:
        """Test get_testrun_test_parameter_definition method."""
        self.api.get_testrun_test_parameter_definition("project1", "TR-1", "def-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testparameterdefinitions/def-1", call_args[0][0])

    def test_create_testrun_test_parameter_definitions(self) -> None:
        """Test create_testrun_test_parameter_definitions method."""
        data: JsonDict = {
            "data": [{"type": "testparameterdefinitions"}],
        }
        self.api.create_testrun_test_parameter_definitions("project1", "TR-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testparameterdefinitions", call_args[0][0])

    def test_delete_testrun_test_parameter_definition(self) -> None:
        """Test delete_testrun_test_parameter_definition method."""
        self.api.delete_testrun_test_parameter_definition("project1", "TR-1", "def-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testruns/TR-1/testparameterdefinitions/def-1", call_args[0][0])


# =============================================================================
# Documents CRUD Tests (3 methods)
# =============================================================================


class TestDocumentsCrud(unittest.TestCase):
    """Test documents CRUD operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_document(self) -> None:
        """Test get_document method."""
        self.api.get_document("project1", "space", "doc1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1", call_args[0][0])

    def test_create_documents(self) -> None:
        """Test create_documents method."""
        data: JsonDict = {
            "data": [{"type": "documents"}],
        }
        self.api.create_documents("project1", "space", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/documents", call_args[0][0])

    def test_update_document(self) -> None:
        """Test update_document method."""
        data: JsonDict = {
            "data": {"type": "documents"},
        }
        self.api.update_document("project1", "space", "doc1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1", call_args[0][0])


# =============================================================================
# Documents Attachments Tests (5 methods)
# =============================================================================


class TestDocumentsAttachments(unittest.TestCase):
    """Test documents attachments operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_document_attachments(self) -> None:
        """Test get_document_attachments method."""
        self.api.get_document_attachments("project1", "space", "doc1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/attachments", call_args[0][0])

    def test_get_document_attachment(self) -> None:
        """Test get_document_attachment method."""
        self.api.get_document_attachment("project1", "space", "doc1", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/attachments/att-1", call_args[0][0])

    def test_get_document_attachment_content(self) -> None:
        """Test get_document_attachment_content method."""
        self.api.get_document_attachment_content("project1", "space", "doc1", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/attachments/att-1/content", call_args[0][0])

    def test_create_document_attachments(self) -> None:
        """Test create_document_attachments method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("test.txt", b"content"),
        }
        self.api.create_document_attachments("project1", "space", "doc1", files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/attachments", call_args[0][0])

    def test_update_document_attachment(self) -> None:
        """Test update_document_attachment method."""
        data: JsonDict = {
            "data": {"type": "document_attachments"},
        }
        self.api.update_document_attachment("project1", "space", "doc1", "att-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/attachments/att-1", call_args[0][0])


# =============================================================================
# Documents Comments Tests (4 methods)
# =============================================================================


class TestDocumentsComments(unittest.TestCase):
    """Test documents comments operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_document_comments(self) -> None:
        """Test get_document_comments method."""
        self.api.get_document_comments("project1", "space", "doc1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/comments", call_args[0][0])

    def test_get_document_comment(self) -> None:
        """Test get_document_comment method."""
        self.api.get_document_comment("project1", "space", "doc1", "comment-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/comments/comment-1", call_args[0][0])

    def test_create_document_comments(self) -> None:
        """Test create_document_comments method."""
        data: JsonDict = {
            "data": [{"type": "document_comments"}],
        }
        self.api.create_document_comments("project1", "space", "doc1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/comments", call_args[0][0])

    def test_update_document_comment(self) -> None:
        """Test update_document_comment method."""
        data: JsonDict = {
            "data": {"type": "document_comments"},
        }
        self.api.update_document_comment("project1", "space", "doc1", "comment-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/comments/comment-1", call_args[0][0])


# =============================================================================
# Documents Parts Tests (3 methods)
# =============================================================================


class TestDocumentsParts(unittest.TestCase):
    """Test documents parts operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_document_parts(self) -> None:
        """Test get_document_parts method."""
        self.api.get_document_parts("project1", "space", "doc1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/parts", call_args[0][0])

    def test_get_document_part(self) -> None:
        """Test get_document_part method."""
        self.api.get_document_part("project1", "space", "doc1", "part-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/parts/part-1", call_args[0][0])

    def test_create_document_parts(self) -> None:
        """Test create_document_parts method."""
        data: JsonDict = {
            "data": [{"type": "document_parts"}],
        }
        self.api.create_document_parts("project1", "space", "doc1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/parts", call_args[0][0])


# =============================================================================
# Documents Branching Tests (5 methods)
# =============================================================================


class TestDocumentsBranching(unittest.TestCase):
    """Test documents branching operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_branch_document(self) -> None:
        """Test branch_document method."""
        data: JsonDict = {
            "targetProjectId": "project2",
        }
        self.api.branch_document("project1", "space", "doc1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/actions/branch", call_args[0][0])

    def test_branch_documents(self) -> None:
        """Test branch_documents method."""
        data: JsonDict = {
            "data": [{"type": "documents"}],
        }
        self.api.branch_documents(data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/all/documents/actions/branch", call_args[0][0])

    def test_copy_document(self) -> None:
        """Test copy_document method."""
        data: JsonDict = {
            "targetProjectId": "project2",
        }
        self.api.copy_document("project1", "space", "doc1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/actions/copy", call_args[0][0])

    def test_merge_document_from_master(self) -> None:
        """Test merge_document_from_master method."""
        data: JsonDict = {
            "revision": "123",
        }
        self.api.merge_document_from_master("project1", "space", "doc1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/actions/mergeFromMaster", call_args[0][0])

    def test_merge_document_to_master(self) -> None:
        """Test merge_document_to_master method."""
        data: JsonDict = {
            "revision": "123",
        }
        self.api.merge_document_to_master("project1", "space", "doc1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/actions/mergeToMaster", call_args[0][0])


# =============================================================================
# Documents Enums Tests (3 methods)
# =============================================================================


class TestDocumentsEnums(unittest.TestCase):
    """Test documents enum operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_documents_available_enum_options(self) -> None:
        """Test get_documents_available_enum_options method."""
        self.api.get_documents_available_enum_options("project1", "status")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/documents/fields/status/actions/getAvailableOptions", call_args[0][0])

    def test_get_document_available_enum_options(self) -> None:
        """Test get_document_available_enum_options method."""
        self.api.get_document_available_enum_options("project1", "space", "doc1", "status")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/fields/status/actions/getAvailableOptions", call_args[0][0])

    def test_get_document_current_enum_options(self) -> None:
        """Test get_document_current_enum_options method."""
        self.api.get_document_current_enum_options("project1", "space", "doc1", "status")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/documents/doc1/fields/status/actions/getCurrentOptions", call_args[0][0])


# =============================================================================
# Projects CRUD Tests (11 methods)
# =============================================================================


class TestProjectsCrud(unittest.TestCase):
    """Test projects CRUD operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_projects(self) -> None:
        """Test get_projects method."""
        self.api.get_projects()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects", call_args[0][0])

    def test_get_project(self) -> None:
        """Test get_project method."""
        self.api.get_project("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1", call_args[0][0])

    def test_create_project(self) -> None:
        """Test create_project method."""
        data: JsonDict = {
            "data": {"type": "projects"},
        }
        self.api.create_project(data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects", call_args[0][0])

    def test_update_project(self) -> None:
        """Test update_project method."""
        data: JsonDict = {
            "data": {"type": "projects"},
        }
        self.api.update_project("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1", call_args[0][0])

    def test_delete_project(self) -> None:
        """Test delete_project method."""
        self.api.delete_project("project1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1", call_args[0][0])

    def test_get_project_templates(self) -> None:
        """Test get_project_templates method."""
        self.api.get_project_templates()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projecttemplates", call_args[0][0])

    def test_move_project(self) -> None:
        """Test move_project method."""
        data: JsonDict = {
            "targetLocation": "/projects",
        }
        self.api.move_project("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/actions/moveProject", call_args[0][0])

    def test_mark_project(self) -> None:
        """Test mark_project method."""
        data: JsonDict = {
            "data": {"type": "projects"},
        }
        self.api.mark_project(data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/actions/markProject", call_args[0][0])

    def test_unmark_project(self) -> None:
        """Test unmark_project method."""
        self.api.unmark_project("project1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/actions/unmarkProject", call_args[0][0])

    def test_get_project_test_parameter_definitions(self) -> None:
        """Test get_project_test_parameter_definitions method."""
        self.api.get_project_test_parameter_definitions("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testparameterdefinitions", call_args[0][0])

    def test_get_project_test_parameter_definition(self) -> None:
        """Test get_project_test_parameter_definition method."""
        self.api.get_project_test_parameter_definition("project1", "def-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testparameterdefinitions/def-1", call_args[0][0])

    def test_create_project_test_parameter_definitions(self) -> None:
        """Test create_project_test_parameter_definitions method."""
        data: JsonDict = {
            "data": [{"type": "testparameterdefinitions"}],
        }
        self.api.create_project_test_parameter_definitions("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testparameterdefinitions", call_args[0][0])

    def test_delete_project_test_parameter_definition(self) -> None:
        """Test delete_project_test_parameter_definition method."""
        self.api.delete_project_test_parameter_definition("project1", "def-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testparameterdefinitions/def-1", call_args[0][0])

    def test_delete_project_test_parameter_definitions(self) -> None:
        """Test delete_project_test_parameter_definitions method."""
        data: JsonDict = {
            "data": [{"type": "testparameterdefinitions"}],
        }
        self.api.delete_project_test_parameter_definitions("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/testparameterdefinitions", call_args[0][0])


# =============================================================================
# Projects Enumerations Tests (7 methods)
# =============================================================================


class TestProjectsEnumerations(unittest.TestCase):
    """Test projects enumerations operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_project_enumeration(self) -> None:
        """Test get_project_enumeration method."""
        self.api.get_project_enumeration("project1", "context", "enum-1", "target-type")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/enumerations/context/enum-1/target-type", call_args[0][0])

    def test_update_project_enumeration(self) -> None:
        """Test update_project_enumeration method."""
        data: JsonDict = {
            "data": {"type": "enumerations"},
        }
        self.api.update_project_enumeration("project1", "context", "enum-1", "target-type", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/enumerations/context/enum-1/target-type", call_args[0][0])

    def test_delete_project_enumeration(self) -> None:
        """Test delete_project_enumeration method."""
        self.api.delete_project_enumeration("project1", "context", "enum-1", "target-type")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/enumerations/context/enum-1/target-type", call_args[0][0])

    def test_get_project_icons(self) -> None:
        """Test get_project_icons method."""
        self.api.get_project_icons("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/enumerations/icons", call_args[0][0])

    def test_get_project_icon(self) -> None:
        """Test get_project_icon method."""
        self.api.get_project_icon("project1", "icon-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/enumerations/icons/icon-1", call_args[0][0])

    def test_create_project_icons(self) -> None:
        """Test create_project_icons method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("icon.png", b"content"),
        }
        self.api.create_project_icons("project1", files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/enumerations/icons", call_args[0][0])


# =============================================================================
# Collections Tests (12 methods)
# =============================================================================


class TestCollections(unittest.TestCase):
    """Test collections operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_collections(self) -> None:
        """Test get_collections method."""
        self.api.get_collections("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/collections", call_args[0][0])

    def test_get_collection(self) -> None:
        """Test get_collection method."""
        self.api.get_collection("project1", "coll-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/collections/coll-1", call_args[0][0])

    def test_create_collections(self) -> None:
        """Test create_collections method."""
        data: JsonDict = {
            "data": [{"type": "collections"}],
        }
        self.api.create_collections("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/collections", call_args[0][0])

    def test_update_collection(self) -> None:
        """Test update_collection method."""
        data: JsonDict = {
            "data": {"type": "collections"},
        }
        self.api.update_collection("project1", "coll-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/collections/coll-1", call_args[0][0])

    def test_delete_collection(self) -> None:
        """Test delete_collection method."""
        self.api.delete_collection("project1", "coll-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/collections/coll-1", call_args[0][0])

    def test_delete_collections(self) -> None:
        """Test delete_collections method."""
        data: JsonDict = {
            "data": [{"type": "collections"}],
        }
        self.api.delete_collections("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/collections", call_args[0][0])

    def test_close_collection(self) -> None:
        """Test close_collection method."""
        self.api.close_collection("project1", "coll-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/collections/coll-1/actions/close", call_args[0][0])

    def test_reopen_collection(self) -> None:
        """Test reopen_collection method."""
        self.api.reopen_collection("project1", "coll-1")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/collections/coll-1/actions/reopen", call_args[0][0])

    def test_get_collection_relationships(self) -> None:
        """Test get_collection_relationships method."""
        self.api.get_collection_relationships("project1", "coll-1", "documents")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/collections/coll-1/relationships/documents", call_args[0][0])

    def test_create_collection_relationships(self) -> None:
        """Test create_collection_relationships method."""
        data: JsonDict = {
            "data": [{"type": "documents"}],
        }
        self.api.create_collection_relationships("project1", "coll-1", "documents", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/collections/coll-1/relationships/documents", call_args[0][0])

    def test_update_collection_relationships(self) -> None:
        """Test update_collection_relationships method."""
        data: JsonDict = {
            "data": [{"type": "documents"}],
        }
        self.api.update_collection_relationships("project1", "coll-1", "documents", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/collections/coll-1/relationships/documents", call_args[0][0])

    def test_delete_collection_relationships(self) -> None:
        """Test delete_collection_relationships method."""
        data: JsonDict = {
            "data": [{"type": "documents"}],
        }
        self.api.delete_collection_relationships("project1", "coll-1", "documents", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/collections/coll-1/relationships/documents", call_args[0][0])


# =============================================================================
# Plans Tests (9 methods)
# =============================================================================


class TestPlans(unittest.TestCase):
    """Test plans operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_plans(self) -> None:
        """Test get_plans method."""
        self.api.get_plans("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/plans", call_args[0][0])

    def test_get_plan(self) -> None:
        """Test get_plan method."""
        self.api.get_plan("project1", "plan-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/plans/plan-1", call_args[0][0])

    def test_create_plans(self) -> None:
        """Test create_plans method."""
        data: JsonDict = {
            "data": [{"type": "plans"}],
        }
        self.api.create_plans("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/plans", call_args[0][0])

    def test_update_plan(self) -> None:
        """Test update_plan method."""
        data: JsonDict = {
            "data": {"type": "plans"},
        }
        self.api.update_plan("project1", "plan-1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/plans/plan-1", call_args[0][0])

    def test_delete_plans(self) -> None:
        """Test delete_plans method."""
        data: JsonDict = {
            "data": [{"type": "plans"}],
        }
        self.api.delete_plans("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/plans", call_args[0][0])

    def test_get_plan_relationships(self) -> None:
        """Test get_plan_relationships method."""
        self.api.get_plan_relationships("project1", "plan-1", "workitems")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/plans/plan-1/relationships/workitems", call_args[0][0])

    def test_create_plan_relationships(self) -> None:
        """Test create_plan_relationships method."""
        data: JsonDict = {
            "data": [{"type": "workitems"}],
        }
        self.api.create_plan_relationships("project1", "plan-1", "workitems", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/plans/plan-1/relationships/workitems", call_args[0][0])

    def test_update_plan_relationships(self) -> None:
        """Test update_plan_relationships method."""
        data: JsonDict = {
            "data": [{"type": "workitems"}],
        }
        self.api.update_plan_relationships("project1", "plan-1", "workitems", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/plans/plan-1/relationships/workitems", call_args[0][0])

    def test_delete_plan_relationships(self) -> None:
        """Test delete_plan_relationships method."""
        data: JsonDict = {
            "data": [{"type": "workitems"}],
        }
        self.api.delete_plan_relationships("project1", "plan-1", "workitems", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/plans/plan-1/relationships/workitems", call_args[0][0])


# =============================================================================
# Pages Tests (7 methods)
# =============================================================================


class TestPages(unittest.TestCase):
    """Test pages operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_page(self) -> None:
        """Test get_page method."""
        self.api.get_page("project1", "space", "page1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/pages/page1", call_args[0][0])

    def test_update_page(self) -> None:
        """Test update_page method."""
        data: JsonDict = {
            "data": {"type": "pages"},
        }
        self.api.update_page("project1", "space", "page1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/spaces/space/pages/page1", call_args[0][0])

    def test_get_page_attachment(self) -> None:
        """Test get_page_attachment method."""
        self.api.get_page_attachment("project1", "space", "page1", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/pages/page1/attachments/att-1", call_args[0][0])

    def test_get_page_attachment_content(self) -> None:
        """Test get_page_attachment_content method."""
        self.api.get_page_attachment_content("project1", "space", "page1", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space/pages/page1/attachments/att-1/content", call_args[0][0])

    def test_create_page_attachments(self) -> None:
        """Test create_page_attachments method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("test.txt", b"content"),
        }
        self.api.create_page_attachments("project1", "space", "page1", files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space/pages/page1/attachments", call_args[0][0])


# =============================================================================
# Users Tests (8 methods)
# =============================================================================


class TestUsers(unittest.TestCase):
    """Test users operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_users(self) -> None:
        """Test get_users method."""
        self.api.get_users()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/users", call_args[0][0])

    def test_get_user(self) -> None:
        """Test get_user method."""
        self.api.get_user("user1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/users/user1", call_args[0][0])

    def test_create_users(self) -> None:
        """Test create_users method."""
        data: JsonDict = {
            "data": [{"type": "users"}],
        }
        self.api.create_users(data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/users", call_args[0][0])

    def test_update_user(self) -> None:
        """Test update_user method."""
        data: JsonDict = {
            "data": {"type": "users"},
        }
        self.api.update_user("user1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/users/user1", call_args[0][0])

    def test_get_user_avatar(self) -> None:
        """Test get_user_avatar method."""
        self.api.get_user_avatar("user1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/users/user1/actions/getAvatar", call_args[0][0])

    def test_update_user_avatar(self) -> None:
        """Test update_user_avatar method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("avatar.png", b"content"),
        }
        self.api.update_user_avatar("user1", files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/users/user1/actions/updateAvatar", call_args[0][0])

    def test_set_user_license(self) -> None:
        """Test set_user_license method."""
        data: JsonDict = {
            "data": {"type": "licenses"},
        }
        self.api.set_user_license("user1", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/users/user1/actions/setLicense", call_args[0][0])

    def test_get_user_group(self) -> None:
        """Test get_user_group method."""
        self.api.get_user_group("group1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/usergroups/group1", call_args[0][0])


# =============================================================================
# Jobs Tests (2 methods)
# =============================================================================


class TestJobs(unittest.TestCase):
    """Test jobs operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_job(self) -> None:
        """Test get_job method."""
        self.api.get_job("job-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/jobs/job-1", call_args[0][0])

    def test_get_job_result_file(self) -> None:
        """Test get_job_result_file method."""
        self.api.get_job_result_file("job-1", "result.zip")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/jobs/job-1/actions/download/result.zip", call_args[0][0])


# =============================================================================
# Revisions Tests (2 methods)
# =============================================================================


class TestRevisions(unittest.TestCase):
    """Test revisions operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_revisions(self) -> None:
        """Test get_revisions method."""
        self.api.get_revisions()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/revisions", call_args[0][0])

    def test_get_revision(self) -> None:
        """Test get_revision method."""
        self.api.get_revision("default", "123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/revisions/default/123", call_args[0][0])


# =============================================================================
# Global Enumerations Tests (10 methods)
# =============================================================================


class TestGlobalEnumerations(unittest.TestCase):
    """Test global enumerations operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_global_enumeration(self) -> None:
        """Test get_global_enumeration method."""
        self.api.get_global_enumeration("context", "enum-1", "target-type")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/enumerations/context/enum-1/target-type", call_args[0][0])

    def test_create_global_enumeration(self) -> None:
        """Test create_global_enumeration method."""
        data: JsonDict = {
            "data": {"type": "enumerations"},
        }
        self.api.create_global_enumeration(data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/enumerations", call_args[0][0])

    def test_update_global_enumeration(self) -> None:
        """Test update_global_enumeration method."""
        data: JsonDict = {
            "data": {"type": "enumerations"},
        }
        self.api.update_global_enumeration("context", "enum-1", "target-type", data)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/enumerations/context/enum-1/target-type", call_args[0][0])

    def test_delete_global_enumeration(self) -> None:
        """Test delete_global_enumeration method."""
        self.api.delete_global_enumeration("context", "enum-1", "target-type")
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/enumerations/context/enum-1/target-type", call_args[0][0])

    def test_get_global_icons(self) -> None:
        """Test get_global_icons method."""
        self.api.get_global_icons()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/enumerations/icons", call_args[0][0])

    def test_get_global_icon(self) -> None:
        """Test get_global_icon method."""
        self.api.get_global_icon("icon-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/enumerations/icons/icon-1", call_args[0][0])

    def test_create_global_icons(self) -> None:
        """Test create_global_icons method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("icon.png", b"content"),
        }
        self.api.create_global_icons(files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/enumerations/icons", call_args[0][0])

    def test_get_default_icons(self) -> None:
        """Test get_default_icons method."""
        self.api.get_default_icons()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/enumerations/defaulticons", call_args[0][0])

    def test_get_default_icon(self) -> None:
        """Test get_default_icon method."""
        self.api.get_default_icon("icon-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/enumerations/defaulticons/icon-1", call_args[0][0])


# =============================================================================
# Misc Tests (5 methods)
# =============================================================================


class TestMisc(unittest.TestCase):
    """Test miscellaneous operations."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_role(self) -> None:
        """Test get_role method."""
        self.api.get_role("role1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/roles/role1", call_args[0][0])

    def test_export_tests_to_excel(self) -> None:
        """Test export_tests_to_excel method."""
        self.api.export_tests_to_excel("project1", "TR-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/testruns/TR-1/actions/exportTestsToExcel", call_args[0][0])

    def test_import_excel_test_results(self) -> None:
        """Test import_excel_test_results method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("results.xlsx", b"content"),
        }
        self.api.import_excel_test_results("project1", "TR-1", files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/actions/importExcelTestResults", call_args[0][0])

    def test_import_xunit_test_results(self) -> None:
        """Test import_xunit_test_results method."""
        files: dict[str, tuple[str, bytes]] = {
            "file": ("results.xml", b"content"),
        }
        self.api.import_xunit_test_results("project1", "TR-1", files)
        call_args: tuple[tuple[str, ...], dict[str, str]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/testruns/TR-1/actions/importXUnitTestResults", call_args[0][0])


# =============================================================================
# Additional Optional Parameter Tests
# =============================================================================


class TestOptionalParameterCoverage(unittest.TestCase):
    """Additional tests to cover optional parameter branches."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    # Revisions optional params
    def test_get_revisions_with_params(self) -> None:
        """Test get_revisions with optional parameters."""
        self.api.get_revisions(page_size=50, page_number=1, fields={"revisions": "id"}, include="author", query="date:[NOW-1DAY TO *]", sort="-created")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[revisions]"], "id")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["query"], "date:[NOW-1DAY TO *]")
        self.assertEqual(params["sort"], "-created")

    def test_get_revision_with_params(self) -> None:
        """Test get_revision with optional parameters."""
        self.api.get_revision("default", "12345", fields={"revisions": "id,message"}, include="author")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[revisions]"], "id,message")
        self.assertEqual(params["include"], "author")

    # Testruns parameters optional params
    def test_get_testrun_test_parameters_with_params(self) -> None:
        """Test get_testrun_test_parameters with optional parameters."""
        self.api.get_testrun_test_parameters("project1", "TR-1", page_size=20, page_number=0, fields={"testparameters": "id"}, include="definition", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[testparameters]"], "id")
        self.assertEqual(params["include"], "definition")
        self.assertEqual(params["revision"], "rev1")

    def test_get_testrun_test_parameter_with_params(self) -> None:
        """Test get_testrun_test_parameter with optional parameters."""
        self.api.get_testrun_test_parameter("project1", "TR-1", "param-1", fields={"testparameters": "id,value"}, include="definition", revision="rev2")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[testparameters]"], "id,value")
        self.assertEqual(params["include"], "definition")
        self.assertEqual(params["revision"], "rev2")

    def test_get_testrun_test_parameter_definitions_with_params(self) -> None:
        """Test get_testrun_test_parameter_definitions with optional parameters."""
        self.api.get_testrun_test_parameter_definitions("project1", "TR-1", page_size=30, page_number=2, fields={"testparameter_definitions": "id,name"}, include="values", revision="rev3")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "30")
        self.assertEqual(params["page[number]"], "2")
        self.assertEqual(params["fields[testparameter_definitions]"], "id,name")
        self.assertEqual(params["include"], "values")
        self.assertEqual(params["revision"], "rev3")

    def test_get_testrun_test_parameter_definition_with_params(self) -> None:
        """Test get_testrun_test_parameter_definition with optional parameters."""
        self.api.get_testrun_test_parameter_definition("project1", "TR-1", "param-1", fields={"testparameter_definitions": "id,type"}, include="values", revision="rev4")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[testparameter_definitions]"], "id,type")
        self.assertEqual(params["include"], "values")
        self.assertEqual(params["revision"], "rev4")

    # Step results optional params
    def test_get_test_step_results_with_params(self) -> None:
        """Test get_test_step_results with optional parameters."""
        self.api.get_test_step_results("project1", "TR-1", "project1", "TC-1", 0, page_size=10, page_number=0, fields={"teststep_results": "id,result"}, include="attachments", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[teststep_results]"], "id,result")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["revision"], "rev1")

    def test_get_test_step_result_with_params(self) -> None:
        """Test get_test_step_result with optional parameters."""
        self.api.get_test_step_result("project1", "TR-1", "project1", "TC-1", 0, 1, fields={"teststep_results": "id,status"}, include="attachments", revision="rev2")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[teststep_results]"], "id,status")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["revision"], "rev2")

    def test_get_test_step_result_attachments_params(self) -> None:
        """Test get_test_step_result_attachments with optional parameters."""
        self.api.get_test_step_result_attachments("project1", "TR-1", "project1", "TC-1", 0, 1, page_size=5, page_number=0, fields={"teststepresult_attachments": "id,name"}, include="author", revision="rev3")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "5")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[teststepresult_attachments]"], "id,name")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev3")

    def test_get_test_step_result_attachment_with_params(self) -> None:
        """Test get_test_step_result_attachment with optional parameters."""
        self.api.get_test_step_result_attachment("project1", "TR-1", "project1", "TC-1", 0, 1, "att-1", fields={"teststepresult_attachments": "id,size"}, include="result", revision="rev4")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[teststepresult_attachments]"], "id,size")
        self.assertEqual(params["include"], "result")
        self.assertEqual(params["revision"], "rev4")

    def test_get_test_step_result_attachment_content_with_params(self) -> None:
        """Test get_test_step_result_attachment_content with revision parameter."""
        self.api.get_test_step_result_attachment_content("project1", "TR-1", "project1", "TC-1", 0, 1, "att-1", revision="rev5")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev5")

    # Users optional params
    def test_get_users_with_params(self) -> None:
        """Test get_users with optional parameters."""
        self.api.get_users(page_size=100, page_number=0, fields={"users": "id,name"}, include="groups", query="name:admin*", sort="name")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "100")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[users]"], "id,name")
        self.assertEqual(params["include"], "groups")
        self.assertEqual(params["query"], "name:admin*")
        self.assertEqual(params["sort"], "name")

    def test_get_user_with_params(self) -> None:
        """Test get_user with optional parameters."""
        self.api.get_user("user1", fields={"users": "id,email"}, include="groups")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[users]"], "id,email")
        self.assertEqual(params["include"], "groups")

    # Jobs optional params
    def test_get_job_with_params(self) -> None:
        """Test get_job with optional parameters."""
        self.api.get_job("job-123", fields={"jobs": "id,status"}, include="results")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[jobs]"], "id,status")
        self.assertEqual(params["include"], "results")

    # Enumerations optional params
    def test_get_global_enumeration_with_params(self) -> None:
        """Test get_global_enumeration with optional parameters."""
        self.api.get_global_enumeration("context", "priority", "workitems", fields={"enumerations": "id,name"}, include="options")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,name")
        self.assertEqual(params["include"], "options")

    def test_get_global_icons_with_params(self) -> None:
        """Test get_global_icons with optional parameters."""
        self.api.get_global_icons(page_size=50, page_number=0, fields={"enumerations": "id,name"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[enumerations]"], "id,name")

    def test_get_global_icon_with_params(self) -> None:
        """Test get_global_icon with optional parameters."""
        self.api.get_global_icon("icon-1", fields={"enumerations": "id,name"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,name")

    def test_get_default_icons_with_params(self) -> None:
        """Test get_default_icons with optional parameters."""
        self.api.get_default_icons(page_size=25, page_number=0, fields={"enumerations": "id,name"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "25")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[enumerations]"], "id,name")

    def test_get_default_icon_with_params(self) -> None:
        """Test get_default_icon with optional parameters."""
        self.api.get_default_icon("icon-1", fields={"enumerations": "id,data"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,data")

    # Projects CRUD optional params
    def test_get_projects_with_params(self) -> None:
        """Test get_projects with optional parameters."""
        self.api.get_projects(page_size=20, page_number=1, fields={"enumerations": "id,name"}, include="lead", query="status:active", sort="name")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[enumerations]"], "id,name")
        self.assertEqual(params["include"], "lead")
        self.assertEqual(params["query"], "status:active")
        self.assertEqual(params["sort"], "name")

    def test_get_project_with_params(self) -> None:
        """Test get_project with optional parameters."""
        self.api.get_project("project1", fields={"enumerations": "id,description"}, include="lead", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,description")
        self.assertEqual(params["include"], "lead")
        self.assertEqual(params["revision"], "rev1")

    # Project enumerations optional params (get_project_categories and get_project_enumerations_list don't exist)
    def test_get_project_enumeration_with_params(self) -> None:
        """Test get_project_enumeration with optional parameters."""
        self.api.get_project_enumeration("project1", "context", "priority", "workitems", fields={"enumerations": "id,name"}, revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,name")
        self.assertEqual(params["revision"], "rev1")

    def test_get_project_icons_with_params(self) -> None:
        """Test get_project_icons with optional parameters."""
        self.api.get_project_icons("project1", page_size=30, page_number=0, fields={"enumerations": "id,name"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "30")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[enumerations]"], "id,name")

    def test_get_project_icon_with_params(self) -> None:
        """Test get_project_icon with optional parameters."""
        self.api.get_project_icon("project1", "icon-1", fields={"enumerations": "id,data"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,data")

    # Project collections optional params (use generic get_collections/get_collection)
    def test_get_collections_with_params(self) -> None:
        """Test get_collections with optional parameters."""
        self.api.get_collections("project1", page_size=15, page_number=1, fields={"enumerations": "id,name"}, include="documents", query="name:*spec*", sort="name", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "15")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[enumerations]"], "id,name")
        self.assertEqual(params["include"], "documents")
        self.assertEqual(params["query"], "name:*spec*")
        self.assertEqual(params["sort"], "name")
        self.assertEqual(params["revision"], "rev1")

    def test_get_collection_with_params(self) -> None:
        """Test get_collection with optional parameters."""
        self.api.get_collection("project1", "col-1", fields={"enumerations": "id,description"}, include="documents", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,description")
        self.assertEqual(params["include"], "documents")
        self.assertEqual(params["revision"], "rev1")

    # Documents optional params (get_documents method doesn't exist - only individual document retrieval)
    def test_get_document_with_params(self) -> None:
        """Test get_document with optional parameters."""
        self.api.get_document("project1", "space1", "doc1", fields={"enumerations": "id,content"}, include="attachments", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,content")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["revision"], "rev1")

    # Document attachments optional params
    def test_get_document_attachments_with_params(self) -> None:
        """Test get_document_attachments with optional parameters."""
        self.api.get_document_attachments("project1", "space1", "doc1", page_size=10, page_number=0, fields={"enumerations": "id,name"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[enumerations]"], "id,name")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_get_document_attachment_with_params(self) -> None:
        """Test get_document_attachment with optional parameters."""
        self.api.get_document_attachment("project1", "space1", "doc1", "att-1", fields={"enumerations": "id,size"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,size")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_get_document_attachment_content_with_revision(self) -> None:
        """Test get_document_attachment_content with revision parameter."""
        self.api.get_document_attachment_content("project1", "space1", "doc1", "att-1", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev1")

    # Document comments optional params
    def test_get_document_comments_with_params(self) -> None:
        """Test get_document_comments with optional parameters."""
        self.api.get_document_comments("project1", "space1", "doc1", page_size=15, page_number=0, fields={"revisions": "id,text"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "15")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[revisions]"], "id,text")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_get_document_comment_with_params(self) -> None:
        """Test get_document_comment with optional parameters."""
        self.api.get_document_comment("project1", "space1", "doc1", "com-1", fields={"revisions": "id,created"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[revisions]"], "id,created")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    # Document fields optional params
    def test_get_document_available_enum_options_with_params(self) -> None:
        """Test get_document_available_enum_options with optional parameters."""
        self.api.get_document_available_enum_options("project1", "space1", "doc1", "status", page_size=20, page_number=0)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "0")

    def test_get_document_current_enum_options_with_params(self) -> None:
        """Test get_document_current_enum_options with optional parameters."""
        self.api.get_document_current_enum_options("project1", "space1", "doc1", "status", page_size=10, page_number=1, revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["revision"], "rev1")

    def test_get_documents_available_enum_options_with_params(self) -> None:
        """Test get_documents_available_enum_options with optional parameters."""
        self.api.get_documents_available_enum_options("project1", "status", page_size=30, page_number=0, document_type="spec")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "30")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["type"], "spec")

    # Document parts optional params
    def test_get_document_parts_with_params(self) -> None:
        """Test get_document_parts with optional parameters."""
        self.api.get_document_parts("project1", "space1", "doc1", page_size=50, page_number=0, fields={"revisions": "id,level"}, include="workitem", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[revisions]"], "id,level")
        self.assertEqual(params["include"], "workitem")
        self.assertEqual(params["revision"], "rev1")

    def test_get_document_part_with_params(self) -> None:
        """Test get_document_part with optional parameters."""
        self.api.get_document_part("project1", "space1", "doc1", "part-1", fields={"revisions": "id,type"}, include="workitem", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[revisions]"], "id,type")
        self.assertEqual(params["include"], "workitem")
        self.assertEqual(params["revision"], "rev1")

    # Document branching optional params
    def test_branch_document_with_params(self) -> None:
        """Test branch_document with revision parameter."""
        data: JsonDict = {
            "data": {"type": "documents"},
        }
        self.api.branch_document("project1", "space1", "doc1", data, revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev1")

    # Plans optional params
    def test_get_plans_with_params(self) -> None:
        """Test get_plans with optional parameters."""
        self.api.get_plans("project1", page_size=25, page_number=0, fields={"revisions": "id,name"}, include="parent", query="status:active", sort="name", revision="rev1", templates="tmpl-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "25")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[revisions]"], "id,name")
        self.assertEqual(params["include"], "parent")
        self.assertEqual(params["query"], "status:active")
        self.assertEqual(params["sort"], "name")
        self.assertEqual(params["revision"], "rev1")
        self.assertEqual(params["templates"], "tmpl-1")

    def test_get_plan_with_params(self) -> None:
        """Test get_plan with optional parameters."""
        self.api.get_plan("project1", "plan-1", fields={"revisions": "id,description"}, include="items", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[revisions]"], "id,description")
        self.assertEqual(params["include"], "items")
        self.assertEqual(params["revision"], "rev1")

    def test_get_plan_relationships_with_params(self) -> None:
        """Test get_plan_relationships with optional parameters."""
        self.api.get_plan_relationships("project1", "plan-1", "workitems", page_size=50, page_number=0, fields={"workitems": "id"}, include="target", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id")
        self.assertEqual(params["include"], "target")
        self.assertEqual(params["revision"], "rev1")

    # Pages optional params
    def test_get_page_with_params(self) -> None:
        """Test get_page with optional parameters."""
        self.api.get_page("project1", "space1", "page1", fields={"workitems": "id,title"}, include="attachments", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,title")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["revision"], "rev1")

    def test_get_page_attachment_with_params(self) -> None:
        """Test get_page_attachment with optional parameters."""
        self.api.get_page_attachment("project1", "space1", "page1", "att-1", fields={"workitems": "id,size"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,size")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_get_page_attachment_content_with_revision(self) -> None:
        """Test get_page_attachment_content with revision parameter."""
        self.api.get_page_attachment_content("project1", "space1", "page1", "att-1", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev1")

    # Workitems CRUD optional params
    def test_get_workitems_with_all_params(self) -> None:
        """Test get_workitems with all optional parameters."""
        self.api.get_workitems("project1", page_size=100, page_number=2, fields={"workitems": "id,title"}, include="attachments", query="type:task", sort="-created", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "100")
        self.assertEqual(params["page[number]"], "2")
        self.assertEqual(params["fields[workitems]"], "id,title")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["query"], "type:task")
        self.assertEqual(params["sort"], "-created")
        self.assertEqual(params["revision"], "rev1")

    def test_get_workitem_with_all_params(self) -> None:
        """Test get_workitem with all optional parameters."""
        self.api.get_workitem("project1", "WI-123", fields={"workitems": "id,description"}, include="comments", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,description")
        self.assertEqual(params["include"], "comments")
        self.assertEqual(params["revision"], "rev1")

    # Workitem comments optional params
    def test_get_workitem_comments_with_params(self) -> None:
        """Test get_workitem_comments with optional parameters."""
        self.api.get_workitem_comments("project1", "WI-123", page_size=20, page_number=0, fields={"workitems": "id,text"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,text")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_get_workitem_comment_with_params(self) -> None:
        """Test get_workitem_comment with optional parameters."""
        self.api.get_workitem_comment("project1", "WI-123", "com-1", fields={"workitems": "id,created"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,created")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    # Workitem approvals optional params
    def test_get_workitem_approvals_with_params(self) -> None:
        """Test get_workitem_approvals with optional parameters."""
        self.api.get_workitem_approvals("project1", "WI-123", page_size=10, page_number=0, fields={"workitems": "id,status"}, include="user", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,status")
        self.assertEqual(params["include"], "user")
        self.assertEqual(params["revision"], "rev1")

    def test_get_workitem_approval_with_params(self) -> None:
        """Test get_workitem_approval with optional parameters."""
        self.api.get_workitem_approval("project1", "WI-123", "user1", fields={"workitems": "id,date"}, include="workitem", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,date")
        self.assertEqual(params["include"], "workitem")
        self.assertEqual(params["revision"], "rev1")

    # Workitem attachments optional params
    def test_get_workitem_attachments_with_params(self) -> None:
        """Test get_workitem_attachments with optional parameters."""
        self.api.get_workitem_attachments("project1", "WI-123", page_size=15, page_number=0, fields={"workitems": "id,name"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "15")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_get_workitem_attachment_with_params(self) -> None:
        """Test get_workitem_attachment with optional parameters."""
        self.api.get_workitem_attachment("project1", "WI-123", "att-1", fields={"workitems": "id,size"}, include="workitem", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,size")
        self.assertEqual(params["include"], "workitem")
        self.assertEqual(params["revision"], "rev1")

    def test_get_workitem_attachment_content_with_revision(self) -> None:
        """Test get_workitem_attachment_content with revision parameter."""
        self.api.get_workitem_attachment_content("project1", "WI-123", "att-1", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev1")

    # Workitem links optional params (methods are get_linked_workitems, not get_workitem_linked_workitems)
    def test_get_linked_workitems_with_params(self) -> None:
        """Test get_linked_workitems with optional parameters."""
        self.api.get_linked_workitems("project1", "WI-123", page_size=30, page_number=0, fields={"workitems": "id,role"}, include="target", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "30")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,role")
        self.assertEqual(params["include"], "target")
        self.assertEqual(params["revision"], "rev1")

    def test_get_linked_workitem_with_params(self) -> None:
        """Test get_linked_workitem with optional parameters."""
        self.api.get_linked_workitem("project1", "WI-123", "link-role", "project2", "WI-456", fields={"workitems": "id,suspect"}, include="workitem", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,suspect")
        self.assertEqual(params["include"], "workitem")
        self.assertEqual(params["revision"], "rev1")

    # Note: backlinks don't exist in API - use linkedworkitems instead

    def test_get_externally_linked_workitems_with_params(self) -> None:
        """Test get_externally_linked_workitems with optional parameters."""
        self.api.get_externally_linked_workitems("project1", "WI-123", page_size=20, page_number=0, fields={"workitems": "id,url"}, include="target", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,url")
        self.assertEqual(params["include"], "target")
        self.assertEqual(params["revision"], "rev1")

    def test_get_externally_linked_workitem_with_params(self) -> None:
        """Test get_externally_linked_workitem with optional parameters."""
        self.api.get_externally_linked_workitem("project1", "WI-123", "ext-link", "ext-host", "ext-project", "EXT-1", fields={"workitems": "id"}, include="workitem", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id")
        self.assertEqual(params["include"], "workitem")
        self.assertEqual(params["revision"], "rev1")

    # Workitem test steps optional params (methods are get_test_steps, not get_workitem_test_steps)
    # Note: test step attachments don't exist as separate API - attachments are included in test step data
    def test_get_test_steps_with_params(self) -> None:
        """Test get_test_steps with optional parameters."""
        self.api.get_test_steps("project1", "WI-123", page_size=50, page_number=0, fields={"workitems": "id,description"}, include="attachments", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,description")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["revision"], "rev1")

    def test_get_test_step_with_params(self) -> None:
        """Test get_test_step with optional parameters."""
        self.api.get_test_step("project1", "WI-123", 0, fields={"workitems": "id,expected"}, include="attachments", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,expected")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["revision"], "rev1")

    # Workitem work records optional params (methods are get_work_records, not get_workitem_work_records)
    def test_get_work_records_with_params(self) -> None:
        """Test get_work_records with optional parameters."""
        self.api.get_work_records("project1", "WI-123", page_size=30, page_number=0, fields={"workitems": "id,time"}, include="user", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "30")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,time")
        self.assertEqual(params["include"], "user")
        self.assertEqual(params["revision"], "rev1")

    def test_get_work_record_with_params(self) -> None:
        """Test get_work_record with optional parameters."""
        self.api.get_work_record("project1", "WI-123", "record-1", fields={"workitems": "id,date"}, include="workitem", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,date")
        self.assertEqual(params["include"], "workitem")
        self.assertEqual(params["revision"], "rev1")

    # Misc with query params
    def test_export_tests_to_excel_with_params(self) -> None:
        """Test export_tests_to_excel with optional parameters."""
        self.api.export_tests_to_excel("project1", "TR-1", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev1")

    # Global misc methods optional params
    def test_get_role_with_params(self) -> None:
        """Test get_role with optional parameters."""
        self.api.get_role("admin", fields={"workitems": "id,name"}, include="permissions")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "permissions")

    def test_get_user_group_with_params(self) -> None:
        """Test get_user_group with optional parameters."""
        self.api.get_user_group("group1", fields={"users": "id,name"}, include="users", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[users]"], "id,name")
        self.assertEqual(params["include"], "users")
        self.assertEqual(params["revision"], "rev1")

    def test_get_all_workitems_with_params(self) -> None:
        """Test get_all_workitems with optional parameters."""
        self.api.get_all_workitems(page_size=50, page_number=1, fields={"workitems": "id,title"}, include="author", query="type:req", sort="id", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[workitems]"], "id,title")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["query"], "type:req")
        self.assertEqual(params["sort"], "id")
        self.assertEqual(params["revision"], "rev1")

    def test_update_all_workitems_with_params(self) -> None:
        """Test update_all_workitems with workflow_action parameter."""
        data: JsonDict = {
            "data": [],
        }
        self.api.update_all_workitems(data, workflow_action="approve")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["workflowAction"], "approve")

    def test_get_project_test_parameter_definitions_with_params(self) -> None:
        """Test get_project_test_parameter_definitions with optional parameters."""
        self.api.get_project_test_parameter_definitions("project1", page_size=25, page_number=0, fields={"workitems": "id,name"}, include="values", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "25")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "values")
        self.assertEqual(params["revision"], "rev1")

    def test_get_project_test_parameter_definition_with_params(self) -> None:
        """Test get_project_test_parameter_definition with optional parameters."""
        self.api.get_project_test_parameter_definition("project1", "param1", fields={"workitems": "id,name"}, include="values", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "values")
        self.assertEqual(params["revision"], "rev1")

    # Workitem test parameter definitions optional params
    def test_get_workitem_test_parameter_definitions_with_params(self) -> None:
        """Test get_workitem_test_parameter_definitions with optional parameters."""
        self.api.get_workitem_test_parameter_definitions("project1", "WI-123", page_size=20, page_number=0, fields={"workitems": "id,name"}, include="values", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "values")
        self.assertEqual(params["revision"], "rev1")

    def test_get_workitem_test_parameter_definition_with_params(self) -> None:
        """Test get_workitem_test_parameter_definition with optional parameters."""
        self.api.get_workitem_test_parameter_definition("project1", "WI-123", "param1", fields={"workitems": "id,name"}, include="values", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "values")
        self.assertEqual(params["revision"], "rev1")

    # Workitem CRUD with workflow actions
    def test_update_workitem_with_workflow_action(self) -> None:
        """Test update_workitem with workflow_action parameter."""
        data: JsonDict = {
            "data": {"type": "workitems"},
        }
        self.api.update_workitem("project1", "WI-123", data, workflow_action="approve")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["workflowAction"], "approve")

    def test_update_workitem_with_change_type(self) -> None:
        """Test update_workitem with change_type_to parameter."""
        data: JsonDict = {
            "data": {"type": "workitems"},
        }
        self.api.update_workitem("project1", "WI-123", data, change_type_to="requirement")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["changeTypeTo"], "requirement")

    def test_update_workitems_with_workflow_action(self) -> None:
        """Test update_workitems with workflow_action parameter."""
        data: JsonDict = {
            "data": [],
        }
        self.api.update_workitems("project1", data, workflow_action="reject")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["workflowAction"], "reject")

    def test_update_workitems_with_change_type(self) -> None:
        """Test update_workitems with change_type_to parameter."""
        data: JsonDict = {
            "data": [],
        }
        self.api.update_workitems("project1", data, change_type_to="task")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["changeTypeTo"], "task")

    def test_get_workflow_actions_with_params(self) -> None:
        """Test get_workflow_actions with optional parameters."""
        self.api.get_workflow_actions("project1", "WI-123", page_size=10, page_number=0, revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["revision"], "rev1")

    # Project templates with params
    def test_get_project_templates_with_params(self) -> None:
        """Test get_project_templates with optional parameters."""
        self.api.get_project_templates(page_size=15, page_number=0, fields={"workitems": "id,name"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "15")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,name")

    # Collection relationships with params
    def test_get_collection_relationships_with_params(self) -> None:
        """Test get_collection_relationships with optional parameters."""
        self.api.get_collection_relationships("project1", "col1", "documents", page_size=20, page_number=1, fields={"workitems": "id"}, include="target", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[workitems]"], "id")
        self.assertEqual(params["include"], "target")
        self.assertEqual(params["revision"], "rev1")

    # OSLC resources with params
    def test_get_oslc_resources_with_params(self) -> None:
        """Test get_oslc_resources with optional parameters."""
        self.api.get_oslc_resources("project1", "WI-123", page_size=20, page_number=0, fields={"workitems": "id,url"}, include="workitem", query="type:req", sort="id", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "0")
        self.assertEqual(params["fields[workitems]"], "id,url")
        self.assertEqual(params["include"], "workitem")
        self.assertEqual(params["query"], "type:req")
        self.assertEqual(params["sort"], "id")
        self.assertEqual(params["revision"], "rev1")

    # Document copy with params
    def test_copy_document_with_params(self) -> None:
        """Test copy_document with optional parameters."""
        data: JsonDict = {
            "data": {"type": "documents"},
        }
        self.api.copy_document("project1", "space1", "doc1", data, revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev1")

    # Update document with params
    def test_update_document_with_params(self) -> None:
        """Test update_document with workflow_action parameter."""
        data: JsonDict = {
            "data": {"type": "documents"},
        }
        self.api.update_document("project1", "space1", "doc1", data, workflow_action="publish")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["workflowAction"], "publish")

    # Users with revision param
    def test_get_users_with_revision(self) -> None:
        """Test get_users with revision parameter."""
        self.api.get_users(revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev1")

    def test_get_user_with_revision(self) -> None:
        """Test get_user with revision parameter."""
        self.api.get_user("user1", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["revision"], "rev1")

    # Plan deletion
    def test_delete_plan(self) -> None:
        """Test delete_plan method."""
        self.api.delete_plan("project1", "plan1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        url: str = call_args[0][0]
        self.assertIn("/projects/project1/plans/plan1", url)

    # Testruns delete parameter and test record operations
    def test_delete_testrun_test_parameter(self) -> None:
        """Test delete_testrun_test_parameter method."""
        self.api.delete_testrun_test_parameter("project1", "TR-1", "param1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        url: str = call_args[0][0]
        self.assertIn("/projects/project1/testruns/TR-1/testparameters/param1", url)

    def test_delete_test_step_result_attachment(self) -> None:
        """Test delete_test_step_result_attachment method."""
        self.api.delete_test_step_result_attachment("project1", "TR-1", "project1", "TC-1", 0, 1, "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        url: str = call_args[0][0]
        self.assertIn("/testrecords/", url)
        self.assertIn("/teststepresults/", url)
        self.assertIn("/attachments/att-1", url)

    # Project templates with all params
    def test_get_project_templates_all_params(self) -> None:
        """Test get_project_templates with all optional parameters."""
        self.api.get_project_templates(page_size=10, page_number=1, fields={"teststepresult_attachments": "id,name"}, include="lead")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[teststepresult_attachments]"], "id,name")
        self.assertEqual(params["include"], "lead")

    # Create project enumeration test
    def test_create_project_enumeration(self) -> None:
        """Test create_project_enumeration method."""
        data: JsonDict = {
            "data": {"type": "enumerations"},
        }
        self.api.create_project_enumeration("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        url: str = call_args[0][0]
        self.assertIn("/projects/project1/enumerations", url)


# =============================================================================
# Polarion 2512 New Endpoints Tests
# =============================================================================


class TestLicense(unittest.TestCase):
    """Test license operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_license(self) -> None:
        """Test get_license method."""
        self.api.get_license()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/license", call_args[0][0])

    def test_get_license_with_params(self) -> None:
        """Test get_license with fields parameter."""
        self.api.get_license(fields={"enumerations": "id,type"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,type")

    def test_update_license(self) -> None:
        """Test update_license method."""
        data: JsonDict = {
            "data": {"type": "license"},
        }
        self.api.update_license(data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/license", call_args[0][0])

    def test_get_license_slots(self) -> None:
        """Test get_license_slots method."""
        self.api.get_license_slots("type-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/license/types/type-1/slots", call_args[0][0])

    def test_get_license_slots_with_params(self) -> None:
        """Test get_license_slots with optional parameters."""
        self.api.get_license_slots("type-1", page_size=50, page_number=1, fields={"enumerations": "id,name"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[enumerations]"], "id,name")

    def test_get_license_slot(self) -> None:
        """Test get_license_slot method."""
        self.api.get_license_slot("type-1", "model-1", "group-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/license/types/type-1/slots/model-1/group-1", call_args[0][0])

    def test_create_license_slots(self) -> None:
        """Test create_license_slots method."""
        data: JsonDict = {
            "data": [{"type": "license_slots"}],
        }
        self.api.create_license_slots("type-1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/license/types/type-1/slots", call_args[0][0])

    def test_delete_license_slots(self) -> None:
        """Test delete_license_slots method."""
        data: JsonDict = {
            "data": [{"type": "license_slots", "id": "slot1"}],
        }
        self.api.delete_license_slots("type-1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/license/types/type-1/slots", call_args[0][0])

    def test_get_license_assignments(self) -> None:
        """Test get_license_assignments method."""
        self.api.get_license_assignments()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/license/assignments", call_args[0][0])

    def test_get_license_assignments_for_user(self) -> None:
        """Test get_license_assignments_for_user method."""
        self.api.get_license_assignments_for_user("user1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/license/assignments/user1", call_args[0][0])

    def test_update_license_assignments(self) -> None:
        """Test update_license_assignments method."""
        data: JsonDict = {
            "data": {"type": "license_assignments"},
        }
        self.api.update_license_assignments(data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/license/assignments", call_args[0][0])


class TestCustomFields(unittest.TestCase):
    """Test custom fields operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_global_custom_fields(self) -> None:
        """Test get_global_custom_fields method."""
        self.api.get_global_custom_fields("workitems", "task")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/customfields/workitems/task", call_args[0][0])

    def test_get_global_custom_fields_with_params(self) -> None:
        """Test get_global_custom_fields with optional parameters."""
        self.api.get_global_custom_fields("workitems", "task", fields={"users": "id,name"}, include="values")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[users]"], "id,name")
        self.assertEqual(params["include"], "values")

    def test_create_global_custom_fields(self) -> None:
        """Test create_global_custom_fields method."""
        data: JsonDict = {
            "data": [{"type": "customfields"}],
        }
        self.api.create_global_custom_fields(data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/customfields", call_args[0][0])

    def test_update_global_custom_fields(self) -> None:
        """Test update_global_custom_fields method."""
        data: JsonDict = {
            "data": {"type": "customfields"},
        }
        self.api.update_global_custom_fields("workitems", "task", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/customfields/workitems/task", call_args[0][0])

    def test_delete_global_custom_fields(self) -> None:
        """Test delete_global_custom_fields method."""
        self.api.delete_global_custom_fields("workitems", "task")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/customfields/workitems/task", call_args[0][0])

    def test_get_project_custom_fields(self) -> None:
        """Test get_project_custom_fields method."""
        self.api.get_project_custom_fields("project1", "workitems", "task")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/customfields/workitems/task", call_args[0][0])

    def test_get_project_custom_fields_with_params(self) -> None:
        """Test get_project_custom_fields with optional parameters."""
        self.api.get_project_custom_fields("project1", "workitems", "task", fields={"users": "id,name"}, include="values")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[users]"], "id,name")
        self.assertEqual(params["include"], "values")

    def test_create_project_custom_fields(self) -> None:
        """Test create_project_custom_fields method."""
        data: JsonDict = {
            "data": [{"type": "customfields"}],
        }
        self.api.create_project_custom_fields("project1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/customfields", call_args[0][0])

    def test_update_project_custom_field(self) -> None:
        """Test update_project_custom_field method."""
        data: JsonDict = {
            "data": {"type": "customfields"},
        }
        self.api.update_project_custom_field("project1", "workitems", "task", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/customfields/workitems/task", call_args[0][0])

    def test_delete_project_custom_fields(self) -> None:
        """Test delete_project_custom_fields method."""
        self.api.delete_project_custom_fields("project1", "workitems", "task")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/customfields/workitems/task", call_args[0][0])


class TestJobsNew(unittest.TestCase):
    """Test new jobs operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_jobs(self) -> None:
        """Test get_jobs method."""
        self.api.get_jobs()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/jobs", call_args[0][0])

    def test_get_jobs_with_params(self) -> None:
        """Test get_jobs with optional parameters."""
        self.api.get_jobs(page_size=50, page_number=1, fields={"jobs": "id,status"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[jobs]"], "id,status")

    def test_execute_job(self) -> None:
        """Test execute_job method."""
        data: JsonDict = {
            "data": {"type": "jobs"},
        }
        self.api.execute_job(data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/jobs", call_args[0][0])

    def test_get_job_log_content(self) -> None:
        """Test get_job_log_content method."""
        self.api.get_job_log_content("job-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/jobs/job-1/log/content", call_args[0][0])


class TestDocumentsNew(unittest.TestCase):
    """Test new documents operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_all_documents(self) -> None:
        """Test get_all_documents method."""
        self.api.get_all_documents()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/all/documents", call_args[0][0])

    def test_get_all_documents_with_params(self) -> None:
        """Test get_all_documents with optional parameters."""
        self.api.get_all_documents(page_size=50, page_number=1, fields={"jobs": "id,title"}, query="type:spec")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[jobs]"], "id,title")
        self.assertEqual(params["query"], "type:spec")

    def test_get_project_documents(self) -> None:
        """Test get_project_documents method."""
        self.api.get_project_documents("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/documents", call_args[0][0])

    def test_get_space_documents(self) -> None:
        """Test get_space_documents method."""
        self.api.get_space_documents("project1", "space1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space1/documents", call_args[0][0])

    def test_move_document_parts(self) -> None:
        """Test move_document_parts method."""
        data: JsonDict = {
            "data": {"type": "parts"},
        }
        self.api.move_document_parts("project1", "space1", "doc1", "part-1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space1/documents/doc1/parts/part-1/actions/move", call_args[0][0])


class TestPagesNew(unittest.TestCase):
    """Test new pages operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_all_pages(self) -> None:
        """Test get_all_pages method."""
        self.api.get_all_pages()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/all/pages", call_args[0][0])

    def test_get_global_pages(self) -> None:
        """Test get_global_pages method."""
        self.api.get_global_pages()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/pages", call_args[0][0])

    def test_get_repository_space_pages(self) -> None:
        """Test get_repository_space_pages method."""
        self.api.get_repository_space_pages("space1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/spaces/space1/pages", call_args[0][0])

    def test_get_project_pages(self) -> None:
        """Test get_project_pages method."""
        self.api.get_project_pages("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/pages", call_args[0][0])

    def test_get_space_pages(self) -> None:
        """Test get_space_pages method."""
        self.api.get_space_pages("project1", "space1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space1/pages", call_args[0][0])

    def test_create_page(self) -> None:
        """Test create_page method."""
        data: JsonDict = {
            "data": {"type": "pages"},
        }
        self.api.create_page("project1", "space1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space1/pages", call_args[0][0])

    def test_delete_page(self) -> None:
        """Test delete_page method."""
        self.api.delete_page("project1", "space1", "page1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1", call_args[0][0])

    def test_get_page_attachments(self) -> None:
        """Test get_page_attachments method."""
        self.api.get_page_attachments("project1", "space1", "page1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/attachments", call_args[0][0])

    def test_update_page_attachment(self) -> None:
        """Test update_page_attachment method."""
        data: JsonDict = {
            "data": {"type": "attachments"},
        }
        self.api.update_page_attachment("project1", "space1", "page1", "att-1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/attachments/att-1", call_args[0][0])

    def test_delete_page_attachment(self) -> None:
        """Test delete_page_attachment method."""
        self.api.delete_page_attachment("project1", "space1", "page1", "att-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/attachments/att-1", call_args[0][0])

    def test_get_page_comments(self) -> None:
        """Test get_page_comments method."""
        self.api.get_page_comments("project1", "space1", "page1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/comments", call_args[0][0])

    def test_get_page_comment(self) -> None:
        """Test get_page_comment method."""
        self.api.get_page_comment("project1", "space1", "page1", "comment-1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/comments/comment-1", call_args[0][0])

    def test_create_page_comment(self) -> None:
        """Test create_page_comment method."""
        data: JsonDict = {
            "data": {"type": "comments"},
        }
        self.api.create_page_comment("project1", "space1", "page1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/comments", call_args[0][0])

    def test_update_page_comment(self) -> None:
        """Test update_page_comment method."""
        data: JsonDict = {
            "data": {"type": "comments"},
        }
        self.api.update_page_comment("project1", "space1", "page1", "comment-1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/comments/comment-1", call_args[0][0])

    def test_get_page_relationships(self) -> None:
        """Test get_page_relationships method."""
        self.api.get_page_relationships("project1", "space1", "page1", "author")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/relationships/author", call_args[0][0])

    def test_create_page_relationships(self) -> None:
        """Test create_page_relationships method."""
        data: JsonDict = {
            "data": [{"type": "users"}],
        }
        self.api.create_page_relationships("project1", "space1", "page1", "watchers", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/relationships/watchers", call_args[0][0])

    def test_update_page_relationships(self) -> None:
        """Test update_page_relationships method."""
        data: JsonDict = {
            "data": [{"type": "users"}],
        }
        self.api.update_page_relationships("project1", "space1", "page1", "watchers", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_patch.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/relationships/watchers", call_args[0][0])

    def test_delete_page_relationships(self) -> None:
        """Test delete_page_relationships method."""
        data: JsonDict = {
            "data": [{"type": "users", "id": "user1"}],
        }
        self.api.delete_page_relationships("project1", "space1", "page1", "watchers", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_delete.call_args
        self.assertIn("/projects/project1/spaces/space1/pages/page1/relationships/watchers", call_args[0][0])


class TestProjectsNew(unittest.TestCase):
    """Test new projects operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_reuse_collection(self) -> None:
        """Test reuse_collection method."""
        data: JsonDict = {
            "data": {"type": "collections"},
        }
        self.api.reuse_collection("project1", "collection-1", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/collections/collection-1/actions/reuse", call_args[0][0])

    def test_get_project_enumerations(self) -> None:
        """Test get_project_enumerations method."""
        self.api.get_project_enumerations("project1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/enumerations", call_args[0][0])

    def test_get_project_enumerations_with_params(self) -> None:
        """Test get_project_enumerations with optional parameters."""
        self.api.get_project_enumerations("project1", page_size=50, page_number=1, fields={"enumerations": "id,name"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[enumerations]"], "id,name")

    def test_get_project_fields_metadata(self) -> None:
        """Test get_project_fields_metadata method."""
        self.api.get_project_fields_metadata("project1", "workitems")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/actions/getFieldsMetadata", call_args[0][0])
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["resourceType"], "workitems")

    def test_get_project_fields_metadata_with_params(self) -> None:
        """Test get_project_fields_metadata with target_type parameter."""
        self.api.get_project_fields_metadata("project1", resource_type="workitems", target_type="task")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["resourceType"], "workitems")
        self.assertEqual(params["targetType"], "task")


class TestGlobalMiscNew(unittest.TestCase):
    """Test new global misc operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_global_enumerations(self) -> None:
        """Test get_global_enumerations method."""
        self.api.get_global_enumerations()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/enumerations", call_args[0][0])

    def test_get_global_enumerations_with_params(self) -> None:
        """Test get_global_enumerations with optional parameters."""
        self.api.get_global_enumerations(page_size=50, page_number=1, fields={"enumerations": "id,name"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[enumerations]"], "id,name")

    def test_get_global_fields_metadata(self) -> None:
        """Test get_global_fields_metadata method."""
        self.api.get_global_fields_metadata("workitems")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/actions/getFieldsMetadata", call_args[0][0])
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["resourceType"], "workitems")

    def test_get_global_fields_metadata_with_params(self) -> None:
        """Test get_global_fields_metadata with target_type parameter."""
        self.api.get_global_fields_metadata(resource_type="workitems", target_type="task")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["resourceType"], "workitems")
        self.assertEqual(params["targetType"], "task")

    def test_get_metadata(self) -> None:
        """Test get_metadata method."""
        self.api.get_metadata()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/metadata", call_args[0][0])

    def test_get_metadata_with_params(self) -> None:
        """Test get_metadata with fields parameter."""
        self.api.get_metadata(fields={"enumerations": "id,version"})
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[enumerations]"], "id,version")


class TestUsersNew(unittest.TestCase):
    """Test new users operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_current_user(self) -> None:
        """Test get_current_user method."""
        self.api.get_current_user()
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/user", call_args[0][0])

    def test_get_current_user_with_params(self) -> None:
        """Test get_current_user with optional parameters."""
        self.api.get_current_user(fields={"users": "id,name"}, include="groups")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[users]"], "id,name")
        self.assertEqual(params["include"], "groups")


class TestWorkitemsLinksNew(unittest.TestCase):
    """Test new workitems links operations (new in Polarion 2512)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_backlinked_workitems(self) -> None:
        """Test get_backlinked_workitems method."""
        self.api.get_backlinked_workitems("project1", "WI-123")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        self.assertIn("/projects/project1/workitems/WI-123/backlinkedworkitems", call_args[0][0])

    def test_get_backlinked_workitems_with_params(self) -> None:
        """Test get_backlinked_workitems with optional parameters."""
        self.api.get_backlinked_workitems("project1", "WI-123", page_size=50, page_number=1, fields={"workitems": "id,title"}, include="author", revision="rev1")
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "50")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[workitems]"], "id,title")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "rev1")

    def test_create_backlinked_workitems(self) -> None:
        """Test create_backlinked_workitems method."""
        data: JsonDict = {
            "data": [{"type": "workitems"}],
        }
        self.api.create_backlinked_workitems("project1", "WI-123", data)
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_post.call_args
        self.assertIn("/projects/project1/workitems/WI-123/backlinkedworkitems", call_args[0][0])


# =============================================================================
# Optional Parameters Coverage Tests
# =============================================================================


class TestPagesOptionalParams(unittest.TestCase):
    """Test pages methods with all optional parameters to achieve full coverage."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_all_pages_with_all_params(self) -> None:
        """Test get_all_pages with all optional parameters."""
        self.api.get_all_pages(
            page_size=10,
            page_number=2,
            fields={"workitems": "id,title"},
            include="author",
            query="type:page",
            sort="title",
            revision="1234",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "2")
        self.assertEqual(params["fields[workitems]"], "id,title")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["query"], "type:page")
        self.assertEqual(params["sort"], "title")
        self.assertEqual(params["revision"], "1234")

    def test_get_global_pages_with_all_params(self) -> None:
        """Test get_global_pages with all optional parameters."""
        self.api.get_global_pages(
            page_size=20,
            page_number=3,
            fields={"workitems": "id,name"},
            include="project",
            query="status:active",
            sort="name",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "3")
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "project")
        self.assertEqual(params["query"], "status:active")
        self.assertEqual(params["sort"], "name")

    def test_get_repository_space_pages_with_all_params(self) -> None:
        """Test get_repository_space_pages with all optional parameters."""
        self.api.get_repository_space_pages(
            space_id="space1",
            page_size=15,
            page_number=1,
            fields={"workitems": "id"},
            include="attachments",
            query="name:test",
            sort="id",
            revision="5678",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "15")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[workitems]"], "id")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["query"], "name:test")
        self.assertEqual(params["sort"], "id")
        self.assertEqual(params["revision"], "5678")

    def test_get_project_pages_with_all_params(self) -> None:
        """Test get_project_pages with all optional parameters."""
        self.api.get_project_pages(
            project_id="project1",
            page_size=25,
            page_number=4,
            fields={"workitems": "id,title,author"},
            include="comments",
            query="type:wiki",
            sort="created",
            revision="9999",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "25")
        self.assertEqual(params["page[number]"], "4")
        self.assertEqual(params["fields[workitems]"], "id,title,author")
        self.assertEqual(params["include"], "comments")
        self.assertEqual(params["query"], "type:wiki")
        self.assertEqual(params["sort"], "created")
        self.assertEqual(params["revision"], "9999")

    def test_get_space_pages_with_all_params(self) -> None:
        """Test get_space_pages with all optional parameters."""
        self.api.get_space_pages(
            project_id="project1",
            space_id="space1",
            page_size=30,
            page_number=5,
            fields={"workitems": "id,name,content"},
            include="author,project",
            query="status:draft",
            sort="updated",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "30")
        self.assertEqual(params["page[number]"], "5")
        self.assertEqual(params["fields[workitems]"], "id,name,content")
        self.assertEqual(params["include"], "author,project")
        self.assertEqual(params["query"], "status:draft")
        self.assertEqual(params["sort"], "updated")

    def test_get_page_with_all_params(self) -> None:
        """Test get_page with all optional parameters."""
        self.api.get_page(
            project_id="project1",
            space_id="space1",
            page_name="page1",
            fields={"workitems": "id,title"},
            include="attachments",
            revision="2222",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,title")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["revision"], "2222")

    def test_get_page_attachments_with_all_params(self) -> None:
        """Test get_page_attachments with all optional parameters."""
        self.api.get_page_attachments(
            project_id="project1",
            space_id="space1",
            page_name="page1",
            page_size=10,
            page_number=1,
            fields={"workitems": "id,fileName"},
            include="author",
            revision="3333",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[workitems]"], "id,fileName")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "3333")

    def test_get_page_attachment_with_all_params(self) -> None:
        """Test get_page_attachment with all optional parameters."""
        self.api.get_page_attachment(
            project_id="project1",
            space_id="space1",
            page_name="page1",
            attachment_id="att-1",
            fields={"workitems": "id,fileName,length"},
            include="author",
            revision="4444",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,fileName,length")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "4444")

    def test_get_page_comments_with_all_params(self) -> None:
        """Test get_page_comments with all optional parameters."""
        self.api.get_page_comments(
            project_id="project1",
            space_id="space1",
            page_name="page1",
            page_size=5,
            page_number=2,
            fields={"workitems": "id,text"},
            include="author",
            revision="5555",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "5")
        self.assertEqual(params["page[number]"], "2")
        self.assertEqual(params["fields[workitems]"], "id,text")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["revision"], "5555")

    def test_get_page_comment_with_all_params(self) -> None:
        """Test get_page_comment with all optional parameters."""
        self.api.get_page_comment(
            project_id="project1",
            space_id="space1",
            page_name="page1",
            comment_id="comment-1",
            fields={"workitems": "id,text,created"},
            include="author,replies",
            revision="6666",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,text,created")
        self.assertEqual(params["include"], "author,replies")
        self.assertEqual(params["revision"], "6666")


class TestDocumentsOptionalParams(unittest.TestCase):
    """Test documents methods with all optional parameters to achieve full coverage."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_all_documents_with_all_params(self) -> None:
        """Test get_all_documents with all optional parameters."""
        self.api.get_all_documents(
            page_size=10,
            page_number=2,
            fields={"workitems": "id,title"},
            include="author",
            query="type:requirement",
            sort="title",
            revision="1234",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "2")
        self.assertEqual(params["fields[workitems]"], "id,title")
        self.assertEqual(params["include"], "author")
        self.assertEqual(params["query"], "type:requirement")
        self.assertEqual(params["sort"], "title")
        self.assertEqual(params["revision"], "1234")

    def test_get_project_documents_with_all_params(self) -> None:
        """Test get_project_documents with all optional parameters."""
        self.api.get_project_documents(
            project_id="project1",
            page_size=20,
            page_number=3,
            fields={"workitems": "id,name"},
            include="project",
            query="status:approved",
            sort="name",
            revision="5678",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "20")
        self.assertEqual(params["page[number]"], "3")
        self.assertEqual(params["fields[workitems]"], "id,name")
        self.assertEqual(params["include"], "project")
        self.assertEqual(params["query"], "status:approved")
        self.assertEqual(params["sort"], "name")
        self.assertEqual(params["revision"], "5678")

    def test_get_space_documents_with_all_params(self) -> None:
        """Test get_space_documents with all optional parameters."""
        self.api.get_space_documents(
            project_id="project1",
            space_id="space1",
            page_size=15,
            page_number=1,
            fields={"workitems": "id"},
            include="attachments",
            query="name:spec",
            sort="id",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "15")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[workitems]"], "id")
        self.assertEqual(params["include"], "attachments")
        self.assertEqual(params["query"], "name:spec")
        self.assertEqual(params["sort"], "id")


class TestLicenseOptionalParams(unittest.TestCase):
    """Test license methods with all optional parameters to achieve full coverage."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        self.mock_connection: MagicMock = MagicMock()
        self.api: PolarionApiV1 = PolarionApiV1(self.mock_connection)

    def test_get_license_with_all_params(self) -> None:
        """Test get_license with all optional parameters."""
        self.api.get_license(
            fields={"workitems": "id,type"},
            include="slots",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,type")
        self.assertEqual(params["include"], "slots")

    def test_get_license_slots_with_all_params(self) -> None:
        """Test get_license_slots with all optional parameters."""
        self.api.get_license_slots(
            type_id="type1",
            page_size=10,
            page_number=1,
            fields={"workitems": "id,user"},
            include="user",
            revision="1234",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "10")
        self.assertEqual(params["page[number]"], "1")
        self.assertEqual(params["fields[workitems]"], "id,user")
        self.assertEqual(params["include"], "user")
        self.assertEqual(params["revision"], "1234")

    def test_get_license_slot_with_all_params(self) -> None:
        """Test get_license_slot with all optional parameters."""
        self.api.get_license_slot(
            type_id="type1",
            model="model1",
            group="group1",
            fields={"workitems": "id,status"},
            include="user",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[workitems]"], "id,status")
        self.assertEqual(params["include"], "user")

    def test_get_license_assignments_with_all_params(self) -> None:
        """Test get_license_assignments with all optional parameters."""
        self.api.get_license_assignments(
            page_size=5,
            page_number=2,
            fields={"workitems": "id,user"},
            include="user",
            active_only=True,
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["page[size]"], "5")
        self.assertEqual(params["page[number]"], "2")
        self.assertEqual(params["fields[workitems]"], "id,user")
        self.assertEqual(params["include"], "user")
        self.assertEqual(params["activeOnly"], "true")

    def test_get_license_assignments_for_user_with_all_params(self) -> None:
        """Test get_license_assignments_for_user with all optional parameters."""
        self.api.get_license_assignments_for_user(
            user_id="user1",
            fields={"users": "id,type"},
            include="licenseType",
        )
        call_args: tuple[tuple[str, ...], dict[str, object]] = self.mock_connection.api_request_get.call_args
        params: dict[str, str] = call_args[1]["params"]  # type: ignore[assignment]
        self.assertEqual(params["fields[users]"], "id,type")
        self.assertEqual(params["include"], "licenseType")


if __name__ == "__main__":
    unittest.main()
