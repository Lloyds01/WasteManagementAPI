from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import DateFieldListFilter
from .models import Transaction
from waste_auth.resources import *
from .models import *

class AccountSystemResourceAdmin(ImportExportModelAdmin):
    resource_class = AccountSystemResource
    search_fields = ("",)
    list_filter = ()
    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

class WalletResourceAdmin(ImportExportModelAdmin):
    resource_class = WalletResource
    search_fields = ("",)
    list_filter = ()
    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user__email', 'description')  

admin.site.register(AccountSystem, AccountSystemResourceAdmin)
admin.site.register(Wallet, WalletResourceAdmin)