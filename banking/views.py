from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm, TransferForm, LoanApplicationForm, ATMCardRequestForm, TransferPINForm
from .models import UserProfile, Transaction, LoanApplication, ATMCardRequest
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from .utils import send_welcome_email, send_transaction_alert, send_login_alert
import io
import json
import logging

logger = logging.getLogger(__name__)

def register_view(request):
    return redirect('login')

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
                send_login_alert(user)
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
    
    pending_transactions = Transaction.objects.filter(
        Q(sender=profile) | Q(receiver=profile),
        status='Pending'
    ).order_by('-timestamp')
    
    loan_applications = LoanApplication.objects.filter(user=profile).order_by('-created_at')
    atm_requests = ATMCardRequest.objects.filter(user=profile).order_by('-created_at')
    return render(request, 'banking/dashboard.html', {
        'recent_transactions': recent_transactions, 
        'pending_transactions': pending_transactions,
        'loan_applications': loan_applications,
        'atm_requests': atm_requests,
        'user': request.user
    })

@login_required
@ratelimit(key='user', rate='3/m', block=True)
def transfer_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.allow_transfers:
        messages.error(request, "Transfers are disabled for your account.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer_data = {
                'amount': str(form.cleaned_data['amount']),
                'recipient_account': str(form.cleaned_data['recipient_account']),
                'account_name': str(form.cleaned_data['account_name']),
                'bank_name': str(form.cleaned_data['bank_name']),
                'iban': str(form.cleaned_data.get('iban', '')),
                'swift_code': str(form.cleaned_data.get('swift_code', '')),
                'ifsc_code': str(form.cleaned_data.get('ifsc_code', '')),
                'description': str(form.cleaned_data.get('description', '')),
            }
            request.session['pending_transfer_data'] = transfer_data
            request.session.modified = True
            return redirect('transfer_pin_verify')
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form})

@login_required
@ratelimit(key='user', rate='3/m', block=True)
def transfer_pin_verify_view(request):
    sender_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not sender_profile.allow_transfers:
        messages.error(request, "Transfers are disabled for your account.")
        return redirect('dashboard')

    transfer_data = request.session.get('pending_transfer_data')
    if not transfer_data:
        messages.error(request, "No pending transfer found.")
        return redirect('transfer')
        
    if request.method == 'POST':
        form = TransferPINForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data.get('pin')
            
            is_valid_pin = False
            if sender_profile.transaction_pin == pin:
                is_valid_pin = True
                sender_profile.transaction_pin = make_password(pin)
                sender_profile.save(update_fields=['transaction_pin'])
            elif sender_profile.transaction_pin and check_password(pin, sender_profile.transaction_pin):
                is_valid_pin = True
                
            if not is_valid_pin:
                messages.error(request, "Incorrect Transaction PIN.")
                return redirect('transfer_pin_verify')
                
            from decimal import Decimal
            amount = Decimal(transfer_data['amount'])
            recipient_account = transfer_data['recipient_account']
            account_name = transfer_data['account_name']
            bank_name = transfer_data['bank_name']
            iban = transfer_data.get('iban', '')
            swift_code = transfer_data.get('swift_code', '')
            ifsc_code = transfer_data.get('ifsc_code', '')
            custom_desc = transfer_data.get('description', '')
            
            description = f'Transfer to {account_name} at {bank_name} (Acct: {recipient_account})'
            if custom_desc:
                description = f'{custom_desc} - {description}'
            if iban:
                description += f' (IBAN: {iban})'
            if swift_code:
                description += f' (SWIFT: {swift_code})'
            ifsc_code = transfer_data.get('ifsc_code', '')
            if ifsc_code:
                description += f' (IFSC: {ifsc_code})'
                
            if sender_profile.account_number == recipient_account and bank_name.lower() == 'nexus trust bank':
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
                
            with transaction.atomic():
                sender_profile = UserProfile.objects.select_for_update().get(id=sender_profile.id)
                if sender_profile.balance < amount:
                    messages.error(request, "Insufficient funds.")
                    return redirect('transfer')
                    
                sender_profile.balance -= amount
                sender_profile.save()
                
                receiver_profile = None
                if bank_name.lower() in ['nexus trust bank', 'nexustrustbank', 'ntb', 'ntb bank']:
                    try:
                        receiver_profile = UserProfile.objects.select_for_update().get(account_number=recipient_account)
                        receiver_profile.balance += amount
                        receiver_profile.save()
                    except UserProfile.DoesNotExist:
                        pass
                
                status = 'Pending' if sender_profile.require_pending_transactions else 'Successful'
                progress_percentage = 50 if sender_profile.require_pending_transactions else 100
                tx = Transaction.objects.create(
                    sender=sender_profile,
                    receiver=receiver_profile,
                    amount=amount,
                    description=description,
                    transaction_type='Transfer',
                    status=status,
                    progress_percentage=progress_percentage
                )
                
            # Send email alerts OUTSIDE the atomic block
            # so DB commits first, and SMTP delays don't hold the lock
            send_transaction_alert(sender_profile, tx, 'debit')
            if receiver_profile:
                send_transaction_alert(receiver_profile, tx, 'credit')
                
            del request.session['pending_transfer_data']
            messages.success(request, f"Successfully transferred ${amount} to {account_name} at {bank_name}.")
            return redirect('receipt', tx_id=tx.id)
    else:
        form = TransferPINForm()
    
    context_data = transfer_data.copy()
    try:
        context_data['amount'] = float(transfer_data['amount'])
    except (ValueError, TypeError):
        pass
        
    return render(request, 'banking/transfer_pin.html', {
        'form': form,
        'transfer_data': context_data
    })

@login_required
def history_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(
        Q(sender=profile) | Q(receiver=profile)
    ).order_by('-timestamp')
    return render(request, 'banking/history.html', {'transactions': transactions, 'profile': profile})

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
        
    external_receiver_name = None
    external_bank_name = None
    external_account = None
    external_iban = None
    if not tx.receiver and "Transfer to" in tx.description:
        import re
        # Try new format with account number
        match = re.search(r'Transfer to (.*?) at (.*?) \(Acct: (.*?)\)', tx.description)
        if match:
            external_receiver_name = match.group(1)
            external_bank_name = match.group(2)
            external_account = match.group(3)
            
            iban_match = re.search(r'\(IBAN: (.*?)\)', tx.description)
            if iban_match:
                external_iban = iban_match.group(1)
        else:
            # Fallback to old format
            match = re.search(r'Transfer to (.*?) at (.*?)(?:\s*\(|$)', tx.description)
            if match:
                external_receiver_name = match.group(1)
                external_bank_name = match.group(2)
            
    return render(request, 'banking/receipt.html', {
        'tx': tx,
        'external_receiver_name': external_receiver_name,
        'external_bank_name': external_bank_name,
        'external_account': external_account,
        'external_iban': external_iban,
        'profile': profile
    })

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

@login_required
def download_receipt_view(request, tx_id):
    try:
        tx = Transaction.objects.get(id=tx_id)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if tx.sender != profile and tx.receiver != profile:
            messages.error(request, "You do not have permission to download this receipt.")
            return redirect('dashboard')
    except Transaction.DoesNotExist:
        messages.error(request, "Transaction not found.")
        return redirect('dashboard')
        
    # Generate high-resolution image using Pillow
    width = 1200
    height = 1600
    image = Image.new('RGB', (width, height), '#F7F9FB')
    draw = ImageDraw.Draw(image)
    
    import os
    from django.conf import settings
    
    font_dir = os.path.join(settings.BASE_DIR, 'banking', 'static', 'fonts')
    regular_font_path = os.path.join(font_dir, 'Roboto-Regular.ttf')
    bold_font_path = os.path.join(font_dir, 'Roboto-Bold.ttf')
    
    try:
        # Try to use bundled fonts
        font_title = ImageFont.truetype(bold_font_path, 64)
        font_header = ImageFont.truetype(regular_font_path, 40)
        font_body = ImageFont.truetype(regular_font_path, 32)
        font_bold = ImageFont.truetype(bold_font_path, 32)
        font_amount = ImageFont.truetype(bold_font_path, 80)
        font_small = ImageFont.truetype(regular_font_path, 24)
    except IOError:
        try:
            # Fallback to system fonts
            font_title = ImageFont.truetype("arialbd.ttf", 64)
            font_header = ImageFont.truetype("arial.ttf", 40)
            font_body = ImageFont.truetype("arial.ttf", 32)
            font_bold = ImageFont.truetype("arialbd.ttf", 32)
            font_amount = ImageFont.truetype("arialbd.ttf", 80)
            font_small = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font_title = ImageFont.load_default()
            font_header = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_bold = ImageFont.load_default()
            font_amount = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Draw Top Red Bar
    draw.rectangle([(0, 0), (width, 20)], fill="#ad0012")

    # Draw Receipt Card Background
    card_margin = 80
    card_top = 100
    card_bottom = height - 100
    draw.rounded_rectangle([(card_margin, card_top), (width - card_margin, card_bottom)], radius=30, fill="white", outline="#E5E7EB", width=2)

    # Draw Header
    try:
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'nexus_logo.png')
        logo = Image.open(logo_path)
        logo.thumbnail((300, 300))
        logo_w, logo_h = logo.size
        # Paste logo with alpha channel if it exists
        if logo.mode == 'RGBA':
            image.paste(logo, (int(width/2 - logo_w/2), card_top + 40), logo)
        else:
            image.paste(logo, (int(width/2 - logo_w/2), card_top + 40))
        
        draw.text((width/2, card_top + 40 + logo_h + 20), "OFFICIAL RECEIPT", fill="#6B7280", font=font_header, anchor="mt")
    except Exception as e:
        draw.text((width/2, card_top + 80), "Nexus Trust Bank", fill="#111827", font=font_title, anchor="mt")
        draw.text((width/2, card_top + 160), "OFFICIAL RECEIPT", fill="#6B7280", font=font_header, anchor="mt")
    
    # Draw Amount Section
    amount_y = card_top + 260
    draw.rounded_rectangle([(card_margin + 60, amount_y), (width - card_margin - 60, amount_y + 240)], radius=20, fill="#F9FAFB", outline="#F3F4F6", width=2)
    
    currency = profile.currency
    draw.text((width/2, amount_y + 40), "TRANSACTION AMOUNT", fill="#6B7280", font=font_body, anchor="mt")
    draw.text((width/2, amount_y + 90), f"{currency}{tx.amount:,.2f}", fill="#111827", font=font_amount, anchor="mt")
    
    # Draw Status
    status_color = "#059669" if tx.status == 'Successful' else "#D97706" if tx.status == 'Pending' else "#DC2626"
    status_bg = "#D1FAE5" if tx.status == 'Successful' else "#FEF3C7" if tx.status == 'Pending' else "#FEE2E2"
    
    status_text = tx.status.upper()
    if tx.status == 'Pending':
        status_text = f"PENDING ({tx.progress_percentage}%)"
    
    # Simple status pill
    bbox = draw.textbbox((0, 0), status_text, font=font_bold)
    text_width = bbox[2] - bbox[0]
    pill_width = text_width + 80
    
    draw.rounded_rectangle([(width/2 - pill_width/2, amount_y + 180), (width/2 + pill_width/2, amount_y + 230)], radius=25, fill=status_bg)
    draw.text((width/2, amount_y + 185), status_text, fill=status_color, font=font_bold, anchor="mt")
    
    # Draw Details
    y = amount_y + 300
    line_height = 60
    
    details = [
        ("Transaction ID", f"#TXN-{tx.id:06d}"),
        ("Date & Time", tx.timestamp.strftime("%B %d, %Y, %I:%M %p")),
        ("Type", tx.transaction_type),
        ("Description", tx.description),
    ]
    
    if tx.sender:
        details.append(("Sender Name", f"{tx.sender.user.first_name} {tx.sender.user.last_name}"))
        details.append(("Sender Account", tx.sender.account_number))
    if tx.receiver:
        details.append(("Receiver Name", f"{tx.receiver.user.first_name} {tx.receiver.user.last_name}"))
        details.append(("Receiver Account", tx.receiver.account_number))
    elif "Transfer to" in tx.description:
        import re
        match = re.search(r'Transfer to (.*?) at (.*?) \(Acct: (.*?)\)', tx.description)
        if match:
            details.append(("Receiver Name", match.group(1)))
            details.append(("Receiver Account", match.group(3)))
            details.append(("Bank Name", match.group(2)))
            
            iban_match = re.search(r'\(IBAN: (.*?)\)', tx.description)
            if iban_match:
                details.append(("IBAN", iban_match.group(1)))
        else:
            match = re.search(r'Transfer to (.*?) at (.*?)(?:\s*\(|$)', tx.description)
            if match:
                details.append(("Receiver Name", match.group(1)))
                details.append(("Bank Name", match.group(2)))
        
    for label, value in details:
        # Wrap value if it's too long
        max_val_width = 580
        words = value.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font_bold)
            w = bbox[2] - bbox[0]
            if w <= max_val_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        if current_line:
            lines.append(' '.join(current_line))
            
        if not lines:
            lines = ['']
            
        # Draw label
        draw.text((card_margin + 80, y), label, fill="#6B7280", font=font_body)
        
        # Draw wrapped lines
        for line in lines:
            draw.text((width - card_margin - 80, y), line, fill="#111827", font=font_bold, anchor="rt")
            y += line_height
        
    # Footer Dashed Line
    y += 40
    for x in range(card_margin + 60, width - card_margin - 60, 20):
        draw.line([(x, y), (x + 10, y)], fill="#E5E7EB", width=3)
        
    # Footer Text
    draw.text((width/2, y + 60), "Thank you for banking with Nexus Trust Bank", fill="#6B7280", font=font_bold, anchor="mt")
    draw.text((width/2, y + 100), "This is a computer generated receipt and does not require a signature.", fill="#9CA3AF", font=font_small, anchor="mt")
    
    # Save to BytesIO
    buffer = io.BytesIO()
    image.save(buffer, format='PNG', quality=100)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="receipt_TXN-{tx.id:06d}.png"'
    return response

def email_diagnostic_view(request):
    """Endpoint to diagnose email configuration (temporarily public for testing)."""
    
    from django.conf import settings
    from django.core.mail import send_mail
    
    config = {
        'EMAIL_BACKEND': settings.EMAIL_BACKEND,
        'EMAIL_HOST': settings.EMAIL_HOST,
        'EMAIL_PORT': settings.EMAIL_PORT,
        'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
        'EMAIL_HOST_PASSWORD_LENGTH': len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 0,
        'EMAIL_HOST_PASSWORD_ENDS_WITH_HASH': settings.EMAIL_HOST_PASSWORD.endswith('#') if settings.EMAIL_HOST_PASSWORD else False,
        'EMAIL_HOST_PASSWORD_STARTS_WITH_QUOTE': settings.EMAIL_HOST_PASSWORD.startswith('"') or settings.EMAIL_HOST_PASSWORD.startswith("'") if settings.EMAIL_HOST_PASSWORD else False,
        'EMAIL_HOST_PASSWORD_ENDS_WITH_QUOTE': settings.EMAIL_HOST_PASSWORD.endswith('"') or settings.EMAIL_HOST_PASSWORD.endswith("'") if settings.EMAIL_HOST_PASSWORD else False,
        'EMAIL_HOST_PASSWORD_HAS_SPACES': ' ' in settings.EMAIL_HOST_PASSWORD if settings.EMAIL_HOST_PASSWORD else False,
        'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
        'SITE_URL': getattr(settings, 'SITE_URL', 'NOT SET'),
    }
    
    result = {'config': config, 'test_email': None}
    
    if request.GET.get('send_test') == '1':
        to_email = request.GET.get('to', settings.DEFAULT_FROM_EMAIL)
        if request.user.is_authenticated and request.user.email:
            to_email = request.GET.get('to', request.user.email)
            
        try:
            send_mail(
                'Email Diagnostic Test - Nexus Trust Bank',
                'If you received this, your email configuration is working correctly!',
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                fail_silently=False,
            )
            result['test_email'] = f'SUCCESS — sent to {to_email}'
        except Exception as e:
            result['test_email'] = f'FAILED — {type(e).__name__}: {e}'
    
    return HttpResponse(
        f"<html><head><title>Email Diagnostic</title></head><body>"
        f"<h1>Email Configuration</h1>"
        f"<pre>{json.dumps(result, indent=2, default=str)}</pre>"
        f"<br><form method='GET'>"
        f"<input type='hidden' name='send_test' value='1'>"
        f"Send test email to: <input type='email' name='to' placeholder='{settings.DEFAULT_FROM_EMAIL}'>"
        f"<button type='submit'>Send Test Email</button>"
        f"</form>"
        f"</body></html>",
        content_type='text/html'
    )

