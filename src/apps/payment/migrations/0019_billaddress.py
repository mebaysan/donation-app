# Generated by Django 5.0.8 on 2024-09-27 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0018_donationtransaction_client_ip_address"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BillAddress",
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
                ("address_name", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=255)),
                ("addr_state", models.CharField(max_length=255)),
                ("add_line", models.CharField(max_length=255)),
                ("postal_code", models.CharField(max_length=255)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]