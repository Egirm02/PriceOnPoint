"""Centralized selector definitions for selector drift management."""

WEEKLY_AD_URL = "https://www.safeway.com/weeklyad"
SALE_PRICES_URL = "https://www.safeway.com/shop/deals/sale-prices.html"

COOKIE_ACCEPT = [
    "button:has-text('Accept')",
    "button:has-text('I Agree')",
    "button:has-text('Continue')",
]

STORE_BUTTONS = [
    "button:has-text('Select Store')",
    "button:has-text('Choose Store')",
    "button:has-text('Change Store')",
]

ZIP_INPUTS = [
    "input[placeholder*='ZIP']",
    "input[aria-label*='ZIP']",
    "input[name*='zip']",
]

SEARCH_BUTTONS = [
    "button:has-text('Search')",
    "button:has-text('Find')",
]

STORE_RESULT_BUTTONS = [
    "button:has-text('Select')",
    "button:has-text('Set as Store')",
]

AD_METADATA = [
    "text=/Viewing Ad for/i",
    "text=/Valid/i",
    "text=/\\b[A-Z][a-z]{2}\\s+\\d{1,2}/",
]

PRODUCT_TILE_SELECTORS = [
    "[data-testid*='product']",
    "[data-testid*='offer']",
    "article:has-text('$')",
    "li:has-text('$')",
    "div:has-text('for $')",
]

LOAD_MORE_SELECTORS = [
    "button:has-text('Load More')",
    "button:has-text('Show More')",
]
