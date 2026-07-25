from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    if not user.email:
        return
    
    subject = 'Welcome to Apple Bank!'
    message = f'''Dear {user.first_name},

Welcome to Apple Bank! Your account has been successfully created.
You have received a welcome bonus of $5.00 in your preferred currency.

Thank you for choosing Apple Bank.

Best regards,
Apple Bank Team
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
        print(f"Failed to send welcome email: {e}")

def send_login_alert(user):
    if not user.email:
        return
        
    subject = 'New Login Alert'
    message = f'''Dear {user.first_name},

This is a notification that a new login was detected on your Apple Bank account.
If this was you, no further action is required.

If you did not authorize this login, please contact support immediately and change your password.

Best regards,
Apple Bank Team
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
    amount = f"{currency}{transaction.amount}"
    
    if alert_type == 'debit':
        subject = f'Debit Alert: {amount}'
        message = f'''Dear {user_profile.user.first_name},

This is a notification of a debit transaction on your account.

Amount: {amount}
Description: {transaction.description}
Date: {transaction.timestamp.strftime("%B %d, %Y, %I:%M %p")}

If you did not authorize this transaction, please contact support immediately.

Best regards,
Apple Bank Team
'''
    elif alert_type == 'credit':
        subject = f'Credit Alert: {amount}'
        message = f'''Dear {user_profile.user.first_name},

This is a notification of a credit transaction on your account.

Amount: {amount}
Description: {transaction.description}
Date: {transaction.timestamp.strftime("%B %d, %Y, %I:%M %p")}

Best regards,
Apple Bank Team
'''
    else:
        return

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_profile.user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send transaction alert: {e}")
