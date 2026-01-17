---
name: pseo-watchdog
description: Monitor pSEO page indexing and traffic. Track new pages from sitemap, alert on indexing delays, traffic issues, and ranking drops.
metadata: {"clawdbot":{"emoji":"🐕","requires":{"bins":["python3"]}}}
---

# pSEO Watchdog

Monitor pSEO page health: indexing status, traffic arrival, and ranking changes.

## Setup

1. **Configure site** in `.env`:
   ```
   PSEOSITE=sc-domain:arthelper.ai
   ```
2. **Set notification preferences** (Slack webhook or stdout)

## Commands

### Daily Health Check
```bash
python scripts/watchdog.py status
```

### Indexing Report
```bash
python scripts/watchdog.py index-report --days 30
```

### Traffic Timeline (when did pages start getting traffic?)
```bash
python scripts/watchdog.py traffic-timeline --days 30
```

### Ranking Drops Alert
```bash
python scripts/watchdog.py drops --days 7 --threshold 5
```

### Full Report
```bash
python scripts/watchdog.py full-report
```

## Output Format

Default: Table with columns:
- `page` - Page URL
- `status` - indexed | pending | stalled
- `first_seen` - Date first appeared in GSC
- `clicks` - Total clicks
- `position` - Avg ranking
- `days_to_index` - Days from sitemap to GSC
- `alert` - Warning flag if any

## Alerts Triggered

| Condition | Alert |
|-----------|-------|
| Page not indexed after 7 days | 🔴 stalled |
| Page has 0 clicks after 14 days | 🟡 no_traffic |
| Position dropped >5 spots | 📉 drop |
| New page indexed today | 🆕 just_indexed |

## Cron Examples

```bash
# Daily health check at 9am
0 9 * * * cd /Users/arthelper/clawd/skills/pseo-watchdog && python scripts/watchdog.py status
```

## Data Source

Uses GSC API via shared `gsc` skill credentials.
