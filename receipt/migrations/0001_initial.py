# Generated by Django 4.2.4 on 2023-09-03 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("printer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Receipt",
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
                    "type",
                    models.CharField(
                        choices=[("kitchen", "Kitchen"), ("client", "Client")],
                        max_length=10,
                    ),
                ),
                ("order", models.JSONField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("rendered", "Rendered"),
                            ("printed", "Printed"),
                        ],
                        default="new",
                        max_length=10,
                    ),
                ),
                (
                    "pdf_file",
                    models.FileField(blank=True, null=True, upload_to="media/pdf"),
                ),
                (
                    "printer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receipts",
                        to="printer.printer",
                    ),
                ),
            ],
        ),
    ]