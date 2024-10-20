# Generated by Django 5.0.8 on 2024-09-28 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0015_alter_billaddress_state_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billaddress",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bill_addresses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
