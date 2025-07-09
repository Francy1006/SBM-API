from django.contrib import admin
from .models import SupportTicket, SupportCategory, SupportResponse, SupportAttachment


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'title', 'status', 'priority', 'franchise', 'created_by', 'created_at']
    list_filter = ['status', 'priority', 'franchise', 'created_at']
    search_fields = ['ticket_number', 'title', 'description']
    readonly_fields = ['id', 'ticket_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('ticket_number', 'title', 'description', 'priority', 'status')
        }),
        ('Asignación', {
            'fields': ('created_by', 'assigned_to', 'franchise')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']


@admin.register(SupportResponse)
class SupportResponseAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'created_by', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_by', 'created_at']
    search_fields = ['content', 'ticket__ticket_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(SupportAttachment)
class SupportAttachmentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'ticket', 'mime_type', 'file_size', 'created_by', 'created_at']
    list_filter = ['mime_type', 'created_by', 'created_at']
    search_fields = ['file_name', 'ticket__ticket_number']
    readonly_fields = ['id', 'file_size', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
