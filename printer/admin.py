from django.contrib import admin

from receipt.models import Printer


class PrinterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_key", "check_type", "point_id")
    list_filter = ("check_type",)


admin.site.register(Printer, PrinterAdmin)
