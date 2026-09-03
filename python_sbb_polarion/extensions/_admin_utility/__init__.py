"""Admin Utility mixins package.

This package provides mixin classes for the Admin Utility extension API.
"""

from python_sbb_polarion.extensions._admin_utility._configuration import ConfigurationMixin
from python_sbb_polarion.extensions._admin_utility._document import DocumentMixin
from python_sbb_polarion.extensions._admin_utility._license import LicenseMixin
from python_sbb_polarion.extensions._admin_utility._live_report import LiveReportMixin
from python_sbb_polarion.extensions._admin_utility._token import TokenMixin
from python_sbb_polarion.extensions._admin_utility._vault import VaultMixin
from python_sbb_polarion.extensions._admin_utility._wiki import WikiMixin


__all__ = [
    "ConfigurationMixin",
    "DocumentMixin",
    "LicenseMixin",
    "LiveReportMixin",
    "TokenMixin",
    "VaultMixin",
    "WikiMixin",
]
