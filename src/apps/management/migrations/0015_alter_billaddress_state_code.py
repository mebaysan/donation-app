# Generated by Django 5.0.8 on 2024-09-28 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0014_alter_billaddress_country_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billaddress",
            name="state_code",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
