# Generated by Django 4.1.5 on 2023-01-25 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentprovider",
            name="is_provider",
            field=models.BooleanField(default=False),
        ),
    ]
