import urllib.request
import urllib.parse
import re
import json

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
    'site:linkedin.com/posts founder "looking for" "lead generation"',
    'site:linkedin.com/posts ceo "looking for" "lead generation"',
    'site:linkedin.com/posts founder "recommend" "lead generation agency"',
    'site:linkedin.com/posts "looking to hire" "lead generation agency"'
]

results = []

for q in queries:
    jina_url = "https://r.jina.ai/https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    try:
        req = urllib.request.Request(jina_url, headers={'User-Agent': 'agent-reach/1.0'})
        content = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')
        
        # In DuckDuckGo Jina output:
        # ## [Title](link)
        # [Snippet text]
        sections = content.split('## [')
        for sec in sections[1:]:
            title_part = sec.split('](')[0]
            url_part = sec.split('](')[1].split(')')[0] if '](' in sec else ''
            # Unquote uddg
            if 'uddg=' in url_part:
                m = re.search(r'uddg=([^&]+)', url_part)
                if m:
                    url_part = urllib.parse.unquote(m.group(1)).split('?')[0]
            
            # Snippet is the text after the second link
            snippet = ""
            lines = sec.split('\n')
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('[') and line.endswith(')') and '...' in line:
                    snippet = line.strip('[]')
                    break
                elif len(line) > 40 and not line.startswith('[!') and not line.startswith('http'):
                    snippet = line
                    break
            
            if ("linkedin.com/posts/" in url_part or "linkedin.com/feed/update/" in url_part) and "/jobs/" not in url_part:
                results.append({
                    "query": q,
                    "title": title_part,
                    "url": url_part,
                    "snippet": snippet
                })
    except Exception as e:
        pass

print(f"Total extracted results: {len(results)}")
with open("scratch/search_snippets.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# De-duplicate by URL
dedup = {}
for r in results:
    u = r["url"]
    if u not in dedup:
        dedup[u] = r

print(f"Unique post results: {len(dedup)}")
for u, r in dedup.items():
    print(f"\nTITLE: {r['title']}")
    print(f"URL: {r['url']}")
    print(f"SNIPPET: {r['snippet'][:200]}")
