# Generated by Django 4.2 on 2025-02-17 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_accountsystem_bvn"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="accountsystem",
            name="bvn",
        ),
    ]
