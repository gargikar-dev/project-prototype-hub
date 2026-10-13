# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import json
import time
import os

DISCOVERY_QUERIES = [
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
    'site:linkedin.com/posts founder "looking for" "lead generation"',
    'site:linkedin.com/posts ceo "looking for" "lead generation"',
    'site:linkedin.com/posts founder "recommend" "lead generation agency"',
    'site:linkedin.com/posts founder "need someone to" "generate leads"',
    'site:linkedin.com/posts "looking to hire" "lead generation agency"'
]

HEADERS = {
    'User-Agent': 'agent-reach/1.0 (Mozilla/5.0 Windows NT 10.0; Win64; x64)'
}

def search_jina_ddg(query):
    jina_url = "https://r.jina.ai/https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(jina_url, headers=HEADERS)
    found_urls = set()
    try:
        content = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'uddg=([^&)\s\"]+)', content)
        for m in matches:
            u = urllib.parse.unquote(m)
            if ("linkedin.com/posts/" in u or "linkedin.com/feed/update/" in u) and "/jobs/" not in u:
                clean_url = u.split('?')[0]
                found_urls.add(clean_url)
    except Exception as e:
        print(f"Error querying Jina DDG for '{query}': {e}")
    return found_urls

def fetch_jina_url(url):
    jina_url = "https://r.jina.ai/" + url
    req = urllib.request.Request(jina_url, headers=HEADERS)
    try:
        content = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', errors='ignore')
        return content
    except Exception as e:
        print(f"Error fetching Jina URL '{url}': {e}")
        return ""

def main():
    print("=== Step 1: Discovering LinkedIn Posts ===")
    all_discovered = set()
    for q in DISCOVERY_QUERIES:
        print(f"Executing search: {q}")
        urls = search_jina_ddg(q)
        print(f" -> Found {len(urls)} post URLs")
        all_discovered.update(urls)
        time.sleep(1.5)

    print(f"\nTotal unique LinkedIn post URLs discovered: {len(all_discovered)}")
    with open("scratch/discovered_founder_posts.json", "w", encoding="utf-8") as f:
        json.dump(list(all_discovered), f, indent=2)

    print("\n=== Step 2: Fetching & Analyzing Posts ===")
    results = []
    for idx, post_url in enumerate(list(all_discovered)):
        print(f"[{idx+1}/{len(all_discovered)}] Fetching {post_url}...")
        text = fetch_jina_url(post_url)
        if not text or len(text) < 100:
            continue
        
        # Save raw post
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', post_url.split('/')[-1])[:50]
        with open(f"scratch/post_{safe_name}.txt", "w", encoding="utf-8") as f:
            f.write(f"URL: {post_url}\n\n" + text)

        results.append({
            "url": post_url,
            "length": len(text),
            "file": f"scratch/post_{safe_name}.txt"
        })
        time.sleep(1)

    print(f"\nCompleted fetching {len(results)} posts. Ready for ICP qualification.")

if __name__ == "__main__":
    main()
