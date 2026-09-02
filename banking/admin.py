from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Transaction, LoanApplication, ATMCardRequest

# Remove username validators to allow spaces and any characters
User._meta.get_field('username').validators = []

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Bank Account Profile'
    fields = ('account_number', 'balance', 'currency', 'phone_number', 'account_status', 'profile_picture', 'transaction_pin', 'daily_limit', 'require_pending_transactions', 'allow_transfers')

class CustomUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep the current password. Required for new users.")
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk and not cleaned_data.get('password'):
            self.add_error('password', 'Password is required for new users.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

class SinglePageUserAdmin(admin.ModelAdmin):
    form = CustomUserForm
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = ['add_money_action', 'disable_pending_action', 'enable_pending_action', 'disable_transfers_action', 'enable_transfers_action']
    
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
        return render(request, 'admin/banking/user/add_money.html', context)

    @admin.action(description='Disable pending transactions for selected users')
    def disable_pending_action(self, request, queryset):
        updated = 0
        for user in queryset:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.require_pending_transactions = False
            profile.save(update_fields=['require_pending_transactions'])
            updated += 1
        self.message_user(request, f"Disabled pending transactions for {updated} user(s).", level=messages.SUCCESS)

    @admin.action(description='Enable pending transactions for selected users')
    def enable_pending_action(self, request, queryset):
        updated = 0
        for user in queryset:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.require_pending_transactions = True
            profile.save(update_fields=['require_pending_transactions'])
            updated += 1
        self.message_user(request, f"Enabled pending transactions for {updated} user(s).", level=messages.SUCCESS)

    @admin.action(description='Disable transfers for selected users')
    def disable_transfers_action(self, request, queryset):
        updated = 0
        for user in queryset:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.allow_transfers = False
            profile.save(update_fields=['allow_transfers'])
            updated += 1
        self.message_user(request, f"Disabled transfers for {updated} user(s).", level=messages.SUCCESS)

    @admin.action(description='Enable transfers for selected users')
    def enable_transfers_action(self, request, queryset):
        updated = 0
        for user in queryset:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.allow_transfers = True
            profile.save(update_fields=['allow_transfers'])
            updated += 1
        self.message_user(request, f"Enabled transfers for {updated} user(s).", level=messages.SUCCESS)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, SinglePageUserAdmin)



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')
    actions = ['reverse_transactions', 'set_pending_action', 'set_successful_action']

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
                
        self.message_user(request, f'Successfully reversed {reversed_count} transaction(s).', messages.SUCCESS)

    @admin.action(description='Set selected transactions to Pending (50%%)')
    def set_pending_action(self, request, queryset):
        updated = 0
        for tx in queryset:
            tx.status = 'Pending'
            tx.progress_percentage = 50
            tx.save()
            updated += 1
        self.message_user(request, f"Set {updated} transaction(s) to Pending (50%).", level=messages.SUCCESS)

    @admin.action(description='Set selected transactions to Successful (100%%)')
    def set_successful_action(self, request, queryset):
        updated = 0
        for tx in queryset:
            tx.status = 'Successful'
            tx.progress_percentage = 100
            tx.save()
            updated += 1
        self.message_user(request, f"Set {updated} transaction(s) to Successful (100%).", level=messages.SUCCESS)

    search_fields = ('sender__account_number', 'receiver__account_number', 'description', 'pending_reason')
    list_filter = ('transaction_type', 'status', 'timestamp')
    list_editable = ('status', 'progress_percentage', 'pending_reason')
    readonly_fields = ('timestamp',)
    fields = ('sender', 'receiver', 'amount', 'description', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at')
    search_fields = ('user__user__username', 'user__account_number')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)

@admin.register(ATMCardRequest)
class ATMCardRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_type', 'status', 'created_at')
    search_fields = ('user__user__username', 'user__account_number')
    list_filter = ('card_type', 'status', 'created_at')
    list_editable = ('status',)
