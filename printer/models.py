from django.db import models


CHECK_TYPE_CHOICES = (
    ("kitchen", "Kitchen"),
    ("client", "Client"),
)


class Printer(models.Model):
    name = models.CharField(max_length=63)
    api_key = models.CharField(max_length=255, unique=True)
    check_type = models.CharField(max_length=10, choices=CHECK_TYPE_CHOICES)
    point_id = models.IntegerField()

    def __str__(self):
        return f"Printer {self.name}"
