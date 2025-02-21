# Generated by Django 4.2 on 2025-02-17 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("waste_auth", "0003_alter_user_options_wasteproduct_schedule"),
    ]

    operations = [
        migrations.CreateModel(
            name="AgentAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "AGENT ASSIGNMENT",
                "verbose_name_plural": "AGENT ASSIGNMENTS",
                "ordering": ["-assigned_at"],
            },
        ),
        migrations.AddField(
            model_name="wasteproduct",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="waste_products/"),
        ),
        migrations.AddField(
            model_name="wasteproduct",
            name="pickup_date",
            field=models.DateTimeField(default="2023-10-26 10:00:00"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="wasteproduct",
            name="pickup_location",
            field=models.CharField(default="2023-10-26 10:00:00", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="wasteproduct",
            name="remarks",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="wasteproduct",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "pending"),
                    ("COMPLETED", "completed"),
                    ("CANCELLED", "cancelled"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
        migrations.DeleteModel(
            name="Schedule",
        ),
        migrations.AddField(
            model_name="agentassignment",
            name="waste_product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assignments",
                to="waste_auth.wasteproduct",
            ),
        ),
    ]
