from django.db import models
from waste_auth.models import BaseModel, User
from waste_auth.enums import (
    AccountType,
    DisbursementFormType,
    TransactionEntry,
    TransactionStatus,
    TransactionType,
)

# Create your models here.
class AccountSystem(BaseModel):
    user = models.ForeignKey(
        User, related_name="accounts", on_delete=models.CASCADE
    )
    account_provider = models.CharField(
        max_length=300,
        choices=DisbursementFormType.choices,
        default=DisbursementFormType.VFD_WALLET,
    )
    account_number = models.CharField(
        max_length=250, unique=True, null=False, blank=False
    )
    account_name = models.CharField(max_length=250, null=True, blank=True)
    bank_name = models.CharField(max_length=250, null=True, blank=True)
    account_type = models.CharField(
        max_length=250, choices=AccountType.choices, null=True, blank=True
    )
    bank_code = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    updated = models.BooleanField(default=False)
    payload = models.TextField(null=True)

    def __str__(self) -> str:
        return str(self.account_name)

    class Meta:
        # ordering = ["-created_at"]
        verbose_name = "ACCOUNT SYSTEM"
        verbose_name_plural = "ACCOUNT SYSTEM"

    @classmethod
    def create_account(cls, user_id,
        account_provider, account_number, account_name, account_type, bank_name, bank_code, payload=None
        ):
        account = cls.objects.create(
        user_id=user_id,
        account_provider="VFD",
        account_number=account_number,
        account_name=account_name,
        account_type=account_type,
        bank_name="VFD Microfinance Bank",
        bank_code="999999",
        payload=create_account_response,)

        return account


class AccountCreationFailure(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creation_fails"
    )
    account_type = models.CharField(
        max_length=250, choices=AccountType.choices, null=True, blank=True
    )
    account_provider = models.CharField(
        max_length=300,
        choices=DisbursementFormType.choices,
        default=DisbursementFormType.VFD_WALLET,
    )
    is_test = models.BooleanField(default=False)
    payload = models.TextField(null=True, blank=True)
    request_payload = models.TextField(null=True, blank=True)

    class Meta:
        # ordering = ["-created_at"]
        verbose_name = "Account Creation Failure"
        verbose_name_plural = "Account Creation Failure"