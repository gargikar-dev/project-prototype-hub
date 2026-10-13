#!/usr/bin/env python3
"""
Reddit Scraper Engine (Ideal Scraper Protocol)
-----------------------------------------------
Autonomous scraping module for Reddit without requiring Reddit API keys,
OAuth registration, or third-party paid subscriptions.

Features:
- Rotating modern browser headers & realistic fingerprints
- Intelligent backoff and rate-limit handling (429 mitigation)
- Multi-tier ingestion: Subreddit Atom/RSS feeds, Subreddit Search, Global Search
- Parsing and extraction of post ID, title, clean body, author, subreddit, and published timestamp.
"""

import sys
import os
import argparse
import json
import time
import re
import random
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
]

def get_headers() -> dict[str, str]:
    """Generate realistic browser headers with rotating User-Agent."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/atom+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

def clean_html(raw_html: str) -> str:
    """Strip HTML markup and return clean text."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    for s in soup(["script", "style"]):
        s.decompose()
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"submitted by\s+/u/\S+", "", text)
    text = re.sub(r"\[link\]\s*\[comments\]", "", text)
    return " ".join(text.split())

def make_polite_request(url: str, retries: int = 2) -> requests.Response | None:
    """Execute HTTP GET with realistic headers, timeout, and polite 429 backoff."""
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=get_headers(), timeout=12)
            if resp.status_code == 200:
                return resp
            elif resp.status_code == 429 and attempt < retries:
                # Polite backoff: pause 3-5 seconds and retry with a new User-Agent
                sleep_sec = 3.0 + (attempt * 2.0)
                time.sleep(sleep_sec)
                continue
            else:
                sys.stderr.write(f"[scrape_reddit] Request to {url} returned HTTP {resp.status_code}\n")
        except Exception as e:
            sys.stderr.write(f"[scrape_reddit] Request error on {url}: {e}\n")
            if attempt < retries:
                time.sleep(2.0)
    return None

def parse_reddit_atom_feed(xml_content: bytes, limit: int = 25) -> list[dict]:
    """Parse Reddit Atom XML feed into clean structured post/comment objects."""
    entries = []
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return []

    for entry in root.findall("atom:entry", ns):
        if len(entries) >= limit:
            break

        id_elem = entry.find("atom:id", ns)
        title_elem = entry.find("atom:title", ns)
        link_elem = entry.find("atom:link", ns)
        content_elem = entry.find("atom:content", ns)
        updated_elem = entry.find("atom:updated", ns)
        author_elem = entry.find("atom:author/atom:name", ns)
        category_elem = entry.find("atom:category", ns)

        raw_id = id_elem.text if id_elem is not None and id_elem.text else ""
        title = title_elem.text if title_elem is not None and title_elem.text else ""
        link = link_elem.attrib.get("href", "") if link_elem is not None else ""
        raw_html = content_elem.text if content_elem is not None and content_elem.text else ""
        author = author_elem.text if author_elem is not None and author_elem.text else "unknown"
        updated = updated_elem.text if updated_elem is not None and updated_elem.text else ""
        category = category_elem.attrib.get("term", "") if category_elem is not None else ""

        sub = category
        if not sub and "/r/" in link:
            parts = link.split("/r/")[1].split("/")
            sub = parts[0] if parts else ""

        post_id = ""
        if "/comments/" in link:
            parts = link.split("/comments/")[1].split("/")
            post_id = parts[0] if parts else ""
        elif raw_id.startswith("t3_") or raw_id.startswith("t1_"):
            post_id = raw_id

        text_content = clean_html(raw_html)

        entries.append({
            "id": post_id or raw_id,
            "title": title,
            "content": text_content,
            "url": link,
            "author": author.replace("/u/", ""),
            "subreddit": sub,
            "published": updated,
            "kind": "comment" if raw_id.startswith("t1_") or " on " in title else "post",
        })

    return entries

def scrape_subreddit_search(subreddit: str, query: str, limit: int = 25, sort: str = "new") -> list[dict]:
    """Search within a specific subreddit using public RSS endpoints."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.reddit.com/r/{subreddit}/search.rss?q={encoded_query}&sort={sort}&restrict_sr=1"
    
    resp = make_polite_request(url)
    if resp and resp.status_code == 200:
        return parse_reddit_atom_feed(resp.content, limit=limit)
    return []

def scrape_global_search(query: str, limit: int = 25, sort: str = "new") -> list[dict]:
    """Search globally across Reddit using public RSS endpoints."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.reddit.com/search.rss?q={encoded_query}&sort={sort}"
    
    resp = make_polite_request(url)
    if resp and resp.status_code == 200:
        return parse_reddit_atom_feed(resp.content, limit=limit)
    return []

def scrape_subreddit_feed(subreddit: str, feed: str = "new", limit: int = 25) -> list[dict]:
    """Fetch recent, hot, or top posts from a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/{feed}/.rss"
    
    resp = make_polite_request(url)
    if resp and resp.status_code == 200:
        return parse_reddit_atom_feed(resp.content, limit=limit)
    return []

def main():
    parser = argparse.ArgumentParser(description="Ideal Scraper Reddit Harvesting CLI")
    parser.add_argument("--sub", help="Subreddit name (without r/)")
    parser.add_argument("--query", help="Search keywords or query")
    parser.add_argument("--feed", choices=["new", "hot", "top"], default="new", help="Subreddit feed type")
    parser.add_argument("--limit", type=int, default=15, help="Maximum number of items to return")
    parser.add_argument("--sort", choices=["new", "relevance", "top"], default="new", help="Sort order")
    parser.add_argument("--output", help="Optional file path to write JSON output")
    args = parser.parse_args()

    results = []
    if args.sub and args.query:
        results = scrape_subreddit_search(args.sub, args.query, limit=args.limit, sort=args.sort)
    elif args.sub:
        results = scrape_subreddit_feed(args.sub, feed=args.feed, limit=args.limit)
    elif args.query:
        results = scrape_global_search(args.query, limit=args.limit, sort=args.sort)

    payload = {
        "success": True,
        "count": len(results),
        "results": results
    }
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
