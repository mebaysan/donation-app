# Generated by Django 4.1.9 on 2023-05-29 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0011_bank_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bank",
            name="order",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
