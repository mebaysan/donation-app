# Generated by Django 4.1.5 on 2023-01-28 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("donor", "0006_alter_donationitem_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="donationtransaction",
            name="donation_item",
        ),
        migrations.AlterField(
            model_name="donationtransaction",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=16),
        ),
        migrations.CreateModel(
            name="Donation",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=16)),
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
        migrations.AddField(
            model_name="donationtransaction",
            name="donations",
            field=models.ManyToManyField(
                related_name="transaction", to="donor.donation"
            ),
        ),
    ]
