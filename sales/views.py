from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Sale, SaleItem, SalePayment, SalesOrder
from .serializers import (
    CustomerSerializer, SaleSerializer, SaleItemSerializer,
    SalePaymentSerializer, SalesOrderSerializer
)

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Customer
    """
    queryset = Customer.objects.select_related('franchise', 'created_by').prefetch_related('sales')
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer_type', 'is_active', 'franchise', 'created_by']
    search_fields = ['name', 'email', 'phone', 'tax_id']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']


class SaleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Sale
    """
    queryset = Sale.objects.select_related(
        'customer', 'franchise', 'created_by'
    ).prefetch_related('items', 'payments')
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'customer', 'franchise', 'created_by']
    search_fields = ['sale_number', 'notes', 'customer__name']
    ordering_fields = ['sale_number', 'sale_date', 'due_date', 'total_amount']
    ordering = ['-sale_date']


class SaleItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SaleItem
    """
    queryset = SaleItem.objects.select_related('sale', 'catalog_item')
    serializer_class = SaleItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sale', 'catalog_item']
    search_fields = ['notes', 'catalog_item__name', 'sale__sale_number']
    ordering_fields = ['quantity', 'unit_price', 'total_price', 'created_at']
    ordering = ['sale', 'created_at']


class SalePaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SalePayment
    """
    queryset = SalePayment.objects.select_related('sale', 'created_by')
    serializer_class = SalePaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_method', 'sale', 'created_by']
    search_fields = ['reference', 'notes', 'sale__sale_number']
    ordering_fields = ['amount', 'payment_date', 'created_at']
    ordering = ['-payment_date']


class SalesOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SalesOrder
    """
    queryset = SalesOrder.objects.select_related('customer', 'franchise', 'created_by')
    serializer_class = SalesOrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'franchise', 'created_by']
    search_fields = ['order_number', 'notes', 'customer__name']
    ordering_fields = ['order_number', 'order_date', 'delivery_date', 'total_amount']
    ordering = ['-order_date']
