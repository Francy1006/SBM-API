from rest_framework import serializers
from .models import (
    Warehouse,
    InventoryItem,
    InventoryMovement,
    InventoryCount,
    InventoryCountItem,
    Package,
    PackageType,
    TransportType,
    MeasureUnit,
    Provider,
    ProviderType,
)


class WarehouseSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Warehouse
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    inventory_items_count = serializers.SerializerMethodField(
        help_text="Número de Items"
    )

    class Meta:
        model = Warehouse
        fields = [
            "id",
            "name",
            "code",
            "address",
            "description",
            "is_active",
            "franchise",
            "created_by",
            "created_at",
            "updated_at",
            "field_verbose_names",
            "franchise_name",
            "created_by_name",
            "inventory_items_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update(
            {
                "franchise_name": "Franquicia",
                "created_by_name": "Creado por",
                "inventory_items_count": "Número de Items",
            }
        )
        return verbose_names

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_inventory_items_count(self, obj):
        return obj.inventory_items.count()


class InventoryItemSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo InventoryItem
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    warehouse_name = serializers.SerializerMethodField(help_text="Almacén")
    catalog_item_name = serializers.SerializerMethodField(help_text="Item del Catálogo")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "quantity",
            "minimum_stock",
            "maximum_stock",
            "unit_cost",
            "total_cost",
            "warehouse",
            "catalog_item",
            "created_by",
            "created_at",
            "updated_at",
            "field_verbose_names",
            "warehouse_name",
            "catalog_item_name",
            "created_by_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update(
            {
                "warehouse_name": "Almacén",
                "catalog_item_name": "Item del Catálogo",
                "created_by_name": "Creado por",
            }
        )
        return verbose_names

    def get_warehouse_name(self, obj):
        return obj.warehouse.name if obj.warehouse else None

    def get_catalog_item_name(self, obj):
        return obj.catalog_item.name if obj.catalog_item else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class InventoryMovementSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo InventoryMovement
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    warehouse_name = serializers.SerializerMethodField(help_text="Almacén")
    catalog_item_name = serializers.SerializerMethodField(help_text="Item del Catálogo")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = InventoryMovement
        fields = [
            "id",
            "movement_type",
            "quantity",
            "unit_cost",
            "total_cost",
            "reference",
            "notes",
            "movement_date",
            "warehouse",
            "catalog_item",
            "created_by",
            "created_at",
            "field_verbose_names",
            "warehouse_name",
            "catalog_item_name",
            "created_by_name",
        ]
        read_only_fields = ["id", "created_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update(
            {
                "warehouse_name": "Almacén",
                "catalog_item_name": "Item del Catálogo",
                "created_by_name": "Creado por",
            }
        )
        return verbose_names

    def get_warehouse_name(self, obj):
        return obj.warehouse.name if obj.warehouse else None

    def get_catalog_item_name(self, obj):
        return obj.catalog_item.name if obj.catalog_item else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class InventoryCountSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo InventoryCount
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    warehouse_name = serializers.SerializerMethodField(help_text="Almacén")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    items_count = serializers.SerializerMethodField(help_text="Número de Items")

    class Meta:
        model = InventoryCount
        fields = [
            "id",
            "count_number",
            "status",
            "start_date",
            "end_date",
            "notes",
            "warehouse",
            "created_by",
            "created_at",
            "updated_at",
            "field_verbose_names",
            "warehouse_name",
            "created_by_name",
            "items_count",
        ]
        read_only_fields = ["id", "count_number", "created_at", "updated_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update(
            {
                "warehouse_name": "Almacén",
                "created_by_name": "Creado por",
                "items_count": "Número de Items",
            }
        )
        return verbose_names

    def get_warehouse_name(self, obj):
        return obj.warehouse.name if obj.warehouse else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_items_count(self, obj):
        return obj.items.count()


class InventoryCountItemSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo InventoryCountItem
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    inventory_count_number = serializers.SerializerMethodField(
        help_text="Conteo de Inventario"
    )
    catalog_item_name = serializers.SerializerMethodField(help_text="Item del Catálogo")

    class Meta:
        model = InventoryCountItem
        fields = [
            "id",
            "expected_quantity",
            "counted_quantity",
            "difference",
            "notes",
            "inventory_count",
            "catalog_item",
            "created_at",
            "updated_at",
            "field_verbose_names",
            "inventory_count_number",
            "catalog_item_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update(
            {
                "inventory_count_number": "Conteo de Inventario",
                "catalog_item_name": "Item del Catálogo",
            }
        )
        return verbose_names

    def get_inventory_count_number(self, obj):
        return obj.inventory_count.count_number if obj.inventory_count else None

    def get_catalog_item_name(self, obj):
        return obj.catalog_item.name if obj.catalog_item else None


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = "__all__"


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = "__all__"


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = "__all__"


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class ProviderSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField()
    field_verbose_names = serializers.SerializerMethodField()

    def get_type_name(self, obj):
        return obj.type.type if obj.type else None

    def get_field_verbose_names(self, obj):
        field_names = [
            "id",
            "code",
            "provider",
            "type",
            "rating",
            "obs_provider",
            "contact_name",
            "contact_mail",
            "contact_phone",
            "contact_phone2",
            "website_url",
            "obs_contact",
            "company_name",
            "company_rut",
            "company_activity",
            "legal_representative",
            "billing_address",
            "billing_mail",
            "billing_phone",
            "company_bank",
            "bank_account_type",
            "bank_account_number",
            "bank_account_mail",
            "dispatch_address",
            "dispatch_maps_location",
            "obs_dispatch",
            "dispatch_district",
            "dispatch_region",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
        ]
        return {
            field: (
                obj._meta.get_field(field).verbose_name
                if field in [f.name for f in obj._meta.fields]
                else field
            )
            for field in field_names
        }

    def create(self, validated_data):
        request = self.context.get("request", None)

        validated_data.pop("code", None)
        validated_data.pop("created_by", None)
        validated_data.pop("updated_by", None)
        validated_data.pop("confirmed_by", None)
        validated_data.pop("deleted_by", None)

        user_code = getattr(getattr(request, "user", None), "code", None)

        provider = Provider._default_manager.create(
            **validated_data,
            created_by=user_code,
        )
        return provider

    def update(self, instance, validated_data):
        request = self.context.get("request", None)
        user_code = getattr(getattr(request, "user", None), "code", None)

        validated_data.pop("code", None)
        validated_data.pop("created_by", None)
        validated_data.pop("confirmed_by", None)
        validated_data.pop("deleted_by", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.updated_by = user_code
        instance.save()
        return instance

    class Meta:
        model = Provider
        fields = [
            "id",
            "code",
            "provider",
            "type",
            "type_name",
            "rating",
            "obs_provider",
            "contact_name",
            "contact_mail",
            "contact_phone",
            "contact_phone2",
            "website_url",
            "obs_contact",
            "company_name",
            "company_rut",
            "company_activity",
            "legal_representative",
            "billing_address",
            "billing_mail",
            "billing_phone",
            "company_bank",
            "bank_account_type",
            "bank_account_number",
            "bank_account_mail",
            "dispatch_address",
            "dispatch_maps_location",
            "obs_dispatch",
            "dispatch_district",
            "dispatch_region",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "field_verbose_names",
            "type_name",
        ]
        extra_kwargs = {
            "obs_provider": {"required": False, "allow_blank": True},
            "contact_name": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "contact_mail": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "website_url": {"required": False, "allow_null": True, "allow_blank": True},
            "obs_contact": {"required": False, "allow_null": True, "allow_blank": True},
            "company_name": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "company_rut": {"required": False, "allow_null": True, "allow_blank": True},
            "company_activity": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "legal_representative": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "billing_address": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "billing_mail": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "bank_account_number": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "bank_account_mail": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "dispatch_address": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "dispatch_maps_location": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "obs_dispatch": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
        }


class ProviderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderType
        fields = "__all__"
