from rest_framework import serializers
from .models import Customer, Sale, SaleItem, SalePayment, SalesOrder


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Customer
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    sales_count = serializers.SerializerMethodField(help_text="Número de Ventas")

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'customer_type', 'email', 'phone', 'address',
            'tax_id', 'credit_limit', 'is_active', 'franchise', 'created_by',
            'created_at', 'updated_at', 'field_verbose_names',
            'franchise_name', 'created_by_name', 'sales_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'franchise_name': 'Franquicia',
            'created_by_name': 'Creado por',
            'sales_count': 'Número de Ventas'
        })
        return verbose_names

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_sales_count(self, obj):
        return obj.sales.count()


class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Sale
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    customer_name = serializers.SerializerMethodField(help_text="Cliente")
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    items_count = serializers.SerializerMethodField(help_text="Número de Items")
    payments_count = serializers.SerializerMethodField(help_text="Número de Pagos")

    class Meta:
        model = Sale
        fields = [
            'id', 'sale_number', 'status', 'payment_status', 'subtotal',
            'tax_amount', 'total_amount', 'discount_amount', 'sale_date',
            'due_date', 'notes', 'customer', 'franchise', 'created_by',
            'created_at', 'updated_at', 'field_verbose_names',
            'customer_name', 'franchise_name', 'created_by_name',
            'items_count', 'payments_count'
        ]
        read_only_fields = ['id', 'sale_number', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'customer_name': 'Cliente',
            'franchise_name': 'Franquicia',
            'created_by_name': 'Creado por',
            'items_count': 'Número de Items',
            'payments_count': 'Número de Pagos'
        })
        return verbose_names

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_items_count(self, obj):
        return obj.items.count()

    def get_payments_count(self, obj):
        return obj.payments.count()


class SaleItemSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SaleItem
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    sale_number = serializers.SerializerMethodField(help_text="Número de Venta")
    catalog_item_name = serializers.SerializerMethodField(help_text="Item del Catálogo")

    class Meta:
        model = SaleItem
        fields = [
            'id', 'quantity', 'unit_price', 'discount_rate', 'discount_amount',
            'total_price', 'notes', 'sale', 'catalog_item', 'created_at',
            'updated_at', 'field_verbose_names', 'sale_number', 'catalog_item_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'sale_number': 'Número de Venta',
            'catalog_item_name': 'Item del Catálogo'
        })
        return verbose_names

    def get_sale_number(self, obj):
        return obj.sale.sale_number if obj.sale else None

    def get_catalog_item_name(self, obj):
        return obj.catalog_item.name if obj.catalog_item else None


class SalePaymentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SalePayment
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    sale_number = serializers.SerializerMethodField(help_text="Número de Venta")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = SalePayment
        fields = [
            'id', 'amount', 'payment_method', 'reference', 'payment_date',
            'notes', 'sale', 'created_by', 'created_at', 'field_verbose_names',
            'sale_number', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'sale_number': 'Número de Venta',
            'created_by_name': 'Creado por'
        })
        return verbose_names

    def get_sale_number(self, obj):
        return obj.sale.sale_number if obj.sale else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class SalesOrderSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SalesOrder
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    customer_name = serializers.SerializerMethodField(help_text="Cliente")
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'status', 'total_amount', 'order_date',
            'delivery_date', 'notes', 'customer', 'franchise', 'created_by',
            'created_at', 'updated_at', 'field_verbose_names',
            'customer_name', 'franchise_name', 'created_by_name'
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'customer_name': 'Cliente',
            'franchise_name': 'Franquicia',
            'created_by_name': 'Creado por'
        })
        return verbose_names

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None 