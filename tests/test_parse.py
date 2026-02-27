from datetime import datetime, timezone

from weeklyad.extract import dedupe_catalog
from weeklyad.models import CatalogItem
from weeklyad.parse import parse_price_text


def make_item(name: str, price: str) -> CatalogItem:
    return CatalogItem(
        item_name=name,
        price_text=price,
        unit_price=None,
        promo=None,
        brand_size=None,
        valid_from=None,
        valid_to=None,
        store_name=None,
        store_address=None,
        source_url="https://www.safeway.com/weeklyad",
        scrape_timestamp=datetime.now(timezone.utc),
        raw_text=f"{name} {price}",
    )


def test_parse_price_dollar_amount() -> None:
    price, unit_price, promo = parse_price_text("Large Avocado $2.99 each")
    assert price == "$2.99"
    assert unit_price is None
    assert promo is None


def test_parse_price_multi_for() -> None:
    price, unit_price, promo = parse_price_text("Soda 2 for $5")
    assert price == "2 for $5"
    assert unit_price is None
    assert promo == "2 for $5"


def test_deduping_logic() -> None:
    items = [make_item("Milk", "$3.99"), make_item("milk", "$3.99"), make_item("Eggs", "$2.99")]
    deduped = dedupe_catalog(items)
    assert len(deduped) == 2


def test_schema_validation_required_fields() -> None:
    item = make_item("Bread", "$1.99")
    assert item.item_name == "Bread"
    assert item.price_text == "$1.99"
