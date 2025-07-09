from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseViewSet, InventoryItemViewSet, InventoryMovementViewSet,
    InventoryCountViewSet, InventoryCountItemViewSet
)

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'items', InventoryItemViewSet)
router.register(r'movements', InventoryMovementViewSet)
router.register(r'counts', InventoryCountViewSet)
router.register(r'count-items', InventoryCountItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 