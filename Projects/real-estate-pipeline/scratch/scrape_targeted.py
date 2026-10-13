import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

queries = [
    ('appointment setter real estate', 'United States'),
    ('inside sales agent real estate', 'United States'),
    ('lead generation freelance', 'United States'),
    ('lead generation freelance', 'United Kingdom'),
    ('appointment setter commission remote', 'United States'),
    ('appointment setter commission remote', 'United Kingdom'),
    ('outbound sales freelance', 'United States'),
    ('outbound sales freelance', 'United Kingdom'),
    ('b2b lead generation contractor', 'United States'),
    ('b2b lead generation contractor', 'United Kingdom'),
]

new_leads = {}
for kw, loc in queries:
    params = urllib.parse.urlencode({
        'keywords': kw,
        'location': loc,
        'f_TPR': 'r86400',
        'sortBy': 'DD',
        'start': 0
    })
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{params}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
            jobs = soup.find_all('li')
            for j in jobs:
                link = j.find('a', class_=lambda x: x and 'link' in x.lower())
                if not link or 'href' not in link.attrs:
                    continue
                href = link['href'].split('?')[0]
                m = re.search(r'/view/(?:.+?-)?(\d+)', href)
                jid = m.group(1) if m else href
                t = j.find('h3', class_=lambda x: x and 'title' in x.lower())
                c = j.find('h4', class_=lambda x: x and 'subtitle' in x.lower())
                l = j.find('span', class_=lambda x: x and 'location' in x.lower())
                time_posted = j.find('time')
                new_leads[jid] = {
                    'job_id': jid,
                    'title': t.get_text(strip=True) if t else '',
                    'company': c.get_text(strip=True) if c else '',
                    'location': l.get_text(strip=True) if l else '',
                    'posted': time_posted.get_text(strip=True) if time_posted else '',
                    'url': href,
                }
        time.sleep(0.4)
    except Exception as e:
        print(f"Error {kw}: {e}")

print(f"Total scraped: {len(new_leads)}")
with open('scratch/targeted_24h.json', 'w', encoding='utf-8') as f:
    json.dump(list(new_leads.values()), f, indent=2)
