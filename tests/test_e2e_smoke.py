from __future__ import annotations

import os

import pytest

from weeklyad.browser import BrowserSession
from weeklyad.extract import extract_raw_tiles, open_and_prepare, read_metadata
from weeklyad.selectors import SALE_PRICES_URL, WEEKLY_AD_URL

try:
    import playwright  # noqa: F401
except ModuleNotFoundError:
    PLAYWRIGHT_AVAILABLE = False
else:
    PLAYWRIGHT_AVAILABLE = True


@pytest.mark.e2e
@pytest.mark.skipif(os.getenv("RUN_E2E") != "1", reason="Set RUN_E2E=1 to run live e2e tests")
@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
@pytest.mark.parametrize("url", [WEEKLY_AD_URL, SALE_PRICES_URL])
def test_smoke_page_load_and_metadata(url: str) -> None:
    session = BrowserSession(headed=False, timeout_ms=30_000)
    with session.open() as page:
        open_and_prepare(page, url, zip_code="94611")
        metadata = read_metadata(page, url)
        tiles = extract_raw_tiles(page, max_scrolls=5)

    assert metadata.source_url
    assert metadata.scrape_timestamp is not None
    assert len(tiles) > 0
