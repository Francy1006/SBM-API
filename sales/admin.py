from django.contrib import admin
from clients.models import Client
from .models import (
    Order,
    OrderDetail,
    OrderType,
    FiscalDocumentation,
    FiscalDocumentType,
    OrderFiscalDocumentation,
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "company_name",
        "owner_name",
        "direct_email",
        "direct_phone",
        "status",
        "platform",
        "is_active",
        "created_at",
    ]
    list_filter = [
        "is_active",
        "contacted",
        "same_address_detected",
        "has_visible_physical_store",
        "status",
        "platform",
        "created_at",
    ]
    search_fields = [
        "code",
        "company_name",
        "owner_name",
        "company_rut",
        "direct_email",
        "direct_phone",
        "exact_address",
    ]
    readonly_fields = ["id", "code", "created_at", "updated_at", "deleted_at"]
    ordering = ["-created_at"]


@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "category", "description"]
    list_filter = ["category"]
    search_fields = ["type", "description", "category"]
    ordering = ["category", "type"]


@admin.register(FiscalDocumentType)
class FiscalDocumentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "description"]
    search_fields = ["type", "description"]
    ordering = ["type"]


@admin.register(FiscalDocumentation)
class FiscalDocumentationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "document_type",
        "document_number",
        "issued_at",
        "created_at",
        "created_by",
    ]
    list_filter = ["document_type", "created_at", "issued_at"]
    search_fields = ["code", "document_number", "url"]
    readonly_fields = ["id", "created_at"]
    ordering = ["-id"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "name",
        "franchise",
        "client",
        "order_type",
        "status",
        "is_processed",
        "is_closed",
        "is_deleted",
        "created_at",
    ]
    list_filter = [
        "order_type",
        "status",
        "franchise",
        "is_processed",
        "is_closed",
        "is_deleted",
        "is_canceled",
        "requires_fiscal_documentation",
        "fiscal_documentation_error",
        "created_at",
    ]
    search_fields = [
        "code",
        "name",
        "description",
        "client__company_name",
        "client__owner_name",
    ]
    readonly_fields = [
        "id",
        "code",
        "created_at",
        "updated_at",
        "deleted_at",
        "log",
        "version",
    ]
    ordering = ["-created_at"]


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "order_type",
        "item_type",
        "id_item",
        "description",
        "quantity",
        "net_amount",
        "is_processed",
        "is_closed",
        "is_deleted",
        "created_at",
    ]
    list_filter = [
        "order_type",
        "item_type",
        "is_processed",
        "is_closed",
        "is_deleted",
        "is_canceled",
        "requires_fiscal_documentation",
        "fiscal_documentation_error",
        "created_at",
    ]
    search_fields = ["description", "id_item", "obs", "order__code"]
    readonly_fields = ["id", "created_at", "updated_at", "deleted_at"]
    ordering = ["order", "id"]


@admin.register(OrderFiscalDocumentation)
class OrderFiscalDocumentationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "fiscal_documentation",
        "is_primary",
        "created_at",
        "created_by",
    ]
    list_filter = ["is_primary", "created_at"]
    search_fields = ["description", "order__code", "fiscal_documentation__code"]
    readonly_fields = ["id", "created_at"]
    ordering = ["order", "-is_primary", "id"]
    
    