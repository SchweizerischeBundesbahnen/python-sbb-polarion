"""Tests python_polarion_utils.common.util_argparse"""

from python_polarion_utils.common import util_argparse


def test_get_script_arguments():
    host = "http://localhost/polarion"
    args = util_argparse.get_script_arguments(host)
    assert args.app_url == host
