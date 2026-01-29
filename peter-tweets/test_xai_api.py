#!/usr/bin/env python3
"""Test X.AI API connection"""

import os
import httpx
import json
from dotenv import load_dotenv

# Load environment
load_dotenv(os.path.expanduser("~/clawd/.env"))

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
print(f"Token found: {bool(bearer_token)}")
print(f"Token prefix: {bearer_token[:10]}..." if bearer_token else "No token")

# X.AI API might be different from Twitter's
# Let's test a few possibilities

headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

print("\nTesting X.AI API endpoints...")

# Test 1: Standard Twitter v2 endpoint
try:
    print("\n1. Testing Twitter v2 API...")
    response = httpx.get(
        "https://api.twitter.com/2/users/by/username/steipete",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Works with Twitter API!")
        print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"❌ Twitter API error: {e}")

# Test 2: X.AI specific endpoint (guessing)
try:
    print("\n2. Testing X.AI API endpoint...")
    response = httpx.get(
        "https://api.x.ai/v1/users/steipete",
        headers=headers
    )
    print(f"Status: {response.status_code}")
except Exception as e:
    print(f"❌ X.AI API error: {e}")

# Test 3: Check if it's an OpenAI-compatible API
try:
    print("\n3. Testing as OpenAI-style API...")
    response = httpx.get(
        "https://api.x.ai/v1/models",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ X.AI uses OpenAI-compatible API!")
        print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"❌ OpenAI-style API error: {e}")

print("\n🔍 Note: X.AI key format suggests it's for their LLM API, not Twitter data access.")
print("You might need a different API or approach for Twitter data.")