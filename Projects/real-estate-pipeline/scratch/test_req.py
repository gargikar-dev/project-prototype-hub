import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

queries = [
    '"Managing Principal" "Commercial Architecture" linkedin',
    '"Founder" "Commercial Interiors" linkedin',
    '"President" "Commercial Roofing" linkedin',
    '"Founder" "3PL Logistics" linkedin',
    '"looking for" "lead generation" site:linkedin.com/posts',
    '"looking for" "cold email" site:linkedin.com/posts',
]

for q in queries:
    print(f"\nQuery: {q}")
    try:
        r = requests.get('https://html.duckduckgo.com/html/', params={'q': q}, headers=headers, timeout=10)
        print(f"Status: {r.status_code}, Length: {len(r.text)}")
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a', class_='result__url')
        print(f"Links found: {len(links)}")
        for l in links[:3]:
            print("  ", l.get('href'))
    except Exception as e:
        print("Error:", e)
