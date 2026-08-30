import re

with open('banking/admin.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add reverse_transactions to TransactionAdmin
target_tx_admin = '''@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')'''

replacement_tx_admin = '''@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')
    actions = ['reverse_transactions']

    @admin.action(description='Reverse selected transactions')
    def reverse_transactions(self, request, queryset):
        from django.db import transaction
        from django.contrib import messages
        
        reversed_count = 0
        with transaction.atomic():
            for tx in queryset:
                if tx.status == 'Reversed':
                    continue
                    
                # Reverse balances
                if tx.transaction_type == 'Transfer':
                    if tx.sender:
                        tx.sender.balance += tx.amount
                        tx.sender.save(update_fields=['balance'])
                    if tx.receiver:
                        tx.receiver.balance -= tx.amount
                        tx.receiver.save(update_fields=['balance'])
                elif tx.transaction_type == 'Withdrawal':
                    if tx.sender:
                        tx.sender.balance += tx.amount
                        tx.sender.save(update_fields=['balance'])
                elif tx.transaction_type == 'Deposit':
                    if tx.receiver:
                        tx.receiver.balance -= tx.amount
                        tx.receiver.save(update_fields=['balance'])
                
                # Create reversal transaction
                Transaction.objects.create(
                    sender=tx.receiver if tx.transaction_type == 'Transfer' else None,
                    receiver=tx.sender if tx.transaction_type in ['Transfer', 'Withdrawal'] else None,
                    amount=tx.amount,
                    description=f"Reversal of TXN-{tx.id:06d}",
                    transaction_type='Transfer',
                    status='Successful',
                    progress_percentage=100
                )
                
                # Mark original as reversed
                tx.status = 'Reversed'
                tx.save(update_fields=['status'])
                reversed_count += 1
                
        self.message_user(request, f'Successfully reversed {reversed_count} transaction(s).', messages.SUCCESS)'''

if target_tx_admin in content:
    content = content.replace(target_tx_admin, replacement_tx_admin)
    print('Success patching TransactionAdmin')
else:
    print('Target not found for TransactionAdmin')

# 2. Add add_money to SinglePageUserAdmin
target_user_admin = '''class SinglePageUserAdmin(admin.ModelAdmin):
    form = CustomUserForm
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')'''

replacement_user_admin = '''from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

class SinglePageUserAdmin(admin.ModelAdmin):
    form = CustomUserForm
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = ['add_money_action']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/add-money/', self.admin_site.admin_view(self.add_money_view), name='user_add_money'),
        ]
        return custom_urls + urls
        
    @admin.action(description='Add Money to Selected Users')
    def add_money_action(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one user to add money to.", level=messages.ERROR)
            return
        user = queryset.first()
        return redirect(f'admin:user_add_money', object_id=user.pk)
        
    def add_money_view(self, request, object_id):
        user = get_object_or_404(User, pk=object_id)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        if request.method == 'POST':
            amount_str = request.POST.get('amount')
            description = request.POST.get('description', 'Account Funding')
            
            try:
                from decimal import Decimal
                amount = Decimal(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                    
                with transaction.atomic():
                    profile.balance += amount
                    profile.save(update_fields=['balance'])
                    
                    Transaction.objects.create(
                        sender=None,
                        receiver=profile,
                        amount=amount,
                        description=description,
                        transaction_type='Deposit',
                        status='Successful',
                        progress_percentage=100
                    )
                    
                self.message_user(request, f"Successfully added {profile.currency}{amount} to {user.username}'s account.", level=messages.SUCCESS)
                return redirect('admin:auth_user_changelist')
            except Exception as e:
                self.message_user(request, f"Error adding money: {str(e)}", level=messages.ERROR)
                
        context = dict(
            self.admin_site.each_context(request),
            title=f"Add Money to {user.username}",
            user_obj=user,
            profile=profile,
        )
        return render(request, 'admin/banking/user/add_money.html', context)'''

if target_user_admin in content:
    content = content.replace(target_user_admin, replacement_user_admin)
    print('Success patching SinglePageUserAdmin')
else:
    print('Target not found for SinglePageUserAdmin')

with open('banking/admin.py', 'w', encoding='utf-8') as f:
    f.write(content)
