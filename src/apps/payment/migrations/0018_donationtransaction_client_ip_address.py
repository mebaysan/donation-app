# Generated by Django 5.0.8 on 2024-09-01 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0017_alter_donationtransaction_donation_platform_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="donationtransaction",
            name="client_ip_address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
