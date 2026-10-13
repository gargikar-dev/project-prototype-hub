import json
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load existing leads to ensure 0 duplicates
existing_urls = set()
existing_comps = set()
with open('leads_linkedin_icp_us_uk_48h.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        existing_urls.add(row['Verified LinkedIn URL'].strip().lower())
        existing_comps.add(row['Company Name'].strip().lower())

with open('scratch/targeted_24h.json', 'r', encoding='utf-8') as f:
    targeted = json.load(f)

with open('scratch/enriched_batch3.json', 'r', encoding='utf-8') as f:
    batch3 = json.load(f)

with open('scratch/enriched_extra.json', 'r', encoding='utf-8') as f:
    extra = json.load(f)

all_candidates = []
seen = set()

for pool in [batch3, extra, targeted]:
    for j in pool:
        jid = j.get('job_id') or j.get('url')
        if jid in seen:
            continue
        seen.add(jid)
        url = j.get('url', '').strip().lower()
        comp = j.get('company', '').strip().lower()
        if url in existing_urls:
            continue
        if any(ec in comp for ec in existing_comps if len(ec) > 3):
            continue
        loc = j.get('location', '').lower()
        if not any(k in loc for k in ['united states', 'united kingdom', 'england', 'ca', 'ny', 'fl', 'tx', 'london', 'remote', 'co', 'oh', 'il', 'az', 'pa', 'nc', 'ga', 'wa', 'mi']):
            continue
        all_candidates.append(j)

print(f"Total fresh candidates: {len(all_candidates)}")
for idx, c in enumerate(all_candidates[30:], start=31):
    print(f"[{idx}] {c.get('company')} | {c.get('title')} | {c.get('location')} | {c.get('posted')}")
    print(f"     URL: {c.get('url')}")
