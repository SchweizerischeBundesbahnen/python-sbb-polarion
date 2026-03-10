"""Documents API mixins."""

from python_sbb_polarion.core.polarion_api._documents._attachments import DocumentsAttachmentsMixin
from python_sbb_polarion.core.polarion_api._documents._branching import DocumentsBranchingMixin
from python_sbb_polarion.core.polarion_api._documents._comments import DocumentsCommentsMixin
from python_sbb_polarion.core.polarion_api._documents._crud import DocumentsCrudMixin
from python_sbb_polarion.core.polarion_api._documents._fields import DocumentsFieldsMixin
from python_sbb_polarion.core.polarion_api._documents._parts import DocumentsPartsMixin


__all__ = [
    "DocumentsAttachmentsMixin",
    "DocumentsBranchingMixin",
    "DocumentsCommentsMixin",
    "DocumentsCrudMixin",
    "DocumentsFieldsMixin",
    "DocumentsPartsMixin",
]
