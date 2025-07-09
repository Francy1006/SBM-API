import uuid
from django.db import models
from django.contrib.auth.models import User


class FiscalDocument(models.Model):
    """
    Modelo para documentos fiscales
    """
    DOCUMENT_TYPE_CHOICES = [
        ('invoice', 'Factura'),
        ('credit_note', 'Nota de Crédito'),
        ('debit_note', 'Nota de Débito'),
        ('receipt', 'Recibo'),
        ('ticket', 'Ticket'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('sent', 'Enviado'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
        ('cancelled', 'Anulado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_number = models.CharField(max_length=50, unique=True, verbose_name="Número de Documento")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='invoice', verbose_name="Tipo de Documento")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto Total")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto de Impuestos")
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto Neto")
    issue_date = models.DateTimeField(verbose_name="Fecha de Emisión")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    
    # Relaciones
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='fiscal_documents', verbose_name="Franquicia")
    customer = models.ForeignKey('sales.Customer', on_delete=models.CASCADE, related_name='fiscal_documents', verbose_name="Cliente")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_fiscal_documents', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'fiscal_document'
        verbose_name = "Documento Fiscal"
        verbose_name_plural = "Documentos Fiscales"
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.document_number} - {self.get_document_type_display()}"


class FiscalItem(models.Model):
    """
    Modelo para items de documentos fiscales
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Total")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tasa de Impuesto (%)")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto de Impuesto")
    description = models.TextField(verbose_name="Descripción")
    
    # Relaciones
    fiscal_document = models.ForeignKey(FiscalDocument, on_delete=models.CASCADE, related_name='items', verbose_name="Documento Fiscal")
    catalog_item = models.ForeignKey('catalog.Catalog', on_delete=models.CASCADE, related_name='fiscal_items', verbose_name="Item del Catálogo")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'fiscal_item'
        verbose_name = "Item Fiscal"
        verbose_name_plural = "Items Fiscales"
        ordering = ['fiscal_document', 'created_at']

    def __str__(self):
        return f"{self.catalog_item.name} - {self.quantity} x ${self.unit_price}"


class TaxRate(models.Model):
    """
    Modelo para tasas de impuestos
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tasa (%)")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    # Relaciones
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='tax_rates', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tax_rates', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'tax_rate'
        verbose_name = "Tasa de Impuesto"
        verbose_name_plural = "Tasas de Impuestos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.rate}%)"


class FiscalPayment(models.Model):
    """
    Modelo para pagos de documentos fiscales
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
        ('check', 'Cheque'),
        ('other', 'Otro'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash', verbose_name="Método de Pago")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Referencia")
    payment_date = models.DateTimeField(verbose_name="Fecha de Pago")
    
    # Relaciones
    fiscal_document = models.ForeignKey(FiscalDocument, on_delete=models.CASCADE, related_name='payments', verbose_name="Documento Fiscal")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_fiscal_payments', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'fiscal_payment'
        verbose_name = "Pago Fiscal"
        verbose_name_plural = "Pagos Fiscales"
        ordering = ['-payment_date']

    def __str__(self):
        return f"Pago de {self.fiscal_document.document_number} - ${self.amount}"
