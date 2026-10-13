import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import re
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/live_24h_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

existing_urls = set()
existing_comps = set()
with open('leads_linkedin_icp_us_uk_48h.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        existing_urls.add(row['Verified LinkedIn URL'].strip().lower())
        existing_comps.add(row['Company Name'].strip().lower())

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

candidates = []
for j in jobs:
    if j['url'].strip().lower() in existing_urls:
        continue
    c_norm = j['company'].strip().lower()
    if any(ec in c_norm for ec in existing_comps):
        continue
    loc = j['location'].lower()
    if not any(k in loc for k in ['united states', 'united kingdom', 'england', 'ca', 'ny', 'fl', 'tx', 'london', 'remote', 'co', 'oh', 'il', 'az', 'pa', 'nc', 'ga']):
        continue
    candidates.append(j)

print(f"Candidates to enrich: {len(candidates)}")

enriched = []
for idx, j in enumerate(candidates):
    job_id = j['job_id']
    detail_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    req = urllib.request.Request(detail_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            criteria_items = soup.find_all('li', class_=lambda x: x and 'criteria' in x.lower())
            criteria_text = ' | '.join([c.get_text(' ', strip=True) for c in criteria_items])
            desc_elem = soup.find('div', class_=lambda x: x and 'description' in x.lower())
            desc_text = desc_elem.get_text(' ', strip=True) if desc_elem else ''
            
            enriched.append({
                'job_id': job_id,
                'title': j['title'],
                'company': j['company'],
                'location': j['location'],
                'posted': j['posted'],
                'url': j['url'],
                'criteria': criteria_text,
                'description': desc_text[:1200]
            })
            print(f"[{idx+1}/{len(candidates)}] {j['company']} - {j['title']} ({j['posted']})")
        time.sleep(0.3)
    except Exception as e:
        print(f"Error {job_id}: {e}")
    if len(enriched) >= 30:
        break

with open('scratch/enriched_batch3.json', 'w', encoding='utf-8') as f:
    json.dump(enriched, f, indent=2, ensure_ascii=False)

print(f"Enriched {len(enriched)} candidate jobs saved to scratch/enriched_batch3.json")
