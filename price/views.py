from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    PriceList,
    PriceItem,
    PriceDiscount,
    PriceHistory,
    PriceConfiguration,
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
from rest_framework.decorators import api_view
from django.urls import path

from catalog.models import Product
from price.models import Price
import re
from django.db import transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import FieldError
from accounting.models import FiscalConfigurationDetail

# Create your views here.


class PriceListViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceList
    """

    queryset = PriceList.objects.select_related("franchise", "created_by").prefetch_related("items")  # type: ignore
    serializer_class = PriceListSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "is_default", "franchise", "created_by"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["name"]


class PriceItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceItem
    """

    queryset = PriceItem.objects.select_related("price_list", "catalog_item", "created_by")  # type: ignore
    serializer_class = PriceItemSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["price_list", "catalog_item", "created_by"]
    search_fields = ["catalog_item__name", "price_list__name"]
    ordering_fields = ["price", "cost", "margin", "created_at"]
    ordering = ["price_list", "catalog_item"]


class PriceDiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceDiscount
    """

    queryset = PriceDiscount.objects.select_related("franchise", "created_by")  # type: ignore
    serializer_class = PriceDiscountSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["discount_type", "is_active", "franchise", "created_by"]
    search_fields = ["name", "description"]
    ordering_fields = ["discount_value", "valid_from", "valid_until", "created_at"]
    ordering = ["-created_at"]


class PriceHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PriceHistory
    """

    queryset = PriceHistory.objects.select_related("price_item", "changed_by")  # type: ignore
    serializer_class = PriceHistorySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["price_item", "changed_by"]
    search_fields = ["change_reason"]
    ordering_fields = ["old_price", "new_price", "changed_at"]
    ordering = ["-changed_at"]


class PriceConfigurationViewSet(viewsets.ModelViewSet):
    queryset = PriceConfiguration.objects.all()
    serializer_class = PriceConfigurationSerializer


class PriceConfigurationDirectivesView(APIView):
    """
    Endpoint que retorna value y var de fiscal_directive y fiscal_configuration_detail para un price_configuration dado.
    """

    def get(self, request):
        configuration = request.query_params.get("configuration")
        if not configuration:
            return Response(
                {"error": "El parámetro configuration es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            from accounting.models import FiscalDirective, FiscalConfigurationDetail

            # Obtener las directivas fiscales para la configuración de precio
            fiscal_details = FiscalConfigurationDetail.objects.filter(
                price_configuration=configuration
            ).select_related("fiscal_directive")

            data = []
            for detail in fiscal_details:
                if detail.fiscal_directive:
                    data.append(
                        {"value": detail.fiscal_directive.value, "var": detail.var}
                    )

            return Response(data)

        except Exception as e:
            return Response(
                {"error": f"Error obteniendo directivas: {str(e)}"}, status=400
            )


class PriceFormulaView(APIView):
    """
    Endpoint que retorna formula, formula_template y formula_translate de variable_formula para un price_configuration dado.
    """

    def get(self, request):
        configuration = request.query_params.get("configuration")
        if not configuration:
            return Response(
                {"error": "El parámetro configuration es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            from accounting.models import VariableFormula

            # Obtener la configuración de precio con su variable_formula
            price_config = PriceConfiguration.objects.select_related(
                "variable_formula"
            ).get(code=configuration)

            if not price_config.variable_formula:
                return Response(
                    {
                        "error": "No se encontró variable_formula para la configuración de precio."
                    },
                    status=400,
                )

            data = [
                {
                    "formula": price_config.variable_formula.formula,
                    "formula_template": price_config.variable_formula.formula_template,
                    "formula_translate": price_config.variable_formula.formula_translate,
                }
            ]

            return Response(data)

        except PriceConfiguration.DoesNotExist:
            return Response(
                {"error": "Configuración de precio no encontrada."}, status=400
            )
        except Exception as e:
            return Response(
                {"error": f"Error obteniendo fórmula: {str(e)}"}, status=400
            )


class PriceConfigurationFormulaView(APIView):
    """
    Endpoint que retorna price_configuration, formula_template y formula_translate para un price_configuration dado (por code).
    """

    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response(
                {"error": "El parámetro code es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            from accounting.models import VariableFormula

            # Obtener la configuración de precio con su variable_formula
            price_config = PriceConfiguration.objects.select_related(
                "variable_formula"
            ).get(code=code)

            data = [
                {
                    "price_configuration": price_config.price_configuration,
                    "formula_template": (
                        price_config.variable_formula.formula_template
                        if price_config.variable_formula
                        else None
                    ),
                    "formula_translate": (
                        price_config.variable_formula.formula_translate
                        if price_config.variable_formula
                        else None
                    ),
                }
            ]

            return Response(data)

        except PriceConfiguration.DoesNotExist:
            return Response(
                {"error": "Configuración de precio no encontrada."}, status=400
            )
        except Exception as e:
            return Response(
                {"error": f"Error obteniendo configuración: {str(e)}"}, status=400
            )


class VariableFormulaView(APIView):

    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response(
                {"error": "El parámetro code es requerido."},
                status=400
            )

        try:
            from accounting.models import FiscalConfigurationDetail, FiscalDirective

            # 1️⃣ Buscar detalles por configuración de precio
            details = FiscalConfigurationDetail.objects.filter(
                price_configuration=code
            )

            if not details.exists():
                return Response([], status=200)

            directive_codes = details.values_list("fiscal_directive", flat=True)

            directives = FiscalDirective.objects.filter(
                code__in=directive_codes
            ).select_related("type")

            directive_map = {d.code: d for d in directives}

            data = []
            for d in details:
                directive = directive_map.get(d.fiscal_directive)
                if not directive:
                    continue

                data.append({
                    "var": d.var,
                    "value": directive.value,
                    "type": directive.type.id if directive.type else None,
                    "variable_type": directive.type.type if directive.type else None
                })

            return Response(data)

        except Exception as e:
            return Response(
                {"error": f"Error obteniendo variables: {str(e)}"},
                status=400
            )

class PriceCalculationFormulaView(APIView):
    """
    Endpoint POST que recibe un product.sku, obtiene la fórmula y variables asociadas a su price_configuration,
    evalúa la fórmula y actualiza los campos net_amount, gross_amount, iva_amount en el modelo Price.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        sku = request.data.get("sku")
        if not sku:
            return Response(
                {"error": "El parámetro sku es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        price_code = product.price
        try:
            price = Price.objects.get(code=price_code)
        except Price.DoesNotExist:
            return Response(
                {"error": "Precio no encontrado para el producto."},
                status=status.HTTP_404_NOT_FOUND,
            )

        price_configuration = price.price_configuration

        # 1. Obtener la fórmula usando ORM
        try:
            # Importar los modelos necesarios
            from accounting.models import VariableFormula
            from django.db.models import Q

            # Obtener la configuración de precio con su variable_formula
            price_config = PriceConfiguration.objects.select_related(
                "variable_formula"
            ).get(code=price_configuration)

            if not price_config.variable_formula:
                return Response(
                    {
                        "error": "No se encontró variable_formula para la configuración de precio."
                    },
                    status=400,
                )

            formula_template = price_config.variable_formula.formula_template
            if not formula_template:
                return Response(
                    {
                        "error": "No se encontró fórmula para la configuración de precio."
                    },
                    status=400,
                )

        except PriceConfiguration.DoesNotExist:
            return Response(
                {"error": "Configuración de precio no encontrada."}, status=400
            )
        except Exception as e:
            return Response(
                {"error": f"Error obteniendo fórmula: {str(e)}"}, status=400
            )

        # 2. Obtener variables usando ORM
        try:
            from accounting.models import (
                FiscalDirective,
                FiscalDirectiveType,
                FiscalConfigurationDetail,
            )

            # Obtener las variables de la configuración fiscal
            fiscal_details = FiscalConfigurationDetail.objects.filter(
                price_configuration=price_configuration
            ).select_related("fiscal_directive", "fiscal_directive__type")

            variables_list = []
            for detail in fiscal_details:
                if detail.var and detail.fiscal_directive:
                    variables_list.append(
                        {
                            "var": detail.var,
                            "value": detail.fiscal_directive.value,
                            "type": (
                                detail.fiscal_directive.type.id
                                if detail.fiscal_directive.type
                                else None
                            ),
                            "variable_type": (
                                detail.fiscal_directive.type.type
                                if detail.fiscal_directive.type
                                else None
                            ),
                        }
                    )

        except Exception as e:
            return Response(
                {"error": f"Error obteniendo variables: {str(e)}"}, status=400
            )

        # 3. Construir contexto de variables
        context = {v["var"]: v["value"] for v in variables_list if v["var"]}
        # Agregar base_net_amount
        context["base_net_amount"] = price.base_net_amount

        # 4. Parsear y evaluar la fórmula
        results = {}
        pattern = r"([a-zA-Z0-9_]+)\s*=([^;|]+)"  # net_amount = ...
        matches = re.findall(pattern, formula_template)

        for field, expr in matches:
            expr_eval = expr.strip()
            # Reemplazar variables en la expresión
            for var, value in context.items():
                # Buscar patrones como ${variable} y reemplazarlos
                expr_eval = expr_eval.replace(f"${{{var}}}", str(value))
            try:
                value = eval(expr_eval, {"__builtins__": {}})
            except Exception as e:
                return Response(
                    {
                        "error": f"Error evaluando la fórmula para {field}: {e}",
                        "expr": expr_eval,
                    },
                    status=400,
                )
            results[field.strip()] = value

        # 5. Actualizar los campos en Price
        with transaction.atomic():
            for field in ["net_amount", "gross_amount", "iva_amount"]:
                if field in results:
                    setattr(price, field, results[field])
            price.save()

        # 6. Responder con los valores calculados
        return Response(
            {
                "sku": sku,
                "price_code": price_code,
                "price_configuration": price_configuration,
                "formula_template": formula_template,
                "variables": context,
                "results": results,
            }
        )
