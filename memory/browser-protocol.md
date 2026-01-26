# Browser Protocol
*Established: 2026-01-25 by Patrick*

## The One Browser Rule
- **Always use** the persistent `clawd` profile browser
- **Never close it** - keeps all logins and sessions intact
- **No cron jobs** - manual restart only if needed
- **Extension ready** - Clawdbot Browser Relay installed

## Status Check
```bash
clawdbot browser status --profile=clawd
```

## Manual Start (if ever needed)
```bash
clawdbot browser start --profile=clawd
```

The browser is our dedicated workhorse. Respect it.