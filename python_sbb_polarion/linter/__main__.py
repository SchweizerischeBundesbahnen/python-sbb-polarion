"""Entry point for running the linter as a module.

Usage:
    python -m python_sbb_polarion.linter [path]
    python -m python_sbb_polarion.linter src/
"""

import sys

from python_sbb_polarion.linter.code_style_linter import main


if __name__ == "__main__":
    sys.exit(main())
