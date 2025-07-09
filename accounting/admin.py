from django.contrib import admin
from .models import (
    Price, PriceFiscalConfiguration, FiscalConfigurationDetail,
    FiscalDirective, FiscalDirectiveType, FiscalFormula
)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'net_amount', 'gross_amount', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['code']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['-created_at']


@admin.register(PriceFiscalConfiguration)
class PriceFiscalConfigurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'fiscal_configuration', 'fiscal_formula', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed']
    search_fields = ['fiscal_configuration', 'fiscal_formula']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['fiscal_configuration']


@admin.register(FiscalConfigurationDetail)
class FiscalConfigurationDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'price_fiscal_configuration', 'price', 'fiscal_directive']
    list_filter = ['price_fiscal_configuration', 'price', 'fiscal_directive']
    search_fields = ['log']
    readonly_fields = ['id']
    ordering = ['id']


@admin.register(FiscalDirective)
class FiscalDirectiveAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'fiscal_directive', 'type', 'percentage', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed', 'type']
    search_fields = ['fiscal_directive', 'code', 'obs']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['fiscal_directive']


@admin.register(FiscalDirectiveType)
class FiscalDirectiveTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(FiscalFormula)
class FiscalFormulaAdmin(admin.ModelAdmin):
    list_display = ['id', 'formula', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed']
    search_fields = ['formula', 'formula_template']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['formula']
