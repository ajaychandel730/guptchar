# Guptchar Core Data Extraction Engine (V1.0)

Guptchar is a high-precision lead-generation and data extraction module built to scrape, enrich, and structure B2B prospect data across multiple stages.

## Features

- **Stage A (Local Search)**: Uses Playwright to search Google Maps and extract initial business profiles (Name, Address, Phone, Website).
- **Stage B (Website Enrichment)**: Crawls the discovered website (and common contact/about pages) to parse primary emails and additional contact numbers.
- **Stage C (Regulatory Extraction)**: Queries the public SEC EDGAR API for C-Suite executives and registered personnel for Financial/Compliance targets.
- **Reporting**: Outputs clean, structured JSON files and a formatted PDF Report (using ReportLab).

## Installation

Ensure you have Python 3.10+ installed. Set up the environment with:

```bash
# Create and activate a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Usage

Run the CLI pipeline using `main.py`:

```bash
python main.py --country "United States" --city "New York" --keyword "Hedge Funds" --finance
```

### Arguments:

- `--country` (Required): Target Country
- `--city` (Required): Target City
- `--keyword` (Required): Target Sector/Keyword
- `--finance` (Optional): Include this flag to enable Stage C (SEC EDGAR extraction) for financial targets.

## Output

The script generates two artifacts in the root directory:
1. `guptchar_output_[city]_[timestamp].json`
2. `guptchar_output_[city]_[timestamp].pdf`

## Architecture Highlights
- Fully modular (`models.py`, `scraper.py`, `pdf_generator.py`, `main.py`).
- Built with `$0` budget (no paid scraping APIs).
- Leverages Playwright for Stealth browsing capabilities and robust modern web evaluation.
