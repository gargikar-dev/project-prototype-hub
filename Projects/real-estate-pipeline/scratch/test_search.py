import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def search_ddg(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, timeout=10)
        html = res.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        links = soup.find_all('a', class_='result__url')
        snippets = soup.find_all('a', class_='result__snippet')
        print(f"Found {len(links)} links")
        for l, s in zip(links, snippets):
            href = l.get('href', '')
            print("Link:", href)
            print("Snippet:", s.get_text()[:100])
        return results
    except Exception as e:
        print("Error:", e)
        return []

if __name__ == '__main__':
    search_ddg('site:linkedin.com/posts "lead generation" "founder"')
