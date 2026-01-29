#!/usr/bin/env python3
"""Test Twitter API v2 connection"""

import os
import httpx
import json
from dotenv import load_dotenv

# Load environment
load_dotenv(os.path.expanduser("~/clawd/.env"))

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
print(f"Token found: {bool(bearer_token)}")
print(f"Token prefix: {bearer_token[:20]}..." if bearer_token else "No token")

headers = {
    "Authorization": f"Bearer {bearer_token}",
}

print("\nTesting Twitter API v2...")

# Test 1: Get user by username
try:
    print("\n1. Fetching @steipete user info...")
    response = httpx.get(
        "https://api.twitter.com/2/users/by/username/steipete",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Twitter API working!")
        data = response.json()
        print(json.dumps(data, indent=2))
        
        user_id = data['data']['id']
        print(f"\nUser ID: {user_id}")
        
        # Test 2: Get recent tweets
        print("\n2. Fetching recent tweets...")
        tweets_response = httpx.get(
            f"https://api.twitter.com/2/users/{user_id}/tweets",
            headers=headers,
            params={
                "max_results": 5,
                "tweet.fields": "created_at,public_metrics"
            }
        )
        
        if tweets_response.status_code == 200:
            tweets_data = tweets_response.json()
            print(f"✅ Found {len(tweets_data.get('data', []))} tweets")
            
            for tweet in tweets_data.get('data', [])[:2]:
                print(f"\n- {tweet['created_at'] if 'created_at' in tweet else 'N/A'}")
                print(f"  {tweet['text'][:100]}...")
                
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")