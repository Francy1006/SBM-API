from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Warehouse, InventoryItem, InventoryMovement, InventoryCount, InventoryCountItem
from .serializers import (
    WarehouseSerializer, InventoryItemSerializer, InventoryMovementSerializer,
    InventoryCountSerializer, InventoryCountItemSerializer
)

# Create your views here.

class WarehouseViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Warehouse
    """
    queryset = Warehouse.objects.select_related('franchise', 'created_by').prefetch_related('inventory_items')  # type: ignore
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'franchise', 'created_by']
    search_fields = ['name', 'code', 'address', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']


class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo InventoryItem
    """
    queryset = InventoryItem.objects.select_related('warehouse', 'catalog_item', 'created_by')  # type: ignore
    serializer_class = InventoryItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['warehouse', 'catalog_item', 'created_by']
    search_fields = ['catalog_item__name', 'warehouse__name']
    ordering_fields = ['quantity', 'unit_cost', 'total_cost', 'created_at']
    ordering = ['warehouse', 'catalog_item']


class InventoryMovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo InventoryMovement
    """
    queryset = InventoryMovement.objects.select_related('warehouse', 'catalog_item', 'created_by')  # type: ignore
    serializer_class = InventoryMovementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movement_type', 'warehouse', 'catalog_item', 'created_by']
    search_fields = ['reference', 'notes', 'catalog_item__name']
    ordering_fields = ['movement_date', 'quantity', 'total_cost', 'created_at']
    ordering = ['-movement_date']


class InventoryCountViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo InventoryCount
    """
    queryset = InventoryCount.objects.select_related('warehouse', 'created_by').prefetch_related('items')  # type: ignore
    serializer_class = InventoryCountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'warehouse', 'created_by']
    search_fields = ['count_number', 'notes', 'warehouse__name']
    ordering_fields = ['count_number', 'start_date', 'end_date', 'created_at']
    ordering = ['-start_date']


class InventoryCountItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo InventoryCountItem
    """
    queryset = InventoryCountItem.objects.select_related('inventory_count', 'catalog_item')  # type: ignore
    serializer_class = InventoryCountItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['inventory_count', 'catalog_item']
    search_fields = ['notes', 'catalog_item__name', 'inventory_count__count_number']
    ordering_fields = ['expected_quantity', 'counted_quantity', 'difference', 'created_at']
    ordering = ['inventory_count', 'catalog_item']
