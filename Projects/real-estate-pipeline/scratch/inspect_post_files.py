import glob
import re
import os

files = glob.glob("scratch/post_*.txt")
print(f"Total post files: {len(files)}")

posts_data = []

for fpath in files:
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    url_m = re.search(r'URL:\s*(\S+)', content)
    url = url_m.group(1) if url_m else ""
    
    title_m = re.search(r'Title:\s*(.+)', content)
    title = title_m.group(1) if title_m else ""
    
    date_m = re.search(r'Published Time:\s*(\S+)', content)
    published = date_m.group(1) if date_m else ""
    
    # Check for relative time like "10h", "2d", "1d", "3d", "4d"
    rel_time = ""
    time_m = re.search(r'\n\s*(\d+[hd])\s*\n', content)
    if time_m:
        rel_time = time_m.group(1)
        
    posts_data.append({
        "file": fpath,
        "url": url,
        "title": title,
        "published": published,
        "rel_time": rel_time,
        "content_preview": content[content.find("Markdown Content:"):content.find("Markdown Content:")+400] if "Markdown Content:" in content else content[:400]
    })

for p in posts_data:
    clean_title = p['title'].encode('ascii', 'replace').decode('ascii')
    print(f"File: {p['file']}")
    print(f"URL: {p['url']}")
    print(f"Time: {p['published']} | Rel: {p['rel_time']}")
    print(f"Title: {clean_title[:80]}")
    print("-" * 50)
