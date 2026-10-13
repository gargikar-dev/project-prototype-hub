import json

posts = json.load(open("scratch/search_snippets.json", encoding="utf-8"))

dedup = {}
for p in posts:
    u = p["url"]
    if u not in dedup:
        dedup[u] = p

print(f"Total Unique Posts: {len(dedup)}\n")

for i, (u, p) in enumerate(dedup.items()):
    clean_snippet = p["snippet"].encode("ascii", "replace").decode("ascii")
    clean_title = p["title"].encode("ascii", "replace").decode("ascii")
    print(f"--- Post {i+1} ---")
    print(f"Query: {p['query']}")
    print(f"URL: {u}")
    print(f"Title: {clean_title}")
    print(f"Snippet: {clean_snippet}")
    print()
