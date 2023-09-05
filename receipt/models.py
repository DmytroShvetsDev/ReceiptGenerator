from django.db import models

from ReceiptGenerator.settings import ROOT_PDF_DIRECTORY
from printer.models import Printer

CHECK_TYPE_CHOICES = (
    ("kitchen", "Kitchen"),
    ("client", "Client"),
)

STATUS_NEW = "new"
STATUS_RENDERED = "rendered"
STATUS_PRINTED = "printed"

STATUS_CHOICES = (
    (STATUS_NEW, "New"),
    (STATUS_RENDERED, "Rendered"),
    (STATUS_PRINTED, "Printed"),
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
        default=STATUS_NEW
    )
    pdf_file = models.FileField(upload_to=ROOT_PDF_DIRECTORY, null=True, blank=True)
    order_number = models.IntegerField()
    point_id = models.IntegerField()

    class Meta:
        unique_together = ("order_number", "point_id", "printer_id")
