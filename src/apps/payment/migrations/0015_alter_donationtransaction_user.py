# Generated by Django 4.1.5 on 2023-02-27 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("payment", "0014_donationtransaction_group_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="donationtransaction",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="donation_transactions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]