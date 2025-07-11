import uuid
from django.db import models

# Create your models here.

class PriceFiscalConfiguration(models.Model):
    """
    Modelo para configuración fiscal de precios
    """
    id = models.CharField(max_length=36, primary_key=True, verbose_name="Código UUID")
    fiscal_configuration = models.CharField(max_length=50, unique=True, verbose_name="Configuración Fiscal")
    fiscal_formula = models.CharField(max_length=36, verbose_name="Fórmula Fiscal")
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
        db_table = 'price_fiscal_configuration'
        verbose_name = "Configuración Fiscal de Precio"
        verbose_name_plural = "Configuraciones Fiscales de Precios"
        ordering = ['fiscal_configuration']

    def __str__(self):
        return self.fiscal_configuration

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)


class FiscalConfigurationDetail(models.Model):
    """
    Modelo para detalles de configuración fiscal
    """
    id = models.AutoField(primary_key=True)
    price_fiscal_configuration = models.CharField(max_length=36, verbose_name="Configuración Fiscal")
    price = models.CharField(max_length=36, verbose_name="Precio")
    fiscal_directive = models.CharField(max_length=36, verbose_name="Directiva Fiscal")
    log = models.TextField(default="init;", verbose_name="Log")

    class Meta:
        db_table = 'fiscal_configuration_detail'
        verbose_name = "Detalle de Configuración Fiscal"
        verbose_name_plural = "Detalles de Configuración Fiscal"
        ordering = ['id']
        unique_together = ['id', 'price', 'fiscal_directive']

    def __str__(self):
        return f"Detalle {self.id}"


class FiscalDirectiveType(models.Model):
    """
    Modelo para tipos de directivas fiscales
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'fiscal_directive_type'
        verbose_name = "Tipo de Directiva Fiscal"
        verbose_name_plural = "Tipos de Directivas Fiscales"
        ordering = ['type']

    def __str__(self):
        return self.type


class FiscalDirective(models.Model):
    """
    Modelo para directivas fiscales
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código UUID")
    obs = models.TextField(null=True, blank=True, verbose_name="Observaciones")
    fiscal_directive = models.CharField(max_length=50, unique=True, verbose_name="Directiva Fiscal")
    type = models.ForeignKey(
        FiscalDirectiveType,
        on_delete=models.PROTECT,
        db_column='type',
        verbose_name="Tipo de Directiva Fiscal",
        related_name='fiscal_directives'
    )
    percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Porcentaje")
    official_source_url = models.CharField(max_length=255, verbose_name="URL de Fuente Oficial")
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
    month = models.IntegerField(null=True, blank=True, verbose_name="Mes Inicio")
    end_month = models.IntegerField(null=True, blank=True, verbose_name="Mes Fin")
    year = models.IntegerField(verbose_name="Año Inicio")
    end_year = models.IntegerField(null=True, blank=True, verbose_name="Año Fin")

    class Meta:
        db_table = 'fiscal_directive'
        verbose_name = "Directiva Fiscal"
        verbose_name_plural = "Directivas Fiscales"
        ordering = ['fiscal_directive']

    def __str__(self):
        return self.fiscal_directive

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class FiscalFormula(models.Model):
    """
    Modelo para fórmulas fiscales
    """
    id = models.CharField(max_length=36, primary_key=True, verbose_name="Código UUID")
    formula = models.CharField(max_length=50, verbose_name="Fórmula")
    formula_template = models.TextField(verbose_name="Plantilla de Fórmula")
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
        db_table = 'fiscal_formula'
        verbose_name = "Fórmula Fiscal"
        verbose_name_plural = "Fórmulas Fiscales"
        ordering = ['formula']

    def __str__(self):
        return self.formula

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)
