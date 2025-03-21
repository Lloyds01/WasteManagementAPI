from django.db import models
from django.conf import settings
from waste_auth.models import BaseModel, User
from waste_auth.enums import (
    AccountType,
    DisbursementFormType,
    TransactionEntry,
    TransactionStatus,
    TransactionType,
    WalletType,
)
from django.core.validators import MinValueValidator
import uuid
from account.helpers.reusable import generate_account_number

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
    is_test = models.BooleanField(default=False)
    account_type = models.CharField(
        max_length=250, choices=AccountType.choices,default=AccountType.COLLECTION, null=True, blank=True
    )
    bank_code = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    available_balance = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    updated = models.BooleanField(default=False)
    payload = models.TextField(null=True)

    def __str__(self) -> str: 
        return str(self.account_name)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "ACCOUNT SYSTEM"
        verbose_name_plural = "ACCOUNT SYSTEM"


    @classmethod
    def create_account(cls,user,
        account_provider, account_name, bank_name, bank_code, 
        ):
        account_number=generate_account_number()
        account = cls.objects.create(
            user=user,
            account_provider="VFD",
            account_number=account_number,
            account_name=account_name,
            bank_name="VFD Microfinance Bank",
            bank_code="999999",
            payload=""
            )
        Wallet.create_wallet_object(account_ins=account, user=user, wallet_type= WalletType.SPEND)
        return account


class AccountCreationFailure(BaseModel):
    account_id = models.UUIDField(default=uuid.uuid4, editable=False)
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
        ordering = ["-created_at"]
        verbose_name = "ACCOUNT CREATION FAILURE"
        verbose_name_plural = "ACCOUNT CREATION FAILURE"


class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    wallet_id = models.UUIDField(default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        AccountSystem, on_delete=models.CASCADE, null=True, blank=True
    )
    available_balance = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    previous_balance = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0)]
    )
    wallet_type = models.CharField(
        max_length=250,
        choices=AccountType.choices,
        default=WalletType.SPEND,
    )
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="wallets", on_delete=models.CASCADE)
    # tracker = FieldTracker()
    
    def __str__(self) -> str:
        return f"wallet-{self.id}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "WALLET SYSTEM"
        verbose_name_plural = "WALLET SYSTEM"

    def save(self, *args, **kwargs):

        try:
            if self.pk:
                self.previous_balance = self.available_balance

            return super(Wallet, self).save(*args, **kwargs)
        except Exception as err:
            raise Exception(f"{err}")

    @classmethod
    def create_wallet_object(cls, account_ins, user, wallet_type):
        wallet_ins = cls.objects.create(
            user=user, account=account_ins, wallet_type=wallet_type
        )
        return wallet_ins

    @classmethod
    def create_user_wallet(cls, data, user_id, account_type, company_id=None):

        create_account_response = VfdBank.create_wallet(**data)

        if company_id is None:
            status_code = create_account_response.get("status")
            if status_code == "00":
                data = create_account_response.get("data")
                _account_instance = AccountSystem.objects.filter(
                    user_id=user_id, account_type=account_type
                )

                if not _account_instance.exists():

                    account = AccountSystem.objects.create(
                        user_id=user_id,
                        account_provider="VFD",
                        account_number=data.get("accountNo"),
                        account_name=f'{data.get("firstname")} {data.get("lastname")}',
                        account_type=account_type,
                        bank_name="VFD Microfinance Bank",
                        bank_code="999999",
                        payload=create_account_response,
                    )

                    _create_wallet = cls.objects.create(
                        user_id=user_id, account=account, wallet_type=account_type
                    )

                    return _create_wallet

                else:
                    return None

            elif (
                status_code == "929"
                and create_account_response.get("message") == "BVN Exist"
            ):
                # add number to bvn
                user_bvn = data.get("bvn")
                phone = data.get("phone")
                result = user_bvn.split("-")
                phone_result = phone.split("-")
                extrated_phone = phone_result[0]

                bvn = result[0]
                number_to_add = (
                    int(result[1])
                    + ConstantTable.get_constant_instance().to_add_num_bvn
                )

                data["phone"] = f"{extrated_phone}-{number_to_add}"
                data["bvn"] = f"{bvn}-{number_to_add}"
                create_account_response = VfdBank.create_wallet(**data)

                status_code = create_account_response.get("status")

                if status_code == "00":
                    data = create_account_response.get("data")
                    _account_instance = AccountSystem.objects.filter(
                        user_id=user_id, account_type=account_type
                    )

                    if not _account_instance.exists():
                        account = AccountSystem.objects.create(
                            user_id=user_id,
                            account_provider="VFD",
                            account_number=data.get("accountNo"),
                            account_name=f'{data.get("firstname")} {data.get("lastname")}',
                            account_type=account_type,
                            bank_name="VFD Microfinance Bank",
                            bank_code="999999",
                            payload=create_account_response,
                        )

                        _create_wallet = cls.objects.create(
                            user_id=user_id, account=account, wallet_type=account_type
                        )

                        return _create_wallet

                else:
                    AccountCreationFailure.objects.create(
                        user_id=user_id,
                        payload=create_account_response,
                        account_type=account_type,
                        request_payload=data,
                        account_provider="VFD",
                    )
                return None

        else:
            if create_account_response.get("status") == "00":
                data = create_account_response.get("data")

                account = AccountSystem.objects.create(
                    user_id=user_id,
                    account_provider="VFD",
                    company_id=company_id,
                    account_number=data.get("accountNo"),
                    account_name=f'{data.get("firstname")} {data.get("lastname")}',
                    account_type=account_type,
                    bank_name="VFD Microfinance Bank",
                    bank_code="999999",
                    payload=create_account_response,
                )

                _create_wallet = cls.objects.create(
                    user_id=user_id, account=account, wallet_type=account_type
                )

                return _create_wallet
            else:
                AccountCreationFailure.objects.create(
                    user_id=user_id,
                    payload=create_account_response,
                    account_type=account_type,
                    account_provider="VFD",
                    request_payload=data,
                )
                return None
            
# def generate_ref():
#     return str(uuid.uuid4())

class Transaction(BaseModel):
    
    user = models.ForeignKey(
        User, related_name="transactions", on_delete=models.CASCADE
    )
    amount = models.FloatField(validators=[MinValueValidator(0)])
    transaction_ref = models.UUIDField(default=uuid.uuid4, editable=False)
    transaction_status = models.CharField(
        max_length=300,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    disbursement_source = models.CharField(
        max_length=300, choices=DisbursementFormType.choices, null=True, blank=True)
    beneficiary_account_number = models.CharField(max_length=300, null=True, blank=True)
    beneficiary_bank_code = models.CharField(max_length=300, null=True, blank=True)
    beneficiary_bank_name = models.CharField(max_length=300, null=True, blank=True)
    beneficiary_account_name = models.CharField(max_length=300, null=True, blank=True)
    
    # --------------------balances-------------------------
    balance_before = models.FloatField(null=True, blank=True)
    balance_after = models.FloatField(null=True, blank=True)
    # ------------------------------------------------------
    source_account_name = models.CharField(max_length=300, null=True, blank=True)
    source_account_number = models.CharField(max_length=300, null=True, blank=True)
    source_bank_code = models.CharField(max_length=300, null=True, blank=True)
    transaction_type = models.CharField(
        max_length=300, choices=TransactionType.choices, null=True, blank=True
    )
    narration = models.CharField(max_length=500, null=True, blank=True)
    attempt_payout = models.BooleanField(default=False)
    is_disbursed = models.BooleanField(default=False)
    escrow_id = models.CharField(max_length=300, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "TRANSACTIONS"
        verbose_name_plural = "TRANSACTIONS"