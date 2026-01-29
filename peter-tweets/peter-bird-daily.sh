#!/bin/bash
# Peter Daily Wisdom Harvester using bird CLI
# Runs once daily, monitors cookie health, alerts on failure

set -e

echo "🐦 Peter's Daily Wisdom Harvest - $(date)"
echo "========================================="

# Configuration
BIRD_CONFIG="$HOME/.config/bird/config.json5"
OUTPUT_DIR="$HOME/clawd/peter-tweets/daily-harvest"
TODAY=$(date +%Y-%m-%d)
OUTPUT_FILE="$OUTPUT_DIR/peter-$TODAY.json"
SLACK_WEBHOOK_URL="" # Add if you want alerts

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to check bird health
check_bird_health() {
    echo "🔍 Checking bird authentication..."
    
    # Test with a known tweet
    if bird read "https://x.com/x/status/1" 2>&1 | grep -q "Tweet not found"; then
        echo "❌ Bird cookies expired or invalid!"
        
        # Send alert if webhook configured
        if [ -n "$SLACK_WEBHOOK_URL" ]; then
            curl -X POST "$SLACK_WEBHOOK_URL" \
                -H 'Content-Type: application/json' \
                -d '{"text":"🚨 Bird cookies expired! Peter tweet harvesting failed. Please refresh cookies."}'
        fi
        
        return 1
    else
        echo "✅ Bird authentication working"
        return 0
    fi
}

# Function to harvest tweets
harvest_tweets() {
    echo "📥 Fetching @steipete timeline..."
    
    # Get user timeline (last 20 tweets)
    bird timeline steipete --limit 20 --json > "$OUTPUT_FILE.tmp" 2>/dev/null || {
        echo "❌ Failed to fetch timeline"
        return 1
    }
    
    # Extract tweet count
    TWEET_COUNT=$(jq '. | length' "$OUTPUT_FILE.tmp" 2>/dev/null || echo "0")
    echo "✅ Found $TWEET_COUNT tweets"
    
    # Process tweets for wisdom
    echo "🧠 Analyzing for wisdom..."
    
    jq '[.[] | {
        id: .id,
        created_at: .created_at,
        text: .full_text // .text,
        retweet_count: .retweet_count,
        favorite_count: .favorite_count,
        is_quote: (.is_quote_status // false),
        has_media: ((.entities.media // []) | length > 0),
        url: "https://x.com/steipete/status/\(.id_str)"
    }]' "$OUTPUT_FILE.tmp" > "$OUTPUT_FILE"
    
    # Clean up temp file
    rm -f "$OUTPUT_FILE.tmp"
}

# Function to generate daily digest
generate_digest() {
    echo "📝 Generating daily digest..."
    
    DIGEST_FILE="$OUTPUT_DIR/digest-$TODAY.md"
    
    cat > "$DIGEST_FILE" << EOF
# Peter's Wisdom - $TODAY

*Harvested via bird at $(date)*

## Today's Tweets

EOF
    
    # Add tweets to digest
    jq -r '.[] | "### \(.created_at)\n\(.text)\n[View on X](\(.url))\n---\n"' "$OUTPUT_FILE" >> "$DIGEST_FILE"
    
    echo "✅ Digest saved to: $DIGEST_FILE"
}

# Main execution
main() {
    # Check if bird is healthy
    if ! check_bird_health; then
        echo "⚠️ Switching to fallback mode..."
        # Could implement firecrawl or browser fallback here
        exit 1
    fi
    
    # Harvest tweets
    if harvest_tweets; then
        generate_digest
        
        echo ""
        echo "✅ Daily harvest complete!"
        echo "📁 Output: $OUTPUT_FILE"
        echo "📄 Digest: $OUTPUT_DIR/digest-$TODAY.md"
        
        # Optional: trigger python analysis with Grok
        if [ -f "$HOME/clawd/.env" ]; then
            source "$HOME/clawd/.env"
            if [ -n "$XAI_API_KEY" ]; then
                echo ""
                echo "🤖 Running Grok analysis..."
                # python analyze_with_grok.py "$OUTPUT_FILE"
            fi
        fi
    else
        echo "❌ Harvest failed!"
        exit 1
    fi
}

# Run it
main