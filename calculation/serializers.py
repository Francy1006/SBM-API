from rest_framework import serializers

from .models import VariableFormula, CalculationConcept, DataType


class VariableFormulaSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = VariableFormula
        fields = "__all__"

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class DataTypeSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = DataType
        fields = "__all__"

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class CalculationConceptSerializer(serializers.ModelSerializer):
    data_type_detail = DataTypeSerializer(source="data_type", read_only=True)
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = CalculationConcept
        fields = "__all__"

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}