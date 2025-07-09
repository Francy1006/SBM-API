import uuid
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    Modelo para clientes
    """
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Empresa'),
        ('wholesale', 'Mayorista'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual', verbose_name="Tipo de Cliente")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    address = models.TextField(blank=True, verbose_name="Dirección")
    tax_id = models.CharField(max_length=50, blank=True, verbose_name="RUT/RFC")
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Límite de Crédito")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    # Relaciones
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='customers', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_customers', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'customer'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['name']

    def __str__(self):
        return self.name


class Sale(models.Model):
    """
    Modelo para ventas
    """
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Completada'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('partial', 'Parcial'),
        ('paid', 'Pagado'),
        ('overdue', 'Vencido'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Venta")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Estado de Pago")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto de Impuestos")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto Total")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Monto de Descuento")
    sale_date = models.DateTimeField(verbose_name="Fecha de Venta")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Relaciones
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales', verbose_name="Cliente")
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='sales', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sales', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'sale'
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-sale_date']

    def __str__(self):
        return f"Venta #{self.sale_number} - {self.customer.name}"


class SaleItem(models.Model):
    """
    Modelo para items de venta
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Tasa de Descuento (%)")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Monto de Descuento")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Total")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Relaciones
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name="Venta")
    catalog_item = models.ForeignKey('catalog.Catalog', on_delete=models.CASCADE, related_name='sale_items', verbose_name="Item del Catálogo")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'sale_item'
        verbose_name = "Item de Venta"
        verbose_name_plural = "Items de Venta"
        ordering = ['sale', 'created_at']

    def __str__(self):
        return f"{self.catalog_item.name} - {self.quantity} x ${self.unit_price}"


class SalePayment(models.Model):
    """
    Modelo para pagos de ventas
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
        ('check', 'Cheque'),
        ('credit', 'Crédito'),
        ('other', 'Otro'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash', verbose_name="Método de Pago")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Referencia")
    payment_date = models.DateTimeField(verbose_name="Fecha de Pago")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Relaciones
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments', verbose_name="Venta")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sale_payments', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'sale_payment'
        verbose_name = "Pago de Venta"
        verbose_name_plural = "Pagos de Ventas"
        ordering = ['-payment_date']

    def __str__(self):
        return f"Pago de {self.sale.sale_number} - ${self.amount}"


class SalesOrder(models.Model):
    """
    Modelo para órdenes de venta
    """
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Orden")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto Total")
    order_date = models.DateTimeField(verbose_name="Fecha de Orden")
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Entrega")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Relaciones
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="Cliente")
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='sales_orders', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sales_orders', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'sales_order'
        verbose_name = "Orden de Venta"
        verbose_name_plural = "Órdenes de Venta"
        ordering = ['-order_date']

    def __str__(self):
        return f"Orden #{self.order_number} - {self.customer.name}"
