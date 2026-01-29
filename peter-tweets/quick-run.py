import os
import httpx
import json
from datetime import datetime, timedelta
from pathlib import Path

# Load token
with open(Path.home() / "clawd" / ".env") as f:
    for line in f:
        if line.startswith("TWITTER_BEARER_TOKEN="):
            bearer_token = line.strip().split("=", 1)[1]
            break

# Fetch tweets
headers = {"Authorization": f"Bearer {bearer_token}"}
response = httpx.get(
    "https://api.twitter.com/2/tweets/search/recent",
    headers=headers,
    params={
        "query": "from:steipete -is:retweet",
        "max_results": 100,
        "tweet.fields": "created_at,public_metrics,in_reply_to_user_id",
    }
)

if response.status_code == 200:
    data = response.json()
    tweets = data.get("data", [])
    
    # Filter last 24h
    cutoff = datetime.now() - timedelta(hours=24)
    recent = []
    
    for t in tweets:
        created = datetime.fromisoformat(t["created_at"].replace("Z", ""))
        if created > cutoff.replace(tzinfo=None):
            recent.append(t)
    
    # Sort and display
    tweets_only = [t for t in recent if not t.get("in_reply_to_user_id")]
    replies = [t for t in recent if t.get("in_reply_to_user_id")]
    
    print(f"PETER'S LAST 24 HOURS: {len(recent)} total ({len(tweets_only)} tweets, {len(replies)} replies)\n")
    
    print("TWEETS:")
    for t in tweets_only[:5]:
        print(f"\n📝 {t['created_at']}")
        print(f"{t['text'][:200]}...")
        print(f"❤️ {t.get('public_metrics',{}).get('like_count',0)} likes")
        
    print(f"\nREPLIES:")
    for r in replies[:5]:
        print(f"\n💬 {r['created_at']}")
        print(f"{r['text'][:200]}...")
        
    # Save
    output_dir = Path.home() / "clawd" / "peter-tweets" / "daily-harvest"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    report = output_dir / f"quick-report-{datetime.now():%Y%m%d-%H%M}.txt"
    with open(report, "w") as f:
        f.write(f"PETER STEINBERGER - LAST 24 HOURS\n{'='*50}\n\n")
        f.write(f"Total: {len(recent)} items\n")
        f.write(f"Tweets: {len(tweets_only)}\n")
        f.write(f"Replies: {len(replies)}\n\n")
        
        f.write("TWEETS:\n")
        for t in tweets_only:
            f.write(f"\n{t['created_at']}\n{t['text']}\n")
            f.write(f"https://x.com/steipete/status/{t['id']}\n")
            
        f.write("\n\nREPLIES:\n")
        for r in replies:
            f.write(f"\n{r['created_at']}\n{r['text']}\n")
            f.write(f"https://x.com/steipete/status/{r['id']}\n")
    
    print(f"\n✅ Full report: {report}")
else:
    print(f"Error: {response.status_code}\n{response.text}")