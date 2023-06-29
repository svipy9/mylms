# Generated by Django 4.2.2 on 2023-06-29 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_squad_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                ("url", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("init", "Initial"),
                            ("success", "Successful"),
                            ("failed", "Failed"),
                            ("refunded", "Refunded"),
                        ],
                        default="init",
                        max_length=20,
                    ),
                ),
                (
                    "admission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.admission"
                    ),
                ),
            ],
        ),
    ]
