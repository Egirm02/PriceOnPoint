from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import CatalogItem

CSV_COLUMNS = [
    "item_name",
    "price_text",
    "unit_price",
    "promo",
    "brand_size",
    "valid_from",
    "valid_to",
    "store_name",
    "store_address",
    "source_url",
    "scrape_timestamp",
]


def write_csv(items: list[CatalogItem], path: str | Path) -> None:
    out = Path(path)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for item in items:
            row = item.to_dict()
            writer.writerow({k: row.get(k) for k in CSV_COLUMNS})


def write_json(items: list[CatalogItem], path: str | Path) -> None:
    out = Path(path)
    payload = [item.to_dict() for item in items]
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
