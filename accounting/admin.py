from django.contrib import admin
from price.models import Price
from .models import (
    FiscalConfigurationDetail,
    FiscalDirective,
    FiscalDirectiveType,
)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'net_amount', 'gross_amount', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed']
    search_fields = ['code']
    readonly_fields = ['id', 'code', 'created_at']
    ordering = ['-created_at']


@admin.register(FiscalConfigurationDetail)
class FiscalConfigurationDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'module_id', 'module_config_id', 'fiscal_directive', 'var', 'is_active']
    list_filter = ['module_id', 'fiscal_directive', 'is_active']
    search_fields = ['module_config_id', 'var']
    readonly_fields = ['id']
    ordering = ['id']


@admin.register(FiscalDirective)
class FiscalDirectiveAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code',
        'fiscal_directive',
        'type',
        'value',
        'year',
        'month',
        'is_deleted',
        'is_confirmed',
        'created_at'
    ]
    list_filter = ['is_deleted', 'is_confirmed', 'type', 'year']
    search_fields = ['fiscal_directive', 'code', 'obs']
    readonly_fields = ['id', 'code']
    ordering = ['fiscal_directive']


@admin.register(FiscalDirectiveType)
class FiscalDirectiveTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']
