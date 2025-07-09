from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    Price, PriceFiscalConfiguration, FiscalConfigurationDetail,
    FiscalDirective, FiscalDirectiveType, FiscalFormula
)
from .serializers import (
    PriceSerializer, PriceFiscalConfigurationSerializer, FiscalConfigurationDetailSerializer,
    FiscalDirectiveSerializer, FiscalDirectiveTypeSerializer, FiscalFormulaSerializer
)


class PriceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Price
    """
    queryset = Price.objects.all()  # type: ignore
    serializer_class = PriceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['code']
    ordering_fields = ['id', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo precios activos
        """
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PriceFiscalConfigurationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceFiscalConfiguration
    """
    queryset = PriceFiscalConfiguration.objects.all()  # type: ignore
    serializer_class = PriceFiscalConfigurationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['fiscal_configuration', 'fiscal_formula']
    ordering_fields = ['id', 'fiscal_configuration', 'created_at']
    ordering = ['fiscal_configuration']


class FiscalConfigurationDetailViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FiscalConfigurationDetail
    """
    queryset = FiscalConfigurationDetail.objects.all()  # type: ignore
    serializer_class = FiscalConfigurationDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price_fiscal_configuration', 'price', 'fiscal_directive']
    search_fields = ['log']
    ordering_fields = ['id']
    ordering = ['id']


class FiscalDirectiveViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FiscalDirective
    """
    queryset = FiscalDirective.objects.all()  # type: ignore
    serializer_class = FiscalDirectiveSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed', 'type']
    search_fields = ['fiscal_directive', 'code', 'obs']
    ordering_fields = ['id', 'fiscal_directive', 'created_at']
    ordering = ['fiscal_directive']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo directivas activas
        """
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Endpoint para filtrar directivas por tipo
        """
        type_id = request.query_params.get('type_id')
        if type_id:
            queryset = self.get_queryset().filter(type=type_id, is_deleted=False)
        else:
            queryset = self.get_queryset().filter(is_deleted=False)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FiscalDirectiveTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FiscalDirectiveType
    """
    queryset = FiscalDirectiveType.objects.all()  # type: ignore
    serializer_class = FiscalDirectiveTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['id', 'type']
    ordering = ['type']


class FiscalFormulaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FiscalFormula
    """
    queryset = FiscalFormula.objects.all()  # type: ignore
    serializer_class = FiscalFormulaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['formula', 'formula_template']
    ordering_fields = ['id', 'formula', 'created_at']
    ordering = ['formula']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo fórmulas activas
        """
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
