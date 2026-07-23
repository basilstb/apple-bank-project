from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm, TransferForm, LoanApplicationForm, ATMCardRequestForm
from .models import UserProfile, Transaction, LoanApplication, ATMCardRequest
from django.db.models import Q
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django_ratelimit.decorators import ratelimit

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Update phone number and profile picture in profile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone_number = form.cleaned_data.get('phone_number', '')
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            
            # Hash and save the transaction PIN
            raw_pin = form.cleaned_data.get('transaction_pin')
            if raw_pin:
                profile.transaction_pin = make_password(raw_pin)
                
            profile.save()

            login(request, user)
            messages.success(request, f"Welcome to Apple Bank, {user.first_name}! Your account has been created with a $5,000.00 welcome bonus.")
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'banking/register.html', {'form': form})

@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'banking/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def dashboard_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    recent_transactions = Transaction.objects.filter(
        Q(sender=profile) | Q(receiver=profile)
    ).order_by('-timestamp')[:5]
    loan_applications = LoanApplication.objects.filter(user=profile).order_by('-created_at')
    return render(request, 'banking/dashboard.html', {
        'recent_transactions': recent_transactions, 
        'loan_applications': loan_applications,
        'user': request.user
    })

@login_required
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
            description = form.cleaned_data.get('description', f'Transfer to {account_name} at {bank_name}')
            
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
                
            messages.success(request, f"Successfully transferred ${amount} to {account_name} at {bank_name}.")
            return redirect('receipt', tx_id=tx.id)
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form})

@login_required
def history_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(
        Q(sender=profile) | Q(receiver=profile)
    ).order_by('-timestamp')
    return render(request, 'banking/history.html', {'transactions': transactions})

@login_required
def receipt_view(request, tx_id):
    try:
        tx = Transaction.objects.get(id=tx_id)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if tx.sender != profile and tx.receiver != profile:
            messages.error(request, "You do not have permission to view this receipt.")
            return redirect('dashboard')
    except Transaction.DoesNotExist:
        messages.error(request, "Transaction not found.")
        return redirect('dashboard')
        
    return render(request, 'banking/receipt.html', {'tx': tx})

@login_required
def loan_application_view(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user, _ = UserProfile.objects.get_or_create(user=request.user)
            loan.save()
            messages.success(request, "Your loan application has been submitted and is pending review.")
            return redirect('dashboard')
    else:
        form = LoanApplicationForm()
    return render(request, 'banking/loan_application.html', {'form': form})

@login_required
def atm_request_view(request):
    if request.method == 'POST':
        form = ATMCardRequestForm(request.POST)
        if form.is_valid():
            atm_request = form.save(commit=False)
            atm_request.user, _ = UserProfile.objects.get_or_create(user=request.user)
            atm_request.save()
            messages.success(request, f"Your request for a {atm_request.card_type} card has been submitted.")
            return redirect('dashboard')
    else:
        form = ATMCardRequestForm()
    return render(request, 'banking/atm_request.html', {'form': form})
