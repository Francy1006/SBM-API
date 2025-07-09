from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PriceListViewSet, PriceItemViewSet,
    PriceDiscountViewSet, PriceHistoryViewSet
)

router = DefaultRouter()
router.register(r'lists', PriceListViewSet)
router.register(r'items', PriceItemViewSet)
router.register(r'discounts', PriceDiscountViewSet)
router.register(r'history', PriceHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 