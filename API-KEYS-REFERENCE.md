# API Keys Reference

## Current Keys in ~/clawd/.env

### X.AI (Grok LLM) ✅
```bash
XAI_API_KEY=xai-l6SD6D5U6JYJvW4Uvv5MppyOD0nWsY5X9oW6do496dZEfsdyzN5wd3AnI0UB5twmXG5w5o9m9DpdeFN7
```

**What it's for:**
- Access to Grok models (grok-4-fast-reasoning, etc.)
- Can analyze text, generate summaries
- NOT for accessing Twitter/X data

**How to use:**
```python
import httpx

headers = {"Authorization": f"Bearer {XAI_API_KEY}"}
response = httpx.post(
    "https://api.x.ai/v1/chat/completions",
    headers=headers,
    json={
        "model": "grok-4-fast-reasoning",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
```

### Twitter API v2 ❌ (Not yet obtained)
Would look like:
```bash
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAA...
```

**To get one:**
1. Go to https://developer.twitter.com
2. Create a project
3. Generate Bearer Token
4. Free tier: 10,000 tweet reads/month

## Other Keys We Have

Check with:
```bash
grep "API_KEY\|TOKEN" ~/clawd/.env | grep -v "^#" | cut -d= -f1
```

Current list:
- FIRECRAWL_API_KEY (web scraping)
- GOOGLE_API_KEY (various Google services)
- GA4 credentials (Analytics)
- And more...

---

*Always store keys in ~/clawd/.env - never commit to git!*