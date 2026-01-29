# Firecrawl Skill + CLI for Agents - January 27, 2026

**Source:** https://x.com/firecrawl/status/2016194162933293563  
**Announcement:** New skill/CLI specifically for AI agents

## What They Announced

Firecrawl released a skill + CLI package designed for:
- Claude Code
- Codex  
- OpenCode
- Other AI agents

**Key Features:**
- Pulls web content to local files
- Bash-powered search
- Optimized for token efficiency
- Easy install: `npx skills add firecrawl/cli`

## Current Status at Art Storefronts

- ✅ Firecrawl CLI installed at `/Users/arthelper/bin/firecrawl`
- ❌ No API key configured (`FIRECRAWL_API_KEY` missing)
- ❌ Not using the new skill package

## Why This Matters

1. **Better Web Scraping** - More efficient than browser automation
2. **Token Optimization** - Pulls only needed content
3. **Local Storage** - Content saved for reuse
4. **Agent-Specific** - Built for our exact use case

## Comparison to Current Methods

**Current:**
- Browser automation (slow)
- web_fetch (limited)
- Manual copy/paste

**With Firecrawl Skill:**
- Direct API access
- Structured data extraction
- Cached content
- Search across scraped data

## Action Items

1. Get Firecrawl API key
2. Install the new skill: `npx skills add firecrawl/cli`
3. Configure environment: `export FIRECRAWL_API_KEY=your_key`
4. Test on real scraping tasks

## Use Cases for Art Storefronts

- Competitor monitoring
- Content research
- Market analysis
- Documentation scraping
- News monitoring

## Installation Commands

```bash
# Install the skill
npx skills add firecrawl/cli

# Set API key
echo 'FIRECRAWL_API_KEY=your_key_here' >> ~/clawd/.env

# Test
firecrawl scrape https://example.com --format markdown
```