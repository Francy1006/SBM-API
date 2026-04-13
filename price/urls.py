from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PriceListViewSet,
    PriceItemViewSet,
    PriceDiscountViewSet,
    PriceHistoryViewSet,
    PriceFormulaView,
    PriceConfigurationViewSet,
    PriceConfigurationFormulaView,
    PriceCalculationFormulaView,
    VariableFormulaView,
    ProductPriceHistoryView,
)

router = DefaultRouter()
router.register(r"lists", PriceListViewSet)
router.register(r"items", PriceItemViewSet)
router.register(r"discounts", PriceDiscountViewSet)
router.register(r"history", PriceHistoryViewSet)
router.register(
    r"price-configurations", PriceConfigurationViewSet, basename="price-configuration"
)

urlpatterns = [
    path("price-formula/", PriceFormulaView.as_view(), name="price-formula"),
    path(
        "price-configuration-formula/",
        PriceConfigurationFormulaView.as_view(),
        name="price-configuration-formula",
    ),
    path("formula-variables/", VariableFormulaView.as_view(), name="formula-variables"),
    path(
        "product-price-calculation/",
        PriceCalculationFormulaView.as_view(),
        name="product-price-calculation",
    ),
    path(
        "product/prices/<str:sku>/",
        ProductPriceHistoryView.as_view(),
        name="product-price-history",
    ),
    path("", include(router.urls)),
]