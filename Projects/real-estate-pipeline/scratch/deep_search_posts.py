import urllib.request
import urllib.parse
import re
import json

queries = [
    # Category 1: looking for
    'site:linkedin.com/posts "looking for" "lead generation agency"',
    'site:linkedin.com/posts "looking for" "freelance lead gen"',
    'site:linkedin.com/posts "looking for" "outbound specialist"',
    'site:linkedin.com/posts "looking for" "b2b lead generation"',
    'site:linkedin.com/posts "looking for" "appointment setter"',
    'site:linkedin.com/posts "looking for" "appointment setting"',
    'site:linkedin.com/posts "looking for" "cold email agency"',

    # Category 2: recommend
    'site:linkedin.com/posts "recommend" "B2B lead generation"',
    'site:linkedin.com/posts "recommend" "lead generation agency"',
    'site:linkedin.com/posts "recommend" "cold email agency"',
    'site:linkedin.com/posts "recommend" "appointment setting service"',
    'site:linkedin.com/posts "recommend" "outbound agency"',

    # Category 3: need someone to
    'site:linkedin.com/posts "need someone to" "generate B2B leads"',
    'site:linkedin.com/posts "need someone to" "generate leads"',
    'site:linkedin.com/posts "need someone to" "build outbound pipeline"',
    'site:linkedin.com/posts "need someone to" "book sales meetings"',
    'site:linkedin.com/posts "need someone to" "book appointments"',

    # Category 4: hiring agency / contractor
    'site:linkedin.com/posts "hiring an agency" "lead gen"',
    'site:linkedin.com/posts "hiring a contractor" "lead gen"',
    'site:linkedin.com/posts "hiring an agency" "outbound"',
    'site:linkedin.com/posts "hiring a contractor" "outbound"',
    'site:linkedin.com/posts "hiring" "freelance lead generation"',
    'site:linkedin.com/posts "looking to hire" "lead generation agency"',

    # Feed updates
    'site:linkedin.com/feed/update "looking for" "lead generation agency"',
    'site:linkedin.com/feed/update "recommend" "lead generation agency"',
    'site:linkedin.com/feed/update "need someone to" "generate leads"'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

all_found = {}

for q in queries:
    # Try DuckDuckGo html
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'uddg=([^&]+)', html)
        for m in matches:
            unquoted = urllib.parse.unquote(m)
            if ("linkedin.com/posts/" in unquoted or "linkedin.com/feed/update/" in unquoted) and "/jobs/" not in unquoted:
                clean_url = unquoted.split("?")[0]
                if clean_url not in all_found:
                    all_found[clean_url] = q
    except Exception as e:
        print(f"Error {q}: {e}")

print(f"Total discovered unique URLs: {len(all_found)}")
for u, q in all_found.items():
    print(f"- {u} (query: {q})")

with open("scratch/discovered_post_urls.json", "w", encoding="utf-8") as f:
    json.dump(all_found, f, indent=2)
