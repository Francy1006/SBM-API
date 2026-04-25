from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PriceViewSet, FiscalConfigurationDetailViewSet,
    FiscalDirectiveViewSet, FiscalDirectiveTypeViewSet, FiscalDirectiveStatsViewSet
)

router = DefaultRouter()
router.register(r'prices', PriceViewSet, basename='price')
router.register(r'fiscal-configuration-details', FiscalConfigurationDetailViewSet, basename='fiscal-configuration-detail')
router.register(r'fiscal-directives', FiscalDirectiveViewSet, basename='fiscal-directive')
router.register(r'fiscal-directive-types', FiscalDirectiveTypeViewSet, basename='fiscal-directive-type')

app_name = 'accounting'

urlpatterns = [
    path('fiscal-directives-stats/', FiscalDirectiveStatsViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
]