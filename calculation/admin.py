from django.contrib import admin

from .models import VariableFormula, CalculationConcept, DataType


@admin.register(VariableFormula)
class VariableFormulaAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'formula', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed']
    search_fields = ['code', 'formula']
    readonly_fields = ['id']
    ordering = ['-created_at']


@admin.register(CalculationConcept)
class CalculationConceptAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'field_name', 'data_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'data_type']
    search_fields = ['field_name', 'description']
    readonly_fields = ['id']
    ordering = ['field_name']


@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'description']
    search_fields = ['code', 'description']
    ordering = ['code']