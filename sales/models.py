from django.db import models
from clients.models import Client


class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = 'sbm_business"."item_type'
        managed = False
        verbose_name = "Tipo de ítem"
        verbose_name_plural = "Tipos de ítem"

    def __str__(self):
        return self.type


class FiscalDocumentType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = 'sbm_business"."fiscal_document_type'
        managed = False
        verbose_name = "Tipo de documento fiscal"
        verbose_name_plural = "Tipos de documento fiscal"

    def __str__(self):
        return self.type


class FiscalDocumentation(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    document_type = models.ForeignKey(
        FiscalDocumentType,
        on_delete=models.DO_NOTHING,
        db_column="document_type",
        related_name="fiscal_documentations",
    )
    document_number = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=2083)
    issued_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=36)

    class Meta:
        db_table = 'sbm_business"."fiscal_documentation'
        managed = False
        verbose_name = "Documentación fiscal"
        verbose_name_plural = "Documentaciones fiscales"

    def __str__(self):
        return self.code


class OrderType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=20)

    class Meta:
        db_table = 'sbm_business"."order_type'
        managed = False
        verbose_name = "Tipo de orden"
        verbose_name_plural = "Tipos de orden"

    def __str__(self):
        return self.type


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    franchise = models.ForeignKey(
        "franchise.Franchise",
        on_delete=models.DO_NOTHING,
        db_column="franchise_code",
        to_field="code",
        related_name="orders",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        db_column="client",
        to_field="code",
        null=True,
        blank=True,
        related_name="orders",
    )
    parent_order = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        db_column="parent_order_id",
        related_name="child_orders",
    )
    order_type = models.ForeignKey(
        OrderType,
        on_delete=models.DO_NOTHING,
        db_column="order_type_id",
        related_name="orders",
    )
    status = models.ForeignKey(
        "config.Status",
        on_delete=models.DO_NOTHING,
        db_column="status_id",
        related_name="orders",
    )

    description = models.TextField(null=True, blank=True)

    is_partial = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_non_conforming = models.BooleanField(default=False)
    requires_cold_chain = models.BooleanField(default=True)
    requires_fiscal_documentation = models.BooleanField(default=False)
    fiscal_documentation_error = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    expected_dispatch_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)
    dispatch_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

    delivery_route = models.CharField(max_length=50, null=True, blank=True)
    delivery_window = models.CharField(max_length=50, null=True, blank=True)
    delivery_comments = models.TextField(null=True, blank=True)

    total_net_amount = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    total_discount = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    total_surcharge = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )

    processed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)
    updated_by = models.CharField(max_length=36, null=True, blank=True)

    log = models.TextField(default="init;")
    version = models.IntegerField(default=1)

    class Meta:
        db_table = 'sbm_business"."order'
        managed = False


class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)

    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        db_column="order_id",
        related_name="details",
    )
    order_type = models.ForeignKey(
        OrderType,
        on_delete=models.DO_NOTHING,
        db_column="order_type_id",
        related_name="order_details",
    )
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.DO_NOTHING,
        db_column="item_type",
        related_name="order_details",
    )

    id_item = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    percent = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    net_amount = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )

    fiscal_documentation = models.ForeignKey(
        FiscalDocumentation,
        on_delete=models.DO_NOTHING,
        db_column="fiscal_documentation",
        related_name="order_details",
        null=True,
        blank=True,
    )

    obs = models.TextField(null=True, blank=True)
    url_evidence = models.CharField(max_length=2083, null=True, blank=True)

    is_delayed = models.BooleanField(default=False)
    is_partial = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_non_conforming = models.BooleanField(default=False)
    requires_cold_chain = models.BooleanField(default=False)
    requires_fiscal_documentation = models.BooleanField(default=False)
    fiscal_documentation_error = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    expected_dispatch_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)
    dispatch_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)

    class Meta:
        db_table = 'sbm_business"."order_detail'
        managed = False


class OrderFiscalDocumentation(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        db_column="order_id",
        related_name="fiscal_documentation_links",
    )
    fiscal_documentation = models.ForeignKey(
        FiscalDocumentation,
        on_delete=models.DO_NOTHING,
        db_column="fiscal_documentation_id",
        related_name="order_fiscal_links",
    )
    description = models.CharField(max_length=255, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=36)

    class Meta:
        db_table = 'sbm_business"."order_fiscal_documentation'
        managed = False
        verbose_name = "Orden — documentación fiscal"
        verbose_name_plural = "Orden — documentaciones fiscales"

    def __str__(self):
        return f"OrderFiscalDoc {self.id}"
