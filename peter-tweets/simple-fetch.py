import urllib.request
import json
import os
from datetime import datetime, timedelta

# Get token
token = None
with open(os.path.expanduser("~/clawd/.env")) as f:
    for line in f:
        if line.startswith("TWITTER_BEARER_TOKEN="):
            token = line.strip().split("=", 1)[1]
            break

if not token:
    print("No token found!")
    exit(1)

# Make API request
url = "https://api.twitter.com/2/tweets/search/recent?query=from:steipete%20-is:retweet&max_results=100&tweet.fields=created_at,public_metrics,in_reply_to_user_id"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        
    tweets = data.get("data", [])
    print(f"PETER'S RECENT ACTIVITY: {len(tweets)} items found\n")
    
    # Separate tweets and replies
    regular = [t for t in tweets if not t.get("in_reply_to_user_id")]
    replies = [t for t in tweets if t.get("in_reply_to_user_id")]
    
    print(f"📝 REGULAR TWEETS ({len(regular)}):")
    print("=" * 80)
    for t in regular[:5]:
        print(f"\nTime: {t['created_at']}")
        print(f"Text: {t['text']}")
        print(f"Stats: ❤️ {t.get('public_metrics', {}).get('like_count', 0)} likes, "
              f"🔁 {t.get('public_metrics', {}).get('retweet_count', 0)} retweets")
        print(f"Link: https://x.com/steipete/status/{t['id']}")
        print("-" * 80)
    
    if len(regular) > 5:
        print(f"\n... and {len(regular) - 5} more tweets")
    
    print(f"\n\n💬 REPLIES ({len(replies)}):")
    print("=" * 80)
    for r in replies[:5]:
        print(f"\nTime: {r['created_at']}")
        print(f"Reply: {r['text'][:200]}...")
        print(f"Link: https://x.com/steipete/status/{r['id']}")
        print("-" * 80)
    
    if len(replies) > 5:
        print(f"\n... and {len(replies) - 5} more replies")
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_dir = os.path.expanduser("~/clawd/peter-tweets/daily-harvest")
    os.makedirs(report_dir, exist_ok=True)
    
    report_file = os.path.join(report_dir, f"peter-report-{timestamp}.txt")
    with open(report_file, "w") as f:
        f.write(f"PETER STEINBERGER - TWITTER ACTIVITY REPORT\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Total: {len(tweets)} items ({len(regular)} tweets, {len(replies)} replies)\n\n")
        
        f.write("TWEETS:\n")
        for t in regular:
            f.write(f"\n{t['created_at']}\n{t['text']}\n")
            f.write(f"https://x.com/steipete/status/{t['id']}\n")
            f.write("-" * 80 + "\n")
        
        f.write("\n\nREPLIES:\n")  
        for r in replies:
            f.write(f"\n{r['created_at']}\n{r['text']}\n")
            f.write(f"https://x.com/steipete/status/{r['id']}\n")
            f.write("-" * 80 + "\n")
    
    print(f"\n\n✅ Full report saved to: {report_file}")
    
except Exception as e:
    print(f"Error: {e}")