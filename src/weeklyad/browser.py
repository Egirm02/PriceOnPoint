from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Any, Iterator, Optional

from . import selectors


class BrowserSession:
    def __init__(self, headed: bool = False, timeout_ms: int = 20_000):
        self.headed = headed
        self.timeout_ms = timeout_ms

    @contextmanager
    def open(self) -> Iterator[Any]:
        try:
            from playwright.sync_api import Browser, BrowserContext, sync_playwright
        except ModuleNotFoundError as exc:
            raise RuntimeError("Playwright is required. Install with `pip install playwright`.") from exc

        with sync_playwright() as pw:
            browser: Browser = pw.chromium.launch(headless=not self.headed)
            context: BrowserContext = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(self.timeout_ms)
            try:
                yield page
            finally:
                context.close()
                browser.close()


def click_first_visible(page: Any, css_selectors: list[str]) -> bool:
    for selector in css_selectors:
        loc = page.locator(selector).first
        try:
            if loc.is_visible(timeout=1000):
                loc.click()
                return True
        except Exception:
            continue
    return False


def fill_first_visible(page: Any, css_selectors: list[str], value: str) -> bool:
    for selector in css_selectors:
        loc = page.locator(selector).first
        try:
            if loc.is_visible(timeout=1000):
                loc.fill(value)
                return True
        except Exception:
            continue
    return False


def dismiss_cookie_banner(page: Any) -> None:
    click_first_visible(page, selectors.COOKIE_ACCEPT)


def select_store_by_zip(page: Any, zip_code: Optional[str]) -> None:
    if not zip_code:
        return
    click_first_visible(page, selectors.STORE_BUTTONS)
    if fill_first_visible(page, selectors.ZIP_INPUTS, zip_code):
        click_first_visible(page, selectors.SEARCH_BUTTONS)
        time.sleep(1.0)
        click_first_visible(page, selectors.STORE_RESULT_BUTTONS)
        time.sleep(1.0)
