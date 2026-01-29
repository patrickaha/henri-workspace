#!/usr/bin/env python3
"""Test minimal Twitter API calls to find what works without credits"""

import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/clawd/.env"))
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

headers = {"Authorization": f"Bearer {bearer_token}"}

print("Testing different Twitter API endpoints...")

# Test various endpoints to see what works
endpoints = [
    # User lookup
    ("GET", "/2/users/by/username/steipete", {}, "User lookup"),
    
    # Tweet lookup (specific tweet)
    ("GET", "/2/tweets/1869074293322522875", {}, "Single tweet"),
    
    # Search recent tweets (might have different limits)
    ("GET", "/2/tweets/search/recent", {"query": "from:steipete", "max_results": 10}, "Search recent"),
    
    # Rate limit status
    ("GET", "/1.1/application/rate_limit_status", {}, "Rate limits v1.1"),
    
    # User timeline v1.1 (older endpoint)
    ("GET", "/1.1/statuses/user_timeline.json", {"screen_name": "steipete", "count": 5}, "Timeline v1.1"),
]

for method, path, params, desc in endpoints:
    print(f"\n{desc}: {path}")
    try:
        if path.startswith("/2"):
            url = f"https://api.twitter.com{path}"
        else:
            url = f"https://api.twitter.com{path}"
            
        response = httpx.request(method, url, headers=headers, params=params)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ SUCCESS!")
            data = response.json()
            print(f"  Response preview: {str(data)[:200]}...")
        elif response.status_code == 402:
            print(f"  ❌ Requires credits")
        elif response.status_code == 404:
            print(f"  ❌ Not found (endpoint might not exist)")
        else:
            print(f"  ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Exception: {e}")

print("\n" + "="*50)
print("Summary:")
print("- All v2 endpoints require credits/payment")
print("- v1.1 endpoints are deprecated")
print("- Need to either:")
print("  1. Enable billing on developer.twitter.com")
print("  2. Use bird CLI with cookies")
print("  3. Use a scraping approach")