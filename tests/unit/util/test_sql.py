"""Unit tests for SQL database connection utilities."""

import unittest
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock, patch

from python_sbb_polarion.util.sql import SqlDatabaseConnection


if TYPE_CHECKING:
    from python_sbb_polarion.util.sql import SqlConnectionConfig


class TestSqlDatabaseConnection(unittest.TestCase):
    """Test SqlDatabaseConnection class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.default_params = {"host": "localhost", "port": 5432, "database": "postgres", "user": "postgres", "password": "testpass"}

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_init_with_defaults(self, mock_connect: Mock) -> None:
        """Test initialization with default parameters."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()

        # Verify connection was created with defaults
        mock_connect.assert_called_once_with(database="postgres", user="postgres", password="", host="localhost", port=5432)
        # Verify autocommit was enabled
        self.assertTrue(mock_conn.autocommit)
        # Verify cursor was created
        mock_conn.cursor.assert_called_once()
        # Verify server version query was executed
        mock_cursor.execute.assert_called_once_with("SHOW server_version")

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_init_with_custom_params(self, mock_connect: Mock) -> None:
        """Test initialization with custom parameters."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        custom_params: SqlConnectionConfig = {"host": "db.example.com", "port": 5433, "database": "mydb", "user": "myuser", "password": "mypass"}

        conn = SqlDatabaseConnection(**custom_params)

        # Verify connection was created with custom params
        mock_connect.assert_called_once_with(**custom_params)

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_init_partial_params(self, mock_connect: Mock) -> None:
        """Test initialization with partial custom parameters."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection(host="custom.host", database="customdb")

        # Verify mix of custom and default params
        expected_params: dict[str, str | int] = {"host": "custom.host", "port": 5432, "database": "customdb", "user": "postgres", "password": ""}
        mock_connect.assert_called_once_with(**expected_params)

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    @patch("python_sbb_polarion.util.sql.logger")
    def test_init_connection_error(self, mock_logger: Mock, mock_connect: Mock) -> None:
        """Test handling of connection errors."""
        import psycopg2

        mock_connect.side_effect = psycopg2.DatabaseError("Connection failed")

        # Now the code properly raises psycopg2.DatabaseError
        with self.assertRaises(psycopg2.DatabaseError):
            SqlDatabaseConnection()

        mock_logger.exception.assert_called_once_with("Cannot connect to database")

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_execute_query_with_fetchall(self, mock_connect: Mock) -> None:
        """Test execute_query with fetchall=True."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [("PostgreSQL 15.0",)],  # For server version check
            [("row1",), ("row2",), ("row3",)],  # For our query
        ]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        result: list[tuple[Any, ...]] | None = conn.execute_query("SELECT * FROM test_table")

        # Verify query was executed
        self.assertEqual(mock_cursor.execute.call_count, 2)  # Server version + our query
        self.assertEqual(mock_cursor.execute.call_args_list[1][0][0], "SELECT * FROM test_table")
        # Verify fetchall was called
        self.assertEqual(result, [("row1",), ("row2",), ("row3",)])

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_execute_query_without_fetchall(self, mock_connect: Mock) -> None:
        """Test execute_query with fetchall=False."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        result: list[tuple[Any, ...]] | None = conn.execute_query("INSERT INTO test_table VALUES (1)", fetchall=False)

        # Verify query was executed
        self.assertEqual(mock_cursor.execute.call_count, 2)
        # Verify result is None when fetchall=False
        self.assertIsNone(result)

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    @patch("python_sbb_polarion.util.sql.logger")
    def test_execute_query_with_print_info(self, mock_logger: Mock, mock_connect: Mock) -> None:
        """Test execute_query with print_info=True."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [[("PostgreSQL 15.0",)], [("result",)]]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        conn.execute_query("SELECT * FROM test", print_info=True)

        # Verify debug messages were logged (expecting "Database executing query..." and "Database fetching response...")
        debug_calls: list[Mock] = [c for c in mock_logger.debug.call_args_list if "Database" in str(c) or "database" in str(c)]
        self.assertGreaterEqual(len(debug_calls), 2)

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_execute_query_empty_result(self, mock_connect: Mock) -> None:
        """Test execute_query with empty result set."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [[("PostgreSQL 15.0",)], []]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        result: list[tuple[Any, ...]] | None = conn.execute_query("SELECT * FROM empty_table")

        self.assertEqual(result, [])

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_execute_query_multiple_calls(self, mock_connect: Mock) -> None:
        """Test multiple execute_query calls."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [("PostgreSQL 15.0",)],  # Server version
            [("result1",)],
            [("result2",)],
            [("result3",)],
        ]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        result1: list[tuple[Any, ...]] | None = conn.execute_query("SELECT 1")
        result2: list[tuple[Any, ...]] | None = conn.execute_query("SELECT 2")
        result3: list[tuple[Any, ...]] | None = conn.execute_query("SELECT 3")

        self.assertEqual(result1, [("result1",)])
        self.assertEqual(result2, [("result2",)])
        self.assertEqual(result3, [("result3",)])
        self.assertEqual(mock_cursor.execute.call_count, 4)  # Server version + 3 queries

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_destructor_closes_connection(self, mock_connect: Mock) -> None:
        """Test that __del__ closes cursor and connection."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        conn.__del__()

        # Verify cursor and connection were closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_autocommit_enabled(self, mock_connect: Mock) -> None:
        """Test that autocommit is enabled on connection."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()

        # Verify autocommit was set to True
        self.assertTrue(mock_conn.autocommit)

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    @patch("python_sbb_polarion.util.sql.logger")
    def test_server_version_logged(self, mock_logger: Mock, mock_connect: Mock) -> None:
        """Test that server version is logged during initialization."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()

        # Verify server version was logged with lazy formatting
        info_calls: list[Mock] = [c for c in mock_logger.info.call_args_list if "PostgreSQL server version" in str(c)]
        self.assertEqual(len(info_calls), 1)
        # Check that it was called with proper lazy formatting
        mock_logger.info.assert_called_with("PostgreSQL server version: %s", "PostgreSQL 15.0")

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_connection_attributes(self, mock_connect: Mock) -> None:
        """Test that connection and cursor are accessible as attributes."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()

        self.assertEqual(conn.connection, mock_conn)
        self.assertEqual(conn.cursor, mock_cursor)

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_destructor_cursor_close_error(self, mock_connect: Mock) -> None:
        """Test destructor handles cursor close errors gracefully."""
        import psycopg2

        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_cursor.close.side_effect = psycopg2.DatabaseError("Cursor close error")
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        # Should not raise exception
        conn.__del__()

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_destructor_connection_close_error(self, mock_connect: Mock) -> None:
        """Test destructor handles connection close errors gracefully."""
        import psycopg2

        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_conn.close.side_effect = psycopg2.DatabaseError("Connection close error")
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        # Should not raise exception
        conn.__del__()

    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_execute_query_error(self, mock_connect: Mock) -> None:
        """Test execute_query handles database errors."""
        import psycopg2

        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("PostgreSQL 15.0",)]
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()
        mock_cursor.execute.side_effect = psycopg2.DatabaseError("Query execution error")

        with self.assertRaises(psycopg2.DatabaseError):
            conn.execute_query("SELECT invalid_query")

    @patch("python_sbb_polarion.util.sql.logger")
    @patch("python_sbb_polarion.util.sql.psycopg2.connect")
    def test_init_server_version_query_fails(self, mock_connect: Mock, mock_logger: Mock) -> None:
        """Test initialization when server version query returns empty result."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        # Server version query returns empty result
        mock_cursor.fetchall.return_value = []
        mock_connect.return_value = mock_conn

        conn = SqlDatabaseConnection()

        # Verify no version was logged (only DB connected)
        info_calls: list[Mock] = [call for call in mock_logger.info.call_args_list if "PostgreSQL server version" in str(call)]
        self.assertEqual(len(info_calls), 0)

    def test_destructor_without_attributes(self) -> None:
        """Test destructor when object has no cursor or connection attributes."""
        # Create a minimal object without going through __init__
        conn: SqlDatabaseConnection = object.__new__(SqlDatabaseConnection)
        # Should not raise exception even without cursor/connection attributes
        conn.__del__()


if __name__ == "__main__":
    unittest.main()
