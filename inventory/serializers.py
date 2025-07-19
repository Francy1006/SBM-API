from rest_framework import serializers
from .models import Warehouse, InventoryItem, InventoryMovement, InventoryCount, InventoryCountItem, Package, PackageType, TransportType, MeasureUnit


class WarehouseSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Warehouse
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    inventory_items_count = serializers.SerializerMethodField(help_text="Número de Items")

    class Meta:
        model = Warehouse
        fields = [
            'id', 'name', 'code', 'address', 'description', 'is_active',
            'franchise', 'created_by', 'created_at', 'updated_at',
            'field_verbose_names', 'franchise_name', 'created_by_name',
            'inventory_items_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'franchise_name': 'Franquicia',
            'created_by_name': 'Creado por',
            'inventory_items_count': 'Número de Items'
        })
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
            'id', 'quantity', 'minimum_stock', 'maximum_stock', 'unit_cost',
            'total_cost', 'warehouse', 'catalog_item', 'created_by',
            'created_at', 'updated_at', 'field_verbose_names',
            'warehouse_name', 'catalog_item_name', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'warehouse_name': 'Almacén',
            'catalog_item_name': 'Item del Catálogo',
            'created_by_name': 'Creado por'
        })
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
            'id', 'movement_type', 'quantity', 'unit_cost', 'total_cost',
            'reference', 'notes', 'movement_date', 'warehouse', 'catalog_item',
            'created_by', 'created_at', 'field_verbose_names',
            'warehouse_name', 'catalog_item_name', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'warehouse_name': 'Almacén',
            'catalog_item_name': 'Item del Catálogo',
            'created_by_name': 'Creado por'
        })
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
            'id', 'count_number', 'status', 'start_date', 'end_date', 'notes',
            'warehouse', 'created_by', 'created_at', 'updated_at',
            'field_verbose_names', 'warehouse_name', 'created_by_name',
            'items_count'
        ]
        read_only_fields = ['id', 'count_number', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'warehouse_name': 'Almacén',
            'created_by_name': 'Creado por',
            'items_count': 'Número de Items'
        })
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
    inventory_count_number = serializers.SerializerMethodField(help_text="Conteo de Inventario")
    catalog_item_name = serializers.SerializerMethodField(help_text="Item del Catálogo")

    class Meta:
        model = InventoryCountItem
        fields = [
            'id', 'expected_quantity', 'counted_quantity', 'difference', 'notes',
            'inventory_count', 'catalog_item', 'created_at', 'updated_at',
            'field_verbose_names', 'inventory_count_number', 'catalog_item_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'inventory_count_number': 'Conteo de Inventario',
            'catalog_item_name': 'Item del Catálogo'
        })
        return verbose_names

    def get_inventory_count_number(self, obj):
        return obj.inventory_count.count_number if obj.inventory_count else None

    def get_catalog_item_name(self, obj):
        return obj.catalog_item.name if obj.catalog_item else None 

class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = '__all__'

class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = '__all__'

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__' 