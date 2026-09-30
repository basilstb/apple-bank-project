"""
PythonAnywhere WSGI configuration for apple_bank project.

INSTRUCTIONS:
  1. Copy the CONTENTS of this file into your PythonAnywhere WSGI file at:
     /var/www/nexustrustbank_pythonanywhere_com_wsgi.py
  2. Replace PROJECT_PATH below if your repo was cloned to a different folder.
"""

import os
import sys

# --- Path Configuration ---
# Update this if you cloned the repo to a different location
PROJECT_PATH = '/home/nexustrustbank/apple-bank-project'
VENV_PATH = os.path.join(PROJECT_PATH, 'venv')

# Add project to Python path
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# Activate the virtual environment
activate_this = os.path.join(VENV_PATH, 'bin', 'activate_this.py')
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'apple_bank.settings'

# Set the PythonAnywhere environment flag (used in settings.py)
os.environ.setdefault('PYTHONANYWHERE_DOMAIN', 'nexustrustbank.pythonanywhere.com')

# Load .env file for secrets
from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_PATH, '.env'))

# Start Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
