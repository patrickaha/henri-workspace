# Folder Structure Enforcement Plan

## 1. Update _TEMPLATE (Immediate)

### _TEMPLATE/CONTEXT.md Addition
```markdown
## Folder Structure

This channel follows the standard 8-folder system:
- `research/` - Analysis, studies, competitive intel
- `reports/` - Generated reports, summaries  
- `exports/` - CSV, TSV, JSON data files
- `assets/` - Images, videos, PDFs, media
- `docs/` - Guides, instructions, READMEs
- `templates/` - Reusable templates
- `archive/` - Old content (move, don't delete)
- `_working/` - Temporary files

**Rules:**
1. Only create folders when you have files
2. No other folder names allowed
3. Files must go in correct folders
```

### _TEMPLATE/FOLDER-RULES.md (New File)
Quick reference card for folder placement rules.

## 2. Channel Factory Updates

### Update CHANNEL-FACTORY-FLOW.md
Add step: "Copy folder structure rules to new channel"

### Channel Creation Script
```bash
# When creating a channel
cp _TEMPLATE/CONTEXT.md $NEW_CHANNEL/
cp _TEMPLATE/TODO.md $NEW_CHANNEL/
cp _TEMPLATE/HOOKS.md $NEW_CHANNEL/
cp _TEMPLATE/SHIPPED.md $NEW_CHANNEL/
cp _TEMPLATE/FOLDER-RULES.md $NEW_CHANNEL/docs/  # First file creates docs/
```

## 3. Henri's Behavior (My Internal Rules)

### Before Saving ANY File
```python
def save_file(filename, content, channel):
    # 1. Determine correct folder
    folder = determine_folder(filename)
    
    # 2. Validate folder name
    if folder not in ALLOWED_FOLDERS:
        raise Error(f"Invalid folder. Must use one of: {ALLOWED_FOLDERS}")
    
    # 3. Create if needed
    if not exists(folder):
        create_folder(folder)
    
    # 4. Save
    save(f"{channel}/{folder}/{filename}", content)
```

### Weekly Audit
Every Monday morning, run folder audit on all channels:
- Flag non-standard folders
- Report empty folders
- Suggest file movements

## 4. Every CONTEXT.md Gets Updated

Add this section to ALL existing channel CONTEXT.md files:
```markdown
## Folder Structure

[Same as template above]
```

## 5. Central Documentation

### Update These Files
1. `04-resources/CHANNEL-STRUCTURE.md` - Full documentation
2. `04-resources/CHANNEL-FACTORY-FLOW.md` - Add folder rules
3. `AGENTS.md` - Add folder discipline section

### Create New Reference
`04-resources/FOLDER-PLACEMENT-GUIDE.md`:
```markdown
# Quick Reference: Where Files Go

| File Type | Folder | Examples |
|-----------|--------|----------|
| Analysis, research | `research/` | competitor-analysis.md, market-study.md |
| Reports, summaries | `reports/` | monthly-report.md, executive-summary.md |
| Data exports | `exports/` | data.csv, results.json, metrics.tsv |
| Images, videos | `assets/` | screenshot.png, demo.mp4, logo.svg |
| Documentation | `docs/` | README.md, setup-guide.md |
| Templates | `templates/` | email-template.md, report-template.md |
| Old content | `archive/` | old-report-2025.md |
| Temporary | `_working/` | draft.md, test-data.csv |
```

## 6. Enforcement Mechanisms

### 1. Channel Wake Check
When I wake in a channel, check folder structure compliance.

### 2. File Save Validation
Never save to non-standard folders.

### 3. Monthly Report
Generate compliance report showing:
- Channels following structure ✅
- Channels with issues ❌
- Files in wrong places

### 4. Channel Factory Integration
Factory bot enforces structure on creation.

## 7. Migration Execution

1. Run migration script on all channels
2. Update all CONTEXT.md files with folder section
3. Update _TEMPLATE
4. Update documentation
5. Set up weekly audit cron job

## Success Metrics

- 100% channels have folder structure documented
- 0 non-standard folders after migration
- 100% new files go to correct folders
- Weekly audit shows continued compliance