import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

queries = [
    'site:linkedin.com/in/ "William Duff" "William Duff Architects"',
    'site:linkedin.com/in/ "Founder" "Commercial Architecture" "United States"',
    'site:linkedin.com/in/ "Owner" "Commercial Roofing" "United States"',
    'site:linkedin.com/in/ "Founder" "Freight Brokerage" "United States"'
]

for q in queries:
    url = "https://www.google.com/search?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            urls = re.findall(r'https://(?:[a-z]{2,3}\.)?linkedin\.com/in/[a-zA-Z0-9_\-%]+', html)
            # Remove any google tracking wrapping
            clean_urls = list(dict.fromkeys(urls))
            print(f"Query: {q}")
            print(f"Found {len(clean_urls)} profiles:", clean_urls[:5])
    except Exception as e:
        print(f"Error on {q}: {e}")
