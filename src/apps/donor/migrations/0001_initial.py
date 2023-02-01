# Generated by Django 4.1.5 on 2023-02-01 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DonationCategory",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="donation_category/"
                    ),
                ),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Donation Category",
                "verbose_name_plural": "Donation Categories",
            },
        ),
        migrations.CreateModel(
            name="DonationItem",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="donation_item/"
                    ),
                ),
                ("is_published", models.BooleanField(default=True)),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="items",
                        to="donor.donationcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Donation Item",
                "verbose_name_plural": "Donation Items",
            },
        ),
    ]
