import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def search_yahoo(query):
    url = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}&n=15"
    req = urllib.request.Request(url, headers=headers)
    items = []
    try:
        res = urllib.request.urlopen(req, timeout=10)
        soup = BeautifulSoup(res.read(), 'html.parser')
        for div in soup.find_all('div', class_='algo'):
            h3 = div.find('h3')
            if not h3:
                continue
            a = h3.find('a')
            if not a:
                continue
            link = a.get('href', '')
            title = a.get_text()
            desc = div.find('div', class_='compText')
            desc_text = desc.get_text() if desc else ""
            items.append({'title': title, 'url': link, 'snippet': desc_text})
    except Exception as e:
        print("Yahoo error:", e)
    return items

def search_ddg_lite(query):
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request('https://lite.duckduckgo.com/lite/', data=data, headers=headers)
    items = []
    try:
        res = urllib.request.urlopen(req, timeout=10)
        soup = BeautifulSoup(res.read(), 'html.parser')
        links = soup.find_all('a', class_='result-link')
        snippets = soup.find_all('td', class_='result-snippet')
        for l, s in zip(links, snippets):
            href = l.get('href', '')
            if 'uddg=' in href:
                m = re.search(r'uddg=([^&]+)', href)
                if m:
                    href = urllib.parse.unquote(m.group(1))
            items.append({'title': l.get_text().strip(), 'url': href, 'snippet': s.get_text().strip()})
    except Exception as e:
        print("DDG Lite error:", e)
    return items

if __name__ == '__main__':
    print("Testing Yahoo:")
    y_res = search_yahoo('site:linkedin.com/in "Founder" "Commercial Architecture"')
    print(f"Yahoo found: {len(y_res)}")
    for r in y_res[:3]:
        print(r['title'], '->', r['url'])

    print("\nTesting DDG Lite:")
    d_res = search_ddg_lite('site:linkedin.com/in "Founder" "Commercial Architecture"')
    print(f"DDG Lite found: {len(d_res)}")
    for r in d_res[:3]:
        print(r['title'], '->', r['url'])
