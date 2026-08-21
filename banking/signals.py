from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .utils import send_welcome_email, send_admin_registration_alert

@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance)
        send_admin_registration_alert(instance)
