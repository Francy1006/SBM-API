from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseViewSet, InventoryItemViewSet, InventoryMovementViewSet,
    InventoryCountViewSet, InventoryCountItemViewSet,
    PackageViewSet, PackageTypeViewSet, TransportTypeViewSet, MeasureUnitViewSet
)

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'items', InventoryItemViewSet)
router.register(r'movements', InventoryMovementViewSet)
router.register(r'counts', InventoryCountViewSet)
router.register(r'count-items', InventoryCountItemViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'package-types', PackageTypeViewSet)
router.register(r'transport-types', TransportTypeViewSet)
router.register(r'measure-units', MeasureUnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 