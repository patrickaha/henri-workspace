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

---

*Add other critical memories below this line*