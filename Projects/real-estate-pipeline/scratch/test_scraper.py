import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

queries = [
    'site:linkedin.com/posts "looking for" "lead generation agency"',
    'site:linkedin.com/posts "looking for" "freelance lead gen"',
    'site:linkedin.com/posts "looking for" "outbound specialist"',
    'site:linkedin.com/posts "recommend" "B2B lead generation"',
    'site:linkedin.com/posts "recommend" "cold email agency"',
    'site:linkedin.com/posts "recommend" "appointment setting service"',
    'site:linkedin.com/posts "need someone to" "generate B2B leads"',
    'site:linkedin.com/posts "need someone to" "build outbound pipeline"',
    'site:linkedin.com/posts "need someone to" "book sales meetings"',
    'site:linkedin.com/posts "hiring an agency" "lead gen"',
    'site:linkedin.com/posts "hiring a contractor" "lead gen"',
    'site:linkedin.com/posts "hiring an agency" "outbound"',
    'site:linkedin.com/posts "hiring a contractor" "outbound"',
    'site:linkedin.com/feed/update "looking for" "lead generation agency"',
    'site:linkedin.com/feed/update "recommend" "B2B lead generation"',
    'site:linkedin.com/feed/update "need someone to" "book sales meetings"',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

found_links = set()

for q in queries:
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        
        # Duckduckgo result links are in <a class="result__url" href="..."> or <a class="result__snippet" ...> or /uddg=...
        matches = re.findall(r'uddg=([^&]+)', html)
        for m in matches:
            unquoted = urllib.parse.unquote(m)
            if ("linkedin.com/posts/" in unquoted or "linkedin.com/feed/update/" in unquoted) and "/jobs/" not in unquoted:
                # clean up url
                clean_url = unquoted.split("?")[0]
                found_links.add(clean_url)
    except Exception as e:
        print(f"Error for {q}: {e}")

print(f"Total unique post links found: {len(found_links)}")
for l in list(found_links)[:10]:
    print(l)
