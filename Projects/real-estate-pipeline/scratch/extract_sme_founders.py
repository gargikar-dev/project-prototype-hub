import time
import json
import re
from playwright.sync_api import sync_playwright

def search_query(page, query):
    print(f"\n--- Searching: {query} ---")
    search_url = f"https://www.google.com/search?q={query}&num=20"
    try:
        page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)
        
        # Check if consent / captcha
        if "consent.google.com" in page.url or "sorry/index" in page.url:
            print("Google captcha/consent encountered. Trying DuckDuckGo / Bing...")
            # Fallback to Bing
            bing_url = f"https://www.bing.com/search?q={query}"
            page.goto(bing_url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            
        # Extract links and text
        links = page.query_selector_all("a")
        results = []
        for l in links:
            href = l.get_attribute("href")
            text = l.inner_text()
            if href and "linkedin.com/in/" in href:
                # Clean URL
                m = re.search(r'(https://[a-z]{2,3}\.linkedin\.com/in/[a-zA-Z0-9_\-%]+|https://linkedin\.com/in/[a-zA-Z0-9_\-%]+)', href)
                if m:
                    clean_href = m.group(1)
                    parent_text = ""
                    try:
                        parent = l.evaluate_handle("el => el.closest('div.g') || el.closest('li.b_algo') || el.parentElement")
                        if parent:
                            parent_text = parent.inner_text()
                    except:
                        pass
                    results.append({
                        "url": clean_href,
                        "title": text,
                        "context": parent_text
                    })
        print(f"Extracted {len(results)} LinkedIn profiles for query.")
        return results
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def main():
    queries = [
        'site:linkedin.com/in/ ("Founder" OR "Managing Principal" OR "Owner") AND ("Commercial Architecture" OR "Commercial Interiors") AND ("United States" OR "United Kingdom")',
        'site:linkedin.com/in/ ("President" OR "Owner") AND ("Commercial Roofing" OR "Facility Services") AND ("United States")',
        'site:linkedin.com/in/ ("Founder" OR "Managing Director") AND ("Freight Brokerage" OR "3PL Logistics") AND ("United States" OR "UK")'
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="en-US"
        )
        page = context.new_page()
        all_results = {}
        for q in queries:
            res = search_query(page, q)
            all_results[q] = res
            time.sleep(3)
        browser.close()
        
    with open("scratch/raw_search_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print("\nSaved raw search results to scratch/raw_search_results.json")

if __name__ == "__main__":
    main()
