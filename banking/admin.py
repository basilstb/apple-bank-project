from django.contrib import admin
from .models import UserProfile, Transaction, LoanApplication, ATMCardRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance', 'account_status')
    search_fields = ('user__username', 'account_number', 'user__email')
    list_filter = ('account_status',)
    list_editable = ('balance', 'account_status')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'timestamp')
    search_fields = ('sender__account_number', 'receiver__account_number', 'description')
    list_filter = ('transaction_type', 'status', 'timestamp')
    list_editable = ('status', 'progress_percentage')
    readonly_fields = ('timestamp',)

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
