from django.db import models


class VariableFormula(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True)
    formula = models.CharField(max_length=50)
    formula_template = models.TextField()
    formula_translate = models.TextField()
    is_deleted = models.BooleanField(null=True)
    is_confirmed = models.BooleanField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    confirmed_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=36)
    confirmed_by = models.CharField(max_length=36, null=True)
    updated_by = models.CharField(max_length=36, null=True)
    deleted_by = models.CharField(max_length=36, null=True)

    class Meta:
        db_table = 'sbm_business"."variable_formula'
        managed = False


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