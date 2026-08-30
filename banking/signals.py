from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import transaction as db_transaction
from .models import Transaction
from .utils import send_welcome_email, send_admin_registration_alert, send_transaction_alert

@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance)
        send_admin_registration_alert(instance)

@receiver(post_save, sender=Transaction)
def transaction_saved_signal(sender, instance, created, **kwargs):
    if created:
        def send_alerts():
            if instance.status in ['Successful', 'Pending']:
                if instance.sender:
                    send_transaction_alert(instance.sender, instance, 'debit')
                if instance.receiver:
                    send_transaction_alert(instance.receiver, instance, 'credit')
        
        db_transaction.on_commit(send_alerts)
