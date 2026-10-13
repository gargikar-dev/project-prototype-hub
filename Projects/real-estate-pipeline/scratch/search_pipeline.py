import urllib.request
import urllib.parse
import json
import re
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def clean_ddg_url(raw_url):
    if 'uddg=' in raw_url:
        match = re.search(r'uddg=([^&]+)', raw_url)
        if match:
            return urllib.parse.unquote(match.group(1))
    return raw_url

def query_ddg(query, max_results=10):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    items = []
    try:
        res = urllib.request.urlopen(req, timeout=12)
        html = res.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        links = soup.find_all('a', class_='result__url')
        snippets = soup.find_all('a', class_='result__snippet')
        titles = soup.find_all('a', class_='result__title')
        
        for l, s, t in zip(links, snippets, titles):
            href = clean_ddg_url(l.get('href', ''))
            title_text = t.get_text().strip()
            snippet_text = s.get_text().strip()
            items.append({
                'title': title_text,
                'url': href,
                'snippet': snippet_text
            })
            if len(items) >= max_results:
                break
    except Exception as e:
        print(f"Error querying '{query}': {e}")
    return items

if __name__ == '__main__':
    queries = [
        'site:linkedin.com/posts "looking for" ("lead generation" OR "outbound" OR "cold email" OR "pipeline")',
        'site:linkedin.com/posts "recommend" ("lead gen agency" OR "outbound specialist" OR "appointment setter")',
        'site:linkedin.com/in/ ("Founder" OR "Managing Principal") "Commercial Architecture" "United States"',
        'site:linkedin.com/in/ ("Founder" OR "Owner") "Commercial Interiors" "United Kingdom"',
        'site:linkedin.com/in/ ("President" OR "Owner") "Commercial Roofing" "United States"',
        'site:linkedin.com/in/ ("Founder" OR "CEO") "3PL Logistics" "United States"',
    ]
    for q in queries:
        print(f"\n--- QUERY: {q} ---")
        results = query_ddg(q, max_results=5)
        for r in results:
            print(f"[{r['title']}] -> {r['url']}")
            print(f"   {r['snippet'][:120]}")
        time.sleep(1)
