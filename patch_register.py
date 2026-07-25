import os

register_path = "banking/templates/banking/register.html"
with open(register_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace old apple-dark classes with primary
content = content.replace('bg-apple-dark', 'bg-primary')
content = content.replace('text-apple-dark', 'text-primary')
content = content.replace('focus:border-apple-dark', 'focus:border-primary')
content = content.replace('focus:ring-apple-dark', 'focus:ring-primary')
content = content.replace('text-apple-red', 'text-primary')

with open(register_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched register.html")
