from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Module, ModuleOrderConfig, VariableFormula
from .serializers import (
    ModuleSerializer,
    ModuleOrderConfigSerializer,
    VariableFormulaSerializer,
)


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ModuleOrderConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleOrderConfig.objects.select_related("order_config_type").all()
    serializer_class = ModuleOrderConfigSerializer


class VariableFormulaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VariableFormula.objects.all()
    serializer_class = VariableFormulaSerializer


class ModuleOrderFormulaView(APIView):
    def get(self, request):
        t = request.query_params.get("type")
        if not t:
            return Response({"code": None})

        config = (
            ModuleOrderConfig.objects.select_related("order_config_type")
            .filter(
                order_config_type__type__iexact=t,
                is_active=True,
            )
            .first()
        )

        return Response({"code": config.variable_formula.code if config else None})


class ModuleOrderFormulaDetailView(APIView):
    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"error": "El parámetro code es requerido."}, status=400)

        formula = VariableFormula.objects.filter(code=code).first()
        if not formula:
            return Response({"error": "Fórmula no encontrada."}, status=400)

        return Response(
            {
                "code": formula.code,
                "formula": formula.formula,
                "formula_template": formula.formula_template,
                "formula_translate": formula.formula_translate,
            }
        )


class ModuleOrderVariableView(APIView):
    def get(self, request):
        module_code = request.query_params.get("module_code")
        module_config_id = request.query_params.get("module_config_id")

        if not module_code or not module_config_id:
            return Response(
                {
                    "error": "Los parámetros module_code y module_config_id son requeridos."
                },
                status=400,
            )

        module = Module.objects.filter(code=module_code, is_active=True).first()
        if not module:
            return Response({"error": "Módulo no encontrado."}, status=400)

        from accounting.models import FiscalConfigurationDetail, FiscalDirective

        fiscal_details = FiscalConfigurationDetail.objects.filter(
            module_id=module.id,
            module_config_id=module_config_id,
            is_active=True,
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