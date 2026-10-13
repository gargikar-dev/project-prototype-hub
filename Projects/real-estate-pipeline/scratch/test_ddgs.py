from duckduckgo_search import DDGS
import json

queries = [
    'linkedin "Managing Principal" "Commercial Architecture"',
    'linkedin "Founder" "Commercial Interiors" "Design"',
    'linkedin "President" "Commercial Roofing" "Services"',
    'linkedin "Founder" "3PL" "Logistics" "Freight"',
    'linkedin "looking for" "lead generation" founder',
    'linkedin "looking for" "cold email" agency founder',
    'linkedin "recommend" "lead gen" founder',
]

with DDGS() as ddgs:
    for q in queries:
        print(f"\n--- {q} ---")
        try:
            results = list(ddgs.text(q, max_results=5))
            for r in results:
                if 'linkedin.com' in r['href']:
                    print("[MATCH]", r['title'])
                    print("       ", r['href'])
                    print("       ", r['body'][:100])
                else:
                    print("[OTHER]", r['title'], "->", r['href'])
        except Exception as e:
            print("Error:", e)
