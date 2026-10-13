import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

queries = [
    'site:linkedin.com/posts "looking for" "lead generation agency"',
    'site:linkedin.com/posts "looking for" "freelance lead gen"',
    'site:linkedin.com/posts "recommend" "B2B lead generation"',
    'site:linkedin.com/posts "recommend" "cold email agency"',
    'site:linkedin.com/posts "need someone to" "generate B2B leads"',
    'site:linkedin.com/posts "need someone to" "book sales meetings"',
    'site:linkedin.com/posts "hiring an agency" "lead gen"',
    'site:linkedin.com/posts "hiring a contractor" "lead gen"',
]

found = set()

for q in queries:
    # Yahoo search
    url = f"https://search.yahoo.com/search?p={urllib.parse.quote(q)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'https?://[a-zA-Z0-9.\-]+linkedin\.com/posts/[^\s\"\'<>?&]+', html)
        for m in matches:
            if "/jobs/" not in m:
                found.add(m)
        print(f"Yahoo {q}: found {len(matches)} matches")
    except Exception as e:
        print(f"Yahoo error {q}: {e}")

print(f"Yahoo Total unique: {len(found)}")
for u in found:
    print(u)
