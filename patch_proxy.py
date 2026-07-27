import os

file_path = 'apple_bank/settings.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    CSRF_TRUSTED_ORIGINS = ["""

new_block = """    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_TRUSTED_ORIGINS = ["""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added SECURE_PROXY_SSL_HEADER")
else:
    print("Could not find block")
