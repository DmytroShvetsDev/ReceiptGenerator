from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ReceiptGenerator.tasks import produce_receipt
from printer.models import Printer
from receipt.models import Receipt
from receipt.serializers import OrderSerializer, ReceiptSerializer


@extend_schema(
    description="""this endpoint accepts JSON from ERP.
    (Ex. {"point_id": 1,"order_number": 1,"type": "client",
    "order_data": [{"name": "banana","price": 20,"count": 2},...]})"""
)
class CreateReceipt(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            order_number = validated_data.get("order_number")
            point_id = validated_data.get("point_id")
            printers = Printer.objects.filter(point_id=point_id)

            if not printers:
                return Response(
                    {"message": "This point has no printers."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            receipts = []
            for printer in printers:
                receipt = Receipt(
                    printer=printer,
                    type=printer.check_type,
                    order=validated_data,
                    order_number=order_number,
                    point_id=point_id
                )
                receipts.append(receipt)

            try:
                Receipt.objects.bulk_create(receipts)
            except IntegrityError:
                return Response(
                    {
                        "message": "Receipts for this order have already been created."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for receipt in receipts:
                produce_receipt.delay(receipt.id)

            return Response(
                {"message": "Receipts were created."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(description="This endpoint displays all receipts")
class ListReceipts(ListAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
