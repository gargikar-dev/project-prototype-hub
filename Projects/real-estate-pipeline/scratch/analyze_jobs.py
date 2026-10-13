import json
import re

with open(r'c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\live_48h_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

existing_companies = {
    "realadvisor", "ac private", "service contractor growth", "emcita",
    "impact recruitment", "docassistant.ai", "flexup", "talentoma",
    "boatman agency", "synergyx global", "the business connector", "wow brand",
    "tri pros remodeling", "strousehouse.io", "stratus building solutions", "northorbis"
}

print(f"Total jobs loaded: {len(jobs)}")
fresh_jobs = []
for j in jobs:
    comp_norm = j['company'].lower().strip()
    is_existing = any(ec in comp_norm for ec in existing_companies)
    if not is_existing:
        fresh_jobs.append(j)

print(f"Fresh jobs not in previous batch: {len(fresh_jobs)}")
for idx, j in enumerate(fresh_jobs[:30], 1):
    print(f"{idx}. [{j['posted']}] {j['company']} - {j['title']} ({j['location']})")
    print(f"   URL: {j['url']}")
