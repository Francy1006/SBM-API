import uuid
from django.db import models
from django.contrib.auth.models import User


class Warehouse(models.Model):
    """
    Modelo para almacenes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    address = models.TextField(verbose_name="Dirección")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    # Relaciones
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='warehouses', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_warehouses', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'warehouse'
        verbose_name = "Almacén"
        verbose_name_plural = "Almacenes"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class InventoryItem(models.Model):
    """
    Modelo para items de inventario
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock Mínimo")
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Stock Máximo")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Unitario")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Costo Total")
    
    # Relaciones
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory_items', verbose_name="Almacén")
    catalog_item = models.ForeignKey('catalog.Catalog', on_delete=models.CASCADE, related_name='inventory_items', verbose_name="Item del Catálogo")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_inventory_items', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'inventory_item'
        verbose_name = "Item de Inventario"
        verbose_name_plural = "Items de Inventario"
        unique_together = ['warehouse', 'catalog_item']
        ordering = ['warehouse', 'catalog_item']

    def __str__(self):
        return f"{self.catalog_item.name} - {self.quantity} unidades"


class InventoryMovement(models.Model):
    """
    Modelo para movimientos de inventario
    """
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
        ('transfer', 'Transferencia'),
        ('adjustment', 'Ajuste'),
        ('return', 'Devolución'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, verbose_name="Tipo de Movimiento")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Unitario")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Costo Total")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Referencia")
    notes = models.TextField(blank=True, verbose_name="Notas")
    movement_date = models.DateTimeField(verbose_name="Fecha del Movimiento")
    
    # Relaciones
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='movements', verbose_name="Almacén")
    catalog_item = models.ForeignKey('catalog.Catalog', on_delete=models.CASCADE, related_name='inventory_movements', verbose_name="Item del Catálogo")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_inventory_movements', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'inventory_movement'
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-movement_date']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.catalog_item.name} - {self.quantity}"


class InventoryCount(models.Model):
    """
    Modelo para conteos de inventario
    """
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    count_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Conteo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Estado")
    start_date = models.DateTimeField(verbose_name="Fecha de Inicio")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Finalización")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Relaciones
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory_counts', verbose_name="Almacén")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_inventory_counts', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'inventory_count'
        verbose_name = "Conteo de Inventario"
        verbose_name_plural = "Conteos de Inventario"
        ordering = ['-start_date']

    def __str__(self):
        return f"Conteo #{self.count_number} - {self.warehouse.name}"


class InventoryCountItem(models.Model):
    """
    Modelo para items de conteo de inventario
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expected_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad Esperada")
    counted_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad Contada")
    difference = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Diferencia")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Relaciones
    inventory_count = models.ForeignKey(InventoryCount, on_delete=models.CASCADE, related_name='items', verbose_name="Conteo de Inventario")
    catalog_item = models.ForeignKey('catalog.Catalog', on_delete=models.CASCADE, related_name='count_items', verbose_name="Item del Catálogo")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'inventory_count_item'
        verbose_name = "Item de Conteo"
        verbose_name_plural = "Items de Conteo"
        unique_together = ['inventory_count', 'catalog_item']
        ordering = ['inventory_count', 'catalog_item']

    def __str__(self):
        return f"{self.catalog_item.name} - Esperado: {self.expected_quantity}, Contado: {self.counted_quantity}"
