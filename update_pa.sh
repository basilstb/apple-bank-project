#!/usr/bin/env bash
# PythonAnywhere one-step update script
set -e

echo "=== 1. Pulling latest code from GitHub ==="
cd "$(dirname "$0")"
git fetch origin main
git reset --hard origin/main

echo "=== 2. Activating virtual environment ==="
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

echo "=== 3. Installing dependencies ==="
pip install -r requirements.txt

echo "=== 4. Applying database migrations ==="
python manage.py migrate

echo "=== 5. Collecting static files & ensuring media directory ==="
python manage.py collectstatic --no-input
mkdir -p media/profile_pics

echo "=== 5b. Updating Brevo email configuration in .env ==="
python update_env_email.py

echo "=== 6. Reloading PythonAnywhere web app ==="
if [ -f "/var/www/nexustrustbank_pythonanywhere_com_wsgi.py" ]; then
    touch /var/www/nexustrustbank_pythonanywhere_com_wsgi.py
    echo "Web app reloaded successfully!"
else
    echo "WSGI file not found at default location. Please click 'Reload' in the Web tab on PythonAnywhere."
fi

echo "=== Update complete! ==="
