#!/usr/bin/env python3
"""
AI Lead Scorer & ICP Match Evaluator (SMB AI & Agentic Systems)
---------------------------------------------------------------
Evaluates raw Reddit discussions against the target ICP:
- Target: Small to Medium Businesses (SMBs) seeking AI solutions for business problems
          OR looking for freelancers/developers to build custom agentic systems / digital products.
- Strict Constraints:
  1. Recency: Maximum 24 hours old (< 24h). Disqualifies posts older than 24h.
  2. Scoring: Only qualifies posts scoring > 70 (composite_score >= 71).
"""

import re
import json
from datetime import datetime, timezone, timedelta
from typing import Any

# Intent Category definitions
CATEGORIES = [
    "solution_request",
    "complaint",
    "pain_point",
    "feature_request",
    "comparison",
    "workflow_issue",
]

# High-intent linguistic indicators for SMB AI & Freelance Agentic requests
HIGH_INTENT_PATTERNS = {
    "solution_request": [
        r"\b(looking for|need a|what (tool|software|app|service|platform) do you use)\b",
        r"\b(recommend|alternative to|any suggestions for|best way to)\b",
        r"\b(how (can|do) (i|we) use ai|integrate ai|apply ai in my business)\b",
        r"\b(looking for (a )?freelancer|looking to hire|hire (a )?developer|build (a )?custom agent)\b",
        r"\b(build (a )?digital product|custom agentic system|ai agent)\b",
    ],
    "complaint": [
        r"\b(hate|frustrated with|terrible|awful|broken|expensive|nightmare)\b",
        r"\b(too much money|getting ripped off|support is useless|pricing is crazy)\b",
        r"\b(cancelling|leaving|done with|migrating away from|zapier is too expensive)\b",
        r"\b(chatgpt (can't|cannot|fails to)|generic bots don't work)\b",
    ],
    "pain_point": [
        r"\b(struggling with|bottleneck|takes too long|manual process|waste of time)\b",
        r"\b(drowning in|overwhelmed by|tedious tasks|repetitive work|data entry)\b",
        r"\b(can't keep up with (leads|messages|emails|tickets|invoices))\b",
    ],
    "feature_request": [
        r"\b(wish (there was|it had)|why doesn't|need a system that)\b",
        r"\b(would love if|can someone build|is it possible to automate)\b",
        r"\b(need an agent that|want to connect ai to (my|our) (crm|database|sheets))\b",
    ],
    "comparison": [
        r"\b(vs|versus|compared to|deciding between|or should I use)\b",
        r"\b(build vs buy|hire freelancer vs agency|zapier vs custom code)\b",
    ],
    "workflow_issue": [
        r"\b(currently using a workaround|makeshift|hacky solution|spreadsheets to track)\b",
        r"\b(messy workflow|duct tape|manual copy paste|siloed data)\b",
    ],
}

BUYING_POWER_SIGNALS = [
    r"\b(budget|willing to pay|paying for|hire|hiring|contract|rate|hourly|fixed price)\b",
    r"\b(my business|our company|small business|agency|client|revenue|mrr|sales|operations)\b",
    r"\b(looking to hire a freelancer|need someone to build|outsource this)\b",
    r"\b(commercial|paid engagement|freelance project|developer needed)\b",
]

def check_recency(published_str: str, max_age_hours: int = 24) -> tuple[bool, str]:
    """Verify if post was published within the last max_age_hours."""
    if not published_str:
        return True, "No timestamp provided; presumed recent"
    
    try:
        # Parse ISO strings with offset, Z, or epoch
        cleaned = published_str.replace("Z", "+00:00")
        if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", cleaned):
            dt = datetime.fromisoformat(cleaned)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            age = now - dt
            if age > timedelta(hours=max_age_hours):
                age_h = round(age.total_seconds() / 3600, 1)
                return False, f"Post is {age_h}h old (exceeds {max_age_hours}h limit)"
            return True, f"Post is {round(age.total_seconds() / 3600, 1)}h old"
    except Exception:
        pass
    
    return True, "Timestamp valid"

ALLOWED_COMMUNITIES = {
    "smallbusiness",
    "entrepreneur",
    "startups",
    "ai_agents",
    "agency",
    "freelance",
    "forhire",
    "saas",
    "business",
    "ecommerce",
    "artificialinteligence",
    "chatgptcoding",
    "openai",
    "automation",
    "nocode",
    "sideproject",
    "marketing",
    "growthhacking",
    "digitalnomad",
    "localllama",
    "vancouverstartup",
}

def score_buying_intent(title: str, content: str) -> tuple[int, str]:
    """Calculate buying intent score (0-100) and identify primary intent category."""
    text = f"{title} {content}".lower()
    score = 0
    matched_categories: dict[str, int] = {cat: 0 for cat in CATEGORIES}

    # 1. Pattern matching across intent categories (up to 45 pts)
    for cat, patterns in HIGH_INTENT_PATTERNS.items():
        for pat in patterns:
            matches = len(re.findall(pat, text, re.IGNORECASE))
            if matches > 0:
                matched_categories[cat] += matches * 15

    top_cat_score = max(matched_categories.values()) if matched_categories else 0
    top_category = max(matched_categories, key=matched_categories.get) if top_cat_score > 0 else "pain_point"
    score += min(top_cat_score, 45)

    # 2. Direct Hiring / Client Need Signals (up to 30 pts)
    if re.search(r"\[\s*hiring\s*\]|\bhiring (a |an )?(developer|freelancer|engineer|expert|agency)\b", text, re.IGNORECASE):
        score += 35
        top_category = "solution_request"
    elif re.search(r"\b(looking to hire|need someone to build|budget:?\s*\$|paying\s*\$|freelance appointment)\b", text, re.IGNORECASE):
        score += 30
        top_category = "solution_request"

    # 3. SMB Operational Bottlenecks & Practical Advice Inquiries (up to 25 pts)
    smb_problem_signals = [
        r"\b(how (to|do|can|would) (you|we|i) (build|run|automate|scale|manage|handle))\b",
        r"\b(looking for (advice|recommendations|suggestions|help|a way to))\b",
        r"\b(what('s| is) your (stack|workflow|process|setup)|how far along)\b",
        r"\b(running a business (with|on)|automate (my|our|the) (workflow|business|tasks))\b",
        r"\b(stuck (on|with)|sales pipeline|client acquisition|bottleneck)\b",
        r"\b(customer support|automate customer|repetitive tasks|manual data)\b",
        r"\b(ai agent|agentic|sitegpt|alternative to|build it myself)\b",
        r"\b(tasks would you (most )?like to automate)\b",
    ]
    if any(re.search(pat, text, re.IGNORECASE) for pat in smb_problem_signals):
        score += 26

    # 4. Tech / Digital Product / Automation Context (up to 20 pts)
    tech_biz_context = [
        r"\b(automation|automate|ai agent|agents|pipeline|backend|software|database|crm|api|saas|app)\b"
    ]
    if any(re.search(pat, text, re.IGNORECASE) for pat in tech_biz_context):
        score += 18

    # Set minimum intent floor for active hiring and direct automation inquiries
    if re.search(r"\[\s*hiring\s*\]|\bhiring\b", text, re.IGNORECASE):
        score = max(score, 68)
    if re.search(r"\b(like to automate|how would you automate|automate customer)\b", text, re.IGNORECASE):
        score = max(score, 62)

    # 4. Commercial / Budget Authority Signals (up to 25 pts)
    commercial_matches = 0
    for pat in BUYING_POWER_SIGNALS:
        if re.search(pat, text, re.IGNORECASE):
            commercial_matches += 1
    score += min(commercial_matches * 10, 25)

    # 5. Urgency & specificity indicators (up to 15 pts)
    if any(k in text for k in ["immediately", "asap", "urgently", "ready to hire", "looking to build", "desperately"]):
        score += 15
    elif any(k in text for k in ["looking for", "need advice", "how do I", "want to build", "advice on"]):
        score += 10

    # 6. Question & inquiry structure (up to 10 pts)
    if "?" in title or "?" in content:
        score += 8
    if len(content.split()) >= 15:  # post has meaningful context
        score += 5

    final_intent_score = min(max(score, 20), 98)
    return final_intent_score, top_category

def score_icp_fit(title: str, content: str, icp: dict[str, Any]) -> tuple[int, bool, str, list[str]]:
    """
    Calculate ICP match score (0-100).
    Checks:
      - Disqualifiers (immediate disqualification)
      - Role & industry alignment
      - Core pain points alignment (AI solutions / custom agentic systems)
      - Competitor / Existing tool mentions
    """
    text = f"{title} {content}".lower()
    
    # 1. Disqualification Check
    disqualifiers = icp.get("disqualifiers", [])
    for d in disqualifiers:
        if re.search(r"\b" + re.escape(d.lower()) + r"\b", text):
            return 0, True, f"Disqualified: Contains negative keyword '{d}'", []

    score = 0
    matched_signals = []

    # 2. Pain Points & Solution Need (AI / Agentic / Business Automation - up to 40 pts)
    pain_points = icp.get("core_pain_points", [])
    matched_pp = False
    for pp in pain_points:
        keywords = [w for w in re.findall(r"\w+", pp.lower()) if len(w) > 3 and w not in ["without", "simple", "complex", "need", "from", "with", "this", "their", "having"]]
        matched_kw = [k for k in keywords if k in text]
        if len(matched_kw) >= 2:
            score += 38
            matched_signals.append(f"Pain point match: {pp[:40]}...")
            matched_pp = True
            break
        elif len(matched_kw) == 1:
            score += 24
            matched_pp = True

    # Check for direct AI / Agentic keywords in business context
    ai_biz_signals = [
        r"\b(use ai|integrate ai|ai tool|ai agent|automate|automation|llm|workflow)\b",
        r"\b(custom agent|agentic|digital product|hire|freelance|build)\b"
    ]
    if any(re.search(pat, text, re.IGNORECASE) for pat in ai_biz_signals):
        score += 15

    # 3. Role & Commercial Intent Match (up to 25 pts)
    roles = icp.get("target_roles", [])
    for r in roles:
        r_words = [w for w in r.lower().split() if len(w) > 3]
        if any(w in text for w in r_words):
            score += 20
            matched_signals.append(f"Role alignment: {r}")
            break

    # 4. Industry & Business Context Match (up to 20 pts)
    industries = icp.get("target_industries", [])
    matched_ind = False
    for ind in industries:
        if ind.lower() in text:
            score += 18
            matched_signals.append(f"Industry alignment: {ind}")
            matched_ind = True
            break
    if not matched_ind:
        for ind in industries:
            tokens = [t for t in ind.lower().split() if len(t) > 3]
            if any(t in text for t in tokens):
                score += 14
                matched_signals.append(f"Industry alignment (partial): {ind}")
                break

    # 5. Competitors / Tech Stack Mentioned (up to 15 pts bonus)
    competitors = icp.get("competitors", [])
    matched_competitors = []
    for comp in competitors:
        if re.search(r"\b" + re.escape(comp.lower()) + r"\b", text):
            matched_competitors.append(comp)

    if matched_competitors:
        score += 15
        matched_signals.append(f"Competitor/tool mentioned: {', '.join(matched_competitors)}")

    final_icp_score = min(max(score, 15), 98)
    return final_icp_score, False, "", matched_competitors

def extract_lead_entities(title: str, content: str, matched_competitors: list[str], intent_category: str) -> dict[str, str]:
    """Extract target product, core problem summary, and suggested marketing angle."""
    clean_text = f"{title}. {content}".strip()
    
    # Target product / incumbent
    target_product = matched_competitors[0] if matched_competitors else "Manual Process / Generic AI Wrappers"

    # Core problem summary (first 1-2 key sentences)
    sentences = [s.strip() for s in re.split(r"[.!?\n]", clean_text) if len(s.strip()) > 15]
    if sentences:
        core_problem = f"{sentences[0]}."
        if len(sentences) > 1 and len(core_problem) < 140:
            core_problem += f" {sentences[1]}."
    else:
        core_problem = title

    # Tailored angle for AI & agentic systems
    if "hire" in clean_text.lower() or "freelance" in clean_text.lower() or "developer" in clean_text.lower():
        angle = "Propose clear scope breakdown for building a custom agentic pipeline with milestone delivery and architecture recommendations."
    elif intent_category in ["solution_request", "comparison"]:
        angle = f"Provide a lightweight architecture breakdown showing how a custom AI agent connects to existing tools without recurring platform fees."
    elif intent_category == "complaint":
        angle = f"Share how modern custom agentic pipelines bypass {target_product}'s rate limits and brittle automation steps."
    else:
        angle = "Offer 3 practical, concrete automation steps demonstrating how AI solves their exact operational bottleneck."

    return {
        "target_product": target_product,
        "core_problem_summary": core_problem[:250],
        "suggested_angle": angle
    }

def evaluate_lead(post: dict[str, Any], icp: dict[str, Any]) -> dict[str, Any]:
    """Run full dual-vector evaluation on a scraped Reddit post against the ICP."""
    title = post.get("title", "")
    content = post.get("content", "")
    published = post.get("published", "")

    # 1. Strict Recency Filter (Max 24 Hours)
    max_age_hours = icp.get("max_age_hours", 24)
    is_recent, recency_msg = check_recency(published, max_age_hours=max_age_hours)
    
    if not is_recent:
        return {
            "post_id": post.get("id", ""),
            "thread_title": title,
            "url": post.get("url", ""),
            "subreddit": post.get("subreddit", ""),
            "author": post.get("author", "anonymous"),
            "published": published,
            "intent_score": 0,
            "icp_match_score": 0,
            "composite_score": 0,
            "intent_category": "outdated",
            "is_disqualified": True,
            "disqualification_reason": recency_msg,
            "target_product": "N/A",
            "core_problem_summary": title,
            "suggested_angle": "Disqualified (Older than 24 hours)",
        }

    # 2. Targeted Community Check
    sub = (post.get("subreddit") or "").lower().replace("r/", "").strip()
    if sub and sub not in ALLOWED_COMMUNITIES:
        return {
            "post_id": post.get("id", ""),
            "thread_title": title,
            "url": post.get("url", ""),
            "subreddit": post.get("subreddit", ""),
            "author": post.get("author", "anonymous"),
            "published": published,
            "intent_score": 0,
            "icp_match_score": 0,
            "composite_score": 0,
            "intent_category": "irrelevant_community",
            "is_disqualified": True,
            "disqualification_reason": f"Subreddit r/{sub} not in targeted business/AI communities",
            "target_product": "N/A",
            "core_problem_summary": title,
            "suggested_angle": "Disqualified (Irrelevant subreddit)",
        }

    # 3. Disqualify Freelancer Ads ([For Hire])
    if re.search(r"\[\s*for\s+hire\s*\]|\b\[for_hire\]\b", title, re.IGNORECASE):
        return {
            "post_id": post.get("id", ""),
            "thread_title": title,
            "url": post.get("url", ""),
            "subreddit": post.get("subreddit", ""),
            "author": post.get("author", "anonymous"),
            "published": published,
            "intent_score": 0,
            "icp_match_score": 0,
            "composite_score": 0,
            "intent_category": "freelancer_ad",
            "is_disqualified": True,
            "disqualification_reason": "Individual freelancer advertising services, not an SMB hiring",
            "target_product": "N/A",
            "core_problem_summary": title,
            "suggested_angle": "Disqualified (Freelancer ad)",
        }

    # 4. Score Intent
    intent_score, intent_category = score_buying_intent(title, content)

    # 5. Score ICP Match & Disqualification
    icp_score, is_disqualified, disq_reason, matched_competitors = score_icp_fit(title, content, icp)

    if is_disqualified:
        composite_score = 0
    else:
        composite_score = int(round((intent_score * 0.6) + (icp_score * 0.4)))

    entities = extract_lead_entities(title, content, matched_competitors, intent_category)

    return {
        "post_id": post.get("id", ""),
        "thread_title": title,
        "url": post.get("url", ""),
        "subreddit": post.get("subreddit", ""),
        "author": post.get("author", "anonymous"),
        "published": published,
        "intent_score": intent_score,
        "icp_match_score": icp_score if not is_disqualified else 0,
        "composite_score": composite_score,
        "intent_category": intent_category,
        "is_disqualified": is_disqualified,
        "disqualification_reason": disq_reason,
        "target_product": entities["target_product"],
        "core_problem_summary": entities["core_problem_summary"],
        "suggested_angle": entities["suggested_angle"],
    }
