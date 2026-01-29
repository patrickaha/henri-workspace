# Peter Tweets - Quick Start Guide

## Current Status

### API Keys
- ✅ **X.AI API Key**: Saved and working (for Grok analysis)
- 🟡 **Twitter Bearer Token**: Valid but needs billing enabled

## Option A: Bird-Based Daily Harvester (Ready Now!)

```bash
# Refresh bird cookies first
cd ~/.config/bird
# Login to X.com manually, export cookies

# Run daily harvest
cd ~/clawd/peter-tweets
./peter-bird-daily.sh

# Add to cron for daily runs
crontab -e
# Add: 0 9 * * * /Users/arthelper/clawd/peter-tweets/peter-bird-daily.sh
```

**Features:**
- ✅ Cookie health monitoring
- ✅ Auto-alerts when cookies expire
- ✅ Daily digest generation
- ✅ JSON export for further processing

## Option B: Full Python Solution (After Twitter billing)

```bash
# Once billing is enabled:
cd ~/clawd/peter-tweets
source venv/bin/activate

# Start 5 parallel agents
peter-tweets monitor

# Or just daily wisdom
peter-tweets wisdom --period today
```

## Option C: Hybrid with Grok Analysis

```python
# Enhance any tweets with Grok after fetching:
from xai_analyzer import analyze_wisdom

tweets = load_bird_harvest()
for tweet in tweets:
    wisdom_score = analyze_wisdom(tweet['text'])
    tweet['grok_wisdom'] = wisdom_score
```

## Daily Workflow

1. **Morning**: Run harvest (bird or API)
2. **Process**: Score with Grok API
3. **Output**: Daily digest with top wisdom
4. **Monitor**: Check cookie/API health

## Next Steps

1. **Immediate**: Use bird-based daily harvest
2. **This week**: Enable Twitter API billing
3. **Future**: Full parallel agent system

---

*Start with: `./peter-bird-daily.sh`*