# Generated by Django 4.2 on 2025-03-14 05:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AccountSystem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "account_provider",
                    models.CharField(
                        choices=[
                            ("VFD_WALLET", "VFD"),
                            ("WOVEN_SPARKLE", "WOVEN_SPARKLE"),
                            ("WOVEN_WEMA", "WOVEN_WEMA"),
                            ("MONNIFY", "MONNIFY"),
                        ],
                        default="VFD_WALLET",
                        max_length=300,
                    ),
                ),
                ("account_number", models.CharField(max_length=250, unique=True)),
                (
                    "account_name",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("bank_name", models.CharField(blank=True, max_length=250, null=True)),
                ("is_test", models.BooleanField(default=False)),
                (
                    "account_type",
                    models.CharField(
                        blank=True,
                        choices=[("FLOAT", "FLOAT"), ("COLLECTION", "COLLECTION")],
                        default="COLLECTION",
                        max_length=250,
                        null=True,
                    ),
                ),
                ("bank_code", models.CharField(blank=True, max_length=250, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "available_balance",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("updated", models.BooleanField(default=False)),
                ("payload", models.TextField(null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "ACCOUNT SYSTEM",
                "verbose_name_plural": "ACCOUNT SYSTEM",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                ("wallet_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "available_balance",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "previous_balance",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "wallet_type",
                    models.CharField(
                        choices=[("FLOAT", "FLOAT"), ("COLLECTION", "COLLECTION")],
                        default="SPEND",
                        max_length=250,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.accountsystem",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wallets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "WALLET SYSTEM",
                "verbose_name_plural": "WALLET SYSTEM",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "amount",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "transaction_ref",
                    models.UUIDField(default=uuid.uuid4, editable=False),
                ),
                (
                    "transaction_status",
                    models.CharField(
                        choices=[
                            ("PENDING", "PENDING"),
                            ("REVERSED", "REVERSED"),
                            ("FAILED", "FAILED"),
                            ("SUCCESSFUL", "SUCCESSFUL"),
                        ],
                        default="PENDING",
                        max_length=300,
                    ),
                ),
                (
                    "disbursement_source",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("VFD_WALLET", "VFD"),
                            ("WOVEN_SPARKLE", "WOVEN_SPARKLE"),
                            ("WOVEN_WEMA", "WOVEN_WEMA"),
                            ("MONNIFY", "MONNIFY"),
                        ],
                        max_length=300,
                        null=True,
                    ),
                ),
                (
                    "beneficiary_account_number",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "beneficiary_bank_code",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "beneficiary_bank_name",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "beneficiary_account_name",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                ("balance_before", models.FloatField(blank=True, null=True)),
                ("balance_after", models.FloatField(blank=True, null=True)),
                (
                    "source_account_name",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "source_account_number",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "source_bank_code",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("DISBURSEMENT", "DISBURSEMENT"),
                            ("WITHDRAWAL", "WITHDRAWAL"),
                            ("UTILITIES", "UTILITIES"),
                            ("DEPOSIT", "DEPOSIT"),
                        ],
                        max_length=300,
                        null=True,
                    ),
                ),
                ("narration", models.CharField(blank=True, max_length=500, null=True)),
                ("attempt_payout", models.BooleanField(default=False)),
                ("is_disbursed", models.BooleanField(default=False)),
                ("escrow_id", models.CharField(blank=True, max_length=300, null=True)),
                ("metadata", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Transactions",
                "verbose_name_plural": "Transactions",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="AccountCreationFailure",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                ("account_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "account_type",
                    models.CharField(
                        blank=True,
                        choices=[("FLOAT", "FLOAT"), ("COLLECTION", "COLLECTION")],
                        max_length=250,
                        null=True,
                    ),
                ),
                (
                    "account_provider",
                    models.CharField(
                        choices=[
                            ("VFD_WALLET", "VFD"),
                            ("WOVEN_SPARKLE", "WOVEN_SPARKLE"),
                            ("WOVEN_WEMA", "WOVEN_WEMA"),
                            ("MONNIFY", "MONNIFY"),
                        ],
                        default="VFD_WALLET",
                        max_length=300,
                    ),
                ),
                ("is_test", models.BooleanField(default=False)),
                ("payload", models.TextField(blank=True, null=True)),
                ("request_payload", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="creation_fails",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Account Creation Failure",
                "verbose_name_plural": "Account Creation Failure",
            },
        ),
    ]
