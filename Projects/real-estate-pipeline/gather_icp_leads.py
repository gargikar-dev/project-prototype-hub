import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

queries = [
    ('lead generation freelance', 'United States'),
    ('lead generation freelance', 'United Kingdom'),
    ('lead generation contractor', 'United States'),
    ('lead generation contractor', 'United Kingdom'),
    ('appointment setter real estate', 'United States'),
    ('appointment setter real estate', 'United Kingdom'),
    ('lead generation real estate', 'United States'),
    ('lead generation real estate', 'United Kingdom'),
    ('lead generation remote', 'United States'),
    ('lead generation remote', 'United Kingdom'),
]

found_jobs = {}

for kw, loc in queries:
    params = urllib.parse.urlencode({'keywords': kw, 'location': loc, 'start': 0})
    url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{params}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            jobs = soup.find_all('li')
            for j in jobs:
                link = j.find('a', class_=lambda x: x and 'link' in x.lower())
                if not link or 'href' not in link.attrs:
                    continue
                href = link['href'].split('?')[0]
                job_id_match = re.search(r'-(\d+)$', href)
                if not job_id_match:
                    job_id_match = re.search(r'/view/(\d+)', href)
                job_id = job_id_match.group(1) if job_id_match else href
                if job_id in found_jobs:
                    continue
                
                t = j.find('h3', class_=lambda x: x and 'title' in x.lower())
                c = j.find('h4', class_=lambda x: x and 'subtitle' in x.lower())
                l = j.find('span', class_=lambda x: x and 'location' in x.lower())
                time_posted = j.find('time')
                
                title = t.get_text(strip=True) if t else 'N/A'
                company = c.get_text(strip=True) if c else 'N/A'
                location = l.get_text(strip=True) if l else 'N/A'
                posted = time_posted.get_text(strip=True) if time_posted else 'Recent'
                
                found_jobs[job_id] = {
                    'job_id': job_id,
                    'title': title,
                    'company': company,
                    'location': location,
                    'posted': posted,
                    'url': href,
                    'query': f"{kw} ({loc})"
                }
        time.sleep(0.5)
    except Exception as e:
        print(f"Error {kw} {loc}: {e}")

print(f"Total unique jobs gathered: {len(found_jobs)}")
with open('gathered_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(list(found_jobs.values()), f, indent=2)
