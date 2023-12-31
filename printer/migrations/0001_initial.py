# Generated by Django 4.2.4 on 2023-09-05 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Printer",
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
                ("name", models.CharField(max_length=63)),
                ("api_key", models.CharField(max_length=255, unique=True)),
                (
                    "check_type",
                    models.CharField(
                        choices=[("kitchen", "Kitchen"), ("client", "Client")],
                        max_length=10,
                    ),
                ),
                ("point_id", models.IntegerField()),
            ],
        ),
    ]
