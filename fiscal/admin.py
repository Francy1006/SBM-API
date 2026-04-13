from django.contrib import admin
from .models import FiscalDocument, FiscalItem, TaxRate, FiscalPayment


@admin.register(FiscalDocument)
class FiscalDocumentAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'document_type', 'status', 'total_amount', 'franchise', 'client', 'issue_date']
    list_filter = ['document_type', 'status', 'franchise', 'issue_date']
    search_fields = ['document_number', 'client__name', 'franchise__name']
    readonly_fields = ['id', 'document_number', 'created_at', 'updated_at']
    date_hierarchy = 'issue_date'
    ordering = ['-issue_date']
    
    fieldsets = (
        ('Información del Documento', {
            'fields': ('document_number', 'document_type', 'status')
        }),
        ('Montos', {
            'fields': ('total_amount', 'tax_amount', 'net_amount')
        }),
        ('Fechas', {
            'fields': ('issue_date', 'due_date')
        }),
        ('Relaciones', {
            'fields': ('franchise', 'client', 'created_by')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FiscalItem)
class FiscalItemAdmin(admin.ModelAdmin):
    list_display = ['fiscal_document', 'catalog_item', 'quantity', 'unit_price', 'total_price', 'tax_rate']
    list_filter = ['tax_rate', 'fiscal_document__document_type', 'created_at']
    search_fields = ['catalog_item__name', 'description', 'fiscal_document__document_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['fiscal_document', 'created_at']
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('quantity', 'unit_price', 'total_price', 'tax_rate', 'tax_amount', 'description')
        }),
        ('Relaciones', {
            'fields': ('fiscal_document', 'catalog_item')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate', 'franchise', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'franchise', 'created_by', 'created_at']
    search_fields = ['name', 'description', 'franchise__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Información de la Tasa', {
            'fields': ('name', 'rate', 'description', 'is_active')
        }),
        ('Relaciones', {
            'fields': ('franchise', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FiscalPayment)
class FiscalPaymentAdmin(admin.ModelAdmin):
    list_display = ['fiscal_document', 'amount', 'payment_method', 'payment_date', 'created_by']
    list_filter = ['payment_method', 'payment_date', 'created_by', 'created_at']
    search_fields = ['reference', 'fiscal_document__document_number']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'payment_date'
    ordering = ['-payment_date']
    
    fieldsets = (
        ('Información del Pago', {
            'fields': ('amount', 'payment_method', 'reference', 'payment_date')
        }),
        ('Relaciones', {
            'fields': ('fiscal_document', 'created_by')
        }),
        ('Fecha', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
