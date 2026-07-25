import os

admin_path = "banking/admin.py"
with open(admin_path, 'r', encoding='utf-8') as f:
    content = f.read()

admin_old = """@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')
    search_fields = ('sender__account_number', 'receiver__account_number', 'description', 'pending_reason')
    list_filter = ('transaction_type', 'status', 'timestamp')
    list_editable = ('status', 'progress_percentage', 'pending_reason')
    readonly_fields = ('timestamp',)"""

admin_new = """@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')
    search_fields = ('sender__account_number', 'receiver__account_number', 'description', 'pending_reason')
    list_filter = ('transaction_type', 'status', 'timestamp')
    list_editable = ('status', 'progress_percentage', 'pending_reason')
    readonly_fields = ('timestamp',)
    fields = ('sender', 'receiver', 'amount', 'description', 'transaction_type', 'status', 'progress_percentage', 'pending_reason', 'timestamp')"""

content = content.replace(admin_old, admin_new)
with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched admin.py")
