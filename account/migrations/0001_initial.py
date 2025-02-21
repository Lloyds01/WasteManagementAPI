# Generated by Django 4.2 on 2025-02-17 11:06

from django.conf import settings
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
                (
                    "account_type",
                    models.CharField(
                        blank=True,
                        choices=[("FLOAT", "FLOAT"), ("COLLECTION", "COLLECTION")],
                        max_length=250,
                        null=True,
                    ),
                ),
                ("bank_code", models.CharField(blank=True, max_length=250, null=True)),
                ("is_active", models.BooleanField(default=True)),
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
