from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import VariableFormula, CalculationConcept, DataType
from .serializers import (
    VariableFormulaSerializer,
    CalculationConceptSerializer,
    DataTypeSerializer,
)
from accounting.models import FiscalConfigurationDetail, FiscalDirective
from price.models import PriceConfigurationDetail


class VariableFormulaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VariableFormula.objects.all()
    serializer_class = VariableFormulaSerializer


class CalculationConceptViewSet(viewsets.ModelViewSet):
    queryset = CalculationConcept.objects.all()
    serializer_class = CalculationConceptSerializer


class DataTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer


class VariableFormulaView(APIView):
    def get(self, request):
        module_id = request.query_params.get("module_id")
        module_config_id = request.query_params.get("module_config_id")
        code = request.query_params.get("code")

        if not module_config_id and code:
            module_config_id = code

        if not module_id:
            return Response({"error": "El parámetro module_id es requerido."}, status=400)

        if not module_config_id:
            return Response(
                {"error": "El parámetro module_config_id es requerido."}, status=400
            )

        try:
            module_id = int(module_id)
        except (TypeError, ValueError):
            return Response(
                {"error": "El parámetro module_id debe ser un entero."}, status=400
            )

        data = []

        fiscal_details = FiscalConfigurationDetail.objects.filter(
            module_id=module_id,
            module_config_id=module_config_id,
            is_active=True,
        )

        directive_codes = fiscal_details.values_list("fiscal_directive", flat=True)

        directives = FiscalDirective.objects.filter(code__in=directive_codes)
        directive_map = {d.code: d for d in directives}

        for detail in fiscal_details:
            directive = directive_map.get(detail.fiscal_directive)

            if directive and detail.var:
                data.append({
                    "var": detail.var,
                    "label": directive.fiscal_directive,
                    "value": directive.value,
                    "data_type": (
                        detail.data_type_id
                        if hasattr(detail, "data_type_id")
                        else detail.data_type
                    )
                })

        price_details = PriceConfigurationDetail.objects.filter(
            price_configuration=module_config_id
        ).select_related("calculation_concept")

        for detail in price_details:
            if detail.calculation_concept and detail.calculation_concept.field_name:
                data.append({
                    "var": detail.calculation_concept.field_name,
                    "label": getattr(detail.calculation_concept, "description", None)
                              or detail.calculation_concept.field_name,
                    "value": 0,
                    "data_type": getattr(detail.calculation_concept, "data_type_id", None)
                })

        return Response(data)