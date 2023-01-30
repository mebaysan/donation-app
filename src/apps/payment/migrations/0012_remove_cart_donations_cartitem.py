# Generated by Django 4.1.5 on 2023-01-29 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0015_donation_user"),
        ("payment", "0011_cart_donations"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="donations",
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "added_date",
                    models.DateTimeField(auto_created=True, auto_now_add=True),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=16),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_items",
                        to="payment.cart",
                    ),
                ),
                (
                    "donation_item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="donor.donationitem",
                    ),
                ),
            ],
        ),
    ]
