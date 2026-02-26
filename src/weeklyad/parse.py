from __future__ import annotations

import re
from typing import Optional

PRICE_DOLLAR_RE = re.compile(r"\$(\d+(?:\.\d{1,2})?)")
MULTI_FOR_RE = re.compile(r"(?P<count>\d+)\s*for\s*\$(?P<price>\d+(?:\.\d{1,2})?)", re.IGNORECASE)
UNIT_RE = re.compile(r"\$(\d+(?:\.\d{1,2})?)\s*/\s*([A-Za-z]+)")

PROMO_KEYWORDS = [
    "member price",
    "digital coupon",
    "buy",
    "save",
    "club price",
    "bogo",
]


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def parse_price_text(raw_text: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
    text = normalize_text(raw_text)

    multi = MULTI_FOR_RE.search(text)
    if multi:
        promo = f"{multi.group('count')} for ${multi.group('price')}"
        return promo, None, promo

    dollar = PRICE_DOLLAR_RE.search(text)
    unit = UNIT_RE.search(text)
    unit_price = None
    if unit:
        unit_price = f"${unit.group(1)}/{unit.group(2)}"

    promo = extract_promo_text(text)
    if dollar:
        return f"${dollar.group(1)}", unit_price, promo

    return None, unit_price, promo


def extract_promo_text(text: str) -> Optional[str]:
    lower = text.lower()
    for keyword in PROMO_KEYWORDS:
        if keyword in lower:
            return text
    return None


def split_name_brand(text: str) -> tuple[str, Optional[str]]:
    parts = [p.strip(" -") for p in re.split(r"\||-", text, maxsplit=1)]
    if len(parts) == 2:
        return parts[0], parts[1]
    return text, None
