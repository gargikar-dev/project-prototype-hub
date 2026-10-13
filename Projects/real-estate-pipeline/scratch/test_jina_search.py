import urllib.request
import urllib.parse
import re

query = 'site:linkedin.com/posts "looking for" "lead generation"'
jina_url = "https://r.jina.ai/https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)

req = urllib.request.Request(jina_url, headers={'User-Agent': 'agent-reach/1.0'})
try:
    content = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')
    print("Content length:", len(content))
    matches = re.findall(r'uddg=([^&)\s\"]+)', content)
    unique_posts = set()
    for m in matches:
        u = urllib.parse.unquote(m)
        if ("linkedin.com/posts/" in u or "linkedin.com/feed/update/" in u) and "/jobs/" not in u:
            unique_posts.add(u.split('?')[0])
    print(f"Extracted {len(unique_posts)} posts:")
    for p in unique_posts:
        print("  ->", p)
except Exception as e:
    print("Error:", e)
