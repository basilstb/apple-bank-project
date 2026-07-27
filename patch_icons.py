import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    def replacer(match):
        tag = match.group(0)
        if 'translate="no"' not in tag and 'notranslate' not in tag:
            # Insert translate="no" before the closing >
            # Handle self-closing tags just in case, though spans usually aren't
            if tag.endswith('/>'):
                return tag[:-2] + ' translate="no"/>'
            else:
                return tag[:-1] + ' translate="no">'
        return tag

    # Match any opening tag containing material-symbols-outlined
    new_content = re.sub(r'<[^>]+class="[^"]*material-symbols-outlined[^"]*"[^>]*>', replacer, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

# Process all HTML files
for root, dirs, files in os.walk('.'):
    if 'venv' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))

print("Finished updating icons.")
