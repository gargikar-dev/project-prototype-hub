import urllib.request
import urllib.parse
import json
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

queries = [
    # 1. looking for
    'site:linkedin.com/posts "looking for" "lead generation agency"',
    'site:linkedin.com/posts "looking for" "freelance lead gen"',
    'site:linkedin.com/posts "looking for" "outbound specialist"',
    'site:linkedin.com/posts "looking for" "lead generation" founder',
    'site:linkedin.com/posts "looking for" "cold email agency"',
    'site:linkedin.com/posts "looking for" "appointment setting"',

    # 2. recommend
    'site:linkedin.com/posts "recommend" "B2B lead generation"',
    'site:linkedin.com/posts "recommend" "cold email agency"',
    'site:linkedin.com/posts "recommend" "lead generation agency"',
    'site:linkedin.com/posts "recommend" "appointment setting"',

    # 3. need someone to
    'site:linkedin.com/posts "need someone to" "generate B2B leads"',
    'site:linkedin.com/posts "need someone to" "build outbound pipeline"',
    'site:linkedin.com/posts "need someone to" "book sales meetings"',
    'site:linkedin.com/posts "need someone to" "generate leads" founder',

    # 4. hiring agency / contractor
    'site:linkedin.com/posts "hiring an agency" "lead gen"',
    'site:linkedin.com/posts "hiring a contractor" "lead gen"',
    'site:linkedin.com/posts "hiring an agency" "outbound"',
    'site:linkedin.com/posts "hiring a contractor" "outbound"',
    'site:linkedin.com/posts "looking to hire" "lead gen" agency',
]

def search_bing(query):
    urls = set()
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'https?://[a-zA-Z0-9.\-]+linkedin\.com/posts/[a-zA-Z0-9_\-]+activity[a-zA-Z0-9_\-]+', html)
        for m in matches:
            urls.add(m)
        # Also any general linkedin.com/posts/
        matches2 = re.findall(r'https?://[a-zA-Z0-9.\-]+linkedin\.com/posts/[^\s\"\'<>?&]+', html)
        for m in matches2:
            if "/jobs/" not in m:
                urls.add(m)
    except Exception as e:
        print(f"Bing error for '{query}': {e}")
    return urls

def search_ddg(query):
    urls = set()
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'uddg=([^&]+)', html)
        for m in matches:
            unquoted = urllib.parse.unquote(m)
            if ("linkedin.com/posts/" in unquoted or "linkedin.com/feed/update/" in unquoted) and "/jobs/" not in unquoted:
                urls.add(unquoted.split("?")[0])
    except Exception as e:
        print(f"DDG error for '{query}': {e}")
    return urls

all_urls = set()

for q in queries:
    print(f"Searching: {q}")
    b_urls = search_bing(q)
    all_urls.update(b_urls)
    time.sleep(1)
    d_urls = search_ddg(q)
    all_urls.update(d_urls)
    time.sleep(1.5)

print(f"\nTotal unique post URLs found: {len(all_urls)}")
for u in sorted(list(all_urls)):
    print(f"- {u}")

with open("scratch/search_results_posts.json", "w", encoding="utf-8") as f:
    json.dump(list(all_urls), f, indent=2)
