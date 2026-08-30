import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

try:
    print("Attempting to send test email...")
    send_mail(
        'Test Email from Nexus Trust Bank',
        'This is a test email to verify SMTP configuration.',
        settings.DEFAULT_FROM_EMAIL,
        ['info@nexuscustomerservice.online'],  # Send to self
        fail_silently=False,
    )
    print("Test email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
