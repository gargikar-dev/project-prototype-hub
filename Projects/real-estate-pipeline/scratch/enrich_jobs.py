import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import re
import sys

# Set stdout to utf-8
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\live_48h_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

existing_companies = {
    "realadvisor", "ac private", "service contractor growth", "emcita",
    "impact recruitment", "docassistant.ai", "flexup", "talentoma",
    "boatman agency", "synergyx global", "the business connector", "wow brand",
    "tri pros remodeling", "strousehouse.io", "stratus building solutions", "northorbis"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

fresh_candidates = []
for j in jobs:
    comp_norm = j['company'].lower().strip()
    if any(ec in comp_norm for ec in existing_companies):
        continue
    # Check if location is US or UK
    loc = j['location'].lower()
    if not any(c in loc for c in ['united states', 'united kingdom', 'england', 'ca', 'ny', 'fl', 'tx', 'london', 'remote', 'co', 'oh', 'il', 'az']):
        continue
    fresh_candidates.append(j)

print(f"Total fresh candidates: {len(fresh_candidates)}")

enriched_jobs = []
for idx, j in enumerate(fresh_candidates[:40]):
    job_id = j['job_id']
    detail_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    req = urllib.request.Request(detail_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            # criteria
            criteria_list = soup.find_all('li', class_=lambda x: x and 'criteria' in x.lower())
            criteria_text = " | ".join([c.get_text(strip=True) for c in criteria_list])
            
            # description
            desc_elem = soup.find('div', class_=lambda x: x and 'description' in x.lower())
            desc_text = desc_elem.get_text(" ", strip=True) if desc_elem else ""
            
            # company info
            comp_elem = soup.find('a', class_=lambda x: x and 'company' in x.lower())
            comp_link = comp_elem['href'] if comp_elem and 'href' in comp_elem.attrs else ""
            
            # criteria items
            emp_range = "10–30 employees"
            for item in soup.find_all('span', class_=lambda x: x and 'criteria' in x.lower()):
                t = item.get_text(strip=True)
                if 'employee' in t.lower():
                    emp_range = t

            enriched_jobs.append({
                'job_id': job_id,
                'title': j['title'],
                'company': j['company'],
                'location': j['location'],
                'posted': j['posted'],
                'url': j['url'],
                'criteria': criteria_text,
                'description': desc_text[:500],
                'full_desc': desc_text
            })
            print(f"[{idx+1}] {j['company']} - {j['title']} | Posted: {j['posted']}")
            time.sleep(0.3)
    except Exception as e:
        print(f"Error {job_id}: {e}")

with open(r'c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\enriched_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(enriched_jobs, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully enriched {len(enriched_jobs)} jobs.")
