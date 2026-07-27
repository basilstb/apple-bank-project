import os

file_path = 'apple_bank/settings.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_csrf = """    CSRF_TRUSTED_ORIGINS = [
        'https://apple-bank-web.onrender.com',
        'https://nexusbank.onrender.com',
        'https://nexus-trust-bank.onrender.com',
        'https://nexustrustbank.online',
        'https://www.nexustrustbank.online',
        'https://applebank.online',
        'https://www.applebank.online',
    ]"""

new_csrf = """    CSRF_TRUSTED_ORIGINS = [
        'https://apple-bank-web.onrender.com',
        'https://nexusbank.onrender.com',
        'https://nexus-trust-bank.onrender.com',
        'https://nexustrustbank.online',
        'https://www.nexustrustbank.online',
        'https://applebank.online',
        'https://www.applebank.online',
        'https://nexusntb.online',
        'https://www.nexusntb.online',
    ]"""

if old_csrf in content:
    content = content.replace(old_csrf, new_csrf)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated CSRF_TRUSTED_ORIGINS with nexusntb.online")
else:
    print("Could not find old CSRF_TRUSTED_ORIGINS block")
