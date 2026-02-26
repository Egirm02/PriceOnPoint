from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse


@dataclass
class CatalogItem:
    item_name: str
    price_text: str
    unit_price: Optional[str]
    promo: Optional[str]
    brand_size: Optional[str]
    valid_from: Optional[str]
    valid_to: Optional[str]
    store_name: Optional[str]
    store_address: Optional[str]
    source_url: str
    scrape_timestamp: datetime
    raw_text: str

    def __post_init__(self) -> None:
        if not self.item_name.strip():
            raise ValueError("item_name is required")
        if not self.price_text.strip():
            raise ValueError("price_text is required")
        parsed = urlparse(self.source_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("source_url must be absolute")

    def to_dict(self) -> dict:
        data = asdict(self)
        data["scrape_timestamp"] = self.scrape_timestamp.isoformat()
        return data


@dataclass
class RunMetadata:
    source_url: str
    store_name: Optional[str]
    store_address: Optional[str]
    valid_from: Optional[str]
    valid_to: Optional[str]
    scrape_timestamp: datetime

    def to_dict(self) -> dict:
        return {
            "source_url": self.source_url,
            "store_name": self.store_name,
            "store_address": self.store_address,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to,
            "scrape_timestamp": self.scrape_timestamp.isoformat(),
        }
