# Channel Folder Structure Template

## Core Files (Root Level Only)
```
channel-name_CHANNELID/
├── CONTEXT.md      # Channel purpose, scope, skills
├── TODO.md         # Active tasks
├── HOOKS.md        # Automations and triggers
└── SHIPPED.md      # Completed work log
```

## Subfolder Structure (USE ONLY THESE)
```
channel-name_CHANNELID/
├── 📁 research/         # Background research, competitor analysis, market insights
├── 📁 reports/          # Generated reports, analyses, dashboards
├── 📁 exports/          # Data exports (CSV, TSV, JSON)
├── 📁 assets/          # Images, screenshots, media files
├── 📁 docs/            # Reference documentation, guides, how-tos
├── 📁 templates/       # Reusable templates specific to this channel
├── 📁 archive/         # Old/deprecated content (move here, don't delete)
└── 📁 _working/        # Temporary work files, drafts, experiments
```

## STRICT RULES - NO EXCEPTIONS

1. **Use ONLY these 8 folder names** - No variations, no new folders
2. **Every file goes in one of these** - If unsure, ask
3. **Context files in folders are fine** - e.g., `research/CONTEXT.md` to explain that folder
4. **Create folders only as needed** - Empty folders = clutter

## Examples Applied

### Cara Channel (Restructured)
```
cara_C0AB4933858/
├── CONTEXT.md
├── TODO.md
├── HOOKS.md
├── SHIPPED.md
├── research/
│   ├── 01-origin-story.md
│   ├── 02-founder-profile.md
│   ├── 03-growth-analysis.md
│   ├── 04-product-deep-dive.md
│   ├── 05-community-sentiment.md
│   ├── 06-financials.md
│   ├── 07-competitive-analysis.md
│   └── research_anti_ai_art_platform_landscape_2026.md
├── reports/
│   ├── cara-complete-report.md
│   └── 08-links-inventory.md
└── docs/
    ├── README.md
    └── IAMAG-Tools.md
```

### AEO Channel (Restructured)
```
aeo_C0A9BSFT25D/
├── CONTEXT.md
├── TODO.md
├── HOOKS.md
├── SHIPPED.md
├── research/           # Already exists - good!
│   ├── ethan-smith-citation-strategy.md
│   ├── microsoft-aeo-geo-framework.md
│   ├── quick-wins.md
│   └── llm-audit/
├── reports/
│   ├── art-helper-aeo-sheets-report.txt
│   └── ART-HELPER-AEO-FINAL.txt
├── exports/
│   ├── art-helper-aeo-dashboard.tsv
│   ├── art-helper-aeo-report.csv
│   └── art-helper-aeo-report.tsv
└── docs/
    └── gog-setup-instructions.md
```

## Rules

1. **Root = Core 4 Only**: CONTEXT, TODO, HOOKS, SHIPPED stay in root
2. **Everything else goes in subfolders**
3. **Use consistent subfolder names** across all channels
4. **Create folders as needed** - not all channels need all folders
5. **Move, don't delete** - Use archive/ for outdated content
6. **_working/** for temporary files that can be cleaned up

## Migration Script

```bash
# Example for cara channel
cd "/path/to/cara_C0AB4933858"
mkdir -p research reports docs archive _working

# Move research files
mv 0[1-7]-*.md research_*.md research/

# Move reports
mv cara-complete-report.md 08-links-inventory.md reports/

# Move documentation
mv README.md IAMAG-Tools.md docs/
```

## Template Creation

When creating a new channel:
```bash
# Create base structure
mkdir -p "channelname_CHANNELID"/{research,reports,exports,docs,templates,archive,_working}

# Copy template files
cp _TEMPLATE/CONTEXT.md "channelname_CHANNELID/"
cp _TEMPLATE/TODO.md "channelname_CHANNELID/"
cp _TEMPLATE/HOOKS.md "channelname_CHANNELID/"
cp _TEMPLATE/SHIPPED.md "channelname_CHANNELID/"
```