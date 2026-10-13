import urllib.parse
import base64
import json
import re
from playwright.sync_api import sync_playwright

def decode_bing_url(href):
    if not href:
        return ""
    if "bing.com/ck/a?" in href and "u=" in href:
        m = re.search(r'u=a1([a-zA-Z0-9_\-]+)', href)
        if m:
            b64 = m.group(1).replace('-', '+').replace('_', '/')
            # Pad base64
            b64 += "=" * ((4 - len(b64) % 4) % 4)
            try:
                return base64.b64decode(b64).decode('utf-8', errors='ignore')
            except:
                pass
    return href

queries = [
    'site:linkedin.com/in "Founder" "Commercial Architecture" "United States"',
    'site:linkedin.com/in "Managing Principal" "Commercial Architecture"',
    'site:linkedin.com/in "Owner" "Commercial Roofing" "United States"',
    'site:linkedin.com/in "President" "Commercial Roofing" "United States"',
    'site:linkedin.com/in "Founder" "Freight Brokerage" "United States"',
    'site:linkedin.com/in "Managing Director" "Freight Brokerage" "UK"',
    'site:linkedin.com/in "Founder" "3PL Logistics" "United States"'
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    
    for q in queries:
        url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(1500)
        items = page.query_selector_all("li.b_algo")
        for item in items:
            title_el = item.query_selector("h2 a")
            snippet_el = item.query_selector(".b_caption p")
            if not title_el:
                continue
            title = title_el.inner_text()
            raw_href = title_el.get_attribute("href")
            decoded_href = decode_bing_url(raw_href)
            snippet = snippet_el.inner_text() if snippet_el else ""
            if "linkedin.com/in/" in decoded_href:
                results.append({
                    "query": q,
                    "title": title,
                    "url": decoded_href,
                    "snippet": snippet
                })
    browser.close()

with open("scratch/bing_linkedin_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Total LinkedIn profiles found: {len(results)}")
for r in results[:10]:
    print(r["title"], "-->", r["url"])
