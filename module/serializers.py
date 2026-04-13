from rest_framework import serializers
from .models import VariableFormula, Module, ModuleOrderConfig, OrderConfigType


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
    variable_formula = serializers.CharField(source="variable_formula.code", read_only=True)

    class Meta:
        model = ModuleOrderConfig
        fields = "__all__"