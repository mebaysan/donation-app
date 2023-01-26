# Generated by Django 4.1.5 on 2023-01-26 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0004_alter_donationtransaction_donation_item"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="donationcategory",
            options={
                "verbose_name": "Donation Category",
                "verbose_name_plural": "Donation Categories",
            },
        ),
        migrations.AlterModelOptions(
            name="donationitem",
            options={
                "verbose_name": "Donation Item",
                "verbose_name_plural": "Donation Items",
            },
        ),
        migrations.AlterModelOptions(
            name="donationtransaction",
            options={
                "verbose_name": "Donation Transaction",
                "verbose_name_plural": "Donation Transactions",
            },
        ),
        migrations.AddField(
            model_name="donationcategory",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="donationitem",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
    ]
