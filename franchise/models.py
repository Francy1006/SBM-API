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
