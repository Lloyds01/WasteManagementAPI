# Generated by Django 4.2 on 2025-02-17 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waste_auth", "0006_alter_agentassignment_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wasteproduct",
            name="pickup_date",
            field=models.DateTimeField(),
        ),
    ]
