from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, SaleViewSet, SaleItemViewSet,
    SalePaymentViewSet, SalesOrderViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'items', SaleItemViewSet)
router.register(r'payments', SalePaymentViewSet)
router.register(r'orders', SalesOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 