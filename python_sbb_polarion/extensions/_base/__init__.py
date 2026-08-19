"""Base classes for extension mixins.

This package provides abstract base classes with type hints for attributes
that are available through PolarionGenericExtensionApi.
"""

from python_sbb_polarion.extensions._base._export_permission import ExportPermissionMixin
from python_sbb_polarion.extensions._base._mixin import BaseMixin
from python_sbb_polarion.extensions._base._roles import RolesMixin


__all__ = ["BaseMixin", "ExportPermissionMixin", "RolesMixin"]
