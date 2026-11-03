"""Paths of Polarion UI pages, for ``PolarionUiBrowser.open_page``."""

from __future__ import annotations

from urllib.parse import quote


DEFAULT_SPACE: str = "_default"


class PolarionUrls:
    """Builds the paths of Polarion UI pages. Names are URL-encoded."""

    @staticmethod
    def page(project_id: str, name: str, space: str = DEFAULT_SPACE) -> str:
        """Path of a LiveDoc, a LiveReport or a classic Wiki page.

        Args:
            project_id: ID of the project
            name: Name of the page
            space: Space of the page

        Returns:
            str: Path of the page
        """
        # Polarion opens the project home for an explicit default space, so the path leaves it out.
        if space == DEFAULT_SPACE:
            return f"/polarion/#/project/{quote(project_id)}/wiki/{quote(name)}"
        return f"/polarion/#/project/{quote(project_id)}/wiki/{quote(space)}/{quote(name)}"

    @staticmethod
    def work_item(project_id: str, work_item_id: str) -> str:
        """Path of a work item.

        Args:
            project_id: ID of the project
            work_item_id: ID of the work item

        Returns:
            str: Path of the work item
        """
        return f"/polarion/#/project/{quote(project_id)}/workitem?id={quote(work_item_id)}"

    @staticmethod
    def project_home(project_id: str) -> str:
        """Path of the home page of a project.

        Args:
            project_id: ID of the project

        Returns:
            str: Path of the project home
        """
        return f"/polarion/#/project/{quote(project_id)}"
