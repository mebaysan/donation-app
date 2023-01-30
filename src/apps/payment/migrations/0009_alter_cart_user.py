# Generated by Django 4.1.5 on 2023-01-29 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("payment", "0008_alter_cart_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart",
                related_query_name="cart",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
