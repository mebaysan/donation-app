# Generated by Django 4.1.5 on 2023-01-30 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0005_user_is_approved_to_be_in_touch"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
