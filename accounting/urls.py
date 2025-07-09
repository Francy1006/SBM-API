from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PriceViewSet, PriceFiscalConfigurationViewSet, FiscalConfigurationDetailViewSet,
    FiscalDirectiveViewSet, FiscalDirectiveTypeViewSet, FiscalFormulaViewSet
)

# Crear el router para los ViewSets
router = DefaultRouter()
router.register(r'prices', PriceViewSet, basename='price')
router.register(r'price-fiscal-configurations', PriceFiscalConfigurationViewSet, basename='price-fiscal-configuration')
router.register(r'fiscal-configuration-details', FiscalConfigurationDetailViewSet, basename='fiscal-configuration-detail')
router.register(r'fiscal-directives', FiscalDirectiveViewSet, basename='fiscal-directive')
router.register(r'fiscal-directive-types', FiscalDirectiveTypeViewSet, basename='fiscal-directive-type')
router.register(r'fiscal-formulas', FiscalFormulaViewSet, basename='fiscal-formula')

app_name = 'accounting'

urlpatterns = [
    # Incluir todas las rutas del router
    path('', include(router.urls)),
] 