"""Global resources API mixins."""

from python_sbb_polarion.core.polarion_api._global._enumerations import GlobalEnumerationsMixin
from python_sbb_polarion.core.polarion_api._global._jobs import JobsMixin
from python_sbb_polarion.core.polarion_api._global._misc import MiscMixin
from python_sbb_polarion.core.polarion_api._global._revisions import RevisionsMixin
from python_sbb_polarion.core.polarion_api._global._users import UsersMixin


__all__ = [
    "GlobalEnumerationsMixin",
    "JobsMixin",
    "MiscMixin",
    "RevisionsMixin",
    "UsersMixin",
]
