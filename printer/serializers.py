from rest_framework import serializers

from printer.models import Printer
from receipt.serializers import ReceiptSerializer


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("id", "name", "api_key", "check_type", "point_id")


class PrinterListSerializer(PrinterSerializer):
    class Meta:
        model = Printer
        fields = ("id", "name", "api_key", "check_type", "point_id")


class PrinterDetailSerializer(PrinterSerializer):
    receipts = ReceiptSerializer(many=True, read_only=True)

    class Meta:
        model = Printer
        fields = ("id", "name", "api_key",
                  "check_type", "point_id", "receipts")


class PrinterUpdateSerializer(PrinterSerializer):
    receipts = ReceiptSerializer(many=True, read_only=True)

    class Meta:
        model = Printer
        fields = ("id", "name", "api_key",
                  "check_type", "point_id", "receipts")
