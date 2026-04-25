from rest_framework import serializers
from calculation.models import CalculationConcept
from .models import (
    Price,
    PriceList,
    PriceItem,
    PriceDiscount,
    PriceHistory,
    PriceConfiguration,
    PriceConfigurationDetail,
    PriceType
)

# -------------------------
# PRICE (DYNAMIC)
# -------------------------
class PriceSerializer(serializers.ModelSerializer):
    dynamic_fields = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields = [f.name for f in Price._meta.fields] + ["dynamic_fields"]

    def get_dynamic_fields(self, obj):
        # evita error si no existe el método
        return getattr(obj, "get_dynamic_fields", lambda: {})()


# -------------------------
# PRICE LIST
# -------------------------
class PriceListSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()
    franchise_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = PriceList
        fields = [
            'id', 'name', 'description', 'is_active', 'is_default',
            'franchise', 'created_by', 'created_at', 'updated_at',
            'field_verbose_names',
            'franchise_name', 'created_by_name', 'items_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        return {
            'franchise_name': 'Franquicia',
            'created_by_name': 'Creado por',
            'items_count': 'Número de Items'
        }

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_items_count(self, obj):
        return obj.items.count()


# -------------------------
# PRICE ITEM
# -------------------------
class PriceItemSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()
    price_list_name = serializers.SerializerMethodField()
    catalog_item_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PriceItem
        fields = [
            'id', 'price', 'cost', 'margin',
            'price_list', 'catalog_item',
            'created_by', 'created_at', 'updated_at',
            'field_verbose_names',
            'price_list_name', 'catalog_item_name', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        return {
            'price_list_name': 'Lista de Precios',
            'catalog_item_name': 'Item del Catálogo',
            'created_by_name': 'Creado por'
        }

    def get_price_list_name(self, obj):
        return obj.price_list.name if obj.price_list else None

    def get_catalog_item_name(self, obj):
        return obj.catalog_item.name if obj.catalog_item else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


# -------------------------
# PRICE DISCOUNT
# -------------------------
class PriceDiscountSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()
    franchise_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PriceDiscount
        fields = [
            'id', 'name', 'description', 'discount_type', 'discount_value',
            'is_active', 'valid_from', 'valid_until',
            'franchise', 'created_by',
            'created_at', 'updated_at',
            'field_verbose_names',
            'franchise_name', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        return {
            'franchise_name': 'Franquicia',
            'created_by_name': 'Creado por'
        }

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


# -------------------------
# PRICE HISTORY
# -------------------------
class PriceHistorySerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()
    price_item_info = serializers.SerializerMethodField()
    changed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PriceHistory
        fields = [
            'id', 'old_price', 'new_price', 'change_reason',
            'price_item', 'changed_by', 'changed_at',
            'field_verbose_names',
            'price_item_info', 'changed_by_name'
        ]
        read_only_fields = ['id', 'changed_at']

    def get_field_verbose_names(self, obj):
        return {
            'price_item_info': 'Item de Precio',
            'changed_by_name': 'Cambiado por'
        }

    def get_price_item_info(self, obj):
        if not obj.price_item:
            return None

        return {
            "id": obj.price_item.id,
            "catalog_item_name": obj.price_item.catalog_item.name if obj.price_item.catalog_item else None,
            "price_list_name": obj.price_item.price_list.name if obj.price_item.price_list else None
        }

    def get_changed_by_name(self, obj):
        return obj.changed_by.get_full_name() if obj.changed_by else None


# -------------------------
# PRICE CONCEPT
# -------------------------
class PriceConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationConcept
        fields = "__all__"


# -------------------------
# PRICE CONFIGURATION DETAIL
# -------------------------
class PriceConfigurationDetailSerializer(serializers.ModelSerializer):
    calculation_concept_field = serializers.CharField(
        source="calculation_concept.field_name",
        read_only=True
    )

    class Meta:
        model = PriceConfigurationDetail
        fields = "__all__"


# -------------------------
# PRICE CONFIGURATION
# -------------------------
class PriceConfigurationSerializer(serializers.ModelSerializer):
    details = PriceConfigurationDetailSerializer(
        source="details",  # FIX correcto con related_name
        many=True,
        read_only=True
    )

    class Meta:
        model = PriceConfiguration
        fields = "__all__"


# -------------------------
# PRICE TYPE
# -------------------------
class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceType
        fields = "__all__"