# TODO

## 📥 Inbox
*Raw ideas from the team. Not ready for execution.*

- Research automated pSEO content updates
- Look into Zoom webinar attendee tracking
- Maybe add Stripe webhook handler?
- GA4 anomaly detection alerts

## 🎯 Ready
*Spec'd and ready for agent execution. Launch the swarm!*

- [ ] Add health check endpoint #task-1
  - **spec**: GET /health returns { status: "ok", version: pkg.version }
  - **repo**: arthelper-api  
  - **agent**: claude-code
  - **estimate**: 30min

- [ ] Fix login redirect loop #task-2
  - **spec**: Users get stuck on /login after successful auth
  - **repo**: arthelper-web
  - **agent**: claude-code
  - **blocked-by**: #task-1
  - **context**: Check middleware order in auth.js

- [ ] Generate December analytics report #task-3
  - **spec**: Pull GA4 data, create PDF with charts
  - **data**: ga4, gsc
  - **agent**: main (data task)
  - **output**: reports/2025-12-analytics.pdf

## ⚡ Active
*Currently being executed by agents*

- [⚡] Building user dashboard #task-4
  - **session**: agent:sub:abc123
  - **started**: 2026-01-24T20:30:00Z
  - **agent**: claude-code
  - **status**: Creating React components...

## ✅ Shipped
*Completed today. Move to SHIPPED.md at EOD.*

- [x] Updated dependencies to latest *(2026-01-24 14:00)*
- [x] Fixed CORS headers on API *(2026-01-24 15:30)*

---

## Task Format

```markdown
- [ ] Task description #task-id
  - **spec**: Clear description of what success looks like
  - **repo**: repository-name (for code tasks)
  - **data**: data sources (for analytics tasks)  
  - **agent**: claude-code | codex | opencode | main
  - **blocked-by**: #task-1, #task-2 (dependencies)
  - **estimate**: 30min | 2h | 1d
  - **context**: Any helpful context or gotchas
```

## Workflow

1. **Team adds to Inbox** → Anyone can drop ideas
2. **Review & Refine** → Add specs, move to Ready
3. **Launch Swarm** → Henri picks Ready tasks, spawns agents
4. **Monitor Active** → Track progress via sessions
5. **Ship It** → Completed → Shipped section → SHIPPED.md at EOD

## Agent Assignment

- **claude-code**: Complex features, refactors
- **codex**: Quick fixes, well-defined tasks
- **opencode**: Experimental/creative work
- **main**: Data analysis, reports, non-code tasks