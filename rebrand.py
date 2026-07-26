import os
import glob

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

replacements = [
    ("Apple Bank", "Nexus Trust Bank"),
    ("AppleBank", "NexusTrustBank"),
    ("applebank", "nexustrustbank"),
    ("apple bank", "nexus trust bank"),
    ("APPLE BANK", "NEXUS TRUST BANK"),
]

# Find all HTML and PY files
search_paths = [
    'templates/**/*.html',
    'banking/templates/**/*.html',
    'banking/*.py',
    'apple_bank/settings.py',
    '.env.example'
]

files_to_process = []
for pattern in search_paths:
    files_to_process.extend(glob.glob(pattern, recursive=True))

for filepath in files_to_process:
    replace_in_file(filepath, replacements)

# Specific fix for views.py internal transfer logic
views_path = 'banking/views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = "if bank_name.lower() in ['nexus trust bank', 'nexustrustbank']:"
new_logic = "if bank_name.lower() in ['nexus trust bank', 'nexustrustbank', 'ntb', 'ntb bank']:"
if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated views.py internal transfer logic")

print("Rebranding complete.")
