# Generated by Django 4.1.5 on 2023-01-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0003_remove_donationtransaction_donation_item_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donationtransaction",
            name="donation_item",
            field=models.ManyToManyField(to="donor.donationitem"),
        ),
    ]
