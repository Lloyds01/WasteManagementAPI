from import_export import resources
from .models import *
from account.models import (AccountSystem, Wallet, Transaction)



class UserResource(resources.ModelResource):
    class Meta:
        model = User

    class Meta:
        model = OTP

class AgentAssignmentResource(resources.ModelResource):
    class Meta:
        model = AgentAssignment

class WasteProductResource(resources.ModelResource):
    class Meta:
        model = WasteProduct

class AccountSystemResource(resources.ModelResource):
    class Meta:
        model = AccountSystem

class WalletResource(resources.ModelResource):
    class Meta:
        model = Wallet

class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction

class OTPResource(resources.ModelResource):
    class Meta:
        model = OTP