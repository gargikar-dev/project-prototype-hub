import urllib.request
import urllib.parse
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def search_ddg(query):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract result blocks
            blocks = re.findall(r'<div class="result__body">([\s\S]*?)</div>\s*</div>', html)
            results = []
            for b in blocks:
                url_match = re.search(r'href="([^"]*linkedin\.com/in/[^"]*)"', b)
                title_match = re.search(r'<a class="result__snippet[^>]*>([\s\S]*?)</a>', b)
                header_match = re.search(r'<a class="result__url[^>]*>([\s\S]*?)</a>', b)
                if url_match:
                    raw_url = url_match.group(1)
                    # unquote DDG redirect if present
                    if 'uddg=' in raw_url:
                        actual_url = urllib.parse.unquote(raw_url.split('uddg=')[1].split('&')[0])
                    else:
                        actual_url = raw_url
                    results.append({
                        'url': actual_url,
                        'snippet': re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else ''
                    })
            return results
    except Exception as e:
        print("DDG Error:", e)
        return []

if __name__ == '__main__':
    q = 'site:linkedin.com/in/ ("Founder" OR "Managing Principal" OR "Owner") "Commercial Architecture" "United States"'
    res = search_ddg(q)
    print(f"Found {len(res)} results:")
    for r in res[:5]:
        print(r)
