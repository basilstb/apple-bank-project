import os

# 1. Patch models.py
models_path = "banking/models.py"
with open(models_path, 'r', encoding='utf-8') as f:
    models_content = f.read()

models_old = """    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Successful')
    progress_percentage = models.IntegerField(default=100)

    def save(self, *args, **kwargs):"""

models_new = """    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Successful')
    progress_percentage = models.IntegerField(default=100)
    pending_reason = models.CharField(max_length=255, blank=True, null=True, help_text="Reason for pending status, visible to user")

    def save(self, *args, **kwargs):"""

models_content = models_content.replace(models_old, models_new)
with open(models_path, 'w', encoding='utf-8') as f:
    f.write(models_content)


# 2. Patch admin.py
admin_path = "banking/admin.py"
with open(admin_path, 'r', encoding='utf-8') as f:
    admin_content = f.read()

admin_old = """class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'timestamp')
    search_fields = ('sender__account_number', 'receiver__account_number', 'description')
    list_filter = ('transaction_type', 'status', 'timestamp')
    list_editable = ('status', 'progress_percentage')"""

admin_new = """class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')
    search_fields = ('sender__account_number', 'receiver__account_number', 'description', 'pending_reason')
    list_filter = ('transaction_type', 'status', 'timestamp')
    list_editable = ('status', 'progress_percentage', 'pending_reason')"""

admin_content = admin_content.replace(admin_old, admin_new)
with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(admin_content)


# 3. Patch views.py
views_path = "banking/views.py"
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

views_old = """@login_required
def dashboard_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    recent_transactions = Transaction.objects.filter(
        Q(sender=profile) | Q(receiver=profile)
    ).order_by('-timestamp')[:5]
    loan_applications = LoanApplication.objects.filter(user=profile).order_by('-created_at')
    atm_requests = ATMCardRequest.objects.filter(user=profile).order_by('-created_at')
    return render(request, 'banking/dashboard.html', {
        'recent_transactions': recent_transactions, 
        'loan_applications': loan_applications,
        'atm_requests': atm_requests,
        'user': request.user
    })"""

views_new = """@login_required
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
    })"""

views_content = views_content.replace(views_old, views_new)
with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)

print("Successfully patched backend files")
