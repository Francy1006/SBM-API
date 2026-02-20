from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CatalogViewSet,
    ProductViewSet,
    MaterialViewSet,
    ServiceViewSet,
    MenuViewSet,
    ItemGroupViewSet,
    ItemCategoryViewSet,
    ItemTypeViewSet,
    RestrictionViewSet,
    InstructionViewSet,
    InstructionTypeViewSet,
    ItemConfigurationViewSet,
    PackageViewSet,
    PackageTypeViewSet,
    TransportTypeViewSet,
    MeasureUnitViewSet,
)

router = DefaultRouter()

router.register(r'catalogs', CatalogViewSet, basename='catalog')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'item-groups', ItemGroupViewSet, basename='item-group')
router.register(r'item-categories', ItemCategoryViewSet, basename='item-category')
router.register(r'item-types', ItemTypeViewSet, basename='item-type')
router.register(r'restrictions', RestrictionViewSet, basename='restriction')
router.register(r'instructions', InstructionViewSet, basename='instruction')
router.register(r'instruction-types', InstructionTypeViewSet, basename='instruction-type')
router.register(r'item-configurations', ItemConfigurationViewSet, basename='item-configuration')
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'package-types', PackageTypeViewSet, basename='package-type')
router.register(r'transport-types', TransportTypeViewSet, basename='transport-type')
router.register(r'measure-units', MeasureUnitViewSet, basename='measure-unit')

urlpatterns = [
    path('', include(router.urls)),
]
