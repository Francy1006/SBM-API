from django.contrib import admin
from .models import FranchiseState, Franchise


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
