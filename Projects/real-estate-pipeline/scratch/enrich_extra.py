import json
import urllib.request
from bs4 import BeautifulSoup
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/live_24h_jobs.json', 'r', encoding='utf-8') as f:
    all_jobs = json.load(f)

with open('scratch/enriched_batch3.json', 'r', encoding='utf-8') as f:
    already_enriched = {j['job_id'] for j in json.load(f)}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

extra = []
for j in all_jobs:
    if j['job_id'] in already_enriched:
        continue
    t = j['title'].lower()
    if any(k in t for k in ['appointment', 'lead gen', 'setter', 'cold call', 'outreach', 'sales representative', 'freelance', 'partner', 'contractor', 'inside sales', 'telemarketer', 'bdr']):
        job_id = j['job_id']
        url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}'
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                crit = ' | '.join([c.get_text(' ', strip=True) for c in soup.find_all('li', class_=lambda x: x and 'criteria' in x.lower())])
                desc = soup.find('div', class_=lambda x: x and 'description' in x.lower())
                desc_text = desc.get_text(' ', strip=True) if desc else ''
                extra.append({
                    'job_id': job_id,
                    'title': j['title'],
                    'company': j['company'],
                    'location': j['location'],
                    'posted': j['posted'],
                    'url': j['url'],
                    'criteria': crit,
                    'description': desc_text[:1200]
                })
                print(f"+ Added: {j['company']} - {j['title']} ({j['posted']})")
            time.sleep(0.3)
        except Exception as e:
            pass
        if len(extra) >= 20:
            break

with open('scratch/enriched_extra.json', 'w', encoding='utf-8') as f:
    json.dump(extra, f, indent=2, ensure_ascii=False)
print(f"Total extra enriched: {len(extra)}")
