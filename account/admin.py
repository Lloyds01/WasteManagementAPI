# account/admin.py
from django.contrib import admin
from .models import Transaction  # Import other models as needed

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_ref', 'user', 'amount', 'transaction_type', 'transaction_status', 'created_at')
    list_filter = ('transaction_status', 'transaction_type', 'created_at', 'is_disbursed')
    search_fields = ('user__email', 'transaction_ref', 'beneficiary_account_name', 'narration')
    readonly_fields = ('transaction_ref', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'amount', 'transaction_ref', 'transaction_status', 'transaction_type', 'narration')
        }),
        ('Beneficiary Details', {
            'fields': ('beneficiary_account_number', 'beneficiary_bank_code', 'beneficiary_bank_name', 'beneficiary_account_name')
        }),
        ('Source Details', {
            'fields': ('source_account_name', 'source_account_number', 'source_bank_code')
        }),
        ('Balance Information', {
            'fields': ('balance_before', 'balance_after')
        }),
        ('Disbursement Information', {
            'fields': ('disbursement_source', 'attempt_payout', 'is_disbursed', 'escrow_id')
        }),
        ('Additional Information', {
            'fields': ('metadata', 'created_at', 'updated_at')
        }),
    )