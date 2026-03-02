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
        if not code or code in ["null", "None", "undefined"]:
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

    def evaluate_formula(self, price_configuration_code, base_net_amount, variables=None):

        from accounting.models import FiscalDirective

        price_config = (
            PriceConfiguration.objects
            .select_related("variable_formula")
            .filter(code=price_configuration_code)
            .first()
        )

        if not price_config:
            raise ValueError("Configuración no encontrada.")

        vf = price_config.variable_formula
        if not vf or not vf.formula_template:
            raise ValueError("Fórmula no encontrada.")

        context = {
            "base_net_amount": float(base_net_amount)
        }

        fiscal_details = FiscalConfigurationDetail.objects.filter(
            price_configuration=price_configuration_code
        )

        directive_codes = fiscal_details.values_list("fiscal_directive", flat=True)
        directives = FiscalDirective.objects.filter(code__in=directive_codes)
        directive_map = {d.code: d for d in directives}

        for detail in fiscal_details:
            directive = directive_map.get(detail.fiscal_directive)
            if directive and detail.var:
                try:
                    context[detail.var] = float(directive.value)
                except:
                    context[detail.var] = 0.0

        if isinstance(variables, dict):
            for k, v in variables.items():
                try:
                    context[k] = float(v)
                except:
                    context[k] = 0.0

        results = {}

        clean_formula = str(vf.formula_template).replace("|", "")
        lines = [l.strip() for l in clean_formula.split(";") if l.strip()]

        for line in lines:
            if "=" not in line:
                continue

            raw_label, expr = line.split("=", 1)
            raw_label = raw_label.strip()
            expr = expr.strip()

            if ":" in raw_label:
                label, _ = raw_label.split(":", 1)
                label = label.strip()
            else:
                label = raw_label

            for var, value in context.items():
                expr = expr.replace(f"${{{var}}}", str(value))

            value = eval(expr, {"__builtins__": None}, {})
            results[label] = round(float(value), 2)

        return results

    def post(self, request):

        price_configuration = request.data.get("price_configuration")
        base_net_amount = request.data.get("base_net_amount")
        variables = request.data.get("variables", {})

        if not price_configuration:
            return Response({"error": "price_configuration es requerido."}, status=400)

        if base_net_amount is None:
            return Response({"error": "base_net_amount es requerido."}, status=400)

        try:
            results = self.evaluate_formula(
                price_configuration,
                base_net_amount,
                variables
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response(results)


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

class ProductPriceHistoryView(APIView):

    def get(self, request, sku):

        product = Product.objects.filter(sku=sku).first()
        if not product:
            return Response({"detail": "Producto no encontrado."}, status=404)

        prices = (
            Price.objects
            .filter(products=product)
            .order_by("created_at")
            .values("created_at", "base_net_amount")
        )

        return Response(list(prices))