"""Command-line argument parsing."""

import argparse


def get_script_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments (unknown arguments are ignored)
    """
    parser = argparse.ArgumentParser(description="Test run configuration")

    parser.add_argument("--app_url", help="Polarion application URL")
    parser.add_argument("--app_token", help="Authentication user token")

    parser.add_argument("--app_username", type=str, help="Application user name")
    parser.add_argument("--app_password", type=str, help="Application user password (please use TOKENS instead of passwords when possible")

    parser.add_argument("--ssh_username", type=str, help="SSH user name")
    parser.add_argument("--ssh_private_key_path", type=str, help="SSH key path", default=None)
    parser.add_argument("--ssh_private_key_password", type=str, help="SSH private key password")

    parser.add_argument("--postgres_db_name", type=str, help="Postgres database name", default="postgres")
    parser.add_argument("--postgres_username", type=str, help="Postgres user name")
    parser.add_argument("--postgres_password", type=str, help="Postgres password")

    parser.add_argument("--apim_client_id", type=str, help="APIM client ID")
    parser.add_argument("--apim_client_secret", type=str, help="APIM client secret")
    parser.add_argument("--apim_api_key", type=str, help="APIM API Key")
    parser.add_argument("--apim_token_endpoint", type=str, help="APIM token endpoint")

    parser.add_argument("--smtp_host", type=str, help="SMTP host")
    parser.add_argument("--smtp_port", type=str, help="SMTP port")
    parser.add_argument("--smtp_username", type=str, help="SMTP username")
    parser.add_argument("--smtp_password", type=str, help="SMTP password")

    parser.add_argument("--tc_polarion_image_name", type=str, help="Polarion docker image")
    parser.add_argument("--tc_weasyprint_service_image_name", type=str, help="Weasyprint service docker image")
    parser.add_argument("--tc_extension_version", type=str, help="Version of testing extension in test container")
    parser.add_argument("--tc_additional_bundles", type=str, help="Comma separated list of additional bundles in format group_id:artifact_id:version")
    parser.add_argument("--tc_admin_utility_version", type=str, help="Admin utility version")

    args: argparse.Namespace
    args, _unknown = parser.parse_known_args()
    return args
