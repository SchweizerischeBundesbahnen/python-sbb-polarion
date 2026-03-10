"""Polarion REST API v1 - Full implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.polarion_api._base import BaseMixin

# Custom Fields
from python_sbb_polarion.core.polarion_api._customfields import CustomFieldsMixin

# Documents
from python_sbb_polarion.core.polarion_api._documents import (
    DocumentsAttachmentsMixin,
    DocumentsBranchingMixin,
    DocumentsCommentsMixin,
    DocumentsCrudMixin,
    DocumentsFieldsMixin,
    DocumentsPartsMixin,
)

# Global
from python_sbb_polarion.core.polarion_api._global import (
    GlobalEnumerationsMixin,
    JobsMixin,
    MiscMixin,
    RevisionsMixin,
    UsersMixin,
)

# Jobs Management (new in Polarion 2512)
from python_sbb_polarion.core.polarion_api._jobs import JobsManagementMixin

# License
from python_sbb_polarion.core.polarion_api._license import LicenseMixin

# Pages
from python_sbb_polarion.core.polarion_api._pages import PagesMixin

# Plans
from python_sbb_polarion.core.polarion_api._plans import PlansMixin

# Projects
from python_sbb_polarion.core.polarion_api._projects import (
    ProjectsActionsMixin,
    ProjectsCollectionsMixin,
    ProjectsCrudMixin,
    ProjectsEnumerationsMixin,
)

# Testruns
from python_sbb_polarion.core.polarion_api._testruns import (
    TestrunsAttachmentsMixin,
    TestrunsCommentsMixin,
    TestrunsCrudMixin,
    TestrunsParametersMixin,
    TestrunsRecordsMixin,
    TestrunsStepResultsMixin,
)

# Workitems
from python_sbb_polarion.core.polarion_api._workitems import (
    WorkitemsApprovalsMixin,
    WorkitemsAttachmentsMixin,
    WorkitemsCommentsMixin,
    WorkitemsCrudMixin,
    WorkitemsFieldsMixin,
    WorkitemsLinksMixin,
    WorkitemsTestStepsMixin,
    WorkitemsWorkRecordsMixin,
)


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


class PolarionApiV1(
    # Workitems
    WorkitemsCrudMixin,
    WorkitemsAttachmentsMixin,
    WorkitemsCommentsMixin,
    WorkitemsLinksMixin,
    WorkitemsApprovalsMixin,
    WorkitemsTestStepsMixin,
    WorkitemsFieldsMixin,
    WorkitemsWorkRecordsMixin,
    # Testruns
    TestrunsCrudMixin,
    TestrunsAttachmentsMixin,
    TestrunsCommentsMixin,
    TestrunsRecordsMixin,
    TestrunsStepResultsMixin,
    TestrunsParametersMixin,
    # Documents
    DocumentsCrudMixin,
    DocumentsAttachmentsMixin,
    DocumentsCommentsMixin,
    DocumentsPartsMixin,
    DocumentsBranchingMixin,
    DocumentsFieldsMixin,
    # Projects
    ProjectsCrudMixin,
    ProjectsActionsMixin,
    ProjectsEnumerationsMixin,
    ProjectsCollectionsMixin,
    # Plans
    PlansMixin,
    # Pages
    PagesMixin,
    # License
    LicenseMixin,
    # Custom Fields
    CustomFieldsMixin,
    # Global
    GlobalEnumerationsMixin,
    UsersMixin,
    JobsMixin,
    JobsManagementMixin,
    RevisionsMixin,
    MiscMixin,
    # Base
    BaseMixin,
):
    """Polarion REST API v1 - Full implementation.

    Provides comprehensive access to the Polarion REST API v1 with ~271 operations
    covering all resources (based on Polarion 2512):

    - **Workitems**: CRUD, attachments, comments, links, backlinks, approvals, test steps, work records
    - **Testruns**: CRUD, attachments, comments, records, step results, parameters
    - **Documents**: CRUD, attachments, comments, parts, branching
    - **Projects**: CRUD, actions, enumerations, collections, fields metadata
    - **Plans**: CRUD, relationships
    - **Pages**: CRUD, attachments, comments, relationships (wiki pages)
    - **License**: License management, slots, assignments
    - **Custom Fields**: Global and project-level custom field definitions
    - **Global**: Enumerations, users, jobs, revisions, roles, groups, metadata

    Usage::

        from python_sbb_polarion.core.base import PolarionRestApiConnection
        from python_sbb_polarion.core.polarion_api import PolarionApiV1

        connection = PolarionRestApiConnection(url="https://polarion.example.com", auth_token="...")
        api = PolarionApiV1(connection)

        # Get workitem
        response = api.get_workitem("MyProject", "WI-123")

        # Get documents
        response = api.get_document("MyProject", "_default", "MyDocument")

        # Get test runs
        response = api.get_testruns("MyProject", query="status:open")
    """

    def __init__(self, polarion_connection: PolarionRestApiConnection) -> None:
        """Initialize PolarionApiV1.

        Args:
            polarion_connection: Polarion REST API connection
        """
        self.polarion_connection = polarion_connection
        self.base_url = "/polarion/rest/v1"
