# Memory: clawdhub-scan-daily Hook

**Channel:** #new_skills (C0A9FM5ADE0)  
**Canvas ID:** F0A98M82E5T  
**Created:** 2026-01-19

## Hook Specification

| Field | Value |
|-------|-------|
| **Name** | clawdhub-scan-daily |
| **Description** | Daily skill intelligence: discover new clawdhub skills that align with current context and projects |
| **Schedule** | Daily at 09:00 UTC |
| **Output Channel** | #new_skills |
| **Documentation Link** | `/Users/arthelper/.clawdbot/skills/clawdhub-scan/SKILL.md` |

## Scoring Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Current project alignment | +30 | Solves active project need |
| Memory match | +25 | Aligns with past preferences/requests |
| Domain relevance | +20 | In area of current work |
| Gap filler | +15 | Fills capability gap |
| Overlap penalty | -20 | Duplicates enabled skill |
| Low relevance | -10 | Outside current scope |

## Context Sources

1. `~/clawd/AGENTS.md` — enabled skills, current projects, team focus
2. `~/clawd/memory/*.md` — past skill requests, rejected ideas, preferences
3. `~/clawd/SOUL.md` — core values, working style
4. `~/clawd/IDENTITY.md` — identity and purpose

## Usage

```bash
clawdhub-scan scan          # Full scan + suggestions (default)
clawdhub-scan recent        # Show recently uploaded skills
clawdhub-scan suggest       # Just suggestions based on context

# Flags
--days N          # Look back N days (default: 7)
--format json|text # Output format (default: text)
--min-score N     # Minimum relevance score (default: 0)
```
