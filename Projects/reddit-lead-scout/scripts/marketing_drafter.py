#!/usr/bin/env python3
"""
Reddit Marketing Drafter
------------------------
Generates value-first, organic Reddit comments for qualified ICP leads.
Adheres strictly to the 80/20 rule (80% actionable guidance, 20% transparent mention).
Evaluates spam risk score to ensure community safety.
"""

import re
from typing import Any

SPAMMY_TRIGGERS = [
    "game-changer",
    "revolutionary",
    "all-in-one",
    "best on the market",
    "check out my",
    "click here",
    "buy now",
    "discount",
    "guaranteed",
    "100% free",
    "sign up now",
    "dm me",
    "inbox me",
]

def audit_spam_risk(response_text: str) -> tuple[float, list[str]]:
    """Evaluate response against Reddit community spam filters."""
    flagged = []
    text_lower = response_text.lower()
    
    for phrase in SPAMMY_TRIGGERS:
        if phrase in text_lower:
            flagged.append(phrase)

    # Count exclamation marks and all-caps words
    exclamation_count = response_text.count("!")
    caps_words = [w for w in response_text.split() if w.isupper() and len(w) > 3]

    risk_score = 0.05
    risk_score += len(flagged) * 0.15
    if exclamation_count > 2:
        risk_score += 0.15
    if len(caps_words) > 1:
        risk_score += 0.10

    # Check link presence
    if "http://" in text_lower or "https://" in text_lower:
        risk_score += 0.10

    return round(min(risk_score, 0.95), 2), flagged

def draft_marketing_response(lead: dict[str, Any], product_profile: dict[str, Any]) -> dict[str, Any]:
    """Craft an authentic, helpful comment tailored to the lead's core frustration."""
    title = lead.get("thread_title", "")
    core_problem = lead.get("core_problem_summary", title)
    target_product = lead.get("target_product", "manual processes")
    category = lead.get("intent_category", "solution_request")
    
    product_name = product_profile.get("name", "our engineering team")
    value_prop = product_profile.get("core_value_prop", "building custom agentic pipelines")
    differentiator = product_profile.get("differentiator", "direct integrations without monthly bloat")

    # Clean core problem for natural flow
    clean_problem = re.sub(r"^[A-Z][a-z]+(\s+[a-z]+)*:\s*", "", core_problem).strip()
    clean_problem = clean_problem.rstrip(".")

    is_hiring = any(k in f"{title} {clean_problem}".lower() for k in ["freelance", "hire", "developer", "contract", "looking for someone"])

    if is_hiring:
        draft = (
            f"If you're scoping out someone to build this, the biggest thing to nail down first is the boundary between deterministic logic and LLM agent decisions.\n\n"
            f"A lot of freelance builds fail or balloon in scope because people try to let an AI agent handle everything end-to-end instead of scoping it into: (1) structured data intake, (2) targeted agentic reasoning for unstructured decisions, and (3) a deterministic action trigger (like writing to your CRM or database).\n\n"
            f"For tech stack, keeping it on a lightweight framework like LangGraph or custom Python scripts with structured tool-calling is usually 10x more maintainable than bloated no-code wrappers.\n\n"
            f"Context: I build custom agentic systems for businesses ({differentiator}). Happy to share a quick architecture blueprint or talk through how to scope the deliverables cleanly!"
        )
    elif category in ["solution_request", "comparison"]:
        draft = (
            f"When approaching {clean_problem.lower()}, the biggest trap is trying to automate the entire workflow in one go.\n\n"
            f"A much cleaner pattern is breaking it into two phases:\n"
            f"1. Centralize the intake: normalize incoming data (forms, emails, or spreadsheets) into a clean JSON schema first.\n"
            f"2. Plug in a focused AI agent: use an LLM only for the fuzzy/decision step, with strict guardrails and human verification before triggering any write actions.\n\n"
            f"Compared to {target_product}, building a lightweight bespoke agentic pipeline keeps your data private and avoids expensive recurring per-task platform fees.\n\n"
            f"Context: we engineer custom AI agentic solutions for growing businesses ({differentiator}). Feel free to ask if you want advice on how to architect the data handoff!"
        )
    elif category == "complaint":
        draft = (
            f"Totally get the frustration with {target_product}. Many businesses hit a ceiling when their workflows become slightly non-standard and off-the-shelf tools start breaking or costing a fortune.\n\n"
            f"The workaround most teams adopt is setting up a localized proxy layer or lightweight custom agent that handles state and error retries before passing data through.\n\n"
            f"If you decide to migrate to a custom build, keep your agentic logic decoupled from the UI so you don't get locked into another proprietary ecosystem. (We focus on {value_prop}). Hope this helps you navigate the immediate hurdle!"
        )
    else:
        draft = (
            f"Dealing with {clean_problem.lower()} is a classic operational bottleneck as teams scale.\n\n"
            f"Here are 2 practical ways to approach it with AI today:\n"
            f"1. Audit the repetitive touchpoints: identify the 20% of manual decisions that eat 80% of your staff's hours and automate just those decision gates.\n"
            f"2. Keep a human-in-the-loop: let the agent draft the output/action, but route it to an internal Slack channel or spreadsheet for 1-click human confirmation before dispatch.\n\n"
            f"Context: I develop custom agentic systems and digital products for businesses ({differentiator}). If you'd like a quick technical breakdown on how to connect this to your current stack, happy to help!"
        )

    spam_risk, flagged_phrases = audit_spam_risk(draft)

    return {
        "engagement_strategy": "DIRECT_HELPFUL_COMMENT",
        "drafted_response": draft,
        "risk_assessment": {
            "spam_risk_score": spam_risk,
            "rule_compliance": spam_risk < 0.30,
            "flagged_phrases": flagged_phrases
        },
        "requires_hitl_approval": True
    }
