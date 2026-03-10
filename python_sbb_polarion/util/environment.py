"""
common implementation for environment information

"""

import locale
import logging
import sys
from importlib.metadata import distributions


logger = logging.getLogger(__name__)


def print_python_information() -> None:
    """Prints python version"""
    python_version: str = sys.version
    logger.info("Python version: %s", python_version)


def print_pip_information() -> None:
    """Prints version of all installed pip modules"""
    installed_packages: list[str] = [f"'{dist.name}' == {dist.version}" for dist in distributions()]
    installed_packages_list: list[str] = sorted(installed_packages)
    for package in installed_packages_list:
        logger.debug(package)


def print_encoding() -> None:
    """Prints the encoding page of the localhost"""
    logger.info("Preferred encoding: %s", locale.getpreferredencoding())
