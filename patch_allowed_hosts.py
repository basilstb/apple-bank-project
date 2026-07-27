import os

file_path = 'apple_bank/settings.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_line = "ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')"
new_line = "ALLOWED_HOSTS = ['*']  # Allow all hosts to prevent 400 Bad Request errors with custom domains"

if old_line in content:
    content = content.replace(old_line, new_line)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated ALLOWED_HOSTS successfully.")
else:
    print("Could not find ALLOWED_HOSTS line.")
