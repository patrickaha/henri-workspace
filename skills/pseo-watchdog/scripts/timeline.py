#!/usr/bin/env python3
"""
pSEO Timeline Tracker - V2 & V3 Focus

Track: Published → Indexed → First Traffic → First Signup

Usage:
    python timeline.py status           # Current status
    python timeline.py v2               # V2 batch (early Jan)
    python timeline.py v3               # V3 batch (today)
    python timeline.py timeline <url>   # Single page timeline
    python timeline.py first-signups    # First signup by page
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Auto-source env vars
ENV_FILE = os.path.expanduser("~/clawd/.env")
if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                if key not in os.environ:
                    os.environ[key] = val


def get_credentials():
    """Get OAuth credentials."""
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")
    site = os.environ.get("PSEOSITE")
    
    if not all([client_id, client_secret, refresh_token, site]):
        print("ERROR: Missing credentials")
        sys.exit(1)
    
    from google.oauth2.credentials import Credentials
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    return creds, site


def parse_sheet_date(date_str):
    """Parse date from sheet."""
    if not date_str:
        return None
    date_str = str(date_str).strip()
    for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def get_pages_from_sheets(spreadsheet_id: str) -> Dict[str, Dict]:
    """
    Fetch pages and dates from tracker.
    Returns: {url: {date_published, batch}}
    """
    import subprocess
    
    pages = {}
    
    subprocess.run(
        'security unlock-keychain -p "313131" ~/Library/Keychains/login.keychain.db',
        shell=True, capture_output=True
    )
    
    # V2: pseo-published-2026-01-07 (Date Published | URL | Keyword)
    try:
        result = subprocess.run(
            f'gog sheets get {spreadsheet_id} "pseo-published-2026-01-07!A2:C"',
            shell=True, capture_output=True, text=True
        )
        
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                match = re.search(r'(https://[^\s]+)', line)
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})', line)
                if match and date_match:
                    url = match.group(1).rstrip('/')
                    date = parse_sheet_date(date_match.group(1))
                    if date and url:
                        pages[url] = {"date_published": date, "batch": "V2"}
    except Exception as e:
        print(f"Warning: Could not read V2 tab: {e}")
    
    # V3: 2026-01-16-pSEO _ Second_Round (published 2026-01-16)
    try:
        result = subprocess.run(
            f'gog sheets get {spreadsheet_id} "2026-01-16-pSEO _ Second_Round!A2:A"',
            shell=True, capture_output=True, text=True
        )
        
        v3_date = datetime(2026, 1, 16)
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                match = re.search(r'(https://[^\s]+)', line)
                if match:
                    url = match.group(1).rstrip('/')
                    if url and url not in pages:
                        pages[url] = {"date_published": v3_date, "batch": "V3"}
    except Exception as e:
        print(f"Warning: Could not read V3 tab: {e}")
    
    return pages


def get_gsc_data(service, site: str, days: int = 60) -> Dict[str, Dict]:
    """Get GSC data for all pages."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    request = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page", "date"],
        "rowLimit": 10000,
    }
    
    response = service.searchanalytics().query(siteUrl=site, body=request).execute()
    rows = response.get("rows", [])
    
    page_data = {}
    page_first_seen = {}
    
    for row in rows:
        page = row["keys"][0]
        date = row["keys"][1]
        clicks = row.get("clicks", 0)
        
        if page not in page_first_seen:
            page_first_seen[page] = date
        
        if page not in page_data:
            page_data[page] = {
                "first_seen": date,
                "clicks": 0,
                "traffic_dates": [],
            }
        
        page_data[page]["clicks"] += clicks
        if clicks > 0:
            page_data[page]["traffic_dates"].append(date)
    
    result = {}
    for page, data in page_data.items():
        first_traffic = min(data["traffic_dates"]) if data["traffic_dates"] else None
        result[page] = {
            "first_seen_gsc": page_first_seen.get(page),
            "first_traffic": first_traffic,
            "clicks": data["clicks"],
        }
    
    return result


def build_timeline(pages: Dict, gsc_data: Dict) -> List[Dict]:
    """Build complete timeline for each page."""
    timeline = []
    
    for url, info in pages.items():
        pub_date = info["date_published"]
        batch = info["batch"]
        gsc = gsc_data.get(url, {})
        
        first_seen = gsc.get("first_seen_gsc")
        first_traffic = gsc.get("first_traffic")
        
        days_to_index = None
        days_to_traffic = None
        
        if first_seen:
            try:
                seen_date = datetime.strptime(first_seen, "%Y-%m-%d")
                days_to_index = (seen_date - pub_date).days
            except:
                pass
        
        if first_traffic:
            try:
                traffic_date = datetime.strptime(first_traffic, "%Y-%m-%d")
                days_to_traffic = (traffic_date - pub_date).days
            except:
                pass
        
        timeline.append({
            "url": url,
            "date_published": pub_date.strftime("%Y-%m-%d"),
            "batch": batch,
            "first_seen_gsc": first_seen or "not indexed",
            "first_traffic": first_traffic or "no traffic",
            "days_to_index": days_to_index,
            "days_to_traffic": days_to_traffic,
            "clicks": gsc.get("clicks", 0),
        })
    
    return sorted(timeline, key=lambda x: x["date_published"], reverse=True)


def report_v2(timeline: List[Dict], ga4_data: Dict = None, days_threshold: int = 30):
    """V2 batch report (early Jan) - excludes pre-indexed pages."""
    v2 = [p for p in timeline if p["batch"] == "V2"]
    
    # Filter: only truly new pages (indexed AND got traffic AFTER publish, not before)
    v2_new = []
    for p in v2:
        # Exclude if indexed before publish
        if p["days_to_index"] is not None and p["days_to_index"] < 0:
            continue
        # Exclude if got traffic before publish
        if p["days_to_traffic"] is not None and p["days_to_traffic"] < 0:
            continue
        v2_new.append(p)
    
    pre_indexed = [p for p in v2 if p["days_to_index"] is not None and p["days_to_index"] < 0]
    
    print(f"\n{'='*90}")
    print(f"V2 BATCH REPORT - Published Early Jan 2026")
    print(f"{'='*90}\n")
    
    print(f"TRULY NEW: {len(v2_new)}")
    print(f"PRE-INDEXED (already in GSC): {len(pre_indexed)}")
    print()
    
    indexed = [p for p in v2_new if p["days_to_index"] is not None]
    not_indexed = [p for p in v2_new if p["days_to_index"] is None]
    with_traffic = [p for p in v2_new if p["days_to_traffic"] is not None]
    
    print(f"Indexed: {len(indexed)}")
    print(f"With traffic: {len(with_traffic)}")
    print(f"Not indexed: {len(not_indexed)}")
    print()
    
    # Indexing speed distribution
    if indexed:
        buckets = {"0": [], "1": [], "2": [], "3-5": [], "6-10": [], "10+": []}
        for p in indexed:
            days = p["days_to_index"]
            if days == 0:
                buckets["0"].append(p)
            elif days == 1:
                buckets["1"].append(p)
            elif days == 2:
                buckets["2"].append(p)
            elif days <= 5:
                buckets["3-5"].append(p)
            elif days <= 10:
                buckets["6-10"].append(p)
            else:
                buckets["10+"].append(p)
        
        print("INDEXING SPEED (days from publish to GSC appearance):")
        for bucket, pages in buckets.items():
            if pages:
                print(f"  Day {bucket}: {len(pages)} pages")
        print()
    
    # Traffic timeline
    if with_traffic:
        buckets = {"0-2": [], "3-5": [], "6-10": [], "10+": []}
        for p in with_traffic:
            days = p["days_to_traffic"] or 999
            if days <= 2:
                buckets["0-2"].append(p)
            elif days <= 5:
                buckets["3-5"].append(p)
            elif days <= 10:
                buckets["6-10"].append(p)
            else:
                buckets["10+"].append(p)
        
        print("TRAFFIC TIMELINE (days from publish to first click):")
        for bucket, pages in buckets.items():
            if pages:
                avg = sum(p["clicks"] for p in pages) / len(pages)
                print(f"  {bucket} days: {len(pages)} pages | Avg clicks: {avg:.1f}")
        print()
    
    # Top performers (truly new pages only)
    print("TOP 10 BY TRAFFIC (truly new pages):")
    for p in sorted(v2_new, key=lambda x: x["clicks"], reverse=True)[:10]:
        days = p["days_to_traffic"] if p["days_to_traffic"] else "N/A"
        print(f"  {p['clicks']:>3} clicks | Day {days} | {p['url'][:50]}")
    
    print(f"\n{'='*90}")


def report_v3(timeline: List[Dict]):
    """V3 batch report (published today)."""
    v3 = [p for p in timeline if p["batch"] == "V3"]
    
    print(f"\n{'='*90}")
    print(f"V3 BATCH REPORT - Published 2026-01-16")
    print(f"{'='*90}\n")
    
    indexed = [p for p in v3 if p["days_to_index"] is not None and p["days_to_index"] >= 0]
    not_indexed = [p for p in v3 if p["days_to_index"] is None]
    
    print(f"Total V3 pages: {len(v3)}")
    print(f"Indexed: {len(indexed)}")
    print(f"Not indexed yet: {len(not_indexed)}")
    print()
    
    if indexed:
        print("INDEXED PAGES:")
        for p in sorted(indexed, key=lambda x: x["days_to_index"]):
            print(f"  Day {p['days_to_index']} | {p['url'][:60]}")
    else:
        print("No pages indexed yet (normal - published today)")
        print("Expected: Indexing within 1-4 days based on V2 data")
    
    print(f"\n{'='*90}")


def report_status(timeline: List[Dict]):
    """Quick status overview."""
    v2 = [p for p in timeline if p["batch"] == "V2"]
    v3 = [p for p in timeline if p["batch"] == "V3"]
    
    v2_indexed = len([p for p in v2 if p["days_to_index"] is not None and p["days_to_index"] >= 0])
    v2_traffic = len([p for p in v2 if p["days_to_traffic"] is not None])
    v3_indexed = len([p for p in v3 if p["days_to_index"] is not None and p["days_to_index"] >= 0])
    
    print(f"\n{'='*90}")
    print(f"pSEO TIMELINE STATUS")
    print(f"{'='*90}\n")
    
    print(f"V2 (early Jan): {v2_indexed}/{len(v2)} indexed | {v2_traffic} with traffic")
    print(f"V3 (today): {v3_indexed}/{len(v3)} indexed")
    print()


def main():
    parser = argparse.ArgumentParser(description="pSEO Timeline Tracker")
    parser.add_argument("--site", help="GSC site")
    parser.add_argument("--days", type=int, default=60)
    parser.add_argument("--sheet", default="1SzFiBL6mDpwSa3de4q540wBWAJodiWEgJL8W6SxNTRU")
    
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("status", help="Quick status")
    subparsers.add_parser("v2", help="V2 batch report")
    subparsers.add_parser("v3", help="V3 batch report")
    
    args = parser.parse_args()
    
    creds, site = get_credentials()
    gsc = build("searchconsole", "v1", credentials=creds)
    site = args.site or site
    
    print("Fetching data...")
    pages = get_pages_from_sheets(args.sheet)
    gsc_data = get_gsc_data(gsc, site, args.days)
    timeline = build_timeline(pages, gsc_data)
    
    if args.command == "status":
        report_status(timeline)
    elif args.command == "v2":
        report_v2(timeline)
    elif args.command == "v3":
        report_v3(timeline)
    else:
        report_status(timeline)


if __name__ == "__main__":
    main()
