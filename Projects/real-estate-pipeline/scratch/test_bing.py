import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def search_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=10)
        soup = BeautifulSoup(res.read(), 'html.parser')
        results = []
        for li in soup.find_all('li', class_='b_algo'):
            h2 = li.find('h2')
            if not h2:
                continue
            a = h2.find('a')
            if not a:
                continue
            title = a.get_text()
            href = a.get('href')
            snippet = li.find('p')
            snip_text = snippet.get_text() if snippet else ""
            results.append({'title': title, 'url': href, 'snippet': snip_text})
        return results
    except Exception as e:
        print("Bing error:", e)
        return []

if __name__ == '__main__':
    res = search_bing('site:linkedin.com/in "Founder" "Commercial Architecture" "United States"')
    print(f"Bing found: {len(res)}")
    for r in res[:5]:
        print(r['title'])
        print(r['url'])
        print(r['snippet'][:100])
