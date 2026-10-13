import json

batch = json.load(open('scratch/search_batch2.json', encoding='utf-8'))
print(f"Batch 2 count: {len(batch)}")
for i, b in enumerate(batch):
    clean_title = b['title'].encode('ascii', 'replace').decode('ascii')
    clean_snippet = b['snippet'].encode('ascii', 'replace').decode('ascii')
    print(f"[{i+1}] {clean_title}")
    print(f"URL: {b['url']}")
    print(f"Snippet: {clean_snippet[:150]}")
    print()
