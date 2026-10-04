import argparse
import json
import os
from datetime import datetime
from scraper import GuptcharScraper
from pdf_generator import generate_pdf

def main():
    parser = argparse.ArgumentParser(description="Guptchar Core Data Extraction Engine")
    parser.add_argument("--country", required=True, help="Target Country (e.g. 'United States')")
    parser.add_argument("--state", default="", help="Target State or Region (Optional)")
    parser.add_argument("--city", required=True, help="Target City (e.g. 'New York')")
    parser.add_argument("--keyword", required=True, help="Target Sector/Keyword (e.g. 'Hedge Funds')")
    parser.add_argument("--finance", action="store_true", help="Enable SEC EDGAR Stage C extraction")
    
    args = parser.parse_args()
    
    print("=============================================")
    print(f"[*] Starting Guptchar Extraction Pipeline")
    print(f"[*] Target: {args.keyword} in {args.city}{', ' + args.state if args.state else ''}, {args.country}")
    print("=============================================")
    
    scraper = GuptcharScraper(args.country, args.city, args.keyword, args.state)
    data = scraper.run(include_finance=args.finance)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    city_str = args.city.replace(' ', '_').lower()
    
    output_dir = "output_pdfs"
    os.makedirs(output_dir, exist_ok=True)
    
    json_filename = os.path.join(output_dir, f"guptchar_output_{city_str}_{timestamp}.json")
    pdf_filename = os.path.join(output_dir, f"guptchar_output_{city_str}_{timestamp}.pdf")
    
    # Save JSON
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data.model_dump(), f, indent=2)
        
    print(f"[*] Data successfully saved to {json_filename}")
    
    # Save PDF
    try:
        generate_pdf(data, pdf_filename)
    except Exception as e:
        print(f"[!] PDF Generation failed: {e}")
        
    print("[*] Guptchar Extraction Complete. Pipeline closed.")

if __name__ == "__main__":
    main()