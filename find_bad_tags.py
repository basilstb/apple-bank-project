import os
import re

def scan_templates(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find {{ ... }} with newlines
                # We search for {{ followed by anything including newlines up to }}
                matches_val = re.findall(r'\{\{[^}]*?\n[^}]*?\}\}', content)
                if matches_val:
                    print(f"File: {path} has {{...}} with newlines:")
                    for m in matches_val:
                        print(repr(m))
                
                # Find {% ... %} with newlines
                matches_tag = re.findall(r'\{%[^%]*?\n[^%]*?%\}', content)
                if matches_tag:
                    print(f"File: {path} has {{%...%}} with newlines:")
                    for m in matches_tag:
                        print(repr(m))

print("Scanning banking/templates:")
scan_templates('banking/templates')
print("\nScanning templates:")
scan_templates('templates')
