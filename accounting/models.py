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

    id = models.AutoField(primary_key=True)
    module_id = models.IntegerField()
    module_config_id = models.CharField(max_length=50)
    fiscal_directive = models.CharField(max_length=36)
    var = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=36, null=True, blank=True)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    deleted_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = '"ditaly_pasta"."fiscal_configuration_detail"'
        managed = False


class FiscalDirectiveType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'sbm_business"."fiscal_directive_type'
        managed = False


class FiscalDirective(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    obs = models.TextField(null=True, blank=True)
    fiscal_directive = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(
        FiscalDirectiveType,
        on_delete=models.DO_NOTHING,
        db_column='type',
        related_name='fiscal_directives'
    )
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    official_source_url = models.CharField(max_length=255)
    is_deleted = models.BooleanField(null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=36)
    confirmed_by = models.CharField(max_length=36, null=True, blank=True)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    deleted_by = models.CharField(max_length=36, null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    end_month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'sbm_business"."fiscal_directive'
        managed = False


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


class FiscalDirectiveStats(models.Model):
    """
    Modelo para la vista analytics.fiscal_directive_stats
    """
    type = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=255, verbose_name="Nombre del Tipo")
    type_description = models.TextField(verbose_name="Descripción del Tipo")
    total_directives = models.IntegerField(verbose_name="Total de Directivas")
    confirmed_directives = models.IntegerField(verbose_name="Directivas Confirmadas")
    deleted_directives = models.IntegerField(verbose_name="Directivas Eliminadas")
    pending_directives = models.IntegerField(verbose_name="Directivas Pendientes")
    avg_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Promedio")
    min_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Mínimo")
    max_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Máximo")
    current_year_directives = models.IntegerField(verbose_name="Directivas del Año Actual")
    directives_with_month = models.IntegerField(verbose_name="Directivas con Mes")
    directives_with_end_month = models.IntegerField(verbose_name="Directivas con Mes Fin")
    directives_with_end_year = models.IntegerField(verbose_name="Directivas con Año Fin")
    earliest_year = models.IntegerField(verbose_name="Año Más Antiguo")
    latest_year = models.IntegerField(verbose_name="Año Más Reciente")
    unique_years = models.IntegerField(verbose_name="Años Únicos")
    unique_months = models.IntegerField(verbose_name="Meses Únicos")

    class Meta:
        db_table = '"analytics"."fiscal_directive_stats"'
        managed = False  # Django no gestiona esta tabla
        verbose_name = "Estadística de Directiva Fiscal"
        verbose_name_plural = "Estadísticas de Directivas Fiscales"

    def __str__(self):
        return f"{self.type_name} - {self.total_directives} directivas"
