import urllib.request
import urllib.parse
import re
import json

new_queries = [
    'site:linkedin.com/posts "lead generation agency" "recommend"',
    'site:linkedin.com/posts "looking for" "appointment setter" founder',
    'site:linkedin.com/posts "looking for" "cold email" founder',
    'site:linkedin.com/posts "need someone to" "book sales meetings" founder',
    'site:linkedin.com/posts "hiring" "lead gen agency" founder',
    'site:linkedin.com/posts "looking for" "b2b lead generation agency"',
    'site:linkedin.com/posts "any recommendations for" "lead generation agency"',
    'site:linkedin.com/posts "recommend a" "cold email agency"',
    'site:linkedin.com/posts "recommend a" "b2b lead generation"'
]

headers = {'User-Agent': 'agent-reach/1.0'}
batch2 = []

for q in new_queries:
    jina_url = "https://r.jina.ai/https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    try:
        req = urllib.request.Request(jina_url, headers=headers)
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
                batch2.append({
                    "query": q,
                    "title": title_part,
                    "url": url_part,
                    "snippet": snippet
                })
    except Exception as e:
        pass

print(f"Batch 2 extracted: {len(batch2)}")
with open("scratch/search_batch2.json", "w", encoding="utf-8") as f:
    json.dump(batch2, f, indent=2)
