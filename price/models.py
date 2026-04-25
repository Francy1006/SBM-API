import uuid
from django.db import models
from django.contrib.auth.models import User


# -------------------------
# PRICE
# -------------------------
class Price(models.Model):
    id = models.AutoField(primary_key=True)

    code = models.CharField(max_length=36, unique=True, null=True)

    base_net_amount = models.IntegerField(default=0)
    net_amount = models.IntegerField(default=0)
    gross_amount = models.IntegerField(default=0)
    iva_amount = models.IntegerField(default=0)
    aditional_tax_amount = models.IntegerField(default=0)
    retention_amount = models.IntegerField(default=0)

    price_configuration = models.ForeignKey(
        "PriceConfiguration",
        to_field="code",
        db_column="price_configuration",
        on_delete=models.PROTECT,
    )

    is_current = models.BooleanField(default=True, null=True)
    is_deleted = models.BooleanField(null=True)
    is_confirmed = models.BooleanField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=36)

    record_item_code = models.CharField(max_length=36, null=True)

    price_record_type = models.ForeignKey(
        "PriceType",
        to_field="id",
        db_column="price_record_type",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="price_records",
    )

    class Meta:
        db_table = "price"
        ordering = ["-created_at"]


# -------------------------
# PRICE CONFIGURATION
# -------------------------
class PriceConfiguration(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    price_configuration = models.CharField(max_length=50, unique=True)
    franchise_configuration = models.CharField(max_length=36)

    variable_formula = models.ForeignKey(
        "calculation.VariableFormula",
        to_field="code",
        db_column="variable_formula",
        on_delete=models.DO_NOTHING,
        related_name="price_configurations",
    )

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
        db_table = '"ditaly_pasta"."price_configuration"'
        managed = False


# -------------------------
# PRICE CONFIG DETAIL
# -------------------------
class PriceConfigurationDetail(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.UUIDField(unique=True)

    price_configuration = models.ForeignKey(
        PriceConfiguration,
        to_field="code",
        db_column="price_configuration",
        on_delete=models.DO_NOTHING,
        related_name="details",
    )

    calculation_concept = models.ForeignKey(
        "calculation.CalculationConcept",
        to_field="code",
        db_column="calculation_concept",
        on_delete=models.DO_NOTHING,
        related_name="config_details",
    )

    label = models.CharField(max_length=100)
    format_type = models.CharField(max_length=50, default="currency_int")

    is_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)
    updated_by = models.CharField(max_length=36, null=True, blank=True)

    class Meta:
        db_table = '"ditaly_pasta"."price_configuration_detail"'
        managed = False
        unique_together = ("price_configuration", "calculation_concept")


# -------------------------
# PRICE LIST
# -------------------------
class PriceList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    franchise = models.ForeignKey(
        "franchise.Franchise",
        on_delete=models.CASCADE,
        related_name="price_lists",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_price_lists",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "price_list"
        ordering = ["name"]


# -------------------------
# PRICE ITEM
# -------------------------
class PriceItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    price_list = models.ForeignKey(
        PriceList,
        on_delete=models.CASCADE,
        related_name="items",
    )

    catalog_item = models.ForeignKey(
        "catalog.Catalog",
        on_delete=models.CASCADE,
        related_name="price_items",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_price_items",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "price_item"
        unique_together = ["price_list", "catalog_item"]


# -------------------------
# PRICE DISCOUNT
# -------------------------
class PriceDiscount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    discount_type = models.CharField(max_length=10)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(null=True, blank=True)

    franchise = models.ForeignKey(
        "franchise.Franchise",
        on_delete=models.CASCADE,
        related_name="price_discounts",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_price_discounts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "price_discount"


# -------------------------
# PRICE HISTORY
# -------------------------
class PriceHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)

    change_reason = models.TextField(blank=True)

    price_item = models.ForeignKey(
        PriceItem,
        on_delete=models.CASCADE,
        related_name="history",
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="price_changes",
    )

    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "price_history"


# -------------------------
# PRICE TYPE
# -------------------------
class PriceType(models.Model):
    id = models.AutoField(primary_key=True)

    type = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "price_type"
        ordering = ["type"]

    def __str__(self):
        return self.type