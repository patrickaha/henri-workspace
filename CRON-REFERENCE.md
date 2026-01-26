# Cron API Reference (for Henri)

## CORRECT Schema

### Main Session (wake heartbeat)
```json
{
  "sessionTarget": "main",
  "schedule": {
    "kind": "at",
    "atMs": 1737912000000
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Reminder: do the thing"
  },
  "wakeMode": "now",
  "deleteAfterRun": true
}
```

### Isolated Job (dedicated turn)
```json
{
  "sessionTarget": "isolated",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "America/Los_Angeles"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Summarize inbox",
    "deliver": true
  }
}
```

## Schedule Types

| kind | Required Fields |
|------|-----------------|
| `at` | `atMs` (epoch ms) |
| `every` | `everyMs` |
| `cron` | `expr`, optionally `tz` |

## WRONG (do not use)
- `schedule: "0 9 * * *"` ❌ (must be object with kind)
- `text: "..."` at root ❌ (must be in payload)
- `active: true` ❌ (not a valid field)
- `cron: "..."` at root ❌ (must be schedule.expr)

## CLI (preferred)
```bash
clawdbot cron add \
  --name "My reminder" \
  --at "20m" \
  --session main \
  --system-event "Do the thing" \
  --wake now \
  --delete-after-run
```
