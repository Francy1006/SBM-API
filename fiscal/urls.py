from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FiscalDocumentViewSet, FiscalItemViewSet,
    TaxRateViewSet, FiscalPaymentViewSet
)

router = DefaultRouter()
router.register(r'documents', FiscalDocumentViewSet)
router.register(r'items', FiscalItemViewSet)
router.register(r'taxes', TaxRateViewSet)
router.register(r'payments', FiscalPaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 