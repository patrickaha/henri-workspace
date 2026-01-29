# Peter Tweets - Parallel Agent Twitter Wisdom Harvester

Harvest @steipete's Twitter wisdom using Peter's own parallel agent architecture.

## Architecture

5 Parallel Agents running simultaneously:
1. **Timeline Monitor** - Polls @steipete every 15 minutes
2. **Reply Harvester** - Fetches replies and conversations
3. **Content Analyzer** - Scores wisdom (1-10), extracts tools
4. **Digest Builder** - Creates daily/weekly summaries
5. **Knowledge Extractor** - Builds permanent knowledge base

## Quick Start

```bash
# 1. Set up environment
cd ~/clawd/peter-tweets
python3 -m venv venv
source venv/bin/activate

# 2. Install
pip install -e .

# 3. Add Twitter API key to ~/clawd/.env
echo "TWITTER_BEARER_TOKEN=your-key-here" >> ~/clawd/.env

# 4. Run parallel monitor
peter-tweets monitor

# 5. Check latest tweets
peter-tweets latest

# 6. Get today's wisdom
peter-tweets wisdom --period today
```

## Commands

```bash
# Start parallel monitoring (Peter-style)
peter-tweets monitor --agents 5

# Get latest tweets
peter-tweets latest --limit 20 --wisdom-only

# Extract wisdom insights
peter-tweets wisdom --period today --export ~/peter-wisdom.md
peter-tweets wisdom --period week

# Search tweet history
peter-tweets search "parallel agents"

# Check system health
peter-tweets health

# Run self-tests (close the loop)
peter-tweets test --full

# Visual orchestration demo
peter-tweets orchestrate
```

## Parallel Agent Status

When running `peter-tweets monitor`, you'll see:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      Agent Orchestra Status         ┃
┣━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┫
┃ Agent              ┃ Status ┃ Tasks ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ Timeline Monitor   │ running│ 42    │
│ Reply Harvester    │ running│ 156   │
│ Content Analyzer   │ running│ 198   │
│ Digest Builder     │ waiting│ 2     │
│ Knowledge Extractor│ running│ 87    │
└────────────────────┴────────┴───────┘
```

## Configuration

Settings in `~/clawd/peter-tweets/config.json`:
```json
{
  "target_user": "steipete",
  "num_agents": 5,
  "poll_interval_minutes": 15,
  "wisdom_threshold": 7
}
```

## Peter's Patterns Implemented

✅ **CLI-First** - Everything is a command
✅ **Parallel Agents** - 5 concurrent workers
✅ **Self-Healing** - Auto-retry, rate limit handling
✅ **Close the Loop** - Self-testing built in
✅ **Local Storage** - SQLite for simplicity
✅ **No Waiting** - Agents work independently

## Database Schema

```sql
tweets:         id, text, created_at, wisdom_score, tools_mentioned
knowledge:      tweet_id, pattern, category, confidence  
digests:        period, content, tweet_count, created_at
```

## Example Wisdom Score Calculation

- Base score: 5
- +1 for each wisdom keyword
- +1 for length > 200 chars
- +2 for "parallel" + "agent"
- +2 for "close the loop"
- Max score: 10

## Scheduled Digests

Add to crontab:
```bash
# Daily digest at 8 PM
0 20 * * * /usr/local/bin/peter-tweets wisdom --period today --export ~/peter-daily-$(date +\%Y-\%m-\%d).md

# Weekly digest on Sundays
0 18 * * 0 /usr/local/bin/peter-tweets wisdom --period week --export ~/peter-weekly-$(date +\%Y-\%m-\%d).md
```

## Architecture Inspiration

Following Peter's quote:
> "I have like five or 10 agents that all work on things and I switch from this one part to this other part... It's like Starcraft."

This tool implements exactly that - 5 agents working in parallel, orchestrated like a real-time strategy game.

---

Built by Henri, following Peter's principles 📷