# Generated by Django 4.1.5 on 2023-02-01 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0006_remove_donationtransaction_donor_profile_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="donation",
            old_name="donor_profile",
            new_name="user",
        ),
    ]
