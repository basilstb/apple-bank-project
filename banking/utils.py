from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user):
    if not user.email:
        return
    
    subject = 'Welcome to Nexus Trust Bank!'
    
    context = {
        'user': user,
    }
    html_message = render_to_string('banking/emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send welcome email: {e}")

def send_admin_registration_alert(user):
    subject = 'New User Registration Alert'
    
    context = {
        'user': user,
    }
    html_message = render_to_string('banking/emails/admin_alert_registration.html', context)
    plain_message = strip_tags(html_message)
    
    # Send to the default from email or a specific admin email
    admin_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send admin registration alert: {e}")

def send_login_alert(user):
    if not user.email:
        return
        
    subject = 'New Login Alert'
    message = f'''Dear {user.first_name},

This is a notification that a new login was detected on your Nexus Trust Bank account.
If this was you, no further action is required.

If you did not authorize this login, please contact support immediately and change your password.

Best regards,
Nexus Trust Bank Team
'''
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send login alert: {e}")

def send_transaction_alert(user_profile, transaction, alert_type):
    if not user_profile.user.email:
        return
        
    currency = user_profile.currency
    
    subject = f'{alert_type.capitalize()} Alert - Nexus Trust Bank'
    
    context = {
        'user': user_profile.user,
        'transaction_type': alert_type,
        'amount': transaction.amount,
        'date': transaction.timestamp,
        'description': transaction.description,
        'reference': f'TXN-{transaction.id:06d}',
        'balance': user_profile.balance,
    }
    
    html_message = render_to_string('banking/emails/transaction_alert.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user_profile.user.email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send transaction alert: {e}")
