from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PriceListViewSet, PriceItemViewSet,
    PriceDiscountViewSet, PriceHistoryViewSet,
    PriceConfigurationDirectivesView,
    PriceFormulaView,
    PriceConfigurationViewSet,
    PriceConfigurationFormulaView,
    VariableFormulaView,
    PriceCalculationFormulaView,
)

router = DefaultRouter()
router.register(r'lists', PriceListViewSet)
router.register(r'items', PriceItemViewSet)
router.register(r'discounts', PriceDiscountViewSet)
router.register(r'history', PriceHistoryViewSet)
router.register(r'price-configurations', PriceConfigurationViewSet, basename='price-configuration')

urlpatterns = [
    path('', include(router.urls)),
    path('price-configuration-directives/', PriceConfigurationDirectivesView.as_view(), name='price-configuration-directives'),
    path('price-formula/', PriceFormulaView.as_view(), name='price-formula'),
    path('price-configuration-formula/', PriceConfigurationFormulaView.as_view(), name='price-configuration-formula'),
    path('formula-variables/', VariableFormulaView.as_view(), name='formula-variables'),
    path('product-price-calculation/', PriceCalculationFormulaView.as_view(), name='product-price-calculation'),
] 