"""Unit tests for PolarionUiBrowser. Playwright and the Playwright container are replaced by mocks."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from python_sbb_polarion.testing.ui_browser import MISSING_HEIGHT_SCRIPT, PASSWORD_FIELD, USERNAME_FIELD, VIEWPORT_HEIGHT, VIEWPORT_WIDTH, PolarionUiBrowser


MODULE: str = "python_sbb_polarion.testing.ui_browser"


def _fluent_container() -> MagicMock:
    container: MagicMock = MagicMock()
    for method in ("with_exposed_ports", "with_kwargs", "with_command"):
        getattr(container, method).return_value = container
    container.get_container_host_ip.return_value = "localhost"
    container.get_exposed_port.return_value = 49153
    return container


class TestStartAndClose(unittest.TestCase):
    """Test start, open_page and close."""

    def setUp(self) -> None:
        self.container: MagicMock = _fluent_container()
        self.playwright: MagicMock = MagicMock()
        self.browser: MagicMock = self.playwright.chromium.connect.return_value
        self.context: MagicMock = self.browser.new_context.return_value
        self.page: MagicMock = self.context.new_page.return_value
        self.enterContext(patch(f"{MODULE}.version", return_value="1.64.1"))
        self.enterContext(patch(f"{MODULE}.wait_for_logs"))
        self.docker_container: MagicMock = self.enterContext(patch(f"{MODULE}.DockerContainer", return_value=self.container))
        sync_playwright: MagicMock = self.enterContext(patch(f"{MODULE}.sync_playwright"))
        sync_playwright.return_value.start.return_value = self.playwright

    def test_start_runs_the_pinned_image_and_logs_in(self) -> None:
        """Test that start uses the Playwright version for the image and fills the login form."""
        browser: PolarionUiBrowser = PolarionUiBrowser("http://localhost/", "user", "secret")

        browser.start()

        self.docker_container.assert_called_once_with(image="mcr.microsoft.com/playwright:v1.64.1-noble")
        self.container.with_command.assert_called_once_with("npx -y playwright@1.64.1 run-server --port 3000 --host 0.0.0.0")
        self.playwright.chromium.connect.assert_called_once_with("ws://localhost:49153/", expose_network="*")
        self.browser.new_context.assert_called_once_with(viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
        self.page.goto.assert_called_once_with("http://localhost/polarion/")
        self.page.fill.assert_has_calls([call(USERNAME_FIELD, "user"), call(PASSWORD_FIELD, "secret")])
        self.page.close.assert_called_once_with()

    def test_rejected_login_raises(self) -> None:
        """Test that a login page which does not go away is reported."""
        self.page.wait_for_url.side_effect = PlaywrightTimeoutError("timeout")
        browser: PolarionUiBrowser = PolarionUiBrowser("http://localhost", "user", "wrong")

        with self.assertRaises(RuntimeError):
            browser.start()
        self.page.close.assert_called_once_with()

    def test_open_page_uses_the_url(self) -> None:
        """Test that open_page opens the path on the Polarion URL."""
        browser: PolarionUiBrowser = PolarionUiBrowser("http://localhost", "user", "secret")
        browser.start()

        browser.open_page("/polarion/#/project/elibrary")

        self.page.goto.assert_called_with("http://localhost/polarion/#/project/elibrary")

    def test_close_stops_everything(self) -> None:
        """Test that close stops the browser, Playwright and the container."""
        browser: PolarionUiBrowser = PolarionUiBrowser("http://localhost", "user", "secret")
        browser.start()

        browser.close()

        self.browser.close.assert_called_once_with()
        self.playwright.stop.assert_called_once_with()
        self.container.stop.assert_called_once_with()

    def test_close_before_start_does_nothing(self) -> None:
        """Test that close works without start."""
        PolarionUiBrowser("http://localhost", "user", "secret").close()

        self.container.stop.assert_not_called()

    def test_open_page_before_start_raises(self) -> None:
        """Test that open_page needs a started browser."""
        with self.assertRaises(RuntimeError):
            PolarionUiBrowser("http://localhost", "user", "secret").open_page("/polarion/")


def _frame(url: str, matches: bool | Exception) -> MagicMock:
    frame: MagicMock = MagicMock()
    frame.url = url
    if isinstance(matches, Exception):
        frame.evaluate.side_effect = matches
    else:
        frame.evaluate.return_value = matches
    return frame


class TestFindFrame(unittest.TestCase):
    """Test find_frame."""

    def test_returns_the_first_matching_frame(self) -> None:
        """Test that a frame which matches is returned."""
        wrong: MagicMock = _frame("http://localhost/polarion/", matches=False)
        right: MagicMock = _frame("http://localhost/polarion/wiki/bin/view/page", matches=True)
        page: MagicMock = MagicMock(frames=[wrong, right])

        self.assertIs(right, PolarionUiBrowser.find_frame(page, selector="#viewcontent", text="Result"))
        right.evaluate.assert_called_once()
        self.assertEqual(["#viewcontent", "Result"], right.evaluate.call_args.args[1])

    def test_url_pattern_skips_other_frames(self) -> None:
        """Test that a frame with another URL is not evaluated."""
        other: MagicMock = _frame("about:blank", matches=True)
        wiki: MagicMock = _frame("http://localhost/polarion/wiki/bin/view/page", matches=True)
        page: MagicMock = MagicMock(frames=[other, wiki])

        self.assertIs(wiki, PolarionUiBrowser.find_frame(page, url_pattern=r"/wiki/bin/view/"))
        other.evaluate.assert_not_called()

    def test_skips_a_frame_which_disappears(self) -> None:
        """Test that a frame which fails to evaluate is skipped."""
        gone: MagicMock = _frame("http://localhost/polarion/", matches=PlaywrightError("detached"))
        right: MagicMock = _frame("http://localhost/polarion/", matches=True)
        page: MagicMock = MagicMock(frames=[gone, right])

        self.assertIs(right, PolarionUiBrowser.find_frame(page, text="Result"))

    def test_invalid_pattern_fails_at_once(self) -> None:
        """Test that a selector or pattern the browser cannot parse fails without waiting."""
        broken: MagicMock = _frame("http://localhost/polarion/", matches=PlaywrightError("SyntaxError: Invalid regular expression"))
        page: MagicMock = MagicMock(frames=[broken])

        with self.assertRaises(ValueError):
            PolarionUiBrowser.find_frame(page, text="(?i)status")
        page.wait_for_timeout.assert_not_called()

    def test_polls_until_a_frame_matches(self) -> None:
        """Test that find_frame waits and searches again."""
        frame: MagicMock = MagicMock(url="http://localhost/polarion/")
        frame.evaluate.side_effect = [False, True]
        page: MagicMock = MagicMock(frames=[frame])

        self.assertIs(frame, PolarionUiBrowser.find_frame(page, text="Result"))
        page.wait_for_timeout.assert_called_once()

    def test_times_out(self) -> None:
        """Test that no matching frame ends with TimeoutError."""
        page: MagicMock = MagicMock(frames=[])

        with self.assertRaises(TimeoutError):
            PolarionUiBrowser.find_frame(page, text="Result", timeout_seconds=0)

    def test_needs_a_condition(self) -> None:
        """Test that find_frame without a condition raises."""
        with self.assertRaises(ValueError):
            PolarionUiBrowser.find_frame(MagicMock())


class TestCaptureElement(unittest.TestCase):
    """Test capture_element."""

    def test_grows_the_viewport_and_passes_the_options(self) -> None:
        """Test that the viewport grows by the missing height and the screenshot gets masks and style."""
        page: MagicMock = MagicMock()
        frame: MagicMock = MagicMock()
        frame.evaluate.side_effect = [300, 0, None]
        mask: MagicMock = MagicMock()
        frame.locator.side_effect = lambda selector: mask if selector == "b" else MagicMock()

        with patch.object(Path, "mkdir"):
            PolarionUiBrowser.capture_element(page, frame, "#viewcontent", Path("out/page.png"), {r"\d+": "<n>"}, ["b"], "body { color: red; }")

        page.set_viewport_size.assert_has_calls(
            [
                call({"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT}),
                call({"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT + 300}),
            ]
        )
        self.assertEqual(MISSING_HEIGHT_SCRIPT, frame.evaluate.call_args_list[0].args[0])
        self.assertEqual(["#viewcontent", [(r"\d+", "<n>")]], frame.evaluate.call_args_list[2].args[1])

    def test_takes_the_screenshot_of_the_element(self) -> None:
        """Test that the screenshot is taken of the first element with masks and style."""
        page: MagicMock = MagicMock()
        frame: MagicMock = MagicMock()
        frame.evaluate.return_value = 0
        element: MagicMock = MagicMock()
        mask: MagicMock = MagicMock()
        frame.locator.side_effect = lambda selector: element if selector == "#viewcontent" else mask

        with patch.object(Path, "mkdir"):
            PolarionUiBrowser.capture_element(page, frame, "#viewcontent", Path("out/page.png"), mask_selectors=["b"], style="body {}")

        element.first.screenshot.assert_called_once_with(path=Path("out/page.png"), animations="disabled", caret="hide", mask=[mask], style="body {}")

    def test_without_options(self) -> None:
        """Test that no replacement runs and no mask is passed without options."""
        page: MagicMock = MagicMock()
        frame: MagicMock = MagicMock()
        frame.evaluate.return_value = 0

        with patch.object(Path, "mkdir"):
            PolarionUiBrowser.capture_element(page, frame, "body", Path("out/page.png"))

        frame.evaluate.assert_called_once()
        frame.locator.return_value.first.screenshot.assert_called_once_with(path=Path("out/page.png"), animations="disabled", caret="hide", mask=[], style=None)
