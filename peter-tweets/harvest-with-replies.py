#!/usr/bin/env python3
"""Harvest Peter's tweets AND replies from the last 24 hours"""

import os
import json
import httpx
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(Path.home() / "clawd" / ".env")

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
xai_api_key = os.getenv("XAI_API_KEY")

def fetch_peter_tweets_and_replies():
    """Fetch tweets AND replies from Peter"""
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    # Query includes replies, excludes only retweets
    response = httpx.get(
        "https://api.twitter.com/2/tweets/search/recent",
        headers=headers,
        params={
            "query": "from:steipete -is:retweet",  # This INCLUDES replies
            "max_results": 100,  # Max allowed
            "tweet.fields": "created_at,public_metrics,entities,referenced_tweets,in_reply_to_user_id,conversation_id",
            "expansions": "referenced_tweets.id,in_reply_to_user_id",
            "user.fields": "username"
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []
        
    data = response.json()
    tweets = data.get("data", [])
    
    # Filter for last 24 hours
    cutoff_time = datetime.now(datetime.UTC) - timedelta(hours=24)
    recent_tweets = []
    
    for tweet in tweets:
        # Parse tweet time
        created_at = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
        if created_at > cutoff_time:
            recent_tweets.append(tweet)
            
    return recent_tweets, data.get("includes", {})

def categorize_tweets(tweets, includes):
    """Categorize tweets into regular tweets and replies"""
    regular_tweets = []
    replies = []
    
    for tweet in tweets:
        # Check if it's a reply
        if tweet.get("in_reply_to_user_id") or tweet.get("referenced_tweets"):
            # It's a reply or quote tweet
            tweet["type"] = "reply"
            replies.append(tweet)
        else:
            # Regular tweet
            tweet["type"] = "tweet"
            regular_tweets.append(tweet)
            
    return regular_tweets, replies

def format_tweet_display(tweet):
    """Format tweet for display"""
    created_at = tweet.get("created_at", "")
    tweet_type = tweet.get("type", "tweet")
    
    # Format time nicely
    if created_at:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        time_str = dt.strftime("%Y-%m-%d %H:%M UTC")
    else:
        time_str = "Unknown time"
        
    output = [
        f"{'💬 REPLY' if tweet_type == 'reply' else '📝 TWEET'} - {time_str}",
        f"{tweet['text']}",
        f"❤️ {tweet.get('public_metrics', {}).get('like_count', 0)} likes | "
        f"🔁 {tweet.get('public_metrics', {}).get('retweet_count', 0)} retweets | "
        f"💬 {tweet.get('public_metrics', {}).get('reply_count', 0)} replies",
        f"🔗 https://x.com/steipete/status/{tweet['id']}",
        "-" * 80
    ]
    
    return "\n".join(output)

def main():
    print("🐦 Peter's 24-Hour Tweet & Reply Harvest")
    print("=" * 50)
    print(f"Time window: Last 24 hours from {datetime.now():%Y-%m-%d %H:%M}")
    print()
    
    # Fetch tweets
    tweets, includes = fetch_peter_tweets_and_replies()
    
    if not tweets:
        print("No tweets found!")
        return
        
    # Categorize
    regular_tweets, replies = categorize_tweets(tweets, includes)
    
    print(f"✅ Found {len(tweets)} total items in last 24 hours:")
    print(f"   📝 {len(regular_tweets)} regular tweets")
    print(f"   💬 {len(replies)} replies")
    print()
    
    # Create output directory
    output_dir = Path.home() / "clawd" / "peter-tweets" / "daily-harvest"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save raw data
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    json_path = output_dir / f"peter-24h-{timestamp}.json"
    
    with open(json_path, "w") as f:
        json.dump({
            "harvested_at": datetime.now().isoformat(),
            "time_window_hours": 24,
            "total_count": len(tweets),
            "tweet_count": len(regular_tweets),
            "reply_count": len(replies),
            "tweets": regular_tweets,
            "replies": replies,
            "raw_data": tweets
        }, f, indent=2)
    
    # Generate report
    report_path = output_dir / f"peter-24h-report-{timestamp}.txt"
    
    with open(report_path, "w") as f:
        f.write("PETER STEINBERGER - LAST 24 HOURS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Report generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        f.write(f"Total activity: {len(tweets)} items\n")
        f.write(f"Regular tweets: {len(regular_tweets)}\n")
        f.write(f"Replies: {len(replies)}\n\n")
        
        # Regular tweets first
        if regular_tweets:
            f.write("REGULAR TWEETS\n")
            f.write("=" * 80 + "\n\n")
            for tweet in sorted(regular_tweets, key=lambda x: x.get("created_at", ""), reverse=True):
                f.write(format_tweet_display(tweet) + "\n\n")
                
        # Then replies
        if replies:
            f.write("\nREPLIES & CONVERSATIONS\n")
            f.write("=" * 80 + "\n\n")
            for reply in sorted(replies, key=lambda x: x.get("created_at", ""), reverse=True):
                f.write(format_tweet_display(reply) + "\n\n")
    
    # Also print to console
    print("📋 REGULAR TWEETS:")
    print("-" * 80)
    for tweet in regular_tweets[:3]:  # Show first 3
        print(format_tweet_display(tweet))
        print()
        
    if len(regular_tweets) > 3:
        print(f"... and {len(regular_tweets) - 3} more regular tweets")
        print()
        
    print("\n💬 REPLIES:")
    print("-" * 80)
    for reply in replies[:3]:  # Show first 3
        print(format_tweet_display(reply))
        print()
        
    if len(replies) > 3:
        print(f"... and {len(replies) - 3} more replies")
        
    print(f"\n✅ Full report saved to:")
    print(f"   📄 Text: {report_path}")
    print(f"   📊 JSON: {json_path}")

if __name__ == "__main__":
    main()