#!/usr/bin/env python3
"""
Henri's Folder Structure Enforcement
Built into my save_file behavior
"""

ALLOWED_FOLDERS = [
    'research',
    'reports',
    'exports',
    'assets',
    'docs',
    'templates',
    'archive',
    '_working'
]

FILE_RULES = {
    'research': ['.md files with analysis, study, research, competitor, market, landscape, framework, strategy'],
    'reports': ['.md/.txt files with report, summary, dashboard, results, findings'],
    'exports': ['.csv, .tsv, .json, .xlsx files - any data exports'],
    'assets': ['.png, .jpg, .gif, .mp4, .pdf, .svg - any media/visual files'],
    'docs': ['README.md, guides, instructions, setup docs, how-tos'],
    'templates': ['Any file with template in name or meant for reuse'],
    'archive': ['Old/outdated versions of any file type'],
    '_working': ['Temporary drafts, experiments - can be deleted']
}

def determine_folder(filename):
    """Determine correct folder for a file"""
    
    # Check by extension first
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    # Data exports
    if ext in ['csv', 'tsv', 'json', 'xlsx', 'xls']:
        return 'exports'
    
    # Media/assets
    if ext in ['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'mp4', 'mov', 'avi', 'pdf']:
        return 'assets'
    
    # Check filename patterns
    fname_lower = filename.lower()
    
    # Research patterns
    if any(word in fname_lower for word in ['analysis', 'research', 'study', 'competitor', 'market', 'landscape', 'framework', 'strategy', 'competitive']):
        return 'research'
    
    # Report patterns
    if any(word in fname_lower for word in ['report', 'summary', 'dashboard', 'results', 'findings', '-final']):
        return 'reports'
    
    # Documentation patterns
    if fname_lower in ['readme.md'] or any(word in fname_lower for word in ['guide', 'instructions', 'setup', 'how-to']):
        return 'docs'
    
    # Template patterns
    if 'template' in fname_lower:
        return 'templates'
    
    # Default for .md files
    if ext == 'md':
        return 'docs'
    
    # When in doubt
    raise ValueError(f"Cannot determine folder for '{filename}'. Please specify.")

def save_file(filename, content, channel_path):
    """Henri's file saving logic with folder enforcement"""
    import os
    
    # Skip core files that stay in root
    if filename in ['CONTEXT.md', 'TODO.md', 'HOOKS.md', 'SHIPPED.md']:
        filepath = os.path.join(channel_path, filename)
        # Save directly to root
        return filepath
    
    # Determine correct folder
    folder = determine_folder(filename)
    
    # Validate folder
    if folder not in ALLOWED_FOLDERS:
        raise ValueError(f"Invalid folder '{folder}'. Must use one of: {ALLOWED_FOLDERS}")
    
    # Create folder if needed
    folder_path = os.path.join(channel_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"✅ Created {folder}/ for {filename}")
    
    # Save file
    filepath = os.path.join(folder_path, filename)
    # Write file logic here
    print(f"💾 Saved {filename} to {folder}/")
    
    return filepath

# Example usage
if __name__ == "__main__":
    # Test file placement
    test_files = [
        "competitor-analysis.md",
        "monthly-report.md", 
        "data-export.csv",
        "screenshot.png",
        "README.md",
        "email-template.md",
        "random-file.txt"
    ]
    
    print("File Placement Test:")
    print("-" * 50)
    
    for file in test_files:
        try:
            folder = determine_folder(file)
            print(f"{file:30} → {folder}/")
        except ValueError as e:
            print(f"{file:30} → ERROR: {e}")