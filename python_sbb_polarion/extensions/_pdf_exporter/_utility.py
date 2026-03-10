"""PDF Exporter utility operations mixin.

This module re-exports SharedUtilityMixin for backward compatibility.
All utility methods are inherited from the shared module.
"""

from python_sbb_polarion.extensions._shared_exporter import SharedExporterUtilityMixin


class UtilityMixin(SharedExporterUtilityMixin):
    """PDF Exporter utility operations.

    All methods are inherited from SharedUtilityMixin:
    - Collection documents
    - Document export filename generation
    - Link role names
    - Document language
    - Webhooks status
    - Project name
    """
