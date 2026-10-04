# Guptchar Core Data Extraction Engine (V1.0)

## Project Context
Guptchar automatically scrapes, enriches, and structures high-value B2B prospect data across multiple stages.

## Data Extraction Pipeline Workflow
1. **Input Parameters:** Country, City, Sector / Keyword
2. **Stage A (Google Maps):** Extract business details, generic_contact_number, and official website URL.
3. **Stage B (Website Enrichment):** Crawl /contact, /about, /team, /leadership pages. Extract primary emails, phone numbers, and associate with team members. Use anti-bot protection (e.g. undetected-chromedriver, playwright-stealth, or cloudscraper).
4. **Stage C (Regulatory Filings):** If sector is Financial/Compliance, query public regulatory repositories (e.g. SEC EDGAR API) for C-Suite executives.

## Output Requirements
- **JSON Structure:** 
  ```json
  {
    "company_name": "...",
    "address": "...",
    "website": "...",
    "generic_contact_number": "...",
    "primary_email": "...",
    "one_sentence_description": "...",
    "executives_and_contacts": [
      {
        "name": "...",
        "title": "...",
        "phone": "...",
        "email": "...",
        "source": "..."
      }
    ]
  }
  ```
- **File Outputs:** 
  - `guptchar_output_[city]_[timestamp].json`
  - Formatted PDF (`ReportLab` or `fpdf2`) with cards/tables for Company Name, Phone, Email, Address, Summary, and Executives.

## Tech Stack
- **Language:** Python 3.10+
- **Scraping:** playwright (with playwright-stealth) OR selenium + BeautifulSoup4 + cloudscraper
- **Parsing:** re, html5lib/lxml
- **PDF Export:** ReportLab or fpdf2
- **Constraints:** $0 budget (open-source only), modular CLI/FastAPI architecture, complete error handling.
