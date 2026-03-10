"""Admin Utility Extension API"""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.base import PolarionGenericExtensionApi
from python_sbb_polarion.extensions._admin_utility import (
    CollectionMixin,
    ConfigurationMixin,
    CustomFieldsMixin,
    DocumentMixin,
    LicenseMixin,
    LiveReportMixin,
    ProjectMixin,
    TokenMixin,
    VaultMixin,
    WikiMixin,
)


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


__all__ = ["PolarionAdminUtilityApi"]


class PolarionAdminUtilityApi(
    TokenMixin,
    ProjectMixin,
    LicenseMixin,
    DocumentMixin,
    CollectionMixin,
    WikiMixin,
    VaultMixin,
    LiveReportMixin,
    CustomFieldsMixin,
    ConfigurationMixin,
    PolarionGenericExtensionApi,
):
    """Admin Utility Polarion Extension API

    This class combines all admin utility functionality through mixins:
    - TokenMixin: Token management (create, delete)
    - ProjectMixin: Project management (create, delete, get)
    - LicenseMixin: License activation
    - DocumentMixin: Document/module management
    - CollectionMixin: Collection management
    - WikiMixin: Wiki page management
    - VaultMixin: Vault record management
    - LiveReportMixin: Live report management
    - CustomFieldsMixin: Custom fields management
    - ConfigurationMixin: Document and workitem configuration
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        super().__init__("admin-utility", polarion_connection)
