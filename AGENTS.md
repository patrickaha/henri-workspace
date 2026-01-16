# AGENTS.md - Clawdbot Workspace

This folder is the assistant's working directory.

## First run (one-time)
- If BOOTSTRAP.md exists, follow its ritual and delete it once complete.
- Your agent identity lives in IDENTITY.md.
- Your profile lives in USER.md.

## Backup tip (recommended)
If you treat this workspace as the agent's "memory", make it a git repo (ideally private) so identity
and notes are backed up.

```bash
git init
git add AGENTS.md
git commit -m "Add agent workspace"
```

## Safety defaults
- Don't exfiltrate secrets or private data.
- Don't run destructive commands unless explicitly asked.
- Be concise in chat; write longer output to files in this workspace.

## Daily memory (recommended)
- Keep a short daily log at memory/YYYY-MM-DD.md (create memory/ if needed).
- On session start, read today + yesterday if present.
- Capture durable facts, preferences, and decisions; avoid secrets.

## Heartbeats (optional)
- HEARTBEAT.md can hold a tiny checklist for heartbeat runs; keep it small.

## Documentation Rule (CRITICAL)
**100% of all documentation, notes, and saved work must go to the Obsidian vault:**
- **Vault path:** `/Users/arthelper/Documents/Master Context Henri`
- **My working docs:** `/02-henri/` folder
- **Never** save documentation elsewhere without explicit permission
- **Always use the obsidian-markdown skill** when creating or editing .md files
- Use Obsidian Flavored Markdown: wikilinks `[[Note Name]]`, callouts `> [!note]`, properties `---title: X---`, tags `#tag`, and embeds `![[Note]]`

## Customize
- Add your preferred style, rules, and "memory" here.
