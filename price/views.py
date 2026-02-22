from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    PriceList,
    PriceItem,
    PriceDiscount,
    PriceHistory,
    PriceConfiguration,
    VariableFormula,
)
from .serializers import (
    PriceListSerializer,
    PriceItemSerializer,
    PriceDiscountSerializer,
    PriceHistorySerializer,
    PriceConfigurationSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import path

from catalog.models import Catalog, Product, Material, Service
from price.models import Price
import re
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounting.models import FiscalConfigurationDetail


class PriceListViewSet(viewsets.ModelViewSet):
    queryset = PriceList.objects.select_related("franchise", "created_by").prefetch_related("items")
    serializer_class = PriceListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active", "is_default", "franchise", "created_by"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["name"]


class PriceItemViewSet(viewsets.ModelViewSet):
    queryset = PriceItem.objects.select_related("price_list", "catalog_item", "created_by")
    serializer_class = PriceItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["price_list", "catalog_item", "created_by"]
    search_fields = ["catalog_item__name", "price_list__name"]
    ordering_fields = ["price", "cost", "margin", "created_at"]
    ordering = ["price_list", "catalog_item"]


class PriceDiscountViewSet(viewsets.ModelViewSet):
    queryset = PriceDiscount.objects.select_related("franchise", "created_by")
    serializer_class = PriceDiscountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["discount_type", "is_active", "franchise", "created_by"]
    search_fields = ["name", "description"]
    ordering_fields = ["discount_value", "valid_from", "valid_until", "created_at"]
    ordering = ["-created_at"]


class PriceHistoryViewSet(viewsets.ModelViewSet):
    queryset = PriceHistory.objects.select_related("price_item", "changed_by")
    serializer_class = PriceHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["price_item", "changed_by"]
    search_fields = ["change_reason"]
    ordering_fields = ["old_price", "new_price", "changed_at"]
    ordering = ["-changed_at"]


class PriceConfigurationViewSet(viewsets.ModelViewSet):
    queryset = PriceConfiguration.objects.select_related("variable_formula").all()
    serializer_class = PriceConfigurationSerializer


class PriceFormulaView(APIView):
    def get(self, request):
        configuration = request.query_params.get("configuration")
        if not configuration:
            return Response({"error": "El parámetro configuration es requerido."}, status=400)

        price_config = PriceConfiguration.objects.select_related("variable_formula").filter(
            code=configuration
        ).first()

        if not price_config:
            return Response({"error": "Configuración de precio no encontrada."}, status=400)

        vf = price_config.variable_formula
        if not vf:
            return Response({"error": "variable_formula no encontrada."}, status=400)

        return Response([
            {
                "formula": vf.formula,
                "formula_template": vf.formula_template,
                "formula_translate": vf.formula_translate,
            }
        ])


class PriceConfigurationFormulaView(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "El parámetro code es requerido."}, status=400)

        price_config = PriceConfiguration.objects.select_related("variable_formula").filter(
            code=code
        ).first()

        if not price_config:
            return Response({"error": "Configuración de precio no encontrada."}, status=400)

        vf = price_config.variable_formula

        return Response([
            {
                "price_configuration": price_config.price_configuration,
                "formula_template": vf.formula_template if vf else None,
                "formula_translate": vf.formula_translate if vf else None,
            }
        ])


class PriceCalculationFormulaView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        sku = (request.data.get("sku") or "").strip()
        item_type = (request.data.get("item_type") or "catalog").strip().lower()

        if not sku:
            return Response({"error": "El parámetro sku es requerido."}, status=400)

        model_map = {
            "catalog": Catalog,
            "product": Product,
            "material": Material,
            "service": Service,
        }

        Model = model_map.get(item_type)
        if not Model:
            return Response({"error": "item_type inválido."}, status=400)

        obj = Model.objects.filter(sku=sku).first()
        if not obj:
            return Response({"error": "Item no encontrado."}, status=404)

        price_code = getattr(obj, "price_id", None) if item_type == "catalog" else getattr(obj, "price", None)
        if not price_code:
            return Response({"error": "Precio no encontrado para el item."}, status=404)

        price = Price.objects.filter(code=price_code, is_current=True).first() \
            or Price.objects.filter(code=price_code).first()

        if not price:
            return Response({"error": "Precio no encontrado para el item."}, status=404)

        price_config = PriceConfiguration.objects.select_related("variable_formula").filter(
            code=price.price_configuration
        ).first()

        if not price_config:
            return Response({"error": "Configuración de precio no encontrada."}, status=400)

        vf = price_config.variable_formula
        if not vf or not vf.formula_template:
            return Response({"error": "Fórmula no encontrada o inválida."}, status=400)

        formula_template = vf.formula_template

        fiscal_details = FiscalConfigurationDetail.objects.filter(
            price_configuration=price.price_configuration
        )

        from accounting.models import FiscalDirective

        directive_codes = fiscal_details.values_list("fiscal_directive", flat=True)
        directives = FiscalDirective.objects.filter(code__in=directive_codes)
        directive_map = {d.code: d for d in directives}

        context = {"base_net_amount": float(price.base_net_amount)}

        for detail in fiscal_details:
            directive = directive_map.get(detail.fiscal_directive)
            if directive and detail.var:
                context[detail.var] = float(directive.value)

        results = {}
        pattern = r"([a-zA-Z0-9_]+)\s*=([^;|]+)"
        matches = re.findall(pattern, formula_template)

        for field, expr in matches:
            expr_eval = expr.strip()
            for var, value in context.items():
                expr_eval = expr_eval.replace(f"${{{var}}}", str(value))

            try:
                value = eval(expr_eval, {"__builtins__": {}})
            except Exception as e:
                return Response(
                    {"error": f"Error evaluando la fórmula para {field}: {e}", "expr": expr_eval},
                    status=400,
                )

            results[field.strip()] = value

        with transaction.atomic():
            for field in ["net_amount", "gross_amount", "iva_amount"]:
                if field in results:
                    setattr(price, field, int(round(results[field])))
            price.save()

        return Response({
            "sku": sku,
            "item_type": item_type,
            "price_code": price_code,
            "price_configuration": price.price_configuration,
            "formula_template": formula_template,
            "variables": context,
            "results": results,
        })


class VariableFormulaView(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "El parámetro code es requerido."}, status=400)

        from accounting.models import FiscalDirective

        fiscal_details = FiscalConfigurationDetail.objects.filter(
            price_configuration=code
        )

        directive_codes = fiscal_details.values_list("fiscal_directive", flat=True)
        directives = FiscalDirective.objects.filter(code__in=directive_codes)
        directive_map = {d.code: d for d in directives}

        data = []
        for detail in fiscal_details:
            directive = directive_map.get(detail.fiscal_directive)
            if directive:
                data.append(
                    {
                        "var": detail.var,
                        "value": directive.value,
                    }
                )

        return Response(data)