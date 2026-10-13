import urllib.request
import sys
from batch3_leads import BATCH_3_LEADS

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

print(f"Checking {len(BATCH_3_LEADS)} leads...")
for idx, lead in enumerate(BATCH_3_LEADS, start=1):
    url = lead['linkedin_url']
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[{idx}/15] OK ({resp.status}): {lead['company_name']} | {lead['date_posted']}")
    except Exception as e:
        print(f"[{idx}/15] ERROR: {lead['company_name']} -> {e}")
