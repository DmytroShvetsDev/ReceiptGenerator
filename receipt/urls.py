from django.urls import path

from receipt.views import CreateReceipt, ListReceipts

app_name = "receipt"

urlpatterns = [
    path("create/", CreateReceipt.as_view(), name="create"),
    path("list/", ListReceipts.as_view(), name="list-receipts"),
]
