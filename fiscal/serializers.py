from rest_framework import serializers
from .models import FiscalDocument, FiscalItem, TaxRate, FiscalPayment


class FiscalDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FiscalDocument
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    customer_name = serializers.SerializerMethodField(help_text="Cliente")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    items_count = serializers.SerializerMethodField(help_text="Número de Items")
    payments_count = serializers.SerializerMethodField(help_text="Número de Pagos")

    class Meta:
        model = FiscalDocument
        fields = [
            'id', 'document_number', 'document_type', 'status', 'total_amount',
            'tax_amount', 'net_amount', 'issue_date', 'due_date', 'franchise',
            'customer', 'created_by', 'created_at', 'updated_at',
            'field_verbose_names', 'franchise_name', 'customer_name',
            'created_by_name', 'items_count', 'payments_count'
        ]
        read_only_fields = ['id', 'document_number', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'franchise_name': 'Franquicia',
            'customer_name': 'Cliente',
            'created_by_name': 'Creado por',
            'items_count': 'Número de Items',
            'payments_count': 'Número de Pagos'
        })
        return verbose_names

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_items_count(self, obj):
        return obj.items.count()

    def get_payments_count(self, obj):
        return obj.payments.count()


class FiscalItemSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FiscalItem
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    fiscal_document_number = serializers.SerializerMethodField(help_text="Documento Fiscal")
    catalog_item_name = serializers.SerializerMethodField(help_text="Item del Catálogo")

    class Meta:
        model = FiscalItem
        fields = [
            'id', 'quantity', 'unit_price', 'total_price', 'tax_rate',
            'tax_amount', 'description', 'fiscal_document', 'catalog_item',
            'created_at', 'updated_at', 'field_verbose_names',
            'fiscal_document_number', 'catalog_item_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'fiscal_document_number': 'Documento Fiscal',
            'catalog_item_name': 'Item del Catálogo'
        })
        return verbose_names

    def get_fiscal_document_number(self, obj):
        return obj.fiscal_document.document_number if obj.fiscal_document else None

    def get_catalog_item_name(self, obj):
        return obj.catalog_item.name if obj.catalog_item else None


class TaxRateSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TaxRate
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = TaxRate
        fields = [
            'id', 'name', 'rate', 'description', 'is_active', 'franchise',
            'created_by', 'created_at', 'updated_at', 'field_verbose_names',
            'franchise_name', 'created_by_name'
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


class FiscalPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FiscalPayment
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    fiscal_document_number = serializers.SerializerMethodField(help_text="Documento Fiscal")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = FiscalPayment
        fields = [
            'id', 'amount', 'payment_method', 'reference', 'payment_date',
            'fiscal_document', 'created_by', 'created_at', 'field_verbose_names',
            'fiscal_document_number', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'fiscal_document_number': 'Documento Fiscal',
            'created_by_name': 'Creado por'
        })
        return verbose_names

    def get_fiscal_document_number(self, obj):
        return obj.fiscal_document.document_number if obj.fiscal_document else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None 