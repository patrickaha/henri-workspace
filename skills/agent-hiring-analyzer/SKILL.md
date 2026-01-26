---
name: agent-hiring-analyzer  
description: Analyze team chat history to identify repetitive tasks, workflow bottlenecks, and opportunities for specialized AI agents. Use when you want to understand where to invest in automation, what agent "hires" would speed up the team, or to audit weekly patterns for efficiency gains. Triggers on requests like "analyze our chats for agent opportunities", "what agents should we build", or "weekly agent hiring analysis".
---

# Agent Hiring Analyzer

Analyze your team's chat history to identify opportunities for specialized AI agents that would accelerate your work.

## Core Analysis Workflow

### 1. Gather Chat History

```bash
# Export last 7 days of messages from all channels
python scripts/export_chat_history.py --days 7 --output chat_export.json

# Or specific channels
python scripts/export_chat_history.py --channels "#general,#dev,#support" --days 7
```

### 2. Run Analysis

```bash
# Full analysis with all modules
python scripts/analyze_patterns.py chat_export.json --output analysis_report.md

# Quick analysis (patterns only, no LLM enhancement)  
python scripts/analyze_patterns.py chat_export.json --quick
```

### 3. Generate Agent Recommendations

The analyzer identifies:

- **Repetitive Tasks** - Same requests appearing multiple times
- **Tool Patterns** - Frequent use of specific tools/commands
- **Workflow Bottlenecks** - Multi-step processes that could be automated
- **Context Switches** - Jumping between different types of work
- **Time Sinks** - Long threads that could be streamlined

## Output Format

The analysis produces a structured report with:

```markdown
# Agent Hiring Recommendations
Date: 2025-01-25

## Executive Summary
- Total messages analyzed: X
- Unique participants: Y  
- Top opportunity: [Agent Name]

## Recommended Hires

### 1. [Agent Name]
**Role:** [One-line description]
**Trigger Phrases:** 
- "check the..."
- "analyze our..." 
**Expected Time Savings:** X hours/week
**Implementation Priority:** High/Medium/Low

**Evidence from chat:**
- [timestamp] User asked about X (link)
- [timestamp] Similar request for Y (link)
- Pattern appears Z times this week

**Suggested Skills:**
- skill-name-1
- skill-name-2
```

## Weekly Automation

Set up a cron job for weekly analysis:

```bash
# Add to crontab (runs Sunday 11pm)
0 23 * * 0 /path/to/analyze_weekly.sh
```

The `scripts/analyze_weekly.sh` script:
1. Exports the past week's chat
2. Runs analysis
3. Posts results to Slack
4. Archives the report

## Manual Trigger Patterns

When you spot a situation that needs an agent:

```bash
# Analyze specific thread
python scripts/analyze_thread.py --channel "#general" --thread-ts 1234567890.123456

# Analyze specific time window  
python scripts/analyze_patterns.py --start "2025-01-20" --end "2025-01-25"

# Focus on specific user's requests
python scripts/analyze_patterns.py --user "U04C7A4DE"
```

## Configuration

Edit `config.yaml` to customize:

```yaml
analysis:
  min_pattern_frequency: 3  # Minimum occurrences to flag
  similarity_threshold: 0.8  # How similar messages need to be
  
priorities:
  high_impact_keywords:
    - "every day"
    - "always have to"
    - "keeps happening"
  
exclusions:
  ignore_patterns:
    - "^/.*"  # Ignore slash commands
    - "^:.*:$"  # Ignore emoji reactions
```

## Integration with Skill Creator

When the analyzer recommends an agent, it can bootstrap creation:

```bash
# Generate skill scaffold from recommendation
python scripts/bootstrap_agent.py --recommendation analysis_report.md --agent-index 1

# This creates:
# - skills/[agent-name]/SKILL.md with trigger phrases
# - Placeholder scripts based on identified patterns
# - References to relevant chat examples
```

## Privacy & Security

- Chat exports are stored locally only
- Analysis runs on your machine (no external APIs for chat data)
- Supports redaction patterns for sensitive data
- Automatic cleanup of exports after analysis