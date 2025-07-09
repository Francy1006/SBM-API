from rest_framework import serializers
from .models import (
    Price, PriceFiscalConfiguration, FiscalConfigurationDetail,
    FiscalDirective, FiscalDirectiveType, FiscalFormula
)


class PriceSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Price
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields = [
            'id', 'code', 'net_amount', 'gross_amount', 'iva_amount', 'retention_amount',
            'price_fiscal_configuration', 'is_active', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'created_by',
            'confirmed_by', 'updated_by', 'deleted_by', 'field_verbose_names'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class PriceFiscalConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PriceFiscalConfiguration
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = PriceFiscalConfiguration
        fields = [
            'id', 'fiscal_configuration', 'fiscal_formula', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'created_by',
            'confirmed_by', 'updated_by', 'deleted_by', 'field_verbose_names'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FiscalConfigurationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FiscalConfigurationDetail
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FiscalConfigurationDetail
        fields = [
            'id', 'price_fiscal_configuration', 'price', 'fiscal_directive', 'log',
            'field_verbose_names'
        ]
        read_only_fields = ['id']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FiscalDirectiveSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FiscalDirective
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FiscalDirective
        fields = [
            'id', 'code', 'obs', 'fiscal_directive', 'type', 'percentage',
            'official_source_url', 'is_deleted', 'is_confirmed', 'created_at',
            'updated_at', 'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by', 'field_verbose_names'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FiscalDirectiveTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FiscalDirectiveType
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FiscalDirectiveType
        fields = ['id', 'type', 'description', 'field_verbose_names']
        read_only_fields = ['id']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FiscalFormulaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FiscalFormula
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FiscalFormula
        fields = [
            'id', 'formula', 'formula_template', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'created_by',
            'confirmed_by', 'updated_by', 'deleted_by', 'field_verbose_names'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields} 