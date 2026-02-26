from __future__ import annotations

import argparse
import json
from pathlib import Path

from .extract import extract_raw_tiles, normalize_tiles, open_and_prepare, read_metadata
from .browser import BrowserSession
from .export import write_csv, write_json
from .selectors import SALE_PRICES_URL, WEEKLY_AD_URL


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Safeway catalog extractor")
    p.add_argument("--zip", dest="zip_code", help="ZIP code used for store selection")
    p.add_argument("--source", choices=["weeklyad", "sale-prices", "both"], default="both")
    p.add_argument("--headed", action="store_true", help="Run browser in headed mode")
    p.add_argument("--debug", action="store_true")
    p.add_argument("--max-scrolls", type=int, default=20)
    p.add_argument("--out-dir", default=".")
    return p


def selected_urls(source: str) -> list[str]:
    if source == "weeklyad":
        return [WEEKLY_AD_URL]
    if source == "sale-prices":
        return [SALE_PRICES_URL]
    return [WEEKLY_AD_URL, SALE_PRICES_URL]


def main() -> int:
    args = build_parser().parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_items = []
    run_meta = []

    browser = BrowserSession(headed=args.headed)
    with browser.open() as page:
        for url in selected_urls(args.source):
            open_and_prepare(page, url, zip_code=args.zip_code)
            metadata = read_metadata(page, url)
            raw_tiles = extract_raw_tiles(page, max_scrolls=args.max_scrolls)
            items = normalize_tiles(raw_tiles, metadata)
            all_items.extend(items)
            run_meta.append(metadata.to_dict())

            if args.debug:
                debug_file = out_dir / f"debug_{url.split('/')[-1] or 'weeklyad'}.txt"
                debug_file.write_text("\n\n".join(x.text for x in raw_tiles[:10]), encoding="utf-8")
                page.screenshot(path=str(out_dir / f"debug_{url.split('/')[-1] or 'weeklyad'}.png"), full_page=True)

    write_csv(all_items, out_dir / "catalog.csv")
    write_json(all_items, out_dir / "catalog.json")
    (out_dir / "run_metadata.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    print(f"Extracted {len(all_items)} items into {out_dir / 'catalog.csv'} and {out_dir / 'catalog.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
