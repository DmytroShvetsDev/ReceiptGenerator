from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from printer.models import Printer
from printer.serializers import (
    PrinterSerializer,
    PrinterListSerializer,
    PrinterDetailSerializer,
    PrinterUpdateSerializer,
)
from receipt.models import Receipt, STATUS_PRINTED


class PrinterViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PrinterListSerializer

        if self.action == "retrieve":
            return PrinterDetailSerializer

        if self.action == "update":
            return PrinterUpdateSerializer

        return PrinterSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        receipt = Receipt.objects.filter(printer_id=instance)
        if receipt.exists():
            receipt.update(status=STATUS_PRINTED)

        return Response(serializer.data, status=status.HTTP_200_OK)
