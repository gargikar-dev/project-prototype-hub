import requests
from bs4 import BeautifulSoup
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# Test Brave Search
q = 'site:linkedin.com/in "Managing Principal" "Commercial Architecture"'
url = f"https://search.brave.com/search?q={urllib.parse.quote(q)}"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print("Brave status:", r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if 'linkedin.com/in/' in href:
            print("Brave LinkedIn:", href)
except Exception as e:
    print("Brave error:", e)
