import re
import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from models import CompanyData, ExecutiveContact

def extract_emails_from_text(text):
    return list(set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)))

def extract_phones_from_text(text):
    return list(set(re.findall(r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}', text)))

class GuptcharScraper:
    def __init__(self, country, city, keyword, state=""):
        self.country = country
        self.city = city
        self.keyword = keyword
        self.state = state
        self.data = CompanyData()
        
    def stage_a_google_maps(self):
        print("[*] Stage A: Google Maps Extraction")
        location = f"{self.city}, {self.state}, {self.country}" if self.state else f"{self.city}, {self.country}"
        query = f"{self.keyword} in {location}"
        url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
            
            try:
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                page.wait_for_selector('a[href^="https://www.google.com/maps/place/"]', timeout=15000)
                first_result = page.locator('a[href^="https://www.google.com/maps/place/"]').first
                first_result.click()
                
                time.sleep(5) 
                
                try:
                    h1_els = page.locator('h1').all()
                    for el in h1_els:
                        text = el.inner_text().strip()
                        if text and text.lower() != "results":
                            self.data.company_name = text
                            break
                except:
                    pass
                
                try:
                    website_el = page.locator('a[data-item-id=authority]').first
                    website_url = website_el.get_attribute("href")
                    print("Website:", website_url)
                    self.data.website = website_el.get_attribute("href") if website_el else "N/A"
                except:
                    pass
                    
                try:
                    phone_el = page.locator('button[data-tooltip="Copy phone number"]').first
                    if phone_el.is_visible():
                        phone_text = phone_el.inner_text()
                        # Clean out icon fonts (e.g. \ue0b0\n)
                        self.data.generic_contact_number = phone_text.split('\n')[-1].strip()
                except:
                    pass
                
                try:
                    address_el = page.locator('button[data-tooltip="Copy address"]').first
                    if address_el.is_visible():
                        addr_text = address_el.inner_text()
                        # Clean out icon fonts
                        self.data.address = addr_text.split('\n')[-1].strip()
                except:
                    pass
                    
            except Exception as e:
                print(f"[!] Error in Stage A: {e}")
            finally:
                browser.close()
                
        print(f"    -> Found: {self.data.company_name} | {self.data.website}")
        
    def stage_b_website_enrichment(self):
        print("[*] Stage B: Website Enrichment")
        if self.data.website == "N/A":
            print("    -> No website found. Skipping Stage B.")
            return
            
        urls_to_visit = [self.data.website]
        base_url = self.data.website.rstrip('/')
        for path in ['/contact', '/about', '/team', '/leadership']:
            urls_to_visit.append(f"{base_url}{path}")
            
        all_text = ""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page = context.new_page()
            
            for url in urls_to_visit:
                try:
                    page.goto(url, timeout=15000)
                    all_text += " " + page.locator("body").inner_text()
                except:
                    pass
            browser.close()
            
        emails = extract_emails_from_text(all_text)
        phones = extract_phones_from_text(all_text)
        
        emails = [e for e in emails if not any(x in e.lower() for x in ['sentry', 'example', 'wix'])]
        
        if emails:
            self.data.primary_email = emails[0]
            
        print(f"    -> Extracted {len(emails)} emails and {len(phones)} phone numbers.")
        if self.data.generic_contact_number == "N/A" and phones:
            self.data.generic_contact_number = phones[0]
            
        if self.data.company_name != "N/A":
            self.data.one_sentence_description = f"{self.data.company_name} is a {self.keyword} business located in {self.city}."
        else:
            self.data.one_sentence_description = f"A {self.keyword} business located in {self.city}."

    def stage_c_sec_edgar(self):
        print("[*] Stage C: SEC EDGAR Look-up")
        if self.data.company_name == "N/A":
            return
            
        headers = {"User-Agent": "Guptchar App (admin@guptchar.local)"}
        try:
            r = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers, timeout=10)
            if r.status_code == 200:
                tickers = r.json()
                search_name = self.data.company_name.lower().split()[0]
                cik = None
                for key, val in tickers.items():
                    if search_name in val['title'].lower():
                        cik = str(val['cik_str']).zfill(10)
                        break
                
                if cik:
                    print(f"    -> Found SEC match, CIK: {cik}")
                    sec_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
                    sub_r = requests.get(sec_url, headers=headers, timeout=10)
                    if sub_r.status_code == 200:
                        company_info = sub_r.json()
                        self.data.executives_and_contacts.append(ExecutiveContact(
                            name="Registered Agent / Principal",
                            title="Executive (SEC Filing)",
                            source="SEC EDGAR",
                            phone=company_info.get("phone", "N/A")
                        ))
                else:
                    print("    -> No SEC EDGAR match found.")
        except Exception as e:
            print(f"[!] SEC EDGAR lookup failed: {e}")

    def run(self, include_finance=False):
        self.stage_a_google_maps()
        self.stage_b_website_enrichment()
        if include_finance:
            self.stage_c_sec_edgar()
        return self.data
