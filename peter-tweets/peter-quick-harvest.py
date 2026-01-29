#!/usr/bin/env python3
"""Quick harvest script using the working Twitter search API"""

import os
import json
import httpx
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(Path.home() / "clawd" / ".env")

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
xai_api_key = os.getenv("XAI_API_KEY")

def fetch_peter_tweets():
    """Fetch recent tweets from Peter using search API"""
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = httpx.get(
        "https://api.twitter.com/2/tweets/search/recent",
        headers=headers,
        params={
            "query": "from:steipete -is:retweet",
            "max_results": 20,
            "tweet.fields": "created_at,public_metrics,entities",
            "expansions": "referenced_tweets.id"
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []
        
    data = response.json()
    return data.get("data", [])

def analyze_with_grok(text):
    """Use Grok to analyze tweet wisdom"""
    if not xai_api_key:
        return {"wisdom_score": 5, "insights": "No Grok API key"}
        
    headers = {
        "Authorization": f"Bearer {xai_api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Analyze this tweet from Peter Steinberger (creator of Clawdbot) for wisdom and insights.
Rate 1-10 for: wisdom level, architectural insights, practical value.

Tweet: {text}

Respond with JSON: {{{{"wisdom_score": N, "category": "...", "key_insight": "..."}}}}"""
    
    try:
        response = httpx.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json={
                "model": "grok-4-fast-reasoning",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            # Try to parse JSON from response
            try:
                return json.loads(content)
            except:
                return {"wisdom_score": 5, "insights": content[:100]}
        else:
            return {"wisdom_score": 5, "error": f"Grok API error: {response.status_code}"}
            
    except Exception as e:
        return {"wisdom_score": 5, "error": str(e)}

def main():
    print("🐦 Peter's Daily Wisdom Harvest")
    print("=" * 50)
    
    # Create output directory
    output_dir = Path.home() / "clawd" / "peter-tweets" / "daily-harvest"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Fetch tweets
    tweets = fetch_peter_tweets()
    print(f"✅ Found {len(tweets)} recent tweets")
    
    if not tweets:
        print("No tweets found!")
        return
        
    # Process tweets
    enhanced_tweets = []
    high_wisdom = []
    
    print("\n🧠 Analyzing with Grok...")
    for i, tweet in enumerate(tweets):
        print(f"  Processing {i+1}/{len(tweets)}...", end="\r")
        
        # Get basic info
        result = {
            "id": tweet["id"],
            "created_at": tweet.get("created_at", ""),
            "text": tweet["text"],
            "likes": tweet.get("public_metrics", {}).get("like_count", 0),
            "retweets": tweet.get("public_metrics", {}).get("retweet_count", 0),
            "url": f"https://x.com/steipete/status/{tweet['id']}"
        }
        
        # Analyze with Grok
        if xai_api_key and i < 5:  # Limit Grok calls to save API usage
            analysis = analyze_with_grok(tweet["text"])
            result.update(analysis)
            
            if analysis.get("wisdom_score", 0) >= 7:
                high_wisdom.append(result)
        else:
            result["wisdom_score"] = 5  # Default score
            
        enhanced_tweets.append(result)
    
    print(f"\n✅ Analysis complete! Found {len(high_wisdom)} high-wisdom tweets")
    
    # Save results
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Save JSON
    json_path = output_dir / f"peter-{today}.json"
    with open(json_path, "w") as f:
        json.dump({
            "harvested_at": datetime.now().isoformat(),
            "tweet_count": len(tweets),
            "high_wisdom_count": len(high_wisdom),
            "tweets": enhanced_tweets
        }, f, indent=2)
    
    # Generate markdown digest
    md_path = output_dir / f"digest-{today}.md"
    with open(md_path, "w") as f:
        f.write(f"# Peter's Wisdom - {today}\n\n")
        f.write(f"*Harvested {len(tweets)} tweets*\n\n")
        
        if high_wisdom:
            f.write("## 🔥 High Wisdom Tweets\n\n")
            for tweet in high_wisdom:
                f.write(f"### Score: {tweet.get('wisdom_score', '?')}/10\n")
                f.write(f"*{tweet['created_at']}*\n\n")
                f.write(f"{tweet['text']}\n\n")
                if tweet.get('key_insight'):
                    f.write(f"**Insight:** {tweet['key_insight']}\n\n")
                f.write(f"[View on X]({tweet['url']})\n\n")
                f.write("---\n\n")
                
        f.write("\n## All Recent Tweets\n\n")
        for tweet in enhanced_tweets[:10]:
            f.write(f"### {tweet['created_at']}\n")
            f.write(f"{tweet['text'][:200]}...\n")
            f.write(f"Likes: {tweet['likes']} | ")
            f.write(f"[View]({tweet['url']})\n\n")
    
    print(f"\n📁 Results saved:")
    print(f"  JSON: {json_path}")
    print(f"  Digest: {md_path}")
    
    # Show top wisdom
    if high_wisdom:
        print(f"\n🔥 Today's top wisdom:")
        print(f"   {high_wisdom[0]['text'][:100]}...")

if __name__ == "__main__":
    main()