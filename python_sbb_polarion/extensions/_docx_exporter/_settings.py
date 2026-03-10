"""DOCX Exporter settings operations mixin.

This module re-exports SharedSettingsMixin for backward compatibility.
All settings methods are inherited from the shared module.
"""

from python_sbb_polarion.extensions._shared_exporter import SharedExporterSettingsMixin


class SettingsMixin(SharedExporterSettingsMixin):
    """DOCX Exporter settings operations.

    All methods are inherited from SharedSettingsMixin:
    - Localization settings (upload/download XLIFF)
    - Style package weights and suitable names
    - Convenience wrappers for style package settings
    """
