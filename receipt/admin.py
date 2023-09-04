from django.contrib import admin

from receipt.models import Receipt


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "printer", "type", "status", "pdf_file")
    list_filter = ("printer", "type", "status")


admin.site.register(Receipt, ReceiptAdmin)
