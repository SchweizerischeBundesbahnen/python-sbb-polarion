"""
Python SBB Polarion - Project Template Manager
"""

from python_sbb_polarion.polarion_project_manager.cli import main as cli_main
from python_sbb_polarion.polarion_project_manager.project_manager import PolarionProjectManager


__all__ = [
    "PolarionProjectManager",
    "cli_main",
]
