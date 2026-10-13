import json

with open('collected_48h_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total jobs: {len(jobs)}")
real_estate_and_agency = []

for j in jobs:
    title = j['title'].lower()
    comp = j['company'].lower()
    loc = j['location']
    posted = j['posted']
    url = j['url']
    
    # Check for real estate, property, appointment setter, lead gen freelancer/contract
    keywords = ['real estate', 'property', 'appointment setter', 'lead gen', 'freelance', 'contract', 'commission', 'outbound', 'prospect']
    if any(k in title for k in keywords) or any(k in comp for k in ['home', 'realty', 'estate', 'property']):
        real_estate_and_agency.append(j)

print(f"Real estate / setter / contract matches: {len(real_estate_and_agency)}")
for idx, r in enumerate(real_estate_and_agency[:35], start=1):
    print(f"[{idx}] {r['title']} | {r['company']} | {r['location']} | {r['posted']} | {r['url']}")
