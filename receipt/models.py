from django.db import models

from printer.models import Printer

CHECK_TYPE_CHOICES = (
    ("kitchen", "Kitchen"),
    ("client", "Client"),
)
STATUS_CHOICES = (
    ("new", "New"),
    ("rendered", "Rendered"),
    ("printed", "Printed"),
)


class Receipt(models.Model):
    printer = models.ForeignKey(
        Printer, on_delete=models.CASCADE, related_name="receipts"
    )
    type = models.CharField(max_length=10, choices=CHECK_TYPE_CHOICES)
    order = models.JSONField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="new"
    )
    pdf_file = models.FileField(upload_to="media/pdf", null=True, blank=True)
