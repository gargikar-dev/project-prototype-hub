import json
import re

with open(r'c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\enriched_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

qualified = []

# Exclude massive conglomerates
exclude_keywords = ['korn ferry', 'sumup', 'blackhawk', 'mishcon de reya', 'northern gas and power', 'thrivecart', 'usergems', 'pareto usa']

for j in jobs:
    comp = j['company']
    if any(ex in comp.lower() for ex in exclude_keywords):
        continue
    
    title = j['title']
    loc = j['location']
    posted = j['posted']
    url = j['url']
    desc = j['full_desc']
    criteria = j['criteria']
    
    # Must be US or UK
    country = "United States"
    if any(uk_word in loc.lower() for uk_word in ['united kingdom', 'england', 'london', 'northampton', 'peterborough', 'driffield', 'yo25']):
        country = "United Kingdom"
    elif not any(us_word in loc.lower() for us_word in ['united states', 'denver', 'co', 'ca', 'fl', 'in', 'tx', 'ny', 'san jose', 'miami', 'indiana']):
        # If remote, check description
        if 'uk' in desc.lower() or 'england' in desc.lower():
            country = "United Kingdom"
        else:
            country = "United States"

    qualified.append({
        'job_id': j['job_id'],
        'company': comp,
        'title': title,
        'location': loc,
        'country': country,
        'posted': posted,
        'url': url,
        'criteria': criteria,
        'desc_sample': desc[:400]
    })

print(f"Total qualified candidates: {len(qualified)}")
with open(r'c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\qualified_raw.json', 'w', encoding='utf-8') as f:
    json.dump(qualified, f, indent=2, ensure_ascii=False)
