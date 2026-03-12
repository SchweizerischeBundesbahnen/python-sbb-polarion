"""Python SBB Polarion

A Python library for interacting with Polarion requirements management system.
Provides utilities, core API access, extension clients, and testing helpers.
"""

import logging

# ============================================================================
# Submodules - Make importable for advanced/explicit usage
# ============================================================================
from python_sbb_polarion import core, extensions, testing, types, util

# ============================================================================
# Core API - Foundation layer (most users start here)
# ============================================================================
from python_sbb_polarion.core import (
    ExtensionApiFactory,
    PolarionApiV1,
    PolarionGenericExtensionApi,
    PolarionRestApiConnection,
)


# Version will be set by CI/CD
__version__ = "2.0.0"

# Add NullHandler to prevent "No handlers could be found" warning
# if the application doesn't configure logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = [
    # ========================================================================
    # Core API (foundation - most users start here)
    # ========================================================================
    "ExtensionApiFactory",
    "PolarionApiV1",
    "PolarionGenericExtensionApi",
    "PolarionRestApiConnection",
    # ========================================================================
    # Submodules (advanced usage - explicit imports)
    # ========================================================================
    "core",
    "extensions",
    "testing",
    "types",
    "util",
]
