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


class DataType(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = '"sbm_business"."data_type"'
        managed = False


class CalculationConcept(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.UUIDField(unique=True)

    field_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    data_type = models.ForeignKey(
        DataType,
        db_column="data_type_id",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="calculation_concepts",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)
    updated_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = '"sbm_business"."calculation_concept"'
        managed = False


class ModuleCalculationDetail(models.Model):
    id = models.AutoField(primary_key=True)

    module = models.ForeignKey(
        "module.Module",
        db_column="module",
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

    # 🔥 agregado según tu SQL (a.format_type)
    format_type = models.IntegerField(db_column="format_type", null=True, blank=True)

    is_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)
    updated_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = '"sbm_business"."module_calculation_detail"'
        managed = False