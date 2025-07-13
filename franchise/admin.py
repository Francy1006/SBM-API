from django.contrib import admin
from .models import FranchiseState, Franchise, FranchiseConfigurationType, FranchiseConfiguration, FranchiseConfigurationDetail


@admin.register(FranchiseState)
class FranchiseStateAdmin(admin.ModelAdmin):
    """
    Configuración del admin para FranchiseState
    """
    list_display = ['id', 'state', 'description']
    list_filter = ['state']
    search_fields = ['state', 'description']
    ordering = ['state']
    readonly_fields = ['id']


@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Franchise
    """
    list_display = ['id', 'code', 'franchise', 'state', 'description']
    list_filter = ['state']
    search_fields = ['franchise', 'description', 'code']
    ordering = ['franchise']
    readonly_fields = ['id', 'code']
    autocomplete_fields = ['state']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('franchise', 'description')
        }),
        ('Estado', {
            'fields': ('state',)
        }),
        ('Información del Sistema', {
            'fields': ('id', 'code'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FranchiseConfigurationType)
class FranchiseConfigurationTypeAdmin(admin.ModelAdmin):
    """
    Configuración del admin para FranchiseConfigurationType
    """
    list_display = ['id', 'configuration_type', 'description']
    list_filter = ['configuration_type']
    search_fields = ['configuration_type', 'description']
    ordering = ['configuration_type']
    readonly_fields = ['id']


@admin.register(FranchiseConfiguration)
class FranchiseConfigurationAdmin(admin.ModelAdmin):
    """
    Configuración del admin para FranchiseConfiguration
    """
    list_display = ['id', 'code', 'configuration', 'franchise', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code', 'configuration', 'franchise']
    ordering = ['-created_at']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    list_per_page = 20

    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'configuration', 'franchise')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Fechas', {
            'fields': ('confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FranchiseConfigurationDetail)
class FranchiseConfigurationDetailAdmin(admin.ModelAdmin):
    """
    Configuración del admin para FranchiseConfigurationDetail
    """
    list_display = ['id', 'code', 'detail', 'type', 'configuration', 'index', 'var', 'value', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed', 'type', 'index', 'created_at']
    search_fields = ['code', 'detail', 'var', 'type__configuration_type', 'configuration']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    autocomplete_fields = ['type']
    list_per_page = 20

    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'detail', 'description', 'type', 'configuration', 'index')
        }),
        ('Valores', {
            'fields': ('var', 'value', 'formula')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
