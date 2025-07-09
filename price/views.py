from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import PriceList, PriceItem, PriceDiscount, PriceHistory
from .serializers import (
    PriceListSerializer, PriceItemSerializer,
    PriceDiscountSerializer, PriceHistorySerializer
)

# Create your views here.

class PriceListViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceList
    """
    queryset = PriceList.objects.select_related('franchise', 'created_by').prefetch_related('items')  # type: ignore
    serializer_class = PriceListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_default', 'franchise', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']


class PriceItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceItem
    """
    queryset = PriceItem.objects.select_related('price_list', 'catalog_item', 'created_by')  # type: ignore
    serializer_class = PriceItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price_list', 'catalog_item', 'created_by']
    search_fields = ['catalog_item__name', 'price_list__name']
    ordering_fields = ['price', 'cost', 'margin', 'created_at']
    ordering = ['price_list', 'catalog_item']


class PriceDiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceDiscount
    """
    queryset = PriceDiscount.objects.select_related('franchise', 'created_by')  # type: ignore
    serializer_class = PriceDiscountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['discount_type', 'is_active', 'franchise', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['discount_value', 'valid_from', 'valid_until', 'created_at']
    ordering = ['-created_at']


class PriceHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceHistory
    """
    queryset = PriceHistory.objects.select_related('price_item', 'changed_by')  # type: ignore
    serializer_class = PriceHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price_item', 'changed_by']
    search_fields = ['change_reason']
    ordering_fields = ['old_price', 'new_price', 'changed_at']
    ordering = ['-changed_at']
