from django.contrib import admin
from .models import (
    Catalog, Product, Material, Service,
    Menu, ItemGroup, ItemCategory, ItemType,
    Restriction, Instruction, InstructionType,
    ItemConfiguration
)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sku', 'is_visible']
    search_fields = ['name', 'description', 'sku', 'code']
    ordering = ['-id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'sku', 'is_active']
    list_filter = ['is_active']
    search_fields = ['description', 'sku', 'code']
    ordering = ['-id']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'sku', 'is_active']
    list_filter = ['is_active']
    search_fields = ['description', 'sku', 'code']
    ordering = ['-id']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'sku', 'is_active']
    list_filter = ['is_active']
    search_fields = ['description', 'sku', 'code']
    ordering = ['-id']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu']
    search_fields = ['menu', 'description']
    ordering = ['menu']


@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name']
    search_fields = ['group_name', 'description']
    ordering = ['group_name']


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']
    search_fields = ['category', 'description']
    ordering = ['category']


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(Restriction)
class RestrictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'restriction']
    search_fields = ['restriction', 'description']
    ordering = ['restriction']


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ['code', 'instruction']
    search_fields = ['instruction', 'description']
    ordering = ['instruction']


@admin.register(InstructionType)
class InstructionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(ItemConfiguration)
class ItemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['code', 'configuration']
    search_fields = ['configuration', 'description']
    ordering = ['-id']
