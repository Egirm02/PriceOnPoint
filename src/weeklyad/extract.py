from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
import time

from . import selectors
from .browser import dismiss_cookie_banner, select_store_by_zip
from .models import CatalogItem, RunMetadata
from .parse import normalize_text, parse_price_text, split_name_brand


@dataclass
class RawTile:
    text: str
    source_url: str


def open_and_prepare(page, source_url: str, zip_code: str | None = None) -> None:
    page.goto(source_url, wait_until="domcontentloaded")
    dismiss_cookie_banner(page)
    select_store_by_zip(page, zip_code)


def _try_read_metadata_text(page) -> str:
    for selector in selectors.AD_METADATA:
        loc = page.locator(selector).first
        try:
            if loc.is_visible(timeout=2000):
                return normalize_text(loc.inner_text())
        except Exception:
            continue
    return ""


def read_metadata(page, source_url: str) -> RunMetadata:
    body = normalize_text(page.locator("body").inner_text())
    marker = _try_read_metadata_text(page)
    if marker:
        body = f"{marker} {body}"

    date_match = re.search(r"([A-Z][a-z]{2}\s+\d{1,2}).{0,12}([A-Z][a-z]{2}\s+\d{1,2})", body)
    valid_from, valid_to = (date_match.group(1), date_match.group(2)) if date_match else (None, None)

    store_match = re.search(r"Viewing Ad for[:\s]+([^\n\|]+)", body, re.IGNORECASE)
    store_name = store_match.group(1).strip() if store_match else None

    return RunMetadata(
        source_url=source_url,
        store_name=store_name,
        store_address=None,
        valid_from=valid_from,
        valid_to=valid_to,
        scrape_timestamp=datetime.now(timezone.utc),
    )


def extract_raw_tiles(page, max_scrolls: int = 20) -> list[RawTile]:
    load_more = True
    previous_count = -1

    for _ in range(max_scrolls):
        if load_more:
            for selector in selectors.LOAD_MORE_SELECTORS:
                btn = page.locator(selector).first
                try:
                    if btn.is_visible(timeout=500):
                        btn.click()
                        time.sleep(0.6)
                except Exception:
                    pass

        page.mouse.wheel(0, 3000)
        time.sleep(0.8)

        tile_count = count_tiles(page)
        if tile_count <= previous_count:
            break
        previous_count = tile_count

    texts: list[str] = []
    for selector in selectors.PRODUCT_TILE_SELECTORS:
        loc = page.locator(selector)
        count = loc.count()
        for idx in range(count):
            try:
                raw = normalize_text(loc.nth(idx).inner_text())
            except Exception:
                continue
            if raw and "$" in raw:
                texts.append(raw)

    deduped = list(dict.fromkeys(texts))
    return [RawTile(text=t, source_url=page.url) for t in deduped]


def count_tiles(page) -> int:
    total = 0
    for selector in selectors.PRODUCT_TILE_SELECTORS:
        total += page.locator(selector).count()
    return total


def normalize_tiles(raw_tiles: list[RawTile], metadata: RunMetadata) -> list[CatalogItem]:
    catalog: list[CatalogItem] = []
    for tile in raw_tiles:
        text = normalize_text(tile.text)
        price_text, unit_price, promo = parse_price_text(text)
        if not price_text:
            continue
        item_name, brand_size = split_name_brand(text)
        catalog.append(
            CatalogItem(
                item_name=item_name,
                price_text=price_text,
                unit_price=unit_price,
                promo=promo,
                brand_size=brand_size,
                valid_from=metadata.valid_from,
                valid_to=metadata.valid_to,
                store_name=metadata.store_name,
                store_address=metadata.store_address,
                source_url=tile.source_url,
                scrape_timestamp=metadata.scrape_timestamp,
                raw_text=text,
            )
        )
    return dedupe_catalog(catalog)


def dedupe_catalog(items: list[CatalogItem]) -> list[CatalogItem]:
    seen: set[tuple[str, str, str]] = set()
    out: list[CatalogItem] = []
    for item in items:
        key = (item.item_name.lower(), item.price_text, str(item.source_url))
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out
