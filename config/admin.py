from django.contrib import admin
from .models import SystemConfig, FranchiseConfig, NotificationTemplate, AuditLog


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_by', 'created_at']
    search_fields = ['key', 'value', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['key']
    
    fieldsets = (
        ('Configuración', {
            'fields': ('key', 'value', 'description', 'is_active')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FranchiseConfig)
class FranchiseConfigAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'franchise', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'franchise', 'created_by', 'created_at']
    search_fields = ['key', 'value', 'description', 'franchise__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['franchise', 'key']
    
    fieldsets = (
        ('Configuración', {
            'fields': ('key', 'value', 'description', 'is_active')
        }),
        ('Relaciones', {
            'fields': ('franchise', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'created_by', 'created_at']
    list_filter = ['template_type', 'is_active', 'created_by', 'created_at']
    search_fields = ['name', 'subject', 'content']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Plantilla', {
            'fields': ('name', 'template_type', 'subject', 'content', 'variables', 'is_active')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'franchise', 'created_at']
    list_filter = ['action', 'model_name', 'user', 'franchise', 'created_at']
    search_fields = ['user__username', 'object_id', 'details', 'ip_address']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Acción', {
            'fields': ('action', 'model_name', 'object_id', 'details')
        }),
        ('Información de Sesión', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Relaciones', {
            'fields': ('user', 'franchise')
        }),
        ('Fecha', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
