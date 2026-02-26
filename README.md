# Safeway Weekly Ad + Sale Prices Extractor

Playwright-based extractor that navigates Safeway weekly ad and sale-prices pages and exports a normalized product/price catalog.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m playwright install chromium
```

## Usage

```bash
python -m weeklyad --source both --zip 94611 --out-dir output
```

Outputs:
- `output/catalog.csv`
- `output/catalog.json` (includes `raw_text`)
- `output/run_metadata.json`

## CLI

```bash
python -m weeklyad --help
```

Options include:
- `--source weeklyad|sale-prices|both`
- `--zip 94611`
- `--headed`
- `--debug`

## Testing

```bash
pytest -q -m "not e2e"
RUN_E2E=1 pytest -q -m e2e
```

## Compliance notes

- Respect Safeway Terms of Use and robots/site policies before production use.
- Keep request rate low and run on small schedules.
- Selectors are centralized in `src/weeklyad/selectors.py` for quick updates when UI changes.

## Known limitations

- Store-selection UI can change and may require selector updates.
- Some products are image-only and may not provide full text on first render.
- End-to-end tests require network and a locally installed Playwright browser.
