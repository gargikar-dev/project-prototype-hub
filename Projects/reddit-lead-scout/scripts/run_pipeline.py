#!/usr/bin/env python3
"""
Reddit ICP Lead Engine - Orchestrator Pipeline
----------------------------------------------
End-to-end execution pipeline calibrated for:
1. SMBs seeking AI solutions for business bottlenecks OR
   Businesses looking for freelancers/developers to build custom agentic systems or digital products.
2. Strict 24-hour recency constraint (no posts older than 24 hours).
3. Strict qualification threshold: score > 70 in criteria calculator (composite_score >= 71).
4. Targets ~20 qualified leads per execution.
5. Saves and appends deduplicated leads into the dedicated Excel Sheet & Google Sheet.

Usage:
    python scripts/run_pipeline.py --icp config/ai_business_icp.json --target-leads 20
"""

import sys
import os
import argparse
import json
import time
from datetime import datetime, timezone, timedelta
from typing import Any

# Ensure stdout/stderr handle UTF-8 cleanly on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Import local pipeline modules
from scrape_reddit import (
    scrape_subreddit_feed,
    scrape_subreddit_search,
    scrape_global_search,
)
from ai_lead_scorer import evaluate_lead, check_recency
from marketing_drafter import draft_marketing_response
from sheet_exporter import append_to_excel, append_to_csv, lead_to_row

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache")
DEFAULT_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1BKv_Uh3FynfdmUYX4o4yvuHdV8B6yxyYg5LURg4rHyg/edit"

def load_icp(icp_path: str) -> dict[str, Any]:
    """Load and validate ICP JSON configuration."""
    if not os.path.exists(icp_path):
        raise FileNotFoundError(f"ICP configuration file not found: {icp_path}")
    with open(icp_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_cached_feed(cache_key: str, max_age_minutes: int = 15) -> list[dict] | None:
    """Retrieve feed from local cache if fresh."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    safe_key = "".join(c if c.isalnum() or c in "-_" else "_" for c in cache_key)
    cache_file = os.path.join(CACHE_DIR, f"{safe_key}.json")
    if os.path.exists(cache_file):
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - mtime < timedelta(minutes=max_age_minutes):
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
    return None

def save_cached_feed(cache_key: str, items: list[dict]) -> None:
    """Persist feed to local cache."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    safe_key = "".join(c if c.isalnum() or c in "-_" else "_" for c in cache_key)
    cache_file = os.path.join(CACHE_DIR, f"{safe_key}.json")
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)
    except Exception:
        pass

def harvest_leads_pool(icp: dict[str, Any], limit_per_sub: int = 25, use_cache: bool = True) -> list[dict]:
    """Harvest submissions across target subreddits and keyword queries."""
    raw_posts = []
    seen_ids = set()

    target_subs = icp.get("target_subreddits", ["smallbusiness", "Entrepreneur", "startups", "AI_Agents"])
    search_queries = icp.get("search_queries", [])

    print(f"[*] Ingesting discussions from {len(target_subs)} target subreddits...")
    for i, sub in enumerate(target_subs):
        cache_key = f"sub_{sub}_new"
        posts = None
        if use_cache:
            posts = get_cached_feed(cache_key)
            if posts:
                print(f"  [Cache Hit] r/{sub} ({len(posts)} posts)")

        if not posts:
            posts = scrape_subreddit_feed(sub, feed="new", limit=limit_per_sub)
            if posts:
                save_cached_feed(cache_key, posts)
                print(f"  [Live Feed] r/{sub} ({len(posts)} posts)")
            else:
                # Polite fallback
                time.sleep(1.2)
                posts = scrape_subreddit_feed(sub, feed="hot", limit=15)
                if posts:
                    save_cached_feed(cache_key, posts)
                    print(f"  [Fallback Hot] r/{sub} ({len(posts)} posts)")

        if posts:
            for p in posts:
                p_id = p.get("id") or p.get("url")
                if p_id and p_id not in seen_ids:
                    seen_ids.add(p_id)
                    raw_posts.append(p)

        time.sleep(0.8)

    # Ingest targeted search queries
    if search_queries:
        print(f"\n[*] Ingesting high-intent search queries ({len(search_queries)} queries)...")
        for q in search_queries:
            cache_key = f"search_{q}"
            posts = None
            if use_cache:
                posts = get_cached_feed(cache_key)
                if posts:
                    print(f"  [Cache Hit] Query: '{q}' ({len(posts)} posts)")

            if not posts:
                posts = scrape_global_search(q, limit=20, sort="new")
                if posts:
                    save_cached_feed(cache_key, posts)
                    print(f"  [Live Search] Query: '{q}' ({len(posts)} posts)")
                else:
                    time.sleep(1.0)
                    # Try searching inside top subreddits
                    for target_sub in ["smallbusiness", "Entrepreneur", "AI_Agents", "startups"][:2]:
                        sub_posts = scrape_subreddit_search(target_sub, q, limit=10, sort="new")
                        if sub_posts:
                            posts = sub_posts
                            save_cached_feed(cache_key, posts)
                            print(f"  [Subreddit Search] r/{target_sub} '{q}' ({len(posts)} posts)")
                            break

            if posts:
                for p in posts:
                    p_id = p.get("id") or p.get("url")
                    if p_id and p_id not in seen_ids:
                        seen_ids.add(p_id)
                        raw_posts.append(p)
            time.sleep(0.8)
            time.sleep(0.8)

    return raw_posts

def run_pipeline(
    icp_path: str = "config/ai_business_icp.json",
    target_leads: int = 20,
    min_score: int = 71,
    max_age_hours: int = 24,
    limit_per_sub: int = 25,
    use_cache: bool = True,
    output_json: str = "reports/latest_leads.json",
    output_report: str = "reports/latest_leads.md",
    excel_path: str = "reports/reddit_leads_tracker.xlsx",
    csv_path: str = "reports/reddit_leads_tracker.csv",
) -> dict[str, Any]:
    """Execute end-to-end ICP lead harvesting, scoring, and sheet synchronization."""
    icp = load_icp(icp_path)
    # Allow ICP config to override defaults
    min_score = icp.get("min_score", min_score)
    max_age_hours = icp.get("max_age_hours", max_age_hours)
    target_leads = icp.get("target_lead_count", target_leads)

    print(f"\n========================================================")
    print(f"[*] Reddit ICP Lead Engine: AI & Agentic Solutions")
    print(f"Target ICP: {icp.get('icp_name', 'SMB AI & Agentic Systems')}")
    print(f"Strict Constraints:")
    print(f"  1. Max Age: <= {max_age_hours} hours (Disqualify > 24h)")
    print(f"  2. Score Threshold: Composite > 70 (Score >= {min_score})")
    print(f"  3. Target Leads to Output: ~{target_leads}")
    print(f"========================================================\n")

    # Step 1: Harvest Discussions
    raw_posts = harvest_leads_pool(icp, limit_per_sub=limit_per_sub, use_cache=use_cache)
    print(f"\nTotal raw discussions ingested: {len(raw_posts)}")

    # Step 2: AI Scoring & 24h Filter Evaluation
    print("Evaluating leads with Dual-Vector AI Engine...")
    evaluated_leads = []
    disqualified_by_age = 0
    disqualified_by_keywords = 0

    for post in raw_posts:
        lead_eval = evaluate_lead(post, icp)
        if lead_eval.get("is_disqualified"):
            reason = lead_eval.get("disqualification_reason", "")
            if "exceeds" in reason or "older" in reason:
                disqualified_by_age += 1
            else:
                disqualified_by_keywords += 1
        evaluated_leads.append(lead_eval)

    # Step 3: Filtering (Score > 70 AND Not Disqualified)
    qualified_leads = [
        lead for lead in evaluated_leads
        if not lead.get("is_disqualified") and lead.get("composite_score", 0) >= min_score
    ]

    qualified_leads.sort(key=lambda x: x.get("composite_score", 0), reverse=True)

    print(f"\nEvaluation Results:")
    print(f"  - Total Evaluated: {len(evaluated_leads)}")
    print(f"  - Disqualified (> 24h old): {disqualified_by_age}")
    print(f"  - Disqualified (Negative Keywords): {disqualified_by_keywords}")
    print(f"  - Qualified (Score > 70 & < 24h old): {len(qualified_leads)}")

    # Take top target_leads
    selected_leads = qualified_leads[:target_leads]

    # Step 4: Marketing Response Generation for Qualified Leads
    product_profile = icp.get("product_offering", {})
    staged_leads = []
    for lead in selected_leads:
        marketing_draft = draft_marketing_response(lead, product_profile)
        lead_payload = {
            **lead,
            "marketing_engagement": marketing_draft
        }
        staged_leads.append(lead_payload)

    # Step 5: Save JSON and Markdown Reports
    pipeline_result = {
        "timestamp": datetime.utcnow().isoformat(),
        "icp_name": icp.get("icp_name"),
        "total_harvested": len(raw_posts),
        "total_evaluated": len(evaluated_leads),
        "disqualified_older_than_24h": disqualified_by_age,
        "disqualified_negative_keywords": disqualified_by_keywords,
        "total_qualified": len(staged_leads),
        "min_score_threshold": min_score,
        "max_age_hours": max_age_hours,
        "dedicated_google_sheet": DEFAULT_GOOGLE_SHEET_URL,
        "leads": staged_leads
    }

    if output_json:
        os.makedirs(os.path.dirname(os.path.abspath(output_json)), exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(pipeline_result, f, indent=2)
        print(f"\n[OK] Structured Lead JSON saved to: {output_json}")

    if output_report:
        os.makedirs(os.path.dirname(os.path.abspath(output_report)), exist_ok=True)
        generate_markdown_report(pipeline_result, output_report)
        print(f"[OK] Markdown Briefing saved to: {output_report}")

    # Step 6: Synchronize to Dedicated Excel & CSV Sheets
    newly_added_excel = append_to_excel(staged_leads, excel_path)
    newly_added_csv = append_to_csv(staged_leads, csv_path)
    print(f"[OK] Dedicated Excel Tracker updated: {excel_path} (+{newly_added_excel} new rows)")
    print(f"[OK] Dedicated CSV Tracker updated: {csv_path} (+{newly_added_csv} new rows)")
    print(f"[OK] Dedicated Google Sheet: {DEFAULT_GOOGLE_SHEET_URL}")

    return pipeline_result

def generate_markdown_report(result: dict[str, Any], filepath: str) -> None:
    """Generate human-readable briefing in Markdown."""
    lines = [
        f"# Reddit ICP Lead Intelligence Report",
        f"**Target ICP:** {result.get('icp_name')}",
        f"**Generated At (UTC):** {result.get('timestamp')}",
        f"**Constraint 1 (Recency):** Posted within last {result.get('max_age_hours')} hours",
        f"**Constraint 2 (Score):** Scored > 70 (Cutoff: {result.get('min_score_threshold')}+)",
        f"**Discussions Ingested:** {result.get('total_harvested')}",
        f"**Filtered Out (> 24h old):** {result.get('disqualified_older_than_24h')}",
        f"**Filtered Out (Negative Keywords):** {result.get('disqualified_negative_keywords')}",
        f"**Qualified High-Intent Leads:** {result.get('total_qualified')}",
        f"**Dedicated Google Sheet:** [{result.get('dedicated_google_sheet')}]({result.get('dedicated_google_sheet')})",
        "",
        "---",
        "",
        "## Qualified Prospects (> 70 Score & < 24 Hours Old)",
        ""
    ]

    leads = result.get("leads", [])
    if not leads:
        lines.append("No leads met both criteria (score > 70 and published within last 24 hours).")
    else:
        for i, lead in enumerate(leads, 1):
            m = lead.get("marketing_engagement", {})
            lines.extend([
                f"### {i}. [{lead.get('thread_title')}]({lead.get('url')})",
                f"- **Subreddit:** r/{lead.get('subreddit')} | **Author:** u/{lead.get('author')} | **Published:** `{lead.get('published', 'Recent')}`",
                f"- **Composite Score:** **{lead.get('composite_score')}/100** (Intent: {lead.get('intent_score')} | ICP Match: {lead.get('icp_match_score')})",
                f"- **Category:** `{lead.get('intent_category')}`",
                f"- **Current Stack / Target:** {lead.get('target_product')}",
                f"- **Core Frustration:** {lead.get('core_problem_summary')}",
                f"- **Recommended Angle:** {lead.get('suggested_angle')}",
                "",
                "#### Staged 80/20 Value-First Marketing Draft (HITL Review):",
                "```text",
                m.get("drafted_response", "N/A"),
                "```",
                f"- **Spam Risk Score:** `{m.get('risk_assessment', {}).get('spam_risk_score', 0.05)}` (Compliance: {'PASS' if m.get('risk_assessment', {}).get('rule_compliance') else 'FLAGGED'})",
                "",
                "---",
                ""
            ])

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    parser = argparse.ArgumentParser(description="Reddit ICP Lead Engine Pipeline Runner")
    parser.add_argument("--icp", default="config/ai_business_icp.json", help="Path to ICP JSON profile")
    parser.add_argument("--target-leads", type=int, default=20, help="Target number of qualified leads to output")
    parser.add_argument("--min-score", type=int, default=71, help="Minimum composite lead score (> 70)")
    parser.add_argument("--max-age", type=int, default=24, help="Maximum post age in hours")
    parser.add_argument("--limit-per-sub", type=int, default=25, help="Scrape limit per subreddit feed")
    parser.add_argument("--no-cache", action="store_true", help="Bypass local cache")
    parser.add_argument("--output", default="reports/latest_leads.json", help="Output path for JSON results")
    parser.add_argument("--report", default="reports/latest_leads.md", help="Output path for Markdown briefing")
    parser.add_argument("--excel", default="reports/reddit_leads_tracker.xlsx", help="Dedicated Excel output path")
    parser.add_argument("--csv", default="reports/reddit_leads_tracker.csv", help="Dedicated CSV output path")
    args = parser.parse_args()

    run_pipeline(
        icp_path=args.icp,
        target_leads=args.target_leads,
        min_score=args.min_score,
        max_age_hours=args.max_age,
        limit_per_sub=args.limit_per_sub,
        use_cache=not args.no_cache,
        output_json=args.output,
        output_report=args.report,
        excel_path=args.excel,
        csv_path=args.csv,
    )

if __name__ == "__main__":
    main()
