"""Collection Checker specific types and enums."""

from enum import StrEnum


class ReportFormat(StrEnum):
    """Report format for collection check results."""

    JSON = "JSON"
    TXT = "TXT"
