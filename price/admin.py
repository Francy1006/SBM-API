from django.contrib import admin
from .models import PriceList, PriceItem, PriceDiscount, PriceHistory


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['name', 'franchise', 'is_active', 'is_default', 'created_by', 'created_at']
    list_filter = ['is_active', 'is_default', 'franchise', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'is_active', 'is_default')
        }),
        ('Relaciones', {
            'fields': ('franchise', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ['catalog_item', 'price_list', 'price', 'cost', 'margin', 'created_by', 'created_at']
    list_filter = ['price_list', 'created_by', 'created_at']
    search_fields = ['catalog_item__name', 'price_list__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['price_list', 'catalog_item']
    
    fieldsets = (
        ('Información de Precio', {
            'fields': ('price', 'cost', 'margin')
        }),
        ('Relaciones', {
            'fields': ('price_list', 'catalog_item', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PriceDiscount)
class PriceDiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_type', 'discount_value', 'franchise', 'is_active', 'valid_from', 'valid_until']
    list_filter = ['discount_type', 'is_active', 'franchise', 'valid_from', 'valid_until']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información del Descuento', {
            'fields': ('name', 'description', 'discount_type', 'discount_value')
        }),
        ('Estado y Validez', {
            'fields': ('is_active', 'valid_from', 'valid_until')
        }),
        ('Relaciones', {
            'fields': ('franchise', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['price_item', 'old_price', 'new_price', 'changed_by', 'changed_at']
    list_filter = ['changed_by', 'changed_at']
    search_fields = ['price_item__catalog_item__name', 'change_reason']
    readonly_fields = ['id', 'changed_at']
    ordering = ['-changed_at']
    
    fieldsets = (
        ('Cambio de Precio', {
            'fields': ('old_price', 'new_price', 'change_reason')
        }),
        ('Relaciones', {
            'fields': ('price_item', 'changed_by')
        }),
        ('Fecha', {
            'fields': ('changed_at',),
            'classes': ('collapse',)
        }),
    )
