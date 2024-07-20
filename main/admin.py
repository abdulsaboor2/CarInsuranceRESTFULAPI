from django.contrib import admin
from .models import Account, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance', 'account_type', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'account_number')
    list_filter = ('account_type', 'status', 'created_at')
    readonly_fields = ('account_number', 'created_at', 'updated_at')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'sender', 'receiver', 'amount', 'created_at', 'updated_at')
    search_fields = ('transaction_id', 'sender__account_number', 'receiver__account_number')
    list_filter = ('created_at',)
    readonly_fields = ('transaction_id', 'created_at', 'updated_at')

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
