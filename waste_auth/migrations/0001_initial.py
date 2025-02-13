# Generated by Django 4.2 on 2025-02-13 14:04

from django.db import migrations, models
import uuid
import waste_auth.helpers.reusable
import waste_auth.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="OTP",
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
                ("type", models.CharField(max_length=255)),
                ("recipient", models.CharField(max_length=255)),
                ("length", models.IntegerField()),
                ("expiry_time", models.IntegerField()),
                ("code", models.CharField(max_length=255)),
                ("is_used", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "ONE TIME PASSWORD",
                "verbose_name_plural": "ONE TIME PASSWORDS",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
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
                ("first_name", models.CharField(max_length=255)),
                (
                    "middle_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("email_verified", models.BooleanField(default=False)),
                (
                    "password",
                    models.CharField(
                        editable=False,
                        max_length=255,
                        validators=[waste_auth.helpers.reusable.validate_password],
                    ),
                ),
                ("phone_number", models.CharField(max_length=25, unique=True)),
                ("phone_verified", models.BooleanField(default=False)),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("MALE", "male"), ("FEMALE", "female")], max_length=10
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "user_type",
                    models.CharField(
                        choices=[("AGENT", "agent"), ("USER", "user")], max_length=12
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "USER",
                "verbose_name_plural": "USER",
                "ordering": ["-created_at"],
            },
            managers=[
                ("objects", waste_auth.managers.UserManager()),
            ],
        ),
    ]
