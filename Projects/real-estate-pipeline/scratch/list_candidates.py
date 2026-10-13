import json

with open(r'c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\scratch\qualified_raw.json', 'r', encoding='utf-8') as f:
    candidates = json.load(f)

for idx, c in enumerate(candidates, 1):
    print(f"--- #{idx} ---")
    print(f"Company: {c['company']}")
    print(f"Role: {c['title']}")
    print(f"Location: {c['location']} | Country: {c['country']}")
    print(f"Posted: {c['posted']}")
    print(f"URL: {c['url']}")
