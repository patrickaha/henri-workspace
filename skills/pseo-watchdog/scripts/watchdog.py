#!/usr/bin/env python3
"""
pSEO Watchdog - Monitor page indexing and traffic health

Usage:
    python watchdog.py status
    python watchdog.py index-report --days 30
    python watchdog.py traffic-timeline --days 30
    python watchdog.py drops --days 7 --threshold 5
    python watchdog.py full-report
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Optional

# Auto-source env vars from Clawdbot .env
ENV_FILE = os.path.expanduser("~/clawd/.env")
if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                if key not in os.environ:
                    os.environ[key] = val

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: Run: pip install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)


def get_credentials():
    """Get OAuth credentials from environment variables."""
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")
    site = os.environ.get("PSEOSITE")
    
    if not all([client_id, client_secret, refresh_token]):
        print("ERROR: Missing credentials. Set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN")
        sys.exit(1)
    
    if not site:
        print("ERROR: Set PSEOSITE env var (e.g., sc-domain:arthelper.ai)")
        sys.exit(1)
    
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )
    return creds, site


def get_search_analytics(service, site, days, limit=1000, dimensions=None):
    """Get search analytics data from GSC."""
    if dimensions is None:
        dimensions = ["page", "date"]
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    request = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": limit,
    }
    
    try:
        response = service.searchanalytics().query(siteUrl=site, body=request).execute()
        return response.get("rows", [])
    except HttpError as e:
        print(f"GSC API Error: {e}")
        sys.exit(1)


def build_page_timeline(rows):
    """Build timeline of when each page first appeared."""
    page_first_seen = {}
    page_data = {}
    
    for row in rows:
        page = row["keys"][0]
        date = row["keys"][1]
        clicks = row["clicks"]
        impressions = row["impressions"]
        ctr = row["ctr"]
        position = row["position"]
        
        if page not in page_first_seen:
            page_first_seen[page] = date
        
        if page not in page_data:
            page_data[page] = {"clicks": 0, "impressions": 0, "positions": []}
        
        page_data[page]["clicks"] += clicks
        page_data[page]["impressions"] += impressions
        page_data[page]["positions"].append(position)
    
    # Calculate averages and build result
    results = []
    for page, data in page_data.items():
        avg_position = sum(data["positions"]) / len(data["positions"]) if data["positions"] else 0
        results.append({
            "page": page,
            "first_seen": page_first_seen.get(page, "unknown"),
            "clicks": data["clicks"],
            "impressions": data["impressions"],
            "position": round(avg_position, 1),
        })
    
    return sorted(results, key=lambda x: x["first_seen"], reverse=True)


def get_all_tool_pages(rows):
    """Filter for /tool/ pages only."""
    return [r for r in rows if "/tool/" in r["page"]]


def status_check(rows, days=14):
    """Check page health status."""
    pages = get_all_tool_pages(build_page_timeline(rows))
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{'='*80}")
    print(f"pSEO WATCHDOG STATUS - Last {days} days")
    print(f"{'='*80}\n")
    
    stalled = []
    no_traffic = []
    healthy = []
    
    for page in pages:
        page_date = datetime.strptime(page["first_seen"], "%Y-%m-%d")
        days_ago = (datetime.now() - page_date).days
        
        status = "🟢 healthy"
        if page["clicks"] == 0:
            if days_ago >= days:
                status = "🔴 stalled"
                stalled.append(page)
            else:
                status = "🟡 pending"
                no_traffic.append(page)
        else:
            healthy.append(page)
        
        print(f"{status} {page['page']}")
        print(f"    First seen: {page['first_seen']} ({days_ago}d ago) | Clicks: {page['clicks']} | Position: {page['position']}")
    
    print(f"\n{'='*80}")
    print(f"SUMMARY: {len(healthy)} healthy | {len(no_traffic)} pending | {len(stalled)} stalled")
    print(f"{'='*80}")
    
    if stalled:
        print(f"\n🔴 STALLED PAGES (0 clicks after {days} days):")
        for p in stalled:
            print(f"  - {p['page']}")
    
    return {"healthy": healthy, "pending": no_traffic, "stalled": stalled}


def index_report(rows):
    """Report on indexing speed."""
    pages = get_all_tool_pages(build_page_timeline(rows))
    
    print(f"\n{'='*80}")
    print(f"INDEXING TIMELINE - When pages first appear in GSC")
    print(f"{'='*80}\n")
    
    # Group by week
    from collections import defaultdict
    by_week = defaultdict(list)
    
    for page in pages:
        week = f"{page['first_seen'][:4]}-W{datetime.strptime(page['first_seen'], '%Y-%m-%d').isocalendar()[1]:02d}"
        by_week[week].append(page)
    
    for week in sorted(by_week.keys()):
        pages_in_week = by_week[week]
        total_clicks = sum(p["clicks"] for p in pages_in_week)
        print(f"\n{week}: {len(pages_in_week)} pages | {total_clicks} total clicks")
        for p in pages_in_week[:5]:  # Show first 5
            print(f"  - {p['page'][:60]}... | {p['clicks']} clicks")
        if len(pages_in_week) > 5:
            print(f"  ... and {len(pages_in_week) - 5} more")


def traffic_timeline(rows):
    """Show when pages started getting traffic."""
    pages = get_all_tool_pages(build_page_timeline(rows))
    
    print(f"\n{'='*80}")
    print(f"TRAFFIC TIMELINE - Pages by first traffic date")
    print(f"{'='*80}\n")
    
    # Sort by clicks (highest first)
    sorted_pages = sorted(pages, key=lambda x: x["clicks"], reverse=True)
    
    for page in sorted_pages[:50]:
        print(f"{page['clicks']:>5} clicks | {page['page'][:60]}")
        print(f"           First seen: {page['first_seen']} | Position: {page['position']}")


def drops_report(rows, days=7, threshold=5):
    """Report on ranking drops."""
    # This would need historical data comparison
    print(f"\n{'='*80}")
    print(f"RANKING DROPS REPORT - Last {days} days (threshold: {threshold} positions)")
    print(f"{'='*80}\n")
    print("Note: Full drop detection requires historical baseline comparison.")
    print("Current implementation shows pages by position:\n")
    
    pages = get_all_tool_pages(build_page_timeline(rows))
    sorted_pages = sorted(pages, key=lambda x: x["position"])
    
    for page in sorted_pages[:20]:
        print(f"Position {page['position']:>5.1f} | {page['page'][:50]} | {page['clicks']} clicks")


def full_report(rows, days=30):
    """Generate comprehensive report."""
    print(f"\n{'='*80}")
    print(f"pSEO WATCHDOG - FULL REPORT ({days} days)")
    print(f"{'='*80}\n")
    
    status_check(rows, days=14)
    print()
    index_report(rows)


def main():
    parser = argparse.ArgumentParser(description="pSEO Watchdog - Monitor page health")
    parser.add_argument("--site", help="GSC site URL (or set PSEOSITE env)")
    parser.add_argument("--days", type=int, default=30, help="Days to analyze")
    parser.add_argument("--limit", type=int, default=1000, help="Max rows")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    subparsers.add_parser("status", help="Quick health check")
    subparsers.add_parser("index-report", help="Indexing timeline report")
    subparsers.add_parser("traffic-timeline", help="Traffic arrival report")
    
    drops_parser = subparsers.add_parser("drops", help="Ranking drops report")
    drops_parser.add_argument("--threshold", type=int, default=5, help="Position drop threshold")
    
    subparsers.add_parser("full-report", help="Comprehensive report")
    
    args = parser.parse_args()
    
    # Get service
    creds, site = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)
    
    # Use site from args if provided, otherwise env
    site = args.site or site
    
    # Get data
    print(f"Fetching GSC data for {site}...")
    rows = get_search_analytics(service, site, args.days, args.limit, ["page", "date"])
    
    if not rows:
        print("No data returned from GSC")
        sys.exit(1)
    
    # Run command
    if args.command == "status":
        status_check(rows, days=14)
    elif args.command == "index-report":
        index_report(rows)
    elif args.command == "traffic-timeline":
        traffic_timeline(rows)
    elif args.command == "drops":
        drops_report(rows, args.days, args.threshold)
    elif args.command == "full-report":
        full_report(rows, args.days)
    else:
        # Default to status
        status_check(rows, days=14)


if __name__ == "__main__":
    main()
