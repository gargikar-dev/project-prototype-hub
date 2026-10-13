from playwright.sync_api import sync_playwright
import time
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://duckduckgo.com")
    page.wait_for_selector("input[name='q']")
    
    query = 'site:linkedin.com/in/ "Commercial Architecture" "Founder" "United States"'
    page.fill("input[name='q']", query)
    page.press("input[name='q']", "Enter")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    
    results = page.query_selector_all("article")
    print(f"DuckDuckGo results count: {len(results)}")
    
    for r in results[:5]:
        title_el = r.query_selector("h2")
        link_el = r.query_selector("a[data-testid='result-title-a']") or r.query_selector("h2 a")
        snippet_el = r.query_selector("[data-result='snippet']")
        title = title_el.inner_text() if title_el else ""
        href = link_el.get_attribute("href") if link_el else ""
        snippet = snippet_el.inner_text() if snippet_el else ""
        print("TITLE:", title.encode('ascii', 'ignore').decode())
        print("HREF:", href)
        print("SNIPPET:", snippet.encode('ascii', 'ignore').decode()[:120])
        print("="*40)
        
    browser.close()
