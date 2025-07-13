from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FiscalDocument, FiscalItem, TaxRate, FiscalPayment
from .serializers import (
    FiscalDocumentSerializer, FiscalItemSerializer,
    TaxRateSerializer, FiscalPaymentSerializer
)

# Create your views here.

class FiscalDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FiscalDocument
    """
    queryset = FiscalDocument.objects.select_related( # type: ignore
        'franchise', 'customer', 'created_by'
    ).prefetch_related('items', 'payments')
    serializer_class = FiscalDocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['document_type', 'status', 'franchise', 'customer', 'created_by']
    search_fields = ['document_number', 'description']
    ordering_fields = ['document_number', 'issue_date', 'due_date', 'total_amount']
    ordering = ['-issue_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FiscalItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FiscalItem
    """
    queryset = FiscalItem.objects.select_related('fiscal_document', 'catalog_item') # type: ignore
    serializer_class = FiscalItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['fiscal_document', 'catalog_item', 'tax_rate']
    search_fields = ['description', 'catalog_item__name']
    ordering_fields = ['quantity', 'unit_price', 'total_price', 'tax_amount']
    ordering = ['fiscal_document', 'created_at']


class TaxRateViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo TaxRate
    """
    queryset = TaxRate.objects.select_related('franchise', 'created_by') # type: ignore
    serializer_class = TaxRateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'franchise', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'rate', 'created_at']
    ordering = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FiscalPaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FiscalPayment
    """
    queryset = FiscalPayment.objects.select_related('fiscal_document', 'created_by') # type: ignore
    serializer_class = FiscalPaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_method', 'fiscal_document', 'created_by']
    search_fields = ['reference', 'fiscal_document__document_number']
    ordering_fields = ['amount', 'payment_date', 'created_at']
    ordering = ['-payment_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
