import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/enriched_batch3.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

for idx in range(min(9, len(jobs))):
    j = jobs[idx]
    print(f"[{idx+1}] Company: {j['company']}")
    print(f"     Title: {j['title']}")
    print(f"     Location: {j['location']}")
    print(f"     Posted: {j['posted']}")
    print(f"     URL: {j['url']}")
    print(f"     Criteria: {j['criteria']}")
    print(f"     Description: {j['description'][:250]}")
    print("=" * 60)
