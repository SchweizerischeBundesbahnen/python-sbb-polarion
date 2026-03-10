"""Common implementation for SQL DB connections."""

import logging
from typing import Any, TypedDict, Unpack

import psycopg2
import psycopg2.extensions

from python_sbb_polarion.types import JsonValue


logger = logging.getLogger(__name__)


class SqlConnectionConfig(TypedDict, total=False):
    """Configuration parameters for SQL database connection."""

    host: str
    port: int
    database: str
    user: str
    password: str


class SqlDatabaseConnection:
    """SQL database connection manager for PostgreSQL databases."""

    def __init__(self, **kwargs: Unpack[SqlConnectionConfig]) -> None:
        """Initialize PostgreSQL database connection.

        Args:
            **kwargs: Database connection parameters (host, port, database, user, password)
                host: Database server hostname (default: localhost)
                port: Database server port (default: 5432)
                database: Database name (default: postgres)
                user: Database username (default: postgres)
                password: Database password (default: empty string)

        Raises:
            psycopg2.DatabaseError: If database connection fails
        """
        host: str = kwargs.get("host", "localhost")
        port: int = kwargs.get("port", 5432)
        database: str = kwargs.get("database", "postgres")
        user: str = kwargs.get("user", "postgres")
        password: str = kwargs.get("password", "")

        params: dict[str, Any] = {  # psp-ignore: PSP017 - psycopg2.connect requires Any
            "database": database,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        try:
            self.connection: psycopg2.extensions.connection = psycopg2.connect(**params)
            self.connection.autocommit = True
            logger.info("DB connected")
        except psycopg2.DatabaseError:
            logger.exception("Cannot connect to database")
            raise

        self.cursor: psycopg2.extensions.cursor = self.connection.cursor()
        version_result: list[tuple[JsonValue, ...]] | None = self.execute_query("SHOW server_version")
        if version_result is not None and version_result:
            logger.info("PostgreSQL server version: %s", version_result[0][0])

    def __del__(self) -> None:
        """Clean up database connections on object destruction."""
        if hasattr(self, "cursor") and self.cursor:
            try:
                self.cursor.close()
            except psycopg2.DatabaseError:
                logger.exception("Failed to close database cursor")
        if hasattr(self, "connection") and self.connection:
            try:
                self.connection.close()
                logger.debug("Database connection closed")
            except psycopg2.DatabaseError:
                logger.exception("Failed to close database connection")

    def execute_query(self, query: str, print_info: bool = False, fetchall: bool = True) -> list[tuple[JsonValue, ...]] | None:
        """Execute a SQL query.

        Args:
            query: SQL query string to execute
            print_info: Enable debug logging for query execution (default: False)
            fetchall: Fetch all results if True, otherwise return None (default: True)

        Returns:
            list[tuple[JsonValue, ...]] | None: List of tuples containing query results if fetchall is True, None otherwise

        Raises:
            psycopg2.DatabaseError: If query execution fails
        """
        if print_info:
            logger.debug("Database executing query...")
        try:
            self.cursor.execute(query)
            if fetchall:
                if print_info:
                    logger.debug("Database fetching response...")
                result: list[tuple[JsonValue, ...]] = self.cursor.fetchall()
                return list(result) if result else []
            return None  # noqa: TRY300
        except psycopg2.DatabaseError:
            logger.exception("Query execution failed: %s", query)
            raise
