import re

with open('banking/templates/banking/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix {{ ... }} with newlines
content = re.sub(r'\{\{([^}]*?)\n([^}]*?)\}\}', lambda m: '{{' + m.group(1).strip() + ' ' + m.group(2).strip() + '}}', content)

# Fix {% ... %} with newlines
content = re.sub(r'\{%([^%]*?)\n([^%]*?)%\}', lambda m: '{%' + m.group(1).strip() + ' ' + m.group(2).strip() + '%}', content)

with open('banking/templates/banking/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
