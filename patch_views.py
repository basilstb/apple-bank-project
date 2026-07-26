import os

file_path = 'banking/views.py'
with open(file_path, 'r') as f:
    content = f.read()

# 1. Update imports
content = content.replace(
    "from .forms import UserRegistrationForm, TransferForm, LoanApplicationForm, ATMCardRequestForm",
    "from .forms import UserRegistrationForm, TransferForm, LoanApplicationForm, ATMCardRequestForm, TransferPINForm"
)

# 2. Replace transfer_view
old_transfer_view = """@login_required
@ratelimit(key='user', rate='3/m', block=True)
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_account = form.cleaned_data['recipient_account']
            account_name = form.cleaned_data['account_name']
            bank_name = form.cleaned_data['bank_name']
            swift_code = form.cleaned_data.get('swift_code', '')
            ifsc_code = form.cleaned_data.get('ifsc_code', '')
            custom_desc = form.cleaned_data.get('description', '')
            description = f'Transfer to {account_name} at {bank_name} (Acct: {recipient_account})'
            if custom_desc:
                description = f'{custom_desc} - {description}'
            
            if swift_code:
                description += f' (SWIFT: {swift_code})'
            if ifsc_code:
                description += f' (IFSC: {ifsc_code})'
            
            sender_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            
            if sender_profile.account_number == recipient_account and bank_name.lower() == 'apple bank':
                messages.error(request, "You cannot transfer money to yourself.")
                return redirect('transfer')
                
            pin = form.cleaned_data.get('pin')
            is_valid_pin = False
            
            # Handle legacy plaintext PINs
            if sender_profile.transaction_pin == pin:
                is_valid_pin = True
                # Upgrade to hashed PIN
                sender_profile.transaction_pin = make_password(pin)
                sender_profile.save(update_fields=['transaction_pin'])
            elif check_password(pin, sender_profile.transaction_pin):
                is_valid_pin = True
                
            if not is_valid_pin:
                messages.error(request, "Incorrect Transaction PIN.")
                return redirect('transfer')
                
            with transaction.atomic():
                # Lock the sender profile to prevent race conditions
                sender_profile = UserProfile.objects.select_for_update().get(id=sender_profile.id)
                
                if sender_profile.balance < amount:
                    messages.error(request, "Insufficient funds.")
                    return redirect('transfer')
                    
                sender_profile.balance -= amount
                sender_profile.save()
                
                # Check if it's an internal transfer
                receiver_profile = None
                if bank_name.lower() in ['apple bank', 'applebank']:
                    try:
                        # Lock the receiver profile
                        receiver_profile = UserProfile.objects.select_for_update().get(account_number=recipient_account)
                        receiver_profile.balance += amount
                        receiver_profile.save()
                    except UserProfile.DoesNotExist:
                        pass # Treat as external if account not found internally
                
                tx = Transaction.objects.create(
                    sender=sender_profile,
                    receiver=receiver_profile,
                    amount=amount,
                    description=description,
                    transaction_type='Transfer',
                    status='Pending',
                    progress_percentage=50
                )
                
                # Send debit alert to sender
                send_transaction_alert(sender_profile, tx, 'debit')
                
                # Send credit alert to receiver if internal
                if receiver_profile:
                    send_transaction_alert(receiver_profile, tx, 'credit')
                
            messages.success(request, f"Successfully transferred ${amount} to {account_name} at {bank_name}.")
            return redirect('receipt', tx_id=tx.id)
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form})"""

new_transfer_view = """@login_required
@ratelimit(key='user', rate='3/m', block=True)
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            request.session['pending_transfer_data'] = form.cleaned_data
            request.session['pending_transfer_data']['amount'] = str(form.cleaned_data['amount'])
            return redirect('transfer_pin_verify')
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form})

@login_required
@ratelimit(key='user', rate='3/m', block=True)
def transfer_pin_verify_view(request):
    transfer_data = request.session.get('pending_transfer_data')
    if not transfer_data:
        messages.error(request, "No pending transfer found.")
        return redirect('transfer')
        
    if request.method == 'POST':
        form = TransferPINForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data.get('pin')
            sender_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            
            is_valid_pin = False
            if sender_profile.transaction_pin == pin:
                is_valid_pin = True
                sender_profile.transaction_pin = make_password(pin)
                sender_profile.save(update_fields=['transaction_pin'])
            elif check_password(pin, sender_profile.transaction_pin):
                is_valid_pin = True
                
            if not is_valid_pin:
                messages.error(request, "Incorrect Transaction PIN.")
                return redirect('transfer_pin_verify')
                
            from decimal import Decimal
            amount = Decimal(transfer_data['amount'])
            recipient_account = transfer_data['recipient_account']
            account_name = transfer_data['account_name']
            bank_name = transfer_data['bank_name']
            swift_code = transfer_data.get('swift_code', '')
            ifsc_code = transfer_data.get('ifsc_code', '')
            custom_desc = transfer_data.get('description', '')
            
            description = f'Transfer to {account_name} at {bank_name} (Acct: {recipient_account})'
            if custom_desc:
                description = f'{custom_desc} - {description}'
            if swift_code:
                description += f' (SWIFT: {swift_code})'
            if ifsc_code:
                description += f' (IFSC: {ifsc_code})'
                
            if sender_profile.account_number == recipient_account and bank_name.lower() == 'apple bank':
                messages.error(request, "You cannot transfer money to yourself.")
                return redirect('transfer')
                
            with transaction.atomic():
                sender_profile = UserProfile.objects.select_for_update().get(id=sender_profile.id)
                if sender_profile.balance < amount:
                    messages.error(request, "Insufficient funds.")
                    return redirect('transfer')
                    
                sender_profile.balance -= amount
                sender_profile.save()
                
                receiver_profile = None
                if bank_name.lower() in ['apple bank', 'applebank']:
                    try:
                        receiver_profile = UserProfile.objects.select_for_update().get(account_number=recipient_account)
                        receiver_profile.balance += amount
                        receiver_profile.save()
                    except UserProfile.DoesNotExist:
                        pass
                
                tx = Transaction.objects.create(
                    sender=sender_profile,
                    receiver=receiver_profile,
                    amount=amount,
                    description=description,
                    transaction_type='Transfer',
                    status='Pending',
                    progress_percentage=50
                )
                
                send_transaction_alert(sender_profile, tx, 'debit')
                if receiver_profile:
                    send_transaction_alert(receiver_profile, tx, 'credit')
                
            del request.session['pending_transfer_data']
            messages.success(request, f"Successfully transferred ${amount} to {account_name} at {bank_name}.")
            return redirect('receipt', tx_id=tx.id)
    else:
        form = TransferPINForm()
    
    return render(request, 'banking/transfer_pin.html', {
        'form': form,
        'transfer_data': transfer_data
    })"""

content = content.replace(old_transfer_view, new_transfer_view)

with open(file_path, 'w') as f:
    f.write(content)

print("Patched views.py")
