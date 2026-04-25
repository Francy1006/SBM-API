import uuid
from django.db import models


class FiscalConfigurationDetail(models.Model):

    id = models.AutoField(primary_key=True)

    module_id = models.IntegerField()

    module_config_id = models.CharField(max_length=50)

    fiscal_directive = models.CharField(max_length=36)

    var = models.CharField(max_length=50)

    data_type = models.IntegerField(
        db_column="data_type_id", null=True, blank=True  # 🔥 ESTE ES EL FIX
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36, null=True, blank=True)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    deleted_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = 'ditaly_pasta"."fiscal_configuration_detail'
        managed = False


class FiscalDirectiveType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = '"sbm_business"."fiscal_directive_type"'
        managed = False


class FiscalDirective(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    obs = models.TextField(null=True, blank=True)
    fiscal_directive = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(
        FiscalDirectiveType,
        on_delete=models.DO_NOTHING,
        db_column="type",
        related_name="fiscal_directives",
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
        db_table = '"sbm_business"."fiscal_directive"'
        managed = False


class FiscalDirectiveStats(models.Model):

    type = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=255)
    type_description = models.TextField()
    total_directives = models.IntegerField()
    confirmed_directives = models.IntegerField()
    deleted_directives = models.IntegerField()
    pending_directives = models.IntegerField()
    avg_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_value = models.DecimalField(max_digits=10, decimal_places=2)
    current_year_directives = models.IntegerField()
    directives_with_month = models.IntegerField()
    directives_with_end_month = models.IntegerField()
    directives_with_end_year = models.IntegerField()
    earliest_year = models.IntegerField()
    latest_year = models.IntegerField()
    unique_years = models.IntegerField()
    unique_months = models.IntegerField()

    class Meta:
        db_table = '"analytics"."fiscal_directive_stats"'
        managed = False
