# 🍪 X.com Cookie Quick Reference

## When You're Ready:
```bash
# Just run this when logged into x.com:
~/.clawdbot/skills/henri-admin/scripts/grab-fresh-cookies.sh
```

## What Happened:
- Cookies from Jan 16 expired (ct0 token rotated)
- Built full automation for daily checks
- 9am cron will alert if cookies fail

## Cookie Locations:
- `~/.config/bird/credentials` - Shell format
- `~/.config/bird/config.json5` - JSON format

## Test Anytime:
```bash
bird whoami  # Should show @ArthelperAi
```

Delete this file after you've refreshed the cookies.