from rest_framework import serializers

from receipt.models import Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ("id", "status", "pdf_file")


class OrderSerializer(serializers.Serializer):
    point_id = serializers.IntegerField()
    order_number = serializers.CharField()
    type = serializers.ChoiceField(choices=["kitchen", "client"])
    order_data = serializers.JSONField()
