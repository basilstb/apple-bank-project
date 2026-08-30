import os

env_file = '.env'
new_env = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'mail.privateemail.com',
    'EMAIL_PORT': '587',
    'EMAIL_USE_TLS': 'True',
    'EMAIL_HOST_USER': 'info@nexuscustomerservice.online',
    'EMAIL_HOST_PASSWORD': 'vsxdustiwgwbqjms',
    'DEFAULT_FROM_EMAIL': 'info@nexuscustomerservice.online'
}

if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        lines = f.readlines()
else:
    lines = []

updated_lines = []
keys_found = set()

for line in lines:
    if '=' in line:
        key = line.split('=', 1)[0].strip()
        if key in new_env:
            updated_lines.append(f"{key}={new_env[key]}\n")
            keys_found.add(key)
        else:
            updated_lines.append(line)
    else:
        updated_lines.append(line)

for key, value in new_env.items():
    if key not in keys_found:
        updated_lines.append(f"{key}={value}\n")

with open(env_file, 'w') as f:
    f.writelines(updated_lines)

print("Updated .env file successfully.")
