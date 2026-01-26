# todo - Vault Todo Management

Manage todos in the Obsidian vault.

## Trigger
When user says: "add todo", "todo list", "check off", "what's on my list"

## Available Lists

| Shortname | Path |
|-----------|------|
| `dashboard` | `00-dashboard/TODO.md` |
| `pseo` | `05-channels/pseo/TODO.md` |
| `webinars` | `05-channels/webinars/TODO.md` |
| `lennys` | `05-channels/lennys-podcast/TODO.md` |
| `factory` | `05-channels/channel-factory/TODO.md` |

## Vault Path
`/Users/arthelper/Library/Mobile Documents/com~apple~CloudDocs/Master Context Henri/`

## Actions

### Add Task
1. If list not specified, ask which list
2. Format: `- [ ] **[P1]** Task description @added-by:{user}`
3. Insert after `## Active` line
4. Confirm: "Added to {list}: {task} [P{n}]"

### List Tasks
1. Read the TODO.md
2. Show Active section items

### Complete Task
1. Find task in Active
2. Change `- [ ]` to `- [x]`
3. Move to Completed section with date: `✓ YYYY-MM-DD`

### Delete Task
1. Confirm which task
2. Remove the line

## Priority Levels
- **P0**: Urgent - drop everything
- **P1**: This week (default)
- **P2**: This month  
- **P3**: Someday/backlog

## Example Interactions

User: "add fix the gif posting to dashboard"
Henri: Added to dashboard: "Fix the gif posting" [P1]

User: "what's on the pseo list?"
Henri: *shows pseo TODO active items*

User: "mark manychat webhook done on dashboard"
Henri: Completed: "ManyChat → Slack webhook" ✓ 2026-01-17
