# Generated by Django 5.0.8 on 2024-10-13 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0013_alter_donationcategory_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="donationitem",
            name="order",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
