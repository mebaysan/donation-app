# Generated by Django 5.0.8 on 2024-09-27 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0020_delete_billaddress"),
    ]

    operations = [
        migrations.AddField(
            model_name="donationtransaction",
            name="add_line",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="donationtransaction",
            name="country",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="donationtransaction",
            name="postal_code",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="donationtransaction",
            name="state_code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="donationtransaction",
            name="state_province",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]