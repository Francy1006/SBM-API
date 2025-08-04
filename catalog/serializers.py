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
    InstructionType,
    Provider,
    ProviderType,
    Bank,
    BankAccountType,
    District,
    Region,
    ItemConfiguration,
)
from inventory.models import Package, PackageType, TransportType, MeasureUnit
from price.models import Price
from django.db import transaction
import uuid
from django.utils import timezone


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
    usage_instructions = serializers.SerializerMethodField()
    configuration = serializers.SerializerMethodField()
    price_data = serializers.DictField(write_only=True, required=True)

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

    def get_usage_instructions(self, obj):
        return obj.usage_instructions.instruction if obj.usage_instructions else None

    def get_configuration(self, obj):
        return obj.configuration.configuration if obj.configuration else None

    def create(self, validated_data):
        request = self.context.get('request', None)
        price_data = validated_data.pop('price_data', None)
        if not price_data:
            raise serializers.ValidationError({'price_data': 'Este campo es requerido.'})
        # Validar que solo estén los campos permitidos
        allowed_fields = {'base_net_amount', 'price_configuration'}
        if set(price_data.keys()) != allowed_fields:
            raise serializers.ValidationError({'price_data': f'Solo se permiten los campos: {allowed_fields}.'})
        # Validar que ambos campos sean obligatorios y no nulos
        if price_data.get('base_net_amount') in [None, '']:
            raise serializers.ValidationError({'price_data': {'base_net_amount': 'Este campo es obligatorio.'}})
        if price_data.get('price_configuration') in [None, '']:
            raise serializers.ValidationError({'price_data': {'price_configuration': 'Este campo es obligatorio.'}})
        validated_data.pop('created_by', None)
        user_code = getattr(getattr(request, 'user', None), 'code', 'system')
        now = timezone.now()
        from price.models import Price
        import uuid
        from django.db import transaction
        with transaction.atomic():
            catalog_code = str(uuid.uuid4())
            catalog = Catalog._default_manager.create(
                **validated_data,
                code=catalog_code,
                created_by=user_code,
                created_at=now
            )
            price_code = str(uuid.uuid4())
            price_obj = Price._default_manager.create(
                code=price_code,
                base_net_amount=price_data['base_net_amount'],
                gross_amount=0,
                iva_amount=0,
                retention_amount=0,
                price_configuration=price_data['price_configuration'],
                created_by=user_code,
                created_at=now,
                record_item_code=catalog_code,
                price_record_type=4
            )
            catalog.price = price_obj.code
            catalog.save()
        return catalog

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
            "usage_instructions",
            "min_quantity_purchase",
            "rations_quantity",
            "is_visible",
            "is_deleted",
            "is_confirmed",
            "restriction",
            "configuration",
            "field_verbose_names",
            "price_data",
            "price",
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
        verbose = {
            "net_amount": "Valor BASE NETO",
        }
        result = {
            field: (
                verbose[field] if field in verbose else (
                    obj._meta.get_field(field).verbose_name
                    if hasattr(obj._meta, "get_field") and field in [f.name for f in obj._meta.fields]
                    else field
                )
            )
            for field in field_names
        }
        return result

    def get_net_amount(self, obj):
        from price.models import Price
        try:
            price_obj = Price._default_manager.get(code=obj.price)
            return price_obj.net_amount
        except Exception:
            return None

    def create(self, validated_data):
        request = self.context.get('request', None)
        price_data = validated_data.pop('price_data', None)
        if not price_data:
            raise serializers.ValidationError({'price_data': 'Este campo es requerido.'})
        # Validar que solo estén los campos permitidos
        allowed_fields = {'base_net_amount', 'price_configuration'}
        if set(price_data.keys()) != allowed_fields:
            raise serializers.ValidationError({'price_data': f'Solo se permiten los campos: {allowed_fields}.'})
        # Validar que ambos campos sean obligatorios y no nulos
        if price_data.get('base_net_amount') in [None, '']:
            raise serializers.ValidationError({'price_data': {'base_net_amount': 'Este campo es obligatorio.'}})
        if price_data.get('price_configuration') in [None, '']:
            raise serializers.ValidationError({'price_data': {'price_configuration': 'Este campo es obligatorio.'}})
        validated_data.pop('price', None)
        validated_data.pop('created_by', None)
        user_code = getattr(getattr(request, 'user', None), 'code', 'system')
        now = timezone.now()
        from price.models import Price
        import uuid
        with transaction.atomic():
            product_code = str(uuid.uuid4())
            product = Product._default_manager.create(
                **validated_data,
                code=product_code,
                created_by=user_code,
                created_at=now
            )
            price_code = str(uuid.uuid4())
            price_obj = Price._default_manager.create(
                code=price_code,
                base_net_amount=price_data['base_net_amount'],
                gross_amount=0,
                iva_amount=0,
                retention_amount=0,
                price_configuration=price_data['price_configuration'],
                created_by=user_code,
                created_at=now,
                record_item_code=product_code,
                price_record_type=1
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
            # "price",  # No permitir en input, pero sí en output
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
            'code': 'Código UUID',
            'sku': 'SKU',
            'description': 'Descripción',
            'base_net_amount': 'Valor Neto Base',
            'obs': 'Observaciones',
            'package_unit': 'Unidad de Empaque',
            'min_package_purchase': 'Compra Mínima de Empaque',
            'provider': 'Proveedor',
            'type': 'Tipo (ID)',
            'type_name': 'Tipo',
            'item_group': 'Grupo (ID)',
            'group_name': 'Nombre del Grupo',
            'category': 'Categoría (ID)',
            'category_name': 'Categoría',
            'url': 'URL',
            'package': 'Empaque (ID)',
            'package_description': 'Descripción de Empaque',
            'is_active': 'Está Activo',
            'is_deleted': 'Está Eliminado',
            'is_confirmed': 'Está Confirmado',
            'created_at': 'Fecha de Creación',
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

    @staticmethod
    def get_verbose_names():
        return {
            'code': 'Código UUID',
            'sku': 'SKU',
            'description': 'Descripción',
            'base_net_amount': 'Valor Neto Base',
            'net_amount': 'Valor Neto',
            'gross_amount': 'Valor Bruto',
            'iva_amount': 'Valor IVA',
            'aditional_tax_amount': 'Valor Impuesto Adicional',
            'retention_amount': 'Valor Retención',
            'obs': 'Observaciones',
            'package_unit': 'Unidad de Empaque',
            'min_package_purchase': 'Compra Mínima de Empaque',
            'provider': 'Proveedor (ID)',
            'type': 'Tipo (ID)',
            'type_name': 'Tipo',
            'item_group': 'Grupo (ID)',
            'group_name': 'Nombre del Grupo',
            'category': 'Categoría (ID)',
            'category_name': 'Categoría',
            'url': 'URL',
            'package': 'Empaque (ID)',
            'package_description': 'Descripción de Empaque',
            'is_active': 'Está Activo',
            'is_deleted': 'Está Eliminado',
            'is_confirmed': 'Está Confirmado',
            'created_at': 'Fecha de Creación',
        }


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
            "code",
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
            "code",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]


class ProviderSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()
    provider_type = serializers.SerializerMethodField()

    def get_field_verbose_names(self, obj):
        field_names = [
            "provider", "type", "provider_type", "rating", "obs_provider", "contact_name", "contact_mail",
            "contact_phone", "contact_phone2", "website_url", "obs_contact", "company_name",
            "company_rut", "company_activity", "legal_representative", "billing_address",
            "billing_mail", "billing_phone", "company_bank", "bank_account_type",
            "bank_account_number", "bank_account_mail", "dispatch_address", "dispatch_maps_location",
            "obs_dispatch", "dispatch_district", "dispatch_region", "is_active", "is_deleted",
            "is_confirmed", "created_at", "updated_at", "confirmed_at", "deleted_at", "created_by",
            "confirmed_by", "updated_by", "deleted_by", "code", "id"
        ]
        # Mapeo manual para campos calculados o especiales
        manual_verbose = {
            "provider_type": "Tipo Proveedor",
            "type": "Tipo (ID)",
            "provider": "Proveedor",
            "obs_provider": "Observaciones del Proveedor",
            "obs_contact": "Observaciones de Contacto",
            "company_name": "Nombre de la Empresa",
            "company_rut": "RUT de la Empresa",
            "company_activity": "Actividad de la Empresa",
            "legal_representative": "Representante Legal",
            "billing_address": "Dirección de Facturación",
            "billing_mail": "Email de Facturación",
            "billing_phone": "Teléfono de Facturación",
            "company_bank": "Banco de la Empresa",
            "bank_account_type": "Tipo de Cuenta Bancaria",
            "bank_account_number": "Número de Cuenta Bancaria",
            "bank_account_mail": "Email de Cuenta Bancaria",
            "dispatch_address": "Dirección de Despacho",
            "dispatch_maps_location": "Ubicación en Maps",
            "obs_dispatch": "Observaciones de Despacho",
            "dispatch_district": "Comuna de Despacho",
            "dispatch_region": "Región de Despacho",
            "is_active": "Está Activo",
            "is_deleted": "Está Eliminado",
            "is_confirmed": "Está Confirmado",
            "created_at": "Fecha de Creación",
            "updated_at": "Fecha de Actualización",
            "confirmed_at": "Fecha de Confirmación",
            "deleted_at": "Fecha de Eliminación",
            "created_by": "Creado Por",
            "confirmed_by": "Confirmado Por",
            "updated_by": "Actualizado Por",
            "deleted_by": "Eliminado Por",
            "code": "Código UUID",
            "id": "ID",
            "rating": "Calificación",
            "contact_name": "Nombre de Contacto",
            "contact_mail": "Email de Contacto",
            "contact_phone": "Teléfono de Contacto",
            "contact_phone2": "Teléfono de Contacto 2",
            "website_url": "URL del Sitio Web"
        }
        result = {}
        for field in field_names:
            if field in manual_verbose:
                result[field] = manual_verbose[field]
            elif hasattr(obj._meta, "get_field") and field in [f.name for f in obj._meta.fields]:
                result[field] = obj._meta.get_field(field).verbose_name
            else:
                # Capitaliza y reemplaza guiones bajos por espacios para campos no mapeados
                result[field] = field.replace('_', ' ').capitalize()
        return result

    def get_provider_type(self, obj):
        from .models import ProviderType
        try:
            provider_type_obj = ProviderType.objects.get(id=obj.type) # type: ignore
            return provider_type_obj.type
        except ProviderType.DoesNotExist: # type: ignore
            return None

    class Meta:
        model = Provider
        fields = [
            "id",
            "code",
            "provider",
            "type",
            "provider_type",
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


class CatalogListSerializer(serializers.Serializer):
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

    @staticmethod
    def get_verbose_names():
        return {
            'sku': 'SKU',
            'cover_image': 'Imagen de Portada',
            'menu': 'Menú ID',
            'menu_name': 'Menú',
            'category': 'Categoría ID',
            'category_name': 'Categoría',
            'name': 'Nombre',
            'description': 'Descripción',
            'obs': 'Observaciones',
            'chef_recommendation': 'Recomendación del Chef',
            'item_type': 'Tipo ID',
            'type_name': 'Tipo',
            'item_group': 'Grupo ID',
            'group_name': 'Grupo',
            'base_net_amount': 'Valor Base Neto',
            'net_amount': 'Valor Neto',
            'gross_amount': 'Valor Bruto',
            'iva_amount': 'IVA',
            'aditional_tax_amount': 'Impuesto Adicional',
            'retention_amount': 'Retención',
            'price_configuration': 'Configuración de Precio',
            'min_quantity_purchase': 'Cantidad Mínima de Compra',
            'rations_quantity': 'Cantidad de Raciones',
            'item_configuration': 'Configuración del Item',
            'configuration': 'Configuración',
            'is_visible': 'Es Visible',
            'is_confirmed': 'Está Confirmado',
            'created_at': 'Fecha de Creación',
        }


class ProviderListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    provider = serializers.CharField()
    type = serializers.IntegerField()
    type_name = serializers.CharField()
    rating = serializers.IntegerField()
    obs_provider = serializers.CharField()
    contact_name = serializers.CharField(allow_null=True)
    contact_mail = serializers.CharField(allow_null=True)
    contact_phone = serializers.CharField(allow_null=True)
    contact_phone2 = serializers.CharField(allow_null=True)
    obs_contact = serializers.CharField(allow_null=True)
    website_url = serializers.CharField(allow_null=True)
    company_name = serializers.CharField(allow_null=True)
    company_rut = serializers.CharField(allow_null=True)
    company_activity = serializers.CharField(allow_null=True)
    legal_representative = serializers.CharField(allow_null=True)
    billing_address = serializers.CharField(allow_null=True)
    billing_mail = serializers.CharField(allow_null=True)
    billing_phone = serializers.CharField(allow_null=True)
    company_bank = serializers.IntegerField(allow_null=True)
    bank = serializers.CharField(allow_null=True)
    bank_account_number = serializers.CharField(allow_null=True)
    bank_account_type = serializers.IntegerField(allow_null=True)
    bank_account_type_name = serializers.CharField(allow_null=True)
    bank_account_mail = serializers.CharField(allow_null=True)
    dispatch_address = serializers.CharField(allow_null=True)
    dispatch_maps_location = serializers.CharField(allow_null=True)
    obs_dispatch = serializers.CharField(allow_null=True)
    dispatch_district = serializers.IntegerField(allow_null=True)
    district = serializers.CharField(allow_null=True)
    dispatch_region = serializers.IntegerField(allow_null=True)
    region = serializers.CharField(allow_null=True)
    is_active = serializers.BooleanField()
    is_deleted = serializers.BooleanField(allow_null=True)
    is_confirmed = serializers.BooleanField(allow_null=True)
    
    field_verbose_names = serializers.SerializerMethodField()

    def get_field_verbose_names(self, obj):
        return {
            'id': 'ID',
            'provider': 'Proveedor',
            'type': 'Tipo',
            'type_name': 'Tipo de Proveedor',
            'rating': 'Calificación',
            'obs_provider': 'Observaciones del Proveedor',
            'contact_name': 'Nombre de Contacto',
            'contact_mail': 'Email de Contacto',
            'contact_phone': 'Teléfono de Contacto',
            'contact_phone2': 'Teléfono de Contacto 2',
            'obs_contact': 'Observaciones de Contacto',
            'website_url': 'URL del Sitio Web',
            'company_name': 'Nombre de la Empresa',
            'company_rut': 'RUT de la Empresa',
            'company_activity': 'Actividad de la Empresa',
            'legal_representative': 'Representante Legal',
            'billing_address': 'Dirección de Facturación',
            'billing_mail': 'Email de Facturación',
            'billing_phone': 'Teléfono de Facturación',
            'company_bank': 'Banco de la Empresa',
            'bank': 'Banco',
            'bank_account_number': 'Número de Cuenta Bancaria',
            'bank_account_type': 'Tipo de Cuenta Bancaria',
            'bank_account_type_name': 'Tipo de Cuenta Bancaria',
            'bank_account_mail': 'Email de Cuenta Bancaria',
            'dispatch_address': 'Dirección de Despacho',
            'dispatch_maps_location': 'Ubicación en Maps',
            'obs_dispatch': 'Observaciones de Despacho',
            'dispatch_district': 'Distrito de Despacho',
            'district': 'Distrito',
            'dispatch_region': 'Región de Despacho',
            'region': 'Región',
            'is_active': 'Está Activo',
            'is_deleted': 'Está Eliminado',
            'is_confirmed': 'Está Confirmado',
        }


class ItemConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemConfiguration
    """
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
                if hasattr(obj._meta, "get_field")
                else field
            )
            for field in field_names
        }

    def create(self, validated_data):
        request = self.context.get('request', None)
        validated_data.pop('created_by', None)
        user_code = getattr(getattr(request, 'user', None), 'code', 'system')
        now = timezone.now()
        
        item_config = ItemConfiguration._default_manager.create(
            **validated_data,
            created_by=user_code,
            created_at=now
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
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
        ]


class PackageSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Package
    """
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
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
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
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "field_verbose_names",
        ]


class PackageTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PackageType
    """
    class Meta:
        model = PackageType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class TransportTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TransportType
    """
    class Meta:
        model = TransportType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class MeasureUnitSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo MeasureUnit
    """
    class Meta:
        model = MeasureUnit
        fields = ["id", "measure_unit", "description"]
        read_only_fields = ["id"]


class InstructionTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo InstructionType
    """
    class Meta:
        model = InstructionType
        fields = ["id", "type", "description", "is_deleted", "is_confirmed", "created_at", "updated_at", "confirmed_at", "deleted_at", "created_by", "confirmed_by", "updated_by", "deleted_by"]
        read_only_fields = ["id", "created_at", "updated_at", "confirmed_at", "deleted_at", "created_by", "confirmed_by", "updated_by", "deleted_by"]
