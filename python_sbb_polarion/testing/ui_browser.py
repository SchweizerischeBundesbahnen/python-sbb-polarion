"""Browser logged in to the Polarion UI. Needs the ``ui`` extra of this package and Docker."""

from __future__ import annotations

import re
import secrets
import time
from importlib.metadata import version
from typing import TYPE_CHECKING

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


if TYPE_CHECKING:
    from pathlib import Path

    from playwright.sync_api import Browser, BrowserContext, Frame, Locator, Page, Playwright


SERVER_PORT: int = 3000
SERVER_START_TIMEOUT_SECONDS: int = 120
# The default /dev/shm of 64 MB can crash Chromium on tall pages.
SERVER_SHM_SIZE: str = "1g"
USERNAME_FIELD: str = "#j_username"
PASSWORD_FIELD: str = "input[name=j_password]"  # noqa: S105 - a CSS selector of the login form, not a password
LOGGED_IN_URL: re.Pattern[str] = re.compile(r"/polarion/#/")
LOGIN_TIMEOUT_MS: int = 60000

VIEWPORT_WIDTH: int = 1600
VIEWPORT_HEIGHT: int = 1000
FRAME_POLL_INTERVAL_MS: int = 1000
LAYOUT_SETTLE_MS: int = 500
# A layout can grow after each viewport change, so one resize does not always show the whole element.
MAX_VIEWPORT_RESIZES: int = 5

MISSING_HEIGHT_SCRIPT: str = """(selector) => {
    const element = document.querySelector(selector);
    const page = document.documentElement;
    return Math.max(element.scrollHeight - element.clientHeight, 0) + Math.max(page.scrollHeight - window.innerHeight, 0);
}"""

FRAME_MATCH_SCRIPT: str = """([selector, pattern]) => {
    if (!document.body) {
        return false;
    }
    if (selector && !document.querySelector(selector)) {
        return false;
    }
    return !pattern || new RegExp(pattern).test(document.body.innerText);
}"""

REPLACE_TEXT_SCRIPT: str = """([selector, replacements]) => {
    const walker = document.createTreeWalker(document.querySelector(selector), NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
        for (const [pattern, replacement] of replacements) {
            walker.currentNode.nodeValue = walker.currentNode.nodeValue.replace(new RegExp(pattern, 'g'), replacement);
        }
    }
}"""


class PolarionUiBrowser:
    """Headless Chromium logged in to Polarion through its login form, as a user does.

    The browser runs in the Playwright Linux image of the installed Playwright version. Fonts render differently
    on each OS, so this keeps screenshots comparable between developer machines and CI.

    ``close`` does not log out: Polarion's logout ends every session of the user, also those of parallel runs.
    The session holds a license until it is idle for the Tomcat session timeout, 30 minutes by default.

    Args:
        url: Polarion URL, for example ``http://localhost``
        username: Polarion user to log in with
        password: Password of the user
    """

    def __init__(self, url: str, username: str, password: str) -> None:
        self.__url: str = url.rstrip("/")
        self.__username: str = username
        self.__password: str = password
        self.__server: DockerContainer | None = None
        self.__playwright: Playwright | None = None
        self.__browser: Browser | None = None
        self.__context: BrowserContext | None = None

    def start(self) -> None:
        """Start the browser and log in.

        Raises:
            RuntimeError: If Polarion does not accept the login
        """
        playwright_version: str = version("playwright")
        # Docker publishes the port on every host interface, so only who knows this path can drive the browser.
        server_path: str = f"/{secrets.token_urlsafe(24)}"
        self.__server = (
            DockerContainer(image=f"mcr.microsoft.com/playwright:v{playwright_version}-noble")
            .with_exposed_ports(SERVER_PORT)
            .with_kwargs(shm_size=SERVER_SHM_SIZE)
            .with_command(f"npx -y playwright@{playwright_version} run-server --port {SERVER_PORT} --host 0.0.0.0 --path {server_path}")
        )
        self.__server.start()
        wait_for_logs(self.__server, "Listening on", timeout=SERVER_START_TIMEOUT_SECONDS)

        self.__playwright = sync_playwright().start()
        self.__browser = self.__playwright.chromium.connect(
            f"ws://{self.__server.get_container_host_ip()}:{self.__server.get_exposed_port(SERVER_PORT)}{server_path}",
            # The browser reaches Polarion through this process, so localhost and VPN hosts work unchanged.
            expose_network="*",
        )
        self.__context = self.__browser.new_context(viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
        self.__log_in()

    def __log_in(self) -> None:
        if self.__context is None:
            raise RuntimeError("The browser is not started")
        page: Page = self.__context.new_page()
        try:
            page.goto(f"{self.__url}/polarion/")
            page.fill(USERNAME_FIELD, self.__username)
            page.fill(PASSWORD_FIELD, self.__password)
            page.locator(PASSWORD_FIELD).press("Enter")
            try:
                # Polarion answers a rejected login with the login page again.
                page.wait_for_url(LOGGED_IN_URL, timeout=LOGIN_TIMEOUT_MS)
            except PlaywrightTimeoutError as e:
                raise RuntimeError(f"Polarion did not accept the login of user '{self.__username}'") from e
        finally:
            page.close()

    def close(self) -> None:
        """Close the browser. Each step runs also when an earlier one fails, so no container is left running."""
        try:
            if self.__browser is not None:
                self.__browser.close()
        finally:
            try:
                if self.__playwright is not None:
                    self.__playwright.stop()
            finally:
                if self.__server is not None:
                    self.__server.stop()

    def open_page(self, path: str) -> Page:
        """Open a Polarion page in a new tab.

        Args:
            path: Path of the page, for example ``/polarion/#/project/elibrary/wiki/Home``

        Returns:
            Page: The opened page

        Raises:
            RuntimeError: If the browser is not started
        """
        if self.__context is None:
            raise RuntimeError("The browser is not started")
        page: Page = self.__context.new_page()
        page.goto(f"{self.__url}{path}")
        return page

    @staticmethod
    def find_frame(page: Page, selector: str | None = None, text: str | None = None, url_pattern: str | None = None, timeout_seconds: float = 90) -> Frame:
        """Wait until a frame matches all given conditions. Polarion renders its pages inside different frames.

        Args:
            page: Page to search
            selector: CSS selector of an element the frame must contain
            text: JavaScript regular expression of a text the frame must show
            url_pattern: Python regular expression the frame URL must match
            timeout_seconds: Time to wait

        Returns:
            Frame: The first frame that matches

        Raises:
            ValueError: If no condition is given, or the selector or the text is invalid
            TimeoutError: If no frame matches in time
        """
        if selector is None and text is None and url_pattern is None:
            raise ValueError("Give a selector, a text or a URL pattern")

        deadline: float = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            for frame in page.frames:
                if url_pattern is not None and not re.search(url_pattern, frame.url):
                    continue
                try:
                    matches: bool = frame.evaluate(FRAME_MATCH_SCRIPT, [selector, text])
                # A frame can reload or disappear while Polarion builds the page.
                except PlaywrightError as error:
                    if "SyntaxError" in str(error):
                        raise ValueError(f"Invalid selector={selector!r} or text={text!r}: {error}") from error
                    continue
                if matches:
                    return frame
            page.wait_for_timeout(FRAME_POLL_INTERVAL_MS)
        raise TimeoutError(f"No frame of '{page.url}' matches selector={selector!r}, text={text!r}, url_pattern={url_pattern!r} after {timeout_seconds} seconds")

    @staticmethod
    def capture_element(
        page: Page,
        frame: Frame,
        selector: str,
        path: Path,
        text_replacements: dict[str, str] | None = None,
        mask_selectors: list[str] | None = None,
        style: str | None = None,
    ) -> None:
        """Save a screenshot of a whole element, also if it is taller than the viewport.

        Polarion scrolls inside nested containers, so a full page screenshot cuts the content.
        A taller viewport makes these containers show all of it.

        Args:
            page: Page of the frame
            frame: Frame of the element
            selector: CSS selector of the element
            path: Path of the image to write
            text_replacements: JavaScript regular expressions of text that changes between runs, with its replacement
            mask_selectors: CSS selectors of elements in the frame that change between runs, painted over with one color
            style: CSS applied only while the screenshot is taken, for example to hide a sidebar
        """
        # Scroll containers fill the viewport, so a viewport grown by an earlier capture would make this one taller.
        height: int = VIEWPORT_HEIGHT
        page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": height})
        page.wait_for_timeout(LAYOUT_SETTLE_MS)
        for _ in range(MAX_VIEWPORT_RESIZES):
            missing_height: int = frame.evaluate(MISSING_HEIGHT_SCRIPT, selector)
            if missing_height <= 0:
                break
            height += missing_height
            page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": height})
            page.wait_for_timeout(LAYOUT_SETTLE_MS)

        if text_replacements:
            frame.evaluate(REPLACE_TEXT_SCRIPT, [selector, list(text_replacements.items())])

        path.parent.mkdir(parents=True, exist_ok=True)
        masks: list[Locator] = [frame.locator(mask_selector) for mask_selector in mask_selectors or []]
        frame.locator(selector).first.screenshot(path=path, animations="disabled", caret="hide", mask=masks, style=style)
