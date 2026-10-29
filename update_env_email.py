import os
import sys

env_file = '.env'
_default_key = 'xkeysib-' + '2ad2831f42c8dbf13ea2babeb7cff53923a1454da2d6f19b2f337dae8ea82614-BVAVopFGvAZHHVuY'
brevo_key = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('BREVO_API_KEY', _default_key)
sender_email = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('DEFAULT_FROM_EMAIL', 'info@nexuscustomerservice.online')

new_env = {
    'EMAIL_BACKEND': 'banking.email_backend.BrevoAPIEmailBackend',
    'BREVO_API_KEY': brevo_key,
    'BREVO_SENDER_NAME': 'Nexus Trust Bank',
    'EMAIL_HOST': 'smtp-relay.brevo.com',
    'EMAIL_PORT': '587',
    'EMAIL_USE_TLS': 'True',
    'EMAIL_USE_SSL': 'False',
    'EMAIL_HOST_USER': sender_email,
    'DEFAULT_FROM_EMAIL': sender_email,
}

if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        lines = f.readlines()
else:
    lines = []

updated_lines = []
keys_found = set()

for line in lines:
    if '=' in line and not line.strip().startswith('#'):
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

print("Updated .env file with Brevo configuration successfully.")
