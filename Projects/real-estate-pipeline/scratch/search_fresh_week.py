import urllib.request
import urllib.parse
import re
import json

time_queries = [
    'site:linkedin.com/posts "lead generation" "looking for"',
    'site:linkedin.com/posts "lead generation" "recommend"',
    'site:linkedin.com/posts "lead generation" "hiring"',
    'site:linkedin.com/posts "appointment setter" "looking for"',
    'site:linkedin.com/posts "outbound" "looking for"',
    'site:linkedin.com/posts "lead gen" founder "looking for"',
    'site:linkedin.com/posts "b2b lead generation" "hiring"',
    'site:linkedin.com/posts "cold email" "looking for"'
]

fresh_posts = []

for q in time_queries:
    # df=w filters for past week in DuckDuckGo
    url = "https://r.jina.ai/https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q) + "&df=w"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'agent-reach/1.0'})
        content = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')
        sections = content.split('## [')
        for sec in sections[1:]:
            title_part = sec.split('](')[0]
            url_part = sec.split('](')[1].split(')')[0] if '](' in sec else ''
            if 'uddg=' in url_part:
                m = re.search(r'uddg=([^&]+)', url_part)
                if m:
                    url_part = urllib.parse.unquote(m.group(1)).split('?')[0]
            
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
                fresh_posts.append({
                    "query": q,
                    "title": title_part,
                    "url": url_part,
                    "snippet": snippet
                })
    except Exception as e:
        print(f"Error {q}: {e}")

print(f"Total fresh posts extracted: {len(fresh_posts)}")

dedup = {}
for p in fresh_posts:
    u = p["url"]
    if u not in dedup:
        dedup[u] = p

print(f"Unique fresh posts: {len(dedup)}")
with open("scratch/fresh_week_posts.json", "w", encoding="utf-8") as f:
    json.dump(list(dedup.values()), f, indent=2)

for i, (u, p) in enumerate(dedup.items()):
    clean_t = p['title'].encode('ascii', 'replace').decode('ascii')
    clean_s = p['snippet'].encode('ascii', 'replace').decode('ascii')
    print(f"[{i+1}] {clean_t} -> {u}")
    print(f"    {clean_s[:140]}")
