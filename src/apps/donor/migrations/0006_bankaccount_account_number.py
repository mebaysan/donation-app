# Generated by Django 4.1.5 on 2023-03-05 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0005_bankaccount_bank"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankaccount",
            name="account_number",
            field=models.CharField(default="", max_length=500),
        ),
    ]
