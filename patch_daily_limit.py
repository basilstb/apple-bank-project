import re

with open('banking/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''            if sender_profile.account_number == recipient_account and bank_name.lower() == 'nexus trust bank':
                messages.error(request, "You cannot transfer money to yourself.")
                return redirect('transfer')
                
            with transaction.atomic():'''

replacement = '''            if sender_profile.account_number == recipient_account and bank_name.lower() == 'nexus trust bank':
                messages.error(request, "You cannot transfer money to yourself.")
                return redirect('transfer')
                
            from django.utils import timezone
            today = timezone.now().date()
            daily_transfers = Transaction.objects.filter(
                sender=sender_profile,
                transaction_type='Transfer',
                timestamp__date=today
            )
            total_today = sum(tx.amount for tx in daily_transfers)
            
            if total_today + amount > sender_profile.daily_limit:
                messages.error(request, f"Transfer rejected. This transaction exceeds your daily limit of {sender_profile.currency}{sender_profile.daily_limit:,.2f}.")
                return redirect('transfer')
                
            with transaction.atomic():'''

if target in content:
    content = content.replace(target, replacement)
    with open('banking/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Success')
else:
    print('Target not found')
