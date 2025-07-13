from django.db import models
from django.contrib.auth.models import User


class FranchiseState(models.Model):
    """
    Modelo para los estados de franquicia
    """
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=50, verbose_name="Estado")
    description = models.TextField(verbose_name="Siglas")

    class Meta:
        db_table = 'franchise_state'
        verbose_name = "Estado de Franquicia"
        verbose_name_plural = "Estados de Franquicia"
        ordering = ['state']

    def __str__(self):
        return self.state


class Franchise(models.Model):
    """
    Modelo para las franquicias
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name="Código",
        help_text="UUID generado automáticamente"
    )
    franchise = models.CharField(max_length=50, verbose_name="Franquicia")
    description = models.TextField(verbose_name="Descripción")
    state = models.ForeignKey(
        FranchiseState, 
        on_delete=models.CASCADE, 
        db_column='state',
        verbose_name="Estado",
        related_name='franchises'
    )

    class Meta:
        db_table = 'franchise'
        verbose_name = "Franquicia"
        verbose_name_plural = "Franquicias"
        ordering = ['franchise']

    def __str__(self):
        return self.franchise

    def save(self, *args, **kwargs):
        # Generar código UUID si no existe
        if not self.code:
            import uuid
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class FranchiseConfigurationType(models.Model):
    """
    Modelo para tipos de configuración de franquicia
    """
    id = models.AutoField(primary_key=True)
    configuration_type = models.CharField(max_length=50, verbose_name="Tipo de Configuración")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'franchise_configuration_type'
        verbose_name = "Tipo de Configuración de Franquicia"
        verbose_name_plural = "Tipos de Configuración de Franquicia"
        ordering = ['configuration_type']

    def __str__(self):
        return self.configuration_type


class FranchiseConfiguration(models.Model):
    """
    Modelo para configuraciones de franquicia
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name="Código",
        help_text="UUID generado automáticamente"
    )
    configuration = models.CharField(max_length=50, verbose_name="Configuración")
    franchise = models.CharField(
        max_length=36,
        verbose_name="Franquicia",
        help_text="Código de la franquicia"
    )
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
        db_table = 'franchise_configuration'
        verbose_name = "Configuración de Franquicia"
        verbose_name_plural = "Configuraciones de Franquicia"
        ordering = ['franchise', 'created_at']

    def __str__(self):
        return f"Configuración - {self.configuration}"

    def save(self, *args, **kwargs):
        # Generar código UUID si no existe
        if not self.code:
            import uuid
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class FranchiseConfigurationDetail(models.Model):
    """
    Modelo para detalles de configuración de franquicia
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        max_length=36, 
        null=True, 
        blank=True,
        verbose_name="Código",
        help_text="UUID generado automáticamente"
    )
    detail = models.CharField(max_length=50, verbose_name="Detalle")
    description = models.TextField(verbose_name="Descripción")
    type = models.ForeignKey(
        FranchiseConfigurationType,
        on_delete=models.CASCADE,
        db_column='type',
        verbose_name="Tipo",
        related_name='configuration_details'
    )
    configuration = models.CharField(
        max_length=36,
        verbose_name="Configuración",
        help_text="Código de la configuración de franquicia"
    )
    index = models.IntegerField(default=1, verbose_name="Índice") # type: ignore
    var = models.CharField(max_length=50, verbose_name="Variable")
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor")
    formula = models.CharField(max_length=36, verbose_name="Fórmula")
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
        db_table = 'franchise_configuration_detail'
        verbose_name = "Detalle de Configuración de Franquicia"
        verbose_name_plural = "Detalles de Configuración de Franquicia"
        ordering = ['configuration', 'type', 'index', 'detail']
        unique_together = ['id', 'type']

    def save(self, *args, **kwargs):
        # Generar código UUID si no existe
        if not self.code:
            import uuid
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.detail}"
