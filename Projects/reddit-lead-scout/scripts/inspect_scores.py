import sys, json, glob
sys.path.append('scripts')
sys.stdout.reconfigure(encoding='utf-8')
from ai_lead_scorer import evaluate_lead

icp = json.load(open('config/ai_business_icp.json', encoding='utf-8'))
recent_posts = []
seen = set()
for f in glob.glob('.cache/*.json'):
    try:
        data = json.load(open(f, encoding='utf-8'))
        for p in data:
            p_id = p.get('id') or p.get('url')
            if p_id in seen: continue
            seen.add(p_id)
            eval_res = evaluate_lead(p, icp)
            if not eval_res['is_disqualified']:
                recent_posts.append(eval_res)
    except Exception:
        pass

recent_posts.sort(key=lambda x: x['composite_score'], reverse=True)
print(f"Total non-disqualified recent posts: {len(recent_posts)}")
print("Posts scoring >= 71:", len([p for p in recent_posts if p['composite_score'] >= 71]))
print("Posts scoring between 55 and 70:", len([p for p in recent_posts if 55 <= p['composite_score'] < 71]))
for p in recent_posts[:25]:
    print(f"Score {p['composite_score']} (Int {p['intent_score']}, ICP {p['icp_match_score']}) | r/{p['subreddit']}: {p['thread_title'][:65]}")
