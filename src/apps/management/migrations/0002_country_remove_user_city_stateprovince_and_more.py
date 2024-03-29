# Generated by Django 4.1.5 on 2023-02-26 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
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
                ("countryCode", models.CharField(max_length=5)),
                ("countryCodeAlpha3", models.CharField(max_length=5)),
                ("phone", models.CharField(max_length=10)),
                ("currency", models.CharField(max_length=5)),
            ],
        ),
        migrations.RemoveField(
            model_name="user",
            name="city",
        ),
        migrations.CreateModel(
            name="StateProvince",
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
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="state_provinces",
                        to="management.country",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="user",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="management.country",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="state",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="management.stateprovince",
            ),
        ),
    ]
