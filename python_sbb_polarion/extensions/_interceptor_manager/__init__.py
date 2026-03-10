"""Interceptor Manager mixins package."""

from python_sbb_polarion.extensions._interceptor_manager._hooks import HooksMixin
from python_sbb_polarion.extensions._interceptor_manager._settings import HookSettingsMixin


__all__ = ["HookSettingsMixin", "HooksMixin"]
