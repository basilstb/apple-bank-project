from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Transaction, LoanApplication, ATMCardRequest

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}), label="Confirm Password")
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-apple-dark file:text-white hover:file:bg-gray-800'}))
    transaction_pin = forms.CharField(max_length=4, min_length=4, widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}), label="Create 4-Digit Transaction PIN")
    currency = forms.ChoiceField(choices=UserProfile.CURRENCY_CHOICES, widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_transaction_pin(self):
        pin = self.cleaned_data.get('transaction_pin')
        if not pin.isdigit() or len(pin) != 4:
            raise forms.ValidationError("PIN must be exactly 4 digits.")
        return pin

class TransferForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Enter Amount", widget=forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm pl-7'}))
    recipient_account = forms.CharField(max_length=20, label="Enter Account Number", widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))
    account_name = forms.CharField(max_length=100, label="Enter Account Name", widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))
    bank_name = forms.CharField(max_length=100, label="Enter Bank Name", widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))
    swift_code = forms.CharField(max_length=20, required=False, label="SWIFT Code (Optional)", widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))
    ifsc_code = forms.CharField(max_length=20, required=False, label="IFSC Code (Optional)", widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))
    description = forms.CharField(max_length=255, required=False, label="Description (Optional)", widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}))

class TransferPINForm(forms.Form):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}), label="Enter 4-Digit PIN to Confirm")

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['full_name', 'country', 'job', 'email_address', 'whatsapp_number', 'amount', 'reason']
        labels = {
            'full_name': 'Your Full Name',
            'country': 'Country',
            'job': 'Job',
            'email_address': 'Email Address',
            'whatsapp_number': 'WhatsApp Number',
            'amount': 'Loan Amount',
            'reason': 'Purpose of Loan',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'country': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'job': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'email_address': forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
            'reason': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm', 'rows': 3}),
        }

class ATMCardRequestForm(forms.ModelForm):
    class Meta:
        model = ATMCardRequest
        fields = ['card_type']
        widgets = {
            'card_type': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-apple-dark focus:ring-apple-dark sm:text-sm'}),
        }

