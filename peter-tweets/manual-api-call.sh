#!/bin/bash
# Manual API call to get Peter's tweets

BEARER_TOKEN=$(grep TWITTER_BEARER_TOKEN ~/clawd/.env | cut -d= -f2)

echo "🐦 Fetching Peter's tweets and replies from last 24 hours..."
echo "=================================================="

# Make API call
curl -s -H "Authorization: Bearer $BEARER_TOKEN" \
  "https://api.twitter.com/2/tweets/search/recent?query=from:steipete%20-is:retweet&max_results=100&tweet.fields=created_at,public_metrics,in_reply_to_user_id" \
  > /tmp/peter-tweets.json

# Check if successful
if [ $? -eq 0 ]; then
    echo "✅ API call successful!"
    
    # Parse with jq
    echo ""
    echo "SUMMARY:"
    TOTAL=$(jq '.data | length' /tmp/peter-tweets.json)
    echo "Total items: $TOTAL"
    
    echo ""
    echo "RECENT TWEETS (not replies):"
    echo "============================="
    jq -r '.data[] | select(.in_reply_to_user_id == null) | 
        "\n📝 \(.created_at)\n\(.text)\n❤️ \(.public_metrics.like_count) likes | 🔁 \(.public_metrics.retweet_count) retweets\n🔗 https://x.com/steipete/status/\(.id)\n" + ("-" * 80)' /tmp/peter-tweets.json | head -n 30
    
    echo ""
    echo "RECENT REPLIES:"
    echo "==============="
    jq -r '.data[] | select(.in_reply_to_user_id != null) | 
        "\n💬 \(.created_at)\n\(.text)\n🔗 https://x.com/steipete/status/\(.id)\n" + ("-" * 80)' /tmp/peter-tweets.json | head -n 30
    
    # Save to file
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    OUTPUT_DIR="$HOME/clawd/peter-tweets/daily-harvest"
    mkdir -p "$OUTPUT_DIR"
    
    cp /tmp/peter-tweets.json "$OUTPUT_DIR/peter-raw-$TIMESTAMP.json"
    
    echo ""
    echo "✅ Raw data saved to: $OUTPUT_DIR/peter-raw-$TIMESTAMP.json"
else
    echo "❌ API call failed!"
fi