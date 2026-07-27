import os
import re

file_path = 'banking/templates/banking/transfer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix {% endif %} split across lines
content = re.sub(r'\{%\s*\n\s*endif\s*%\}', '{% endif %}', content)
content = re.sub(r'\{%\s*endif\s*\n\s*%\}', '{% endif %}', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed transfer.html")
