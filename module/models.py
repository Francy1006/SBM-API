from django.db import models

from calculation.models import VariableFormula, CalculationConcept


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=36, null=True, blank=True)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    deleted_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = 'sbm_business"."module'
        managed = False


class OrderConfigType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'sbm_business"."order_config_type'
        managed = False


class ModuleOrderConfig(models.Model):
    id = models.AutoField(primary_key=True)

    order_config_type = models.ForeignKey(
        OrderConfigType,
        db_column="order_config_type",
        on_delete=models.DO_NOTHING,
        related_name="module_order_configs",
    )

    variable_formula = models.ForeignKey(
        VariableFormula,
        to_field="code",
        db_column="variable_formula",
        on_delete=models.DO_NOTHING,
        related_name="module_order_configs",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=36, null=True, blank=True)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    deleted_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = 'sbm_business"."module_order_config'
        managed = False


class ModuleOrderCalculationDetail(models.Model):
    id = models.AutoField(primary_key=True)
    module_config_type = models.ForeignKey(
        ModuleOrderConfig,
        db_column="module_config_type",
        on_delete=models.DO_NOTHING,
        related_name="calculation_details",
    )
    calculation_concept = models.ForeignKey(
        CalculationConcept,
        to_field="code",
        db_column="calculation_concept",
        on_delete=models.DO_NOTHING,
        related_name="module_calculation_details",
    )
    label = models.CharField(max_length=100)
    var = models.CharField(max_length=50)
    format_type = models.CharField(max_length=50, default="currency_int")
    is_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=36)
    updated_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = 'sbm_business"."module_order_calculation_detail'
        managed = False
        unique_together = ("module_config_type", "calculation_concept")