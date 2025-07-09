from django.contrib import admin
from .models import Customer, Sale, SaleItem, SalePayment, SalesOrder


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer_type', 'email', 'phone', 'franchise', 'is_active', 'created_by', 'created_at']
    list_filter = ['customer_type', 'is_active', 'franchise', 'created_by', 'created_at']
    search_fields = ['name', 'email', 'phone', 'tax_id', 'franchise__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('name', 'customer_type', 'email', 'phone', 'address', 'tax_id', 'credit_limit', 'is_active')
        }),
        ('Relaciones', {
            'fields': ('franchise', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'customer', 'status', 'payment_status', 'total_amount', 'franchise', 'sale_date']
    list_filter = ['status', 'payment_status', 'franchise', 'sale_date', 'created_by']
    search_fields = ['sale_number', 'customer__name', 'notes', 'franchise__name']
    readonly_fields = ['id', 'sale_number', 'created_at', 'updated_at']
    date_hierarchy = 'sale_date'
    ordering = ['-sale_date']
    
    fieldsets = (
        ('Información de la Venta', {
            'fields': ('sale_number', 'status', 'payment_status', 'sale_date', 'due_date', 'notes')
        }),
        ('Montos', {
            'fields': ('subtotal', 'tax_amount', 'total_amount', 'discount_amount')
        }),
        ('Relaciones', {
            'fields': ('customer', 'franchise', 'created_by')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'catalog_item', 'quantity', 'unit_price', 'total_price', 'discount_rate', 'created_at']
    list_filter = ['discount_rate', 'sale__status', 'created_at']
    search_fields = ['notes', 'catalog_item__name', 'sale__sale_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['sale', 'created_at']
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('quantity', 'unit_price', 'discount_rate', 'discount_amount', 'total_price', 'notes')
        }),
        ('Relaciones', {
            'fields': ('sale', 'catalog_item')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SalePayment)
class SalePaymentAdmin(admin.ModelAdmin):
    list_display = ['sale', 'amount', 'payment_method', 'payment_date', 'created_by', 'created_at']
    list_filter = ['payment_method', 'payment_date', 'created_by', 'created_at']
    search_fields = ['reference', 'notes', 'sale__sale_number']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'payment_date'
    ordering = ['-payment_date']
    
    fieldsets = (
        ('Información del Pago', {
            'fields': ('amount', 'payment_method', 'reference', 'payment_date', 'notes')
        }),
        ('Relaciones', {
            'fields': ('sale', 'created_by')
        }),
        ('Fecha', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'status', 'total_amount', 'franchise', 'order_date', 'delivery_date']
    list_filter = ['status', 'franchise', 'order_date', 'delivery_date', 'created_by']
    search_fields = ['order_number', 'customer__name', 'notes', 'franchise__name']
    readonly_fields = ['id', 'order_number', 'created_at', 'updated_at']
    date_hierarchy = 'order_date'
    ordering = ['-order_date']
    
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('order_number', 'status', 'order_date', 'delivery_date', 'notes')
        }),
        ('Montos', {
            'fields': ('total_amount',)
        }),
        ('Relaciones', {
            'fields': ('customer', 'franchise', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
