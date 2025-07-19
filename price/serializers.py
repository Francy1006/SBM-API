from rest_framework import serializers
from .models import PriceList, PriceItem, PriceDiscount, PriceHistory, PriceConfiguration


class PriceListSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PriceList
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    items_count = serializers.SerializerMethodField(help_text="Número de Items")

    class Meta:
        model = PriceList
        fields = [
            'id', 'name', 'description', 'is_active', 'is_default', 'franchise',
            'created_by', 'created_at', 'updated_at', 'field_verbose_names',
            'franchise_name', 'created_by_name', 'items_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'franchise_name': 'Franquicia',
            'created_by_name': 'Creado por',
            'items_count': 'Número de Items'
        })
        return verbose_names

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_items_count(self, obj):
        return obj.items.count()


class PriceItemSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PriceItem
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    price_list_name = serializers.SerializerMethodField(help_text="Lista de Precios")
    catalog_item_name = serializers.SerializerMethodField(help_text="Item del Catálogo")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = PriceItem
        fields = [
            'id', 'price', 'cost', 'margin', 'price_list', 'catalog_item',
            'created_by', 'created_at', 'updated_at', 'field_verbose_names',
            'price_list_name', 'catalog_item_name', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'price_list_name': 'Lista de Precios',
            'catalog_item_name': 'Item del Catálogo',
            'created_by_name': 'Creado por'
        })
        return verbose_names

    def get_price_list_name(self, obj):
        return obj.price_list.name if obj.price_list else None

    def get_catalog_item_name(self, obj):
        return obj.catalog_item.name if obj.catalog_item else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class PriceDiscountSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PriceDiscount
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = PriceDiscount
        fields = [
            'id', 'name', 'description', 'discount_type', 'discount_value',
            'is_active', 'valid_from', 'valid_until', 'franchise', 'created_by',
            'created_at', 'updated_at', 'field_verbose_names', 'franchise_name',
            'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'franchise_name': 'Franquicia',
            'created_by_name': 'Creado por'
        })
        return verbose_names

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class PriceHistorySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PriceHistory
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    price_item_info = serializers.SerializerMethodField(help_text="Item de Precio")
    changed_by_name = serializers.SerializerMethodField(help_text="Cambiado por")

    class Meta:
        model = PriceHistory
        fields = [
            'id', 'old_price', 'new_price', 'change_reason', 'price_item',
            'changed_by', 'changed_at', 'field_verbose_names', 'price_item_info',
            'changed_by_name'
        ]
        read_only_fields = ['id', 'changed_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'price_item_info': 'Item de Precio',
            'changed_by_name': 'Cambiado por'
        })
        return verbose_names

    def get_price_item_info(self, obj):
        if obj.price_item:
            return {
                'id': obj.price_item.id,
                'catalog_item_name': obj.price_item.catalog_item.name if obj.price_item.catalog_item else None,
                'price_list_name': obj.price_item.price_list.name if obj.price_item.price_list else None
            }
        return None

    def get_changed_by_name(self, obj):
        return obj.changed_by.get_full_name() if obj.changed_by else None 


class PriceConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceConfiguration
        fields = [
            'id', 'code', 'price_configuration', 'franchise_configuration', 'variable_formula',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at'] 