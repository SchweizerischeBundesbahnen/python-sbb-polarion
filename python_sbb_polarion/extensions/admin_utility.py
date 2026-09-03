"""Admin Utility Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._admin_utility import (
    ConfigurationMixin,
    DocumentMixin,
    LicenseMixin,
    LiveReportMixin,
    TokenMixin,
    VaultMixin,
    WikiMixin,
)


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


__all__ = ["PolarionAdminUtilityApi"]


class PolarionAdminUtilityApi(
    TokenMixin,
    LicenseMixin,
    DocumentMixin,
    WikiMixin,
    VaultMixin,
    LiveReportMixin,
    ConfigurationMixin,
    PolarionGenericExtensionApi,
):
    """Admin Utility Polarion Extension API

    This class combines all admin utility functionality through mixins:
    - TokenMixin: Token management (create, delete)
    - LicenseMixin: License activation
    - DocumentMixin: Document/module deletion
    - WikiMixin: Wiki page management
    - VaultMixin: Vault record management
    - LiveReportMixin: Default-space live report management
    - ConfigurationMixin: Document and workitem configuration

    Operations covered by the standard Polarion REST API v1 (projects, collections, documents,
    pages, custom fields, test run templates) are not part of this client: the admin-utility
    extension removed those endpoints in v5.0.1. Use ``PolarionApiV1`` instead.
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("admin-utility", polarion_connection)
