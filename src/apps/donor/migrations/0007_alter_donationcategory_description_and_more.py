# Generated by Django 4.1.5 on 2023-03-11 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0006_bankaccount_account_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donationcategory",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="donationitem",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
