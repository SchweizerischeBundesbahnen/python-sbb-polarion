"""
common implementation for argument parsing

"""

import argparse


def get_script_arguments(url: str) -> argparse.Namespace:
    """common implementation for argument parsing"""
    parser = argparse.ArgumentParser(description="Universal parser configuration for all utilities")
    parser.add_argument("-l", "--app_url", type=str, help=f"Application URL (default: {url})", default=url)
    parser.add_argument("-n", "--app_name", type=str, help="Application name")
    parser.add_argument("-u", "--app_username", type=str, help="Application user name")
    parser.add_argument("-p", "--app_password", type=str, help="Application user password (please use TOKENS instead of passwords when possible")
    parser.add_argument("-t", "--app_token", type=str, help="Application user token")
    parser.add_argument("-a", "--analyse", action="store_true", help="No actions will be performed only printing")
    parser.add_argument("--dry_run", type=eval, choices=[True, False], default="True", help="Default, true no actions will be performed only printing")
    parser.add_argument("--tc_polarion_image_name", type=str, help="Polarion docker image name for test container")
    parser.add_argument("--tc_weasyprint_service_image_name", type=str, help="Weasyprint service docker image name for test container")
    parser.add_argument("--tc_extension_version", type=str, help="Version of testing extension in test container")
    parser.add_argument("--tc_additional_bundles", type=str, help="Comma separated list of additional bundles in format group_id:artifact_id:version")
    parser.add_argument("--tc_admin_utility_version", type=str, help="Custom version of admin utility extension")
    args, unknown = parser.parse_known_args()
    return args
