import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

def test_bing_search(query):
    # Bing search with standard web results
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=10)
        html = res.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for li in soup.find_all('li', class_='b_algo'):
            h2 = li.find('h2')
            if not h2: continue
            a = h2.find('a')
            if not a: continue
            title = a.get_text()
            href = a.get('href', '')
            p = li.find('p')
            snip = p.get_text() if p else ''
            results.append({'title': title, 'url': href, 'snippet': snip})
        return results
    except Exception as e:
        print("Error:", e)
        return []

if __name__ == '__main__':
    # Test queries
    q1 = 'site:linkedin.com/in "Commercial Architecture" "Managing Principal" "United States"'
    print("Testing q1...")
    res = test_bing_search(q1)
    print(f"Results: {len(res)}")
    for r in res[:5]:
        print("T:", r['title'])
        print("U:", r['url'])
        print("S:", r['snippet'][:80])
