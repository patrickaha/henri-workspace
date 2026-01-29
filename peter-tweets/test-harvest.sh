#!/bin/bash
# Quick test of Peter tweet harvesting

echo "🧪 Testing Peter Tweet Harvester..."
echo "=================================="

# Load environment
if [ -f "$HOME/clawd/.env" ]; then
    export $(grep -v '^#' "$HOME/clawd/.env" | xargs)
fi

# Test 1: Check API keys
echo ""
echo "1️⃣ Checking API keys..."
if [ -n "$TWITTER_BEARER_TOKEN" ]; then
    echo "✅ Twitter Bearer Token found"
else
    echo "❌ Missing TWITTER_BEARER_TOKEN"
    exit 1
fi

if [ -n "$XAI_API_KEY" ]; then
    echo "✅ X.AI API Key found (for Grok analysis)"
else
    echo "⚠️  No X.AI key (wisdom scoring disabled)"
fi

# Test 2: Test Twitter API
echo ""
echo "2️⃣ Testing Twitter Search API..."
RESPONSE=$(curl -s -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" \
    "https://api.twitter.com/2/tweets/search/recent?query=from:steipete%20-is:retweet&max_results=1")

if echo "$RESPONSE" | grep -q '"data"'; then
    echo "✅ Twitter API working!"
    TWEET=$(echo "$RESPONSE" | grep -o '"text":"[^"]*' | head -1 | cut -d'"' -f4)
    echo "   Latest tweet preview: ${TWEET:0:60}..."
else
    echo "❌ Twitter API failed"
    echo "$RESPONSE"
    exit 1
fi

# Test 3: Run harvest
echo ""
echo "3️⃣ Running quick harvest..."
cd "$(dirname "$0")"

if [ -f "venv/bin/python" ]; then
    venv/bin/python peter-quick-harvest.py
else
    python3 peter-quick-harvest.py
fi

echo ""
echo "✅ Test complete! Check daily-harvest/ for results"