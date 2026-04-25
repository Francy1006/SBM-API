from rest_framework import serializers
from price.models import Price
from .models import (
    FiscalConfigurationDetail,
    FiscalDirective,
    FiscalDirectiveType,
    FiscalDirectiveStats,
)


class PriceSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields = [
            "id",
            "code",
            "base_net_amount",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "price_configuration",
            "is_current",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "created_by",
            "record_item_code",
            "price_record_type",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "created_by",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        user_code = getattr(getattr(request, "user", None), "code", None)
        validated_data["created_by"] = user_code
        return super().create(validated_data)

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FiscalConfigurationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalConfigurationDetail
        fields = [
            "id",
            "module",
            "module_config_id",
            "fiscal_directive",
            "var",
            "data_type",
            "is_active",
        ]
        read_only_fields = ["id"]


class FiscalDirectiveTypeSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FiscalDirectiveType
        fields = ["id", "type", "description", "field_verbose_names"]
        read_only_fields = ["id"]

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FiscalDirectiveSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FiscalDirective
        fields = [
            "id",
            "code",
            "obs",
            "fiscal_directive",
            "type",
            "value",
            "official_source_url",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "month",
            "end_month",
            "year",
            "end_year",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
        ]

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FiscalDirectiveStatsSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FiscalDirectiveStats
        fields = [
            "type",
            "type_name",
            "type_description",
            "total_directives",
            "confirmed_directives",
            "deleted_directives",
            "pending_directives",
            "avg_value",
            "min_value",
            "max_value",
            "current_year_directives",
            "directives_with_month",
            "directives_with_end_month",
            "directives_with_end_year",
            "earliest_year",
            "latest_year",
            "unique_years",
            "unique_months",
            "field_verbose_names",
        ]
        read_only_fields = ["type"]

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}