from rest_framework import serializers
from django.db import transaction
from django.utils import timezone

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
    InstructionType,
    ItemConfiguration,
)

from inventory.models import Package, PackageType, TransportType, MeasureUnit
from price.models import Price


class CatalogSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Catalog con datos relacionados
    """
    field_verbose_names = serializers.SerializerMethodField()
    menu_name = serializers.SerializerMethodField()
    item_group_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()
    restriction_name = serializers.SerializerMethodField()
    usage_instructions_name = serializers.SerializerMethodField()
    configuration_name = serializers.SerializerMethodField()
    price_data = serializers.DictField(write_only=True, required=False)

    def get_field_verbose_names(self, obj):
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

    def get_menu_name(self, obj):
        try:
            return obj.menu.menu if obj.menu else None
        except Exception:
            return None

    def get_item_group_name(self, obj):
        try:
            return obj.item_group.group_name if obj.item_group else None
        except Exception:
            return None

    def get_category_name(self, obj):
        try:
            return obj.category.category if obj.category else None
        except Exception:
            return None

    def get_type_name(self, obj):
        try:
            return obj.type.type if obj.type else None
        except Exception:
            return None

    def get_restriction_name(self, obj):
        try:
            return obj.restriction.restriction if obj.restriction else None
        except Exception:
            return None

    def get_usage_instructions_name(self, obj):
        try:
            return obj.usage_instructions.instruction if obj.usage_instructions else None
        except Exception:
            return None

    def get_configuration_name(self, obj):
        try:
            return obj.configuration.configuration if obj.configuration else None
        except Exception:
            return None

    def create(self, validated_data):
        price_data = validated_data.pop("price_data", None)

        if not price_data:
            from price.models import PriceConfiguration
            price_config = PriceConfiguration.objects.filter(price_type=4).first()
            if not price_config:
                raise serializers.ValidationError(
                    {"price_data": "No se encontró una configuración de precio válida para catálogos (price_type=4)."}
                )
            price_data = {"base_net_amount": 1, "price_configuration": price_config.code}
        else:
            allowed_fields = {"base_net_amount", "price_configuration"}
            if set(price_data.keys()) != allowed_fields:
                raise serializers.ValidationError({"price_data": f"Solo se permiten los campos: {allowed_fields}."})
            if price_data.get("base_net_amount") in [None, ""]:
                raise serializers.ValidationError({"price_data": {"base_net_amount": "Este campo es obligatorio."}})
            if price_data.get("price_configuration") in [None, ""]:
                raise serializers.ValidationError({"price_data": {"price_configuration": "Este campo es obligatorio."}})

        self.context["price_data"] = price_data
        return super().create(validated_data)

    class Meta:
        model = Catalog
        fields = [
            "code",
            "sku",
            "cover_image",
            "menu",
            "menu_name",
            "name",
            "description",
            "item_group",
            "item_group_name",
            "category",
            "category_name",
            "type",
            "type_name",
            "chef_recommendation",
            "usage_instructions",
            "usage_instructions_name",
            "min_quantity_purchase",
            "rations_quantity",
            "is_visible",
            "is_deleted",
            "is_confirmed",
            "restriction",
            "restriction_name",
            "configuration",
            "configuration_name",
            "field_verbose_names",
            "price_data",
            "price",
        ]
        read_only_fields = [
            "code",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "price",
            "configuration",
        ]


class ProductSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()
    net_amount = serializers.SerializerMethodField()
    price_data = serializers.DictField(write_only=True, required=True)

    def get_field_verbose_names(self, obj):
        field_names = [
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
            "item_group",
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
            "net_amount",
        ]
        verbose = {"net_amount": "Valor BASE NETO"}
        return {
            field: (
                verbose[field]
                if field in verbose
                else (
                    obj._meta.get_field(field).verbose_name
                    if hasattr(obj._meta, "get_field") and field in [f.name for f in obj._meta.fields]
                    else field
                )
            )
            for field in field_names
        }

    def get_net_amount(self, obj):
        try:
            price_obj = Price._default_manager.get(code=obj.price)
            return price_obj.net_amount
        except Exception:
            return None

    def create(self, validated_data):
        request = self.context.get("request", None)
        price_data = validated_data.pop("price_data", None)
        if not price_data:
            raise serializers.ValidationError({"price_data": "Este campo es requerido."})

        allowed_fields = {"base_net_amount", "price_configuration"}
        if set(price_data.keys()) != allowed_fields:
            raise serializers.ValidationError({"price_data": f"Solo se permiten los campos: {allowed_fields}."})
        if price_data.get("base_net_amount") in [None, ""]:
            raise serializers.ValidationError({"price_data": {"base_net_amount": "Este campo es obligatorio."}})
        if price_data.get("price_configuration") in [None, ""]:
            raise serializers.ValidationError({"price_data": {"price_configuration": "Este campo es obligatorio."}})

        validated_data.pop("price", None)
        validated_data.pop("created_by", None)

        user_code = getattr(getattr(request, "user", None), "code", "system")
        now = timezone.now()

        import uuid
        with transaction.atomic():
            product_code = str(uuid.uuid4())
            product = Product._default_manager.create(
                **validated_data,
                code=product_code,
                created_by=user_code,
                created_at=now,
            )

            price_code = str(uuid.uuid4())
            price_obj = Price._default_manager.create(
                code=price_code,
                base_net_amount=price_data["base_net_amount"],
                gross_amount=0,
                iva_amount=0,
                retention_amount=0,
                price_configuration=price_data["price_configuration"],
                created_by=user_code,
                created_at=now,
                record_item_code=product_code,
                price_record_type=1,
            )
            product.price = price_obj.code
            product.save()

        return product

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
            "provider",
            "type",
            "item_group",
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
            "net_amount",
            "field_verbose_names",
            "price_data",
            "price",
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
            "price",
        ]


class ProductManageSerializer(serializers.Serializer):
    code = serializers.CharField()
    sku = serializers.CharField()
    description = serializers.CharField()
    base_net_amount = serializers.IntegerField()
    obs = serializers.CharField()
    package_unit = serializers.IntegerField()
    min_package_purchase = serializers.IntegerField()
    provider = serializers.IntegerField()
    type = serializers.IntegerField()
    type_name = serializers.CharField()
    item_group = serializers.IntegerField()
    group_name = serializers.CharField()
    category = serializers.IntegerField()
    category_name = serializers.CharField()
    url = serializers.CharField(allow_null=True, allow_blank=True)
    package = serializers.IntegerField()
    package_description = serializers.CharField()
    is_active = serializers.BooleanField()
    is_deleted = serializers.BooleanField(allow_null=True)
    is_confirmed = serializers.BooleanField(allow_null=True)
    created_at = serializers.DateTimeField()

    @staticmethod
    def get_verbose_names():
        return {
            "code": "Código UUID",
            "sku": "SKU",
            "description": "Descripción",
            "base_net_amount": "Valor Neto Base",
            "obs": "Observaciones",
            "package_unit": "Unidad de Empaque",
            "min_package_purchase": "Compra Mínima de Empaque",
            "provider": "Proveedor",
            "type": "Tipo (ID)",
            "type_name": "Tipo",
            "item_group": "Grupo (ID)",
            "group_name": "Nombre del Grupo",
            "category": "Categoría (ID)",
            "category_name": "Categoría",
            "url": "URL",
            "package": "Empaque (ID)",
            "package_description": "Descripción de Empaque",
            "is_active": "Está Activo",
            "is_deleted": "Está Eliminado",
            "is_confirmed": "Está Confirmado",
            "created_at": "Fecha de Creación",
        }


class ProductListSerializer(serializers.Serializer):
    code = serializers.CharField()
    sku = serializers.CharField()
    description = serializers.CharField()
    base_net_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    net_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    gross_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    iva_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    aditional_tax_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    retention_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    price_configuration = serializers.CharField(allow_null=True)
    price_configuration_label = serializers.CharField(allow_null=True)
    obs = serializers.CharField(allow_null=True)
    package_unit = serializers.IntegerField(allow_null=True)
    min_package_purchase = serializers.IntegerField(allow_null=True)
    provider = serializers.IntegerField(allow_null=True)
    type = serializers.IntegerField(allow_null=True)
    type_name = serializers.CharField(allow_null=True)
    item_group = serializers.IntegerField(allow_null=True)
    group_name = serializers.CharField(allow_null=True)
    category = serializers.IntegerField(allow_null=True)
    category_name = serializers.CharField(allow_null=True)
    url = serializers.CharField(allow_null=True)
    package = serializers.IntegerField(allow_null=True)
    package_description = serializers.CharField(allow_null=True)
    is_active = serializers.BooleanField()
    is_deleted = serializers.BooleanField(allow_null=True)
    is_confirmed = serializers.BooleanField(allow_null=True)
    created_at = serializers.DateTimeField()


class MaterialSerializer(serializers.ModelSerializer):
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


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "menu", "description", "franchise_only"]
        read_only_fields = ["id"]


class ItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemGroup
        fields = ["id", "group_name", "description"]
        read_only_fields = ["id"]


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ["id", "category", "description"]
        read_only_fields = ["id"]


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class RestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restriction
        fields = ["id", "restriction", "description", "is_deleted", "is_confirmed", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = "__all__"


class CatalogListSerializer(serializers.Serializer):
    # FIX: NO incluir "code" (en la lista inicial NO estaba)
    sku = serializers.CharField()
    cover_image = serializers.CharField(allow_null=True)
    menu = serializers.IntegerField(allow_null=True)
    menu_name = serializers.CharField(allow_null=True)
    category = serializers.IntegerField(allow_null=True)
    category_name = serializers.CharField(allow_null=True)
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    obs = serializers.CharField(allow_null=True)
    chef_recommendation = serializers.BooleanField()
    item_type = serializers.IntegerField(allow_null=True)
    type_name = serializers.CharField(allow_null=True)
    item_group = serializers.IntegerField(allow_null=True)
    group_name = serializers.CharField(allow_null=True)
    base_net_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    net_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    gross_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    iva_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    aditional_tax_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    retention_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    price_configuration = serializers.CharField(allow_null=True)
    min_quantity_purchase = serializers.IntegerField(allow_null=True)
    rations_quantity = serializers.IntegerField(allow_null=True)
    item_configuration = serializers.CharField(allow_null=True)
    configuration = serializers.CharField(allow_null=True)
    is_visible = serializers.BooleanField()
    is_confirmed = serializers.BooleanField(allow_null=True)
    created_at = serializers.DateTimeField()


class ItemConfigurationSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    def get_field_verbose_names(self, obj):
        field_names = [
            "id",
            "code",
            "configuration",
            "description",
            "package",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]
        return {
            field: (
                obj._meta.get_field(field).verbose_name
                if hasattr(obj._meta, "get_field")
                else field
            )
            for field in field_names
        }

    def create(self, validated_data):
        request = self.context.get("request", None)
        validated_data.pop("created_by", None)
        user_code = getattr(getattr(request, "user", None), "code", "system")
        now = timezone.now()

        item_config = ItemConfiguration._default_manager.create(
            **validated_data,
            created_by=user_code,
            created_at=now,
        )
        return item_config

    class Meta:
        model = ItemConfiguration
        fields = [
            "id",
            "code",
            "configuration",
            "description",
            "package",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class PackageSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    def get_field_verbose_names(self, obj):
        field_names = [
            "id",
            "description",
            "package_type",
            "transport_type",
            "size",
            "weight",
            "measure_unit",
            "quantity_unit",
            "storage_instructions",
            "transport_instructions",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]
        return {
            field: (
                obj._meta.get_field(field).verbose_name
                if hasattr(obj._meta, "get_field")
                else field
            )
            for field in field_names
        }

    class Meta:
        model = Package
        fields = [
            "id",
            "description",
            "package_type",
            "transport_type",
            "size",
            "weight",
            "measure_unit",
            "quantity_unit",
            "storage_instructions",
            "transport_instructions",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "field_verbose_names",
        ]


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = ["id", "measure_unit", "description"]
        read_only_fields = ["id"]


class InstructionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionType
        fields = [
            "id",
            "type",
            "description",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "confirmed_at", "deleted_at"]