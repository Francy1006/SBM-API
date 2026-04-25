from django.db import models


class VariableFormula(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    formula = models.CharField(max_length=50)
    formula_template = models.TextField()
    formula_translate = models.TextField()
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

    class Meta:
        db_table = '"sbm_business"."variable_formula"'
        managed = False


class CalculationConcept(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.UUIDField(unique=True)

    field_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    data_type = models.ForeignKey(   # ✅ FIX
        "DataType",
        db_column="data_type_id",    # 🔥 CLAVE
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)
    updated_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = 'sbm_business"."calculation_concept'
        managed = False


class DataType(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = '"sbm_business"."data_type"'
        managed = False