from django.urls import path, include
from rest_framework import routers

from printer.views import PrinterViewSet

router = routers.DefaultRouter()
router.register("", PrinterViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "printer"
