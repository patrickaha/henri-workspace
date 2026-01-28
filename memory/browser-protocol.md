# Browser Protocol
*Established: 2026-01-25 by Patrick*

## The One Browser Rule
- **Always use** the persistent `clawd` profile browser
- **Never close it** - keeps all logins and sessions intact
- **No cron jobs** - manual restart only if needed
- **Extension ready** - Clawdbot Browser Relay installed

## Tab Attachment Required
Browser tools need a tab attached via the extension. If you get:
> "Chrome extension relay is running, but no tab is connected"

**Fix:** Patrick connects via Jump Desktop → clicks extension icon on any tab.

This only needs to happen:
- After browser restart
- If the attached tab was closed

Once attached, it stays connected until that tab closes.

## Status Check
```bash
clawdbot browser status --profile=clawd
```

## Manual Start (if ever needed)
```bash
clawdbot browser start --profile=clawd
```

The browser is our dedicated workhorse. Respect it.
