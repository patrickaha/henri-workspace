# Channel Folder Philosophy

## The Golden Rule: No Empty Folders

**Folders exist to organize files, not to sit empty.**

## How It Works

### Creating New Channels
When you create a channel, start with ONLY:
- `CONTEXT.md`
- `TODO.md`
- `HOOKS.md`
- `SHIPPED.md`

That's it. No subfolders.

### Adding Content
When you save a file, THEN create its folder:

```bash
# WRONG - Creating empty folders
mkdir research reports exports docs

# RIGHT - Create folder when saving file
mkdir research
mv competitor-analysis.md research/
```

## In Practice

### Henri's Behavior
When I save files:
1. Check if the target folder exists
2. If not, create it
3. Then save the file

```python
# Example: Saving a report
folder = "reports"
if not exists(folder):
    create_folder(folder)
save_file("monthly-analysis.md", folder)
```

### The 8 Standard Folders (when needed)
- `research/` - Only when you have research
- `reports/` - Only when you have reports
- `exports/` - Only when you have data exports
- `assets/` - Only when you have images/media
- `docs/` - Only when you have documentation
- `templates/` - Only when you have templates
- `archive/` - Only when archiving old content
- `_working/` - Only for temporary work

## Benefits
1. **Clean channels** - See only what exists
2. **Self-documenting** - Presence of folder = content inside
3. **No confusion** - Empty folders make people wonder what's missing
4. **Faster navigation** - Less clutter to click through

## Template Update

The _TEMPLATE folder should contain:
- The 4 core files
- A README explaining this philosophy
- NO empty subfolders

## Migration Approach

When organizing existing channels:
1. Scan for files that need organizing
2. Create folders ONLY for categories that have files
3. Move files
4. Report what happened

This way, each channel has exactly the folders it needs - no more, no less.