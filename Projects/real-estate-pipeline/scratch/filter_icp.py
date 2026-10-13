import json
import re

with open(r'c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\enriched_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Loaded {len(jobs)} enriched jobs.")

target_candidates = []
for j in jobs:
    title = j['title'].lower()
    desc = j['full_desc'].lower()
    crit = j['criteria'].lower()
    loc = j['location']
    comp = j['company']
    posted = j['posted']
    url = j['url']

    # Filter out massive corporations (>500 or enterprise)
    if any(big in comp.lower() for big in ['korn ferry', 'sumup', 'blackhawk', 'mishcon de reya', 'northern gas and power', 'thrivecart', 'usergems']):
        continue
        
    print(f"\n==========================================")
    print(f"Company: {comp} | Title: {j['title']} | Location: {loc} | Posted: {posted}")
    print(f"Criteria: {j['criteria']}")
    print(f"Desc snippet: {desc[:250]}...")
