from rest_framework import serializers
from .models import (
    Catalog,
    Product,
    Material,
    Service,
    Menu,
    ItemGroup,
    ItemCategory,
    ItemType,
    Restriction,
    Instruction,
    Provider,
    ProviderType,
    Bank,
    BankAccountType,
    District,
    Region,
)


class CatalogSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Catalog con datos relacionados
    """

    field_verbose_names = serializers.SerializerMethodField()
    menu = serializers.SerializerMethodField()
    item_group = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    restriction = serializers.SerializerMethodField()

    def get_field_verbose_names(self, obj):
        # Solo incluir los campos listados en fields, excepto field_verbose_names
        field_names = [
            "code",
            "sku",
            "menu",
            "name",
            "description",
            "item_group",
            "category",
            "type",
            "chef_recommendation",
            "min_quantity_purchase",
            "rations_quantity",
            "cover_image",
            "is_visible",
            "is_deleted",
            "is_confirmed",
            "restriction",
        ]
        return {
            field: (
                obj._meta.get_field(field).verbose_name
                if hasattr(obj._meta, "get_field")
                else field
            )
            for field in field_names
        }

    def get_menu(self, obj):
        return obj.menu.menu if obj.menu else None

    def get_item_group(self, obj):
        return obj.item_group.group_name if obj.item_group else None

    def get_category(self, obj):
        return obj.category.category if obj.category else None

    def get_type(self, obj):
        return obj.type.type if obj.type else None

    def get_restriction(self, obj):
        return obj.restriction.restriction if obj.restriction else None

    class Meta:
        model = Catalog
        fields = [
            "code",
            "sku",
            "cover_image",
            "menu",
            "name",
            "description",
            "item_group",
            "category",
            "type",
            "chef_recommendation",
            "min_quantity_purchase",
            "rations_quantity",
            "is_visible",
            "is_deleted",
            "is_confirmed",
            "restriction",
            "field_verbose_names",
        ]
        read_only_fields = [
            "code",
            "sku",
            "code",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Product
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Product
        fields = [
            "id",
            "code",
            "sku",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "price",
            "provider",
            "type",
            "group",
            "category",
            "url",
            "package",
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
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]


class MaterialSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Material
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Material
        fields = [
            "id",
            "code",
            "sku",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "price",
            "provider",
            "type",
            "group",
            "category",
            "url",
            "package",
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
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Service
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Service
        fields = [
            "id",
            "code",
            "sku",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "price",
            "provider",
            "type",
            "group",
            "category",
            "url",
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
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]


# Serializers para modelos de referencia
class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Menu
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Menu
        fields = ["id", "menu", "description", "franchise_only"]
        read_only_fields = ["id"]


class ItemGroupSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemGroup
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = ItemGroup
        fields = ["id", "group_name", "description", "catalog_render"]
        read_only_fields = ["id"]


class ItemCategorySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemCategory
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = ItemCategory
        fields = ["id", "category", "description", "catalog_render"]
        read_only_fields = ["id"]


class ItemTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemType
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = ItemType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class RestrictionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Restriction
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Restriction
        fields = [
            "id",
            "restriction",
            "description",
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
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]


class InstructionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Instruction
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Instruction
        fields = [
            "id",
            "instruction",
            "description",
            "url_documentation",
            "type",
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
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]


class ProviderSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Provider
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Provider
        fields = [
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
        ]
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]


class ProviderTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ProviderType
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = ProviderType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class BankSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Bank
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Bank
        fields = ["id", "bank", "description"]
        read_only_fields = ["id"]


class BankAccountTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo BankAccountType
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = BankAccountType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class RegionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Region
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = Region
        fields = ["id", "region", "description"]
        read_only_fields = ["id"]


class DistrictSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo District
    """

    # Elimino el SerializerMethodField y el método get_field_verbose_names

    class Meta:
        model = District
        fields = ["id", "district", "region", "description"]
        read_only_fields = ["id"]
