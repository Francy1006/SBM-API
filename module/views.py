from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Module, ModuleOrderConfig, VariableFormula
from accounting.models import FiscalConfigurationDetail, FiscalDirective
from .serializers import (
    ModuleSerializer,
    ModuleOrderConfigSerializer,
    VariableFormulaSerializer,
)


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ModuleOrderConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleOrderConfig.objects.select_related(
        "order_config_type", "variable_formula"
    ).all()
    serializer_class = ModuleOrderConfigSerializer


class VariableFormulaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VariableFormula.objects.all()
    serializer_class = VariableFormulaSerializer


class ModuleOrderFormulaView(APIView):
    def get(self, request):
        t = request.query_params.get("type", "").strip()
        if not t:
            return Response({"code": None})

        config = (
            ModuleOrderConfig.objects.select_related(
                "order_config_type",
                "variable_formula",
            )
            .filter(order_config_type__type=t)
            .order_by("-id")
            .first()
        )

        return Response(
            {
                "code": (
                    config.variable_formula.code
                    if config and config.variable_formula
                    else None
                )
            }
        )

class ModuleOrderFormulaDetailView(APIView):
    def get(self, request):
        code = request.query_params.get("code")

        if not code:
            return Response(
                {"error": "El parámetro code es requerido."},
                status=400
            )

        config = ModuleOrderConfig.objects.select_related(
            "order_config_type",
            "variable_formula"
        ).filter(
            variable_formula__code=code,
            is_active=True
        ).first()

        if not config or not config.variable_formula:
            return Response(
                {"error": "Configuración o fórmula no encontrada."},
                status=400
            )

        formula = config.variable_formula

        return Response({
            "code": formula.code,
            "formula": formula.formula,
            "formula_template": formula.formula_template,
            "formula_translate": formula.formula_translate,
            "order_config_type": config.order_config_type.type
        })

class ModuleOrderVariablesView(APIView):
    def get(self, request):
        qs = FiscalConfigurationDetail.objects.filter(
            module_id=2,
            is_active=True
        ).values(
            "id",
            "module_id",
            "module_config_id",
            "fiscal_directive",
            "var",
        )

        directives = {
            d["code"]: d["value"]
            for d in FiscalDirective.objects.filter(
                code__in=[q["fiscal_directive"] for q in qs]
            ).values("code", "value")
        }

        result = []
        for q in qs:
            q["value"] = directives.get(q["fiscal_directive"])
            result.append(q)

        return Response(result)