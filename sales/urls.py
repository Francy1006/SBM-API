from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    CustomerViewSet,
    FiscalDocumentationViewSet,
    FiscalDocumentTypeViewSet,
    OrderDetailViewSet,
    OrderFiscalDocumentationViewSet,
    OrderTypeViewSet,
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-details', OrderDetailViewSet, basename='order-details')
router.register(r'order-types', OrderTypeViewSet, basename='order-types')
router.register(r'order-fiscal-documentations', OrderFiscalDocumentationViewSet, basename='order-fiscal-documentations')
router.register(r'fiscal-document-types', FiscalDocumentTypeViewSet, basename='fiscal-document-types')
router.register(r'fiscal-documentations', FiscalDocumentationViewSet, basename='fiscal-documentations')

urlpatterns = [
    path('', include(router.urls)),
]