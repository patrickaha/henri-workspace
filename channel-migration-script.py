#!/usr/bin/env python3
"""
Channel Folder Structure Migration
Only creates folders when there are files to put in them
"""

import os
import shutil
from pathlib import Path

# Folder rules - which files go where
FOLDER_RULES = {
    'research': [
        '*-analysis.md', '*-research.md', '*-study.md', 
        '*-competitor*.md', '*-market*.md', '*-landscape*.md',
        '*origin-story*', '*founder-profile*', '*growth-analysis*',
        '*product-deep-dive*', '*community-sentiment*', '*financials*',
        '*competitive-analysis*', '*citation-strategy*', '*framework*'
    ],
    'reports': [
        '*-report.md', '*-report.txt', '*-complete-report.md',
        '*-summary.md', '*-dashboard.md', '*-FINAL.txt',
        '*links-inventory*'
    ],
    'exports': [
        '*.csv', '*.tsv', '*.json', '*.xlsx', '*.xls'
    ],
    'assets': [
        '*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.webp',
        '*.mp4', '*.mov', '*.pdf'
    ],
    'docs': [
        'README.md', '*-guide.md', '*-instructions.md', 
        '*-setup*.md', '*-Tools.md', '*-how-to*.md'
    ],
    'templates': [
        '*-template.*', 'template-*.*'
    ]
}

# Core files that stay in root
CORE_FILES = ['CONTEXT.md', 'TODO.md', 'HOOKS.md', 'SHIPPED.md']

def should_move_file(filename, patterns):
    """Check if file matches any pattern"""
    from fnmatch import fnmatch
    return any(fnmatch(filename, pattern) for pattern in patterns)

def migrate_channel(channel_path):
    """Migrate a single channel to new structure"""
    channel_name = os.path.basename(channel_path)
    print(f"\n📁 Processing {channel_name}")
    
    moves_made = {}
    
    # Scan files in root
    for item in os.listdir(channel_path):
        item_path = os.path.join(channel_path, item)
        
        # Skip if it's a directory or core file
        if os.path.isdir(item_path) or item in CORE_FILES:
            continue
            
        # Check each folder rule
        for folder, patterns in FOLDER_RULES.items():
            if should_move_file(item, patterns):
                # Create folder only when we have something to put in it
                folder_path = os.path.join(channel_path, folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print(f"  ✅ Created {folder}/ (for {item})")
                
                # Move the file
                dest_path = os.path.join(folder_path, item)
                shutil.move(item_path, dest_path)
                
                if folder not in moves_made:
                    moves_made[folder] = []
                moves_made[folder].append(item)
                print(f"  → Moved {item} to {folder}/")
                break
    
    # Report
    if moves_made:
        print(f"  📊 Summary: Organized {sum(len(v) for v in moves_made.values())} files")
    else:
        print(f"  ✨ Already organized!")
    
    return moves_made

def audit_nonstandard_folders(channel_path):
    """Find any non-standard folders"""
    standard_folders = set(FOLDER_RULES.keys()) | {'_working', 'archive'}
    
    existing_folders = [
        d for d in os.listdir(channel_path) 
        if os.path.isdir(os.path.join(channel_path, d))
    ]
    
    nonstandard = [f for f in existing_folders if f not in standard_folders]
    
    if nonstandard:
        print(f"  ⚠️  Non-standard folders: {', '.join(nonstandard)}")
    
    return nonstandard

def main():
    vault_channels = "/Users/arthelper/Library/Mobile Documents/com~apple~CloudDocs/Master Context Henri/05-channels"
    
    print("🚀 Channel Folder Migration")
    print("Philosophy: Only create folders when there are files to put in them\n")
    
    # Get all channel folders
    channels = [
        d for d in os.listdir(vault_channels)
        if os.path.isdir(os.path.join(vault_channels, d)) 
        and not d.startswith('_')
    ]
    
    print(f"Found {len(channels)} channels to process")
    
    for channel in sorted(channels):
        channel_path = os.path.join(vault_channels, channel)
        migrate_channel(channel_path)
        audit_nonstandard_folders(channel_path)
    
    print("\n✅ Migration complete!")
    print("\n📝 Remember: Never create empty folders. Create them only when saving files.")

if __name__ == "__main__":
    main()