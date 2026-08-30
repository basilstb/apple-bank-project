import os
import django

os.environ['DATABASE_URL'] = 'postgresql://apple_bank_user:Qr9WE23xdv9f8fWa2imfNtGma1ZOAWK8@dpg-d9hav8mpbkes73dnac90-a.oregon-postgres.render.com/apple_bank'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.db import connection
from django.contrib import admin

print("Live database tables:")
print(connection.introspection.table_names())

print("\nRegistered admin models:")
for model, model_admin in admin.site._registry.items():
    print(f"Model: {model.__name__}, App: {model._meta.app_label}")
