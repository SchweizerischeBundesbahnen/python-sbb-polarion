"""Base mixin class for extensions.

This module provides an abstract base mixin class with type hints for attributes
that are available through PolarionGenericExtensionApi.
"""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection


class BaseMixin(ABC):
    """Abstract base mixin with type hints for extension attributes.

    All extension mixins inherit from this class to get proper type hints
    for rest_api_url and polarion_connection without repeating them.

    This class is abstract and should not be instantiated directly.
    """

    rest_api_url: str
    polarion_connection: PolarionRestApiConnection
