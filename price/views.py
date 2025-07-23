from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import PriceList, PriceItem, PriceDiscount, PriceHistory, PriceConfiguration
from .serializers import (
    PriceListSerializer, PriceItemSerializer,
    PriceDiscountSerializer, PriceHistorySerializer, PriceConfigurationSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework.decorators import api_view
from django.urls import path

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


class PriceConfigurationViewSet(viewsets.ModelViewSet):
    queryset = PriceConfiguration.objects.all()
    serializer_class = PriceConfigurationSerializer


class PriceConfigurationDirectivesView(APIView):
    """
    Endpoint que retorna value y var de fiscal_directive y fiscal_configuration_detail para un price_configuration dado.
    """
    def get(self, request):
        configuration = request.query_params.get('configuration')
        if not configuration:
            return Response({'error': 'El parámetro configuration es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT fd.value, fcd.var
                FROM sbm_business.fiscal_directive fd
                LEFT JOIN ditaly_pasta.fiscal_configuration_detail fcd
                  ON fd.code = fcd.fiscal_directive
                LEFT JOIN ditaly_pasta.price_configuration pc
                  ON pc.code = fcd.price_configuration
                WHERE fcd.price_configuration = %s
            ''', [configuration])
            results = cursor.fetchall()
        data = [
            {'value': row[0], 'var': row[1]} for row in results
        ]
        return Response(data)


class PriceFormulaView(APIView):
    """
    Endpoint que retorna formula, formula_template y formula_translate de variable_formula para un price_configuration dado.
    """
    def get(self, request):
        configuration = request.query_params.get('configuration')
        if not configuration:
            return Response({'error': 'El parámetro configuration es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT vf.formula, vf.formula_template, vf.formula_translate
                FROM sbm_business.variable_formula vf
                LEFT JOIN ditaly_pasta.price_configuration pc
                  ON vf.code = pc.variable_formula
                WHERE pc.code = %s
            ''', [configuration])
            results = cursor.fetchall()
        data = [
            {'formula': row[0], 'formula_template': row[1], 'formula_translate': row[2]} for row in results
        ]
        return Response(data)


class PriceConfigurationFormulaView(APIView):
    """
    Endpoint que retorna price_configuration, formula_template y formula_translate para un price_configuration dado (por code).
    """
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'El parámetro code es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT pc.price_configuration, vf.formula_template, vf.formula_translate
                FROM ditaly_pasta.price_configuration pc
                LEFT JOIN sbm_business.variable_formula vf ON pc.variable_formula = vf.code
                WHERE pc.code = %s
            ''', [code])
            results = cursor.fetchall()
        data = [
            {'price_configuration': row[0], 'formula_template': row[1], 'formula_translate': row[2]} for row in results
        ]
        return Response(data)


class VariableFormulaView(APIView):
    """
    Endpoint que retorna var, value, type (id) y variable_type (type) para un price_configuration dado (por code en query param).
    """
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'El parámetro code es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT fcd.var, fd.value, fdt.id as type, fdt."type" as variable_type
                FROM ditaly_pasta.price_configuration pc
                LEFT JOIN sbm_business.variable_formula vf ON pc.variable_formula = vf.code
                LEFT JOIN ditaly_pasta.fiscal_configuration_detail fcd ON pc.code = fcd.price_configuration
                LEFT JOIN sbm_business.fiscal_directive fd ON fcd.fiscal_directive = fd.code
                LEFT JOIN sbm_business.fiscal_directive_type fdt ON fd.type = fdt.id
                WHERE pc.code = %s
            ''', [code])
            results = cursor.fetchall()
        data = [
            {'var': row[0], 'value': row[1], 'type': row[2], 'variable_type': row[3]} for row in results
        ]
        return Response(data)
