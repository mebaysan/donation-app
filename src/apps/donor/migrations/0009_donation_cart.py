# Generated by Django 4.1.5 on 2023-01-28 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0006_remove_cart_donations"),
        ("donor", "0008_remove_donationtransaction_donations_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="cart",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_query_name="donations",
                to="payment.cart",
            ),
        ),
    ]
