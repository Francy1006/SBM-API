import uuid
from django.db import models
from django.contrib.auth.models import User


class Price(models.Model):
    """
    Modelo para precios
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código UUID")
    net_amount = models.IntegerField(default=0, verbose_name="Monto Neto")  # type: ignore
    gross_amount = models.IntegerField(default=0, verbose_name="Monto Bruto")  # type: ignore
    iva_amount = models.IntegerField(default=0, verbose_name="Monto IVA")  # type: ignore
    retention_amount = models.IntegerField(default=0, verbose_name="Monto Retención")  # type: ignore
    price_fiscal_configuration = models.CharField(max_length=36, verbose_name="Configuración Fiscal")
    is_active = models.BooleanField(default=True, verbose_name="Está Activo")  # type: ignore
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Está Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Está Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.CharField(max_length=36, verbose_name="Creado Por")
    confirmed_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Confirmado Por")
    updated_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Actualizado Por")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")

    class Meta:
        db_table = 'price'
        verbose_name = "Precio"
        verbose_name_plural = "Precios"
        ordering = ['-created_at']

    def __str__(self):
        return f"Precio {self.code}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class PriceList(models.Model):
    """
    Modelo para listas de precios
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")  # type: ignore
    is_default = models.BooleanField(default=False, verbose_name="Lista por Defecto")  # type: ignore
    
    # Relaciones
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='price_lists', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_price_lists', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'price_list'
        verbose_name = "Lista de Precios"
        verbose_name_plural = "Listas de Precios"
        ordering = ['name']

    def __str__(self):
        return self.name


class PriceItem(models.Model):
    """
    Modelo para items de precio
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Costo")
    margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Margen (%)")
    
    # Relaciones
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE, related_name='items', verbose_name="Lista de Precios")
    catalog_item = models.ForeignKey('catalog.Catalog', on_delete=models.CASCADE, related_name='price_items', verbose_name="Item del Catálogo")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_price_items', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'price_item'
        verbose_name = "Item de Precio"
        verbose_name_plural = "Items de Precio"
        unique_together = ['price_list', 'catalog_item']
        ordering = ['price_list', 'catalog_item']

    def __str__(self):
        return f"{self.catalog_item.name} - ${self.price}"


class PriceDiscount(models.Model):
    """
    Modelo para descuentos de precio
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Porcentaje'),
        ('fixed', 'Monto Fijo'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage', verbose_name="Tipo de Descuento")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor del Descuento")
    is_active = models.BooleanField(default=True, verbose_name="Activo")  # type: ignore
    valid_from = models.DateTimeField(verbose_name="Válido Desde")
    valid_until = models.DateTimeField(null=True, blank=True, verbose_name="Válido Hasta")
    
    # Relaciones
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='price_discounts', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_price_discounts', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'price_discount'
        verbose_name = "Descuento de Precio"
        verbose_name_plural = "Descuentos de Precio"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_discount_type_display()}"  # type: ignore


class PriceHistory(models.Model):
    """
    Modelo para historial de cambios de precio
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Anterior")
    new_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Nuevo")
    change_reason = models.TextField(blank=True, verbose_name="Motivo del Cambio")
    
    # Relaciones
    price_item = models.ForeignKey(PriceItem, on_delete=models.CASCADE, related_name='history', verbose_name="Item de Precio")
    
    # Campos de auditoría
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_changes', verbose_name="Cambiado por")
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Cambio")
    
    class Meta:
        db_table = 'price_history'
        verbose_name = "Historial de Precio"
        verbose_name_plural = "Historial de Precios"
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.price_item} - ${self.old_price} → ${self.new_price}"
