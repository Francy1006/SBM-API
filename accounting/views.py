from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import connection
from price.models import Price
from .models import (
    PriceFiscalConfiguration, FiscalConfigurationDetail,
    FiscalDirective, FiscalDirectiveType, FiscalFormula
)
from .serializers import (
    PriceSerializer, FiscalConfigurationDetailSerializer,
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
    serializer_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['fiscal_configuration', 'fiscal_formula']
    ordering_fields = ['id', 'fiscal_configuration', 'created_at']
    ordering = ['fiscal_configuration']


class FiscalConfigurationDetailViewSet(viewsets.ModelViewSet):
    queryset = FiscalConfigurationDetail.objects.all()  # type: ignore
    serializer_class = FiscalConfigurationDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['module_id', 'module_config_id', 'fiscal_directive', 'is_active']
    search_fields = ['var']
    ordering_fields = ['id']
    ordering = ['id']


class FiscalDirectiveViewSet(viewsets.ModelViewSet):
    queryset = FiscalDirective.objects.all()  # type: ignore
    serializer_class = FiscalDirectiveSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed', 'type']
    search_fields = ['fiscal_directive', 'code', 'obs', 'type__type']
    ordering_fields = ['id', 'fiscal_directive', 'created_at', 'value']
    ordering = ['fiscal_directive']
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')

    @action(detail=False, methods=['get'])
    def active(self, request):
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        type_id = request.query_params.get('type_id')
        if type_id:
            queryset = self.get_queryset().filter(type=type_id, is_deleted=False)
        else:
            queryset = self.get_queryset().filter(is_deleted=False)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    fd.type,
                    fdt.type AS type_name,
                    fdt.description AS type_description,
                    COUNT(*) AS total_directives,
                    COUNT(CASE WHEN fd.is_confirmed = true THEN 1 END) AS confirmed_directives,
                    COUNT(CASE WHEN fd.is_deleted = true THEN 1 END) AS deleted_directives,
                    COUNT(CASE WHEN fd.is_confirmed IS NULL THEN 1 END) AS pending_directives,
                    AVG(fd.value) AS avg_value,
                    MIN(fd.value) AS min_value,
                    MAX(fd.value) AS max_value,
                    COUNT(CASE WHEN fd.year = EXTRACT(YEAR FROM CURRENT_DATE) THEN 1 END) AS current_year_directives,
                    COUNT(CASE WHEN fd.month IS NOT NULL THEN 1 END) AS directives_with_month,
                    COUNT(CASE WHEN fd.end_month IS NOT NULL THEN 1 END) AS directives_with_end_month,
                    COUNT(CASE WHEN fd.end_year IS NOT NULL THEN 1 END) AS directives_with_end_year,
                    MIN(fd.year) AS earliest_year,
                    MAX(fd.year) AS latest_year,
                    COUNT(DISTINCT fd.year) AS unique_years,
                    COUNT(DISTINCT fd.month) AS unique_months
                FROM sbm_business.fiscal_directive fd
                LEFT JOIN sbm_business.fiscal_directive_type fdt ON fd.type = fdt.id
                GROUP BY fd.type, fdt.type, fdt.description
                ORDER BY fd.type
            """)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(results)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    'TOTAL' AS category,
                    COUNT(*) AS total_directives,
                    COUNT(CASE WHEN is_confirmed = true THEN 1 END) AS confirmed_directives,
                    COUNT(CASE WHEN is_deleted = true THEN 1 END) AS deleted_directives,
                    COUNT(CASE WHEN is_confirmed IS NULL THEN 1 END) AS pending_directives,
                    COUNT(DISTINCT type) AS unique_types,
                    COUNT(DISTINCT year) AS unique_years,
                    AVG(value) AS avg_value,
                    MIN(value) AS min_value,
                    MAX(value) AS max_value
                FROM sbm_business.fiscal_directive

                UNION ALL

                SELECT 
                    'ACTIVE' AS category,
                    COUNT(*) AS total_directives,
                    COUNT(CASE WHEN is_confirmed = true THEN 1 END) AS confirmed_directives,
                    COUNT(CASE WHEN is_deleted = true THEN 1 END) AS deleted_directives,
                    COUNT(CASE WHEN is_confirmed IS NULL THEN 1 END) AS pending_directives,
                    COUNT(DISTINCT type) AS unique_types,
                    COUNT(DISTINCT year) AS unique_years,
                    AVG(value) AS avg_value,
                    MIN(value) AS min_value,
                    MAX(value) AS max_value
                FROM sbm_business.fiscal_directive
                WHERE is_deleted IS NULL OR is_deleted = false
            """)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(results)

    @action(detail=False, methods=['get'])
    def by_year(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    year,
                    COUNT(*) AS total_directives,
                    COUNT(CASE WHEN is_confirmed = true THEN 1 END) AS confirmed_directives,
                    COUNT(CASE WHEN is_deleted = true THEN 1 END) AS deleted_directives,
                    COUNT(CASE WHEN is_confirmed IS NULL THEN 1 END) AS pending_directives,
                    COUNT(DISTINCT type) AS unique_types,
                    AVG(value) AS avg_value,
                    MIN(value) AS min_value,
                    MAX(value) AS max_value
                FROM sbm_business.fiscal_directive
                GROUP BY year
                ORDER BY year DESC
            """)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(results)


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


class FiscalDirectiveStatsViewSet(viewsets.ViewSet):
    """
    ViewSet para el modelo FiscalDirectiveStats (vista de analytics)
    """
    def list(self, request):
        """
        Endpoint para obtener estadísticas de directivas fiscales por tipo
        """
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM analytics.fiscal_directive_stats")
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(results)
