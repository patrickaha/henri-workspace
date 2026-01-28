# MEMORY.md - Persistent Context

## Browser Protocol (2026-01-25)
**Critical rule from Patrick:** We have ONE persistent browser that must NEVER be closed.

- **Profile:** `clawd` (isolated Clawdbot browser)
- **Current PID:** 30628
- **User data:** `/Users/arthelper/.clawdbot/browser/clawd/user-data`
- **Extension:** Clawdbot Browser Relay is installed
- **Logins:** Preserved across sessions

### The Rules
1. **Always use this browser** - no exceptions
2. **Never close it** - it's our dedicated workhorse
3. **No auto-restart cron** - manual only if absolutely needed
4. **Check before starting:** `browser status --profile=clawd`

Patrick killed all other Chrome instances on 2026-01-25. This is now our single source of truth for browser automation. The browser contains logged-in sessions that must be preserved.

## Channel Factory Allowlist Fix (2026-01-27)
**Critical bug discovered:** New channels created via factory weren't responding because they weren't in the Slack allowlist.

### The Problem
- Slack config has `groupPolicy: "allowlist"`
- Channel factory creates channel but doesn't add to config
- Henri can't see messages in new channels (even with @mentions)

### The Fix
After creating ANY channel, must patch the config:
```bash
clawdbot gateway config.patch '{
  "channels": {
    "slack": {
      "channels": {
        "CHANNEL_ID": {
          "enabled": true,
          "requireMention": false
        }
      }
    }
  }
}'
```

**Patrick's directive:** "Commit this to your memory" - this is now part of the standard channel creation flow.

## GA4 Analytics Setup (2026-01-27)
**Successfully configured Google Analytics 4 API access** after OAuth account confusion.

### Key Facts
- **GA4 Property:** 472129308 (owned by patrick@arthelper.ai)
- **OAuth Client:** Owned by patrick@artstorefronts.com
- **Active Account:** patrick@arthelper.ai has the refresh token
- **Config:** All credentials in `/Users/arthelper/clawd/.env`

### Critical Learning
OAuth clients can be used by any Google account - the client owner (artstorefronts) doesn't need to match the GA4 property owner (arthelper). We initially authenticated with the wrong account and got 403 errors.

### Quick Test
```bash
cd /Users/arthelper/clawd/skills/ga4
python3 scripts/ga4_query.py --metric screenPageViews --dimension pagePath --limit 5
```

Full details in: `memory/ga4-setup-2026-01-27.md`

---

*Add other critical memories below this line*