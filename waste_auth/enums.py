from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class UserType(TextChoices):
    AGENT = "AGENT", "agent"
    USER = "USER", "user"
  

class GenderChoices(TextChoices):
    MALE = "MALE", "male"
    FEMALE = "FEMALE", "female"

class WasteType(TextChoices):
    PLASTIC = "PLASTIC", "plastic"
    METAL = "METAL", "metal"
    GLASS = "GLASS", "glass"
    PAPER = "PAPER", "paper"
    ORGANIC = "ORGANIC", "organic"
    OTHER = "OTHER", "other"

class WasteScheduleStatus(TextChoices):
    PENDING = "PENDING", "pending"
    COMPLETED = "COMPLETED", "completed"
    CANCELLED = "CANCELLED", "cancelled"

class DisbursementFormType(models.TextChoices):
    VFD_WALLET = "VFD_WALLET", _("VFD")
    # WOVEN_SPARKLE = "WOVEN_SPARKLE", _("WOVEN_SPARKLE")
    # WEMA_BANK = "WOVEN_WEMA", _("WOVEN_WEMA")
    MONNIFY = "MONNIFY", _("MONNIFY")


class DisbursementFormType(models.TextChoices):
    VFD_WALLET = "VFD_WALLET", _("VFD")
    WOVEN_SPARKLE = "WOVEN_SPARKLE", _("WOVEN_SPARKLE")
    WEMA_BANK = "WOVEN_WEMA", _("WOVEN_WEMA")
    MONNIFY = "MONNIFY", _("MONNIFY")


class TransactionStatus(TextChoices):
    PENDING = "PENDING", "PENDING"
    FAILED_MANDATE = "FAILED_MANDATE", "FAILED MANDATE"
    REVERSED = "REVERSED", "REVERSED"
    FAILED = "FAILED", "FAILED"
    SUCCESSFUL = "SUCCESSFUL", "SUCCESSFUL"


class TransactionType(TextChoices):
    DISBURSEMENT = "DISBURSEMENT", "DISBURSEMENT"
    REPAYMENT = "REPAYMENT", "REPAYMENT"
    DEPOSIT = "DEPOSIT", "DEPOSIT"


class AccountType(TextChoices):
    FLOAT = "FLOAT", "FLOAT"
    COLLECTION = "COLLECTION", "COLLECTION"

class TransactionEntry(TextChoices):
    DEBIT = "DEBIT", "DEBIT"
    CREDIT = "CREDIT", "CREDIT"
    REVERSAL = "REVERSAL", "REVERSAL"