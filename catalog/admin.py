from django.contrib import admin
from .models import (
    Catalog, Product, Material, Service,
    Menu, ItemGroup, ItemCategory, ItemType, Restriction, Instruction,
    Provider, ProviderType, Bank, BankAccountType, District, Region
)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sku', 'is_visible', 'chef_recommendation', 'created_at']
    list_filter = ['is_visible', 'is_deleted', 'is_confirmed', 'chef_recommendation']
    search_fields = ['name', 'description', 'sku', 'code']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['-created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'sku', 'is_active', 'provider', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'is_confirmed', 'provider', 'type', 'group', 'category']
    search_fields = ['description', 'sku', 'code', 'obs']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['-created_at']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'sku', 'is_active', 'provider', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'is_confirmed', 'provider', 'type', 'group', 'category']
    search_fields = ['description', 'sku', 'code', 'obs']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['-created_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'sku', 'is_active', 'provider', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'is_confirmed', 'provider', 'type', 'group', 'category']
    search_fields = ['description', 'sku', 'code', 'obs']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['-created_at']


# Admin para modelos de referencia
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu', 'franchise_only']
    list_filter = ['franchise_only']
    search_fields = ['menu', 'description']
    ordering = ['menu']


@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'catalog_render']
    list_filter = ['catalog_render']
    search_fields = ['group_name', 'description']
    ordering = ['group_name']


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'catalog_render']
    list_filter = ['catalog_render']
    search_fields = ['category', 'description']
    ordering = ['category']


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(Restriction)
class RestrictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'restriction', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed']
    search_fields = ['restriction', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['restriction']


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ['id', 'instruction', 'type', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed', 'type']
    search_fields = ['instruction', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['instruction']



@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider', 'type', 'rating', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_deleted', 'is_confirmed', 'type']
    search_fields = ['provider', 'company_name', 'contact_name', 'code']
    readonly_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    ordering = ['provider']


@admin.register(ProviderType)
class ProviderTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank']
    search_fields = ['bank', 'description']
    ordering = ['bank']


@admin.register(BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'region']
    search_fields = ['region', 'description']
    ordering = ['region']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'district', 'region']
    list_filter = ['region']
    search_fields = ['district', 'description']
    ordering = ['district']
