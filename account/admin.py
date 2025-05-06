from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import DateFieldListFilter
from .models import Transaction
from waste_auth.resources import *
from .models import *


class WalletResourceAdmin(ImportExportModelAdmin):
    resource_class = WalletResource
    search_fields = ("",)
    list_filter = (("created_at", DateFieldListFilter),
    )

    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data


class TransactionResourceAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource
    search_fields = ("",)
    list_filter = (("created_at", DateFieldListFilter),
    )

    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

class AccountSystemResourceAdmin(ImportExportModelAdmin):
    resource_class = AccountSystemResource
    search_fields = ("",)
    list_filter = (("created_at", DateFieldListFilter),
    )
    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

admin.site.register(AccountSystem, AccountSystemResourceAdmin)
admin.site.register(Wallet, WalletResourceAdmin)
admin.site.register(Transaction, TransactionResourceAdmin)