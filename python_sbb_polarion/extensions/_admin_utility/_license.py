"""Admin Utility license management mixin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from python_sbb_polarion.core.annotations import restapi_endpoint
from python_sbb_polarion.extensions._base import BaseMixin


if TYPE_CHECKING:
    from requests import Response


class LicenseMixin(BaseMixin):
    """License management operations."""

    @restapi_endpoint(
        method="POST",
        path="/api/licenses/{evalLicense}/activation",
        path_params={
            "evalLicense": "eval_license",
        },
        required_params=["evalLicense"],
    )
    def activate_trial_license(self, eval_license: str = "trial") -> Response:
        """Activate trial license

        Returns:
            Response: Response object from the API call
        """
        url: str = f"{self.rest_api_url}/licenses/{eval_license}/activation"
        return self.polarion_connection.api_request_post(url)
