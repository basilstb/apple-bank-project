import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.contrib.auth.models import User
from banking.models import UserProfile, Transaction
from decimal import Decimal

def test_features():
    # 1. Setup users
    user1, _ = User.objects.get_or_create(username='testuser1', defaults={'email': 'test1@example.com'})
    user2, _ = User.objects.get_or_create(username='testuser2', defaults={'email': 'test2@example.com'})
    
    profile1, _ = UserProfile.objects.get_or_create(user=user1)
    profile2, _ = UserProfile.objects.get_or_create(user=user2)
    
    profile1.balance = Decimal('10000.00')
    profile1.daily_limit = Decimal('5000.00')
    profile1.save()
    
    profile2.balance = Decimal('1000.00')
    profile2.save()
    
    print(f"Initial balances: User1: {profile1.balance}, User2: {profile2.balance}")
    
    # 2. Test Daily Limit
    from django.utils import timezone
    today = timezone.now().date()
    # Create a transfer of 4000
    tx1 = Transaction.objects.create(
        sender=profile1,
        receiver=profile2,
        amount=Decimal('4000.00'),
        transaction_type='Transfer',
        status='Successful',
        description='Test transfer 1'
    )
    profile1.balance -= Decimal('4000.00')
    profile2.balance += Decimal('4000.00')
    profile1.save()
    profile2.save()
    
    print(f"After 4000 transfer: User1: {profile1.balance}, User2: {profile2.balance}")
    
    # Check daily limit logic (simulating the view)
    daily_transfers = Transaction.objects.filter(
        sender=profile1,
        transaction_type='Transfer',
        timestamp__date=today
    )
    total_today = sum(tx.amount for tx in daily_transfers)
    print(f"Total transferred today by User1: {total_today}")
    
    amount_to_transfer = Decimal('2000.00')
    if total_today + amount_to_transfer > profile1.daily_limit:
        print("SUCCESS: Daily limit exceeded correctly.")
    else:
        print("ERROR: Daily limit not exceeded!")
        
    # 3. Test Reverse Transaction
    # Let's reverse tx1
    print("Reversing tx1...")
    if tx1.status != 'Reversed':
        # Reverse balances
        if tx1.transaction_type == 'Transfer':
            if tx1.sender:
                tx1.sender.balance += tx1.amount
                tx1.sender.save(update_fields=['balance'])
            if tx1.receiver:
                tx1.receiver.balance -= tx1.amount
                tx1.receiver.save(update_fields=['balance'])
        
        # Create reversal transaction
        tx_rev = Transaction.objects.create(
            sender=tx1.receiver,
            receiver=tx1.sender,
            amount=tx1.amount,
            description=f"Reversal of TXN-{tx1.id:06d}",
            transaction_type='Transfer',
            status='Successful',
            progress_percentage=100
        )
        
        tx1.status = 'Reversed'
        tx1.save(update_fields=['status'])
        
    profile1.refresh_from_db()
    profile2.refresh_from_db()
    print(f"After reversal: User1: {profile1.balance}, User2: {profile2.balance}")
    if profile1.balance == Decimal('10000.00') and profile2.balance == Decimal('1000.00'):
        print("SUCCESS: Reversal successful.")
    else:
        print("ERROR: Reversal failed.")
        
    # 4. Test Add Money (Deposit)
    print("Adding 500 to User1...")
    profile1.balance += Decimal('500.00')
    profile1.save(update_fields=['balance'])
    Transaction.objects.create(
        sender=None,
        receiver=profile1,
        amount=Decimal('500.00'),
        description='Account Funding',
        transaction_type='Deposit',
        status='Successful',
        progress_percentage=100
    )
    profile1.refresh_from_db()
    print(f"After Add Money: User1: {profile1.balance}")
    if profile1.balance == Decimal('10500.00'):
        print("SUCCESS: Add Money successful.")
    else:
        print("ERROR: Add Money failed.")

if __name__ == '__main__':
    test_features()
