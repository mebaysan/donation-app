# Generated by Django 5.0.8 on 2024-09-27 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0011_alter_country_options_alter_stateprovince_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billaddress",
            name="add_line",
            field=models.CharField(max_length=500),
        ),
    ]
