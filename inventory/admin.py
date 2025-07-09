from django.contrib import admin
from .models import Warehouse, InventoryItem, InventoryMovement, InventoryCount, InventoryCountItem


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'franchise', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'franchise', 'created_by', 'created_at']
    search_fields = ['name', 'code', 'address', 'description', 'franchise__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Información del Almacén', {
            'fields': ('name', 'code', 'address', 'description', 'is_active')
        }),
        ('Relaciones', {
            'fields': ('franchise', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['catalog_item', 'warehouse', 'quantity', 'unit_cost', 'total_cost', 'created_by', 'created_at']
    list_filter = ['warehouse', 'created_by', 'created_at']
    search_fields = ['catalog_item__name', 'warehouse__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['warehouse', 'catalog_item']
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('quantity', 'minimum_stock', 'maximum_stock', 'unit_cost', 'total_cost')
        }),
        ('Relaciones', {
            'fields': ('warehouse', 'catalog_item', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ['movement_type', 'catalog_item', 'warehouse', 'quantity', 'total_cost', 'movement_date', 'created_by']
    list_filter = ['movement_type', 'warehouse', 'created_by', 'movement_date']
    search_fields = ['reference', 'notes', 'catalog_item__name', 'warehouse__name']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'movement_date'
    ordering = ['-movement_date']
    
    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('movement_type', 'quantity', 'unit_cost', 'total_cost', 'reference', 'notes', 'movement_date')
        }),
        ('Relaciones', {
            'fields': ('warehouse', 'catalog_item', 'created_by')
        }),
        ('Fecha', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(InventoryCount)
class InventoryCountAdmin(admin.ModelAdmin):
    list_display = ['count_number', 'warehouse', 'status', 'start_date', 'end_date', 'created_by', 'created_at']
    list_filter = ['status', 'warehouse', 'created_by', 'start_date']
    search_fields = ['count_number', 'notes', 'warehouse__name']
    readonly_fields = ['id', 'count_number', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    
    fieldsets = (
        ('Información del Conteo', {
            'fields': ('count_number', 'status', 'start_date', 'end_date', 'notes')
        }),
        ('Relaciones', {
            'fields': ('warehouse', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InventoryCountItem)
class InventoryCountItemAdmin(admin.ModelAdmin):
    list_display = ['inventory_count', 'catalog_item', 'expected_quantity', 'counted_quantity', 'difference', 'created_at']
    list_filter = ['inventory_count__status', 'inventory_count__warehouse', 'created_at']
    search_fields = ['notes', 'catalog_item__name', 'inventory_count__count_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['inventory_count', 'catalog_item']
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('expected_quantity', 'counted_quantity', 'difference', 'notes')
        }),
        ('Relaciones', {
            'fields': ('inventory_count', 'catalog_item')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
