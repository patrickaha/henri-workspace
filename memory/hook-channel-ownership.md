# Memory: Hook Channel Ownership

## Pattern
**Hooks live with their channel.**

- #new_skills → #new_skills Cron canvas
- #pseo → #pseo Cron canvas
- #webinars → #webinars Cron canvas
- etc.

## Workflow
1. **Create hook** → If active, add to ✅ Active Hooks section
2. **Disable hook** → Move to ⏸️ Paused section
3. **Each channel owns its hooks** — clean ownership model

## Canvas Structure (per channel)
```markdown
# 🕐 Cron Jobs

## ✅ Active Hooks
[Active hooks in standard format]

## ⏸️ Paused
[Previously active hooks]
```

## When Creating New Hooks
- Add active hooks directly to the channel's Cron canvas
- Use consistent hook format (name, schedule, command, output, description)
- Move to Paused when disabled, not delete
