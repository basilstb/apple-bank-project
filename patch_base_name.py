import os

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Replace Apple Bank split across lines
content = re.sub(r'Apple\s+Bank', '<span class="text-blue-900 font-bold">Nexus Trust Bank</span>', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed base.html")
