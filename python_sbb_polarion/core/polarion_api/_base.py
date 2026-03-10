"""Base mixin class for Polarion API v1 mixins."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from python_sbb_polarion.core.base import PolarionRestApiConnection
    from python_sbb_polarion.types import SparseFields


class BaseMixin(ABC):
    """Base mixin providing type hints for Polarion API v1 mixins.

    All mixins inherit from this class to get proper type hints for
    the shared attributes from PolarionApiV1.
    """

    base_url: str
    polarion_connection: PolarionRestApiConnection

    @staticmethod
    def _add_sparse_fields(params: dict[str, str], fields: SparseFields | None) -> None:
        """Add JSON:API sparse fieldset parameters to request params.

        JSON:API sparse fieldsets use the format fields[TYPE]=field1,field2.
        This method converts a dict like {"workitems": "@all"} to params like
        {"fields[workitems]": "@all"}.

        See: https://jsonapi.org/format/#fetching-sparse-fieldsets

        Args:
            params: Request params dict to modify in place
            fields: Sparse fields dict mapping resource type to field spec.
                    Example: {"workitems": "@all", "categories": "id,name"}
        """
        if fields is not None:
            for resource_type, field_spec in fields.items():
                params[f"fields[{resource_type}]"] = field_spec
