from rest_framework import serializers
from calculation.models import VariableFormula, ModuleCalculationDetail
from .models import (
    Module,
    ModuleOrderConfig,
    OrderConfigType,
)

class VariableFormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableFormula
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class OrderConfigTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderConfigType
        fields = "__all__"


class ModuleOrderConfigSerializer(serializers.ModelSerializer):
    order_config_type = OrderConfigTypeSerializer(read_only=True)
    variable_formula = serializers.SlugRelatedField(
        read_only=True,
        slug_field="code"
    )

    class Meta:
        model = ModuleOrderConfig
        fields = "__all__"


class ModuleCalculationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleCalculationDetail
        fields = "__all__"