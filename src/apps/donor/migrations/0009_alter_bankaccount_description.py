# Generated by Django 4.1.5 on 2023-03-20 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0008_bankaccount_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankaccount",
            name="description",
            field=models.CharField(blank=True, default="", max_length=500, null=True),
        ),
    ]