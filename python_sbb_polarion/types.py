"""Common type definitions for the python-sbb-polarion library."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import StrEnum
from typing import IO, Protocol, TypeAlias, TypeVar


class MediaType(StrEnum):
    """Standard MIME media types used across the library.

    Using StrEnum allows these values to be used directly as strings
    in HTTP headers while providing type safety and avoiding duplication.
    """

    JSON = "application/json"
    HTML = "text/html"
    XML = "application/xml"
    PDF = "application/pdf"
    PLAIN = "text/plain"
    OCTET_STREAM = "application/octet-stream"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ZIP = "application/zip"
    ANY = "*/*"


class Header(StrEnum):
    """Standard HTTP header names."""

    ACCEPT = "Accept"
    AUTHORIZATION = "Authorization"
    CONTENT_TYPE = "Content-Type"
    X_API_KEY = "X-API-Key"


class AuthScheme(StrEnum):
    """HTTP authentication schemes."""

    BEARER = "Bearer"
    BASIC = "Basic"


# Generic protocol for file-like objects that provide a read() method.
_T_co = TypeVar("_T_co", covariant=True)


class SupportsRead(Protocol[_T_co]):
    """Protocol for file-like objects that support read() method."""

    def read(self, size: int = -1) -> _T_co: ...


# JSON-compatible types
JsonPrimitive: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonPrimitive | dict[str, "JsonValue"] | list["JsonValue"]
JsonDict: TypeAlias = dict[str, JsonValue]
JsonList: TypeAlias = list[JsonValue]

# JSON:API sparse fieldsets type
# Used for ?fields[workitems]=@all&fields[documents]=id,title format
# See: https://jsonapi.org/format/#fetching-sparse-fieldsets
SparseFields: TypeAlias = dict[str, str]


# File upload types for HTTP requests (compatible with requests library)
# Note: SupportsRead[bytes] provides type safety for any file-like object with read().
# The requests library uses duck typing at runtime and accepts any object with read().
FileContent: TypeAlias = str | bytes | IO[bytes] | IO[str] | SupportsRead[bytes]

# FileTuple represents the various tuple formats accepted by requests for file uploads:
# - (filename, content)
# - (filename, content, content_type)
# - (filename, content, content_type, headers)
FileTuple: TypeAlias = tuple[str | None, FileContent] | tuple[str | None, FileContent, str] | tuple[str | None, FileContent, str, Mapping[str, str]]

# Match requests library expectations exactly:
# - For dict values: FileContent or FileTuple only (no Sequence)
# - For iterable: sequence of tuples
FileDictValue: TypeAlias = FileContent | FileTuple
FilesDict: TypeAlias = Mapping[str, FileDictValue]
FilesIterable: TypeAlias = Sequence[tuple[str, FileDictValue]]
FileUpload: TypeAlias = FilesDict | FilesIterable
