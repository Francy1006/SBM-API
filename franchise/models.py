from django.db import models
from django.contrib.auth.models import User


class FranchiseState(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = 'sbm_business"."franchise_state'
        managed = False


class Franchise(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True)
    franchise = models.CharField(max_length=50)
    description = models.TextField()
    state = models.ForeignKey(
        FranchiseState,
        on_delete=models.DO_NOTHING,
        db_column='state',
        related_name='franchises'
    )

    class Meta:
        db_table = 'sbm_business"."franchise'
        managed = False


class FranchiseConfigurationType(models.Model):
    id = models.AutoField(primary_key=True)
    configuration_type = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = 'sbm_business"."franchise_configuration_type'
        managed = False


class FranchiseConfiguration(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True)
    configuration = models.CharField(max_length=50)
    franchise = models.CharField(max_length=36)
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
        db_table = 'ditaly_pasta"."franchise_configuration'
        managed = False


class FranchiseConfigurationDetail(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, null=True, blank=True)
    detail = models.CharField(max_length=50)
    description = models.TextField()
    type = models.ForeignKey(
        FranchiseConfigurationType,
        on_delete=models.DO_NOTHING,
        db_column='type',
        related_name='configuration_details'
    )
    configuration = models.CharField(max_length=36)
    variable_formula = models.CharField(max_length=36, null=True, blank=True)
    index = models.IntegerField(default=1)
    var = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
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
        db_table = 'ditaly_pasta"."franchise_configuration_detail'
        managed = False
