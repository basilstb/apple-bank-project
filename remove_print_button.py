import sys
import re

with open('banking/templates/banking/receipt.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove print button
pattern = re.compile(r'\s*<button onclick=\"window\.print\(\)\".*?</button>', re.DOTALL)
content = pattern.sub('', content)

with open('banking/templates/banking/receipt.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
