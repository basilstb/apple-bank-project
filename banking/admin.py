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

class SinglePageUserAdmin(admin.ModelAdmin):
    form = CustomUserForm
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, SinglePageUserAdmin)



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')
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
