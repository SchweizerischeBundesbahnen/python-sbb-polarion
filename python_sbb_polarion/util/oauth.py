"""Common implementation for OAuth2 connections."""

import logging

from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from requests_oauthlib import OAuth2Session


logger = logging.getLogger(__name__)


def get_oauth2_client_credentials(client_id: str, client_secret: str, token_endpoint: str) -> str:
    """Get the OAuth2 client access token for a backend application.

    Uses OAuth2 Client Credentials flow to obtain an access token.

    Args:
        client_id: OAuth2 client identifier
        client_secret: OAuth2 client secret
        token_endpoint: OAuth2 token endpoint URL

    Returns:
        str: OAuth2 access token for the backend application

    Raises:
        OAuth2Error: If OAuth2 authentication fails
        RequestException: If HTTP request fails (network error, timeout, etc.)
        KeyError: If response doesn't contain access_token
    """
    try:
        auth: HTTPBasicAuth = HTTPBasicAuth(client_id, client_secret)
        client: BackendApplicationClient = BackendApplicationClient(client_id=client_id)
        oauth: OAuth2Session = OAuth2Session(client=client)
        token_response: dict[str, str] = oauth.fetch_token(token_url=token_endpoint, auth=auth)
        access_token: str = str(token_response["access_token"])
        logger.info("Successfully obtained OAuth2 access token")
        return access_token  # noqa: TRY300
    except OAuth2Error:
        logger.exception("OAuth2 authentication failed for client_id %s", client_id)
        raise
    except RequestException:
        logger.exception("HTTP request failed to token endpoint %s", token_endpoint)
        raise
    except KeyError:
        logger.exception("Token response missing 'access_token' field")
        raise
