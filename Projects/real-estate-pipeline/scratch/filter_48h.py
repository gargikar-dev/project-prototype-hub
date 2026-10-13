import json

with open('collected_48h_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total <48h jobs: {len(jobs)}")

# Let's filter for relevant titles and locations
relevant = []
for j in jobs:
    title = j['title'].lower()
    comp = j['company']
    loc = j['location']
    posted = j['posted']
    url = j['url']
    
    # Check if title or query indicates lead generation, appointment setting, prospecting, SDR
    if any(k in title for k in ['lead', 'prospect', 'appointment', 'sales development', 'business development', 'acquisit', 'inside sales']):
        relevant.append(j)

print(f"Relevant matching jobs: {len(relevant)}")

for idx, r in enumerate(relevant[:40], start=1):
    print(f"[{idx}] {r['title']} | {r['company']} | {r['location']} | {r['posted']} | {r['url']}")
