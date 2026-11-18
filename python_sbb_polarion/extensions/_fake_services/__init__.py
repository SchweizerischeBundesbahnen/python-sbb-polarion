"""Fake Services mixins package.

This package provides mixin classes for the Fake Services extension API.
"""

from python_sbb_polarion.extensions._fake_services._open_text import OpenTextMixin
from python_sbb_polarion.extensions._fake_services._webhook import WebhookMixin


__all__ = [
    "OpenTextMixin",
    "WebhookMixin",
]
