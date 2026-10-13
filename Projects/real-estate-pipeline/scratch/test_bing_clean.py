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
            b64 += "=" * ((4 - len(b64) % 4) % 4)
            try:
                return base64.b64decode(b64).decode('utf-8', errors='ignore')
            except:
                pass
    return href

queries = [
    'site:linkedin.com "Founder" "Commercial Architecture" "United States"',
    'site:linkedin.com "President" "Commercial Roofing" "United States"',
    'site:linkedin.com "Founder" "Freight Brokerage" "United States"'
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    for q in queries:
        url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(2000)
        items = page.query_selector_all("li.b_algo")
        print(f"Query: {q} -> Items: {len(items)}")
        for item in items[:4]:
            title_el = item.query_selector("h2 a")
            snippet_el = item.query_selector(".b_caption p")
            if title_el:
                title = title_el.inner_text()
                href = decode_bing_url(title_el.get_attribute("href"))
                snippet = snippet_el.inner_text() if snippet_el else ""
                print(f"  Title: {title}")
                print(f"  Href: {href}")
                print(f"  Snippet: {snippet[:100]}...")
    browser.close()
