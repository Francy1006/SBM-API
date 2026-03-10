from django.db import models
import uuid
from inventory.models import Package, Provider

# =========================
# CATALOG
# =========================


class Catalog(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    sku = models.CharField(max_length=50, unique=True)

    menu = models.ForeignKey(
        "Menu", db_column="menu", on_delete=models.CASCADE, related_name="catalogs"
    )
    item_group = models.ForeignKey(
        "ItemGroup",
        db_column="item_group",
        on_delete=models.CASCADE,
        related_name="catalogs",
    )
    category = models.ForeignKey(
        "ItemCategory",
        db_column="category",
        on_delete=models.CASCADE,
        related_name="catalogs",
    )
    type = models.ForeignKey(
        "ItemType", db_column="type", on_delete=models.CASCADE, related_name="catalogs"
    )
    restriction = models.ForeignKey(
        "Restriction",
        db_column="restriction",
        on_delete=models.CASCADE,
        related_name="catalogs",
        null=True,
        blank=True,
    )
    usage_instructions = models.ForeignKey(
        "Instruction",
        db_column="usage_instructions",
        on_delete=models.CASCADE,
        related_name="catalogs",
        null=True,
        blank=True,
    )
    configuration = models.ForeignKey(
        "ItemConfiguration",
        db_column="configuration",
        to_field="code",
        on_delete=models.CASCADE,
        related_name="catalogs",
        null=True,
        blank=True,
    )

    price = models.ForeignKey(
        "price.Price",
        db_column="price",
        to_field="code",
        on_delete=models.CASCADE,
        related_name="catalogs",
    )

    name = models.CharField(max_length=50)
    description = models.TextField()
    obs = models.CharField(max_length=255, null=True, blank=True)

    chef_recommendation = models.BooleanField(default=False)
    min_quantity_purchase = models.IntegerField(default=1)
    rations_quantity = models.IntegerField(default=1)

    cover_image = models.CharField(max_length=2083, null=True, blank=True)
    secondary_image = models.CharField(max_length=2083, null=True, blank=True)
    complementary_image = models.CharField(max_length=2083, null=True, blank=True)
    image_gallery = models.CharField(max_length=2083, null=True, blank=True)

    is_visible = models.BooleanField(default=True)
    is_deleted = models.BooleanField(null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)
    confirmed_by = models.CharField(max_length=36, null=True, blank=True)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    deleted_by = models.CharField(max_length=36, null=True, blank=True)

    log = models.TextField(default="init;")
    version = models.IntegerField(default=1)

    class Meta:
        db_table = "catalog"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


# =========================
# PRODUCT
# =========================

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    obs = models.TextField()
    package_unit = models.IntegerField()
    min_package_purchase = models.IntegerField()

    price = models.ForeignKey(
        "price.Price",
        db_column="price",
        to_field="code",
        on_delete=models.PROTECT,
        related_name="products",
    )

    provider = models.ForeignKey(
        Provider,
        db_column="provider",
        on_delete=models.PROTECT,
        related_name="products",
    )

    type = models.ForeignKey(
        "ItemType",
        db_column="type",
        on_delete=models.PROTECT,
        related_name="products",
    )

    item_group = models.ForeignKey(
        "ItemGroup",
        db_column="item_group",
        on_delete=models.PROTECT,
        related_name="products",
    )

    category = models.ForeignKey(
        "ItemCategory",
        db_column="category",
        on_delete=models.PROTECT,
        related_name="products",
    )

    package = models.ForeignKey(
        Package,
        db_column="package",
        on_delete=models.PROTECT,
        related_name="products",
    )

    url = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)
    confirmed_by = models.CharField(max_length=36, null=True, blank=True)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    deleted_by = models.CharField(max_length=36, null=True, blank=True)

    log = models.TextField(default="init;")
    version = models.IntegerField(default=1)

    class Meta:
        db_table = "product"
        ordering = ["-created_at"]

    def __str__(self):
        return self.description


# =========================
# MATERIAL
# =========================


class Material(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    obs = models.TextField()
    package_unit = models.IntegerField()
    min_package_purchase = models.IntegerField()
    price = models.ForeignKey("price.Price", db_column="price", to_field="code", on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, db_column="provider", on_delete=models.PROTECT)
    type = models.ForeignKey("ItemType", db_column="type", on_delete=models.PROTECT)
    item_group = models.ForeignKey("ItemGroup", db_column="item_group", on_delete=models.PROTECT)
    category = models.ForeignKey("ItemCategory", db_column="category", on_delete=models.PROTECT)
    url = models.CharField(max_length=255, null=True, blank=True)
    package = models.ForeignKey(Package, db_column="package", on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "material"

    def __str__(self):
        return self.description


# =========================
# SERVICE
# =========================


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    obs = models.TextField()
    package_unit = models.IntegerField()
    min_package_purchase = models.IntegerField()
    price = models.ForeignKey("price.Price", db_column="price", to_field="code", on_delete=models.PROTECT)
    provider = models.ForeignKey(Provider, db_column="provider", on_delete=models.PROTECT)
    type = models.ForeignKey("ItemType", db_column="type", on_delete=models.PROTECT)
    item_group = models.ForeignKey("ItemGroup", db_column="item_group", on_delete=models.PROTECT)
    category = models.ForeignKey("ItemCategory", db_column="category", on_delete=models.PROTECT)
    url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "service"

    def __str__(self):
        return self.description


# =========================
# REFERENCIA
# =========================


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.CharField(max_length=50)
    description = models.TextField()
    franchise_only = models.BooleanField(default=False)

    background_color = models.CharField(max_length=6, null=True, blank=True)
    text_color = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        db_table = "menu"

    def __str__(self):
        return self.menu

class ItemGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = "item_group"

    def __str__(self):
        return self.group_name


class ItemCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = "item_category"

    def __str__(self):
        return self.category


class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = "item_type"

    def __str__(self):
        return self.type


class Restriction(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    restriction = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "restriction"

    def __str__(self):
        return self.restriction


class Instruction(models.Model):
    code = models.CharField(max_length=36, primary_key=True)
    instruction = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = "instruction"

    def __str__(self):
        return self.instruction


class InstructionType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = "instruction_type"

    def __str__(self):
        return self.type


class ItemConfiguration(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    configuration = models.CharField(max_length=50)
    description = models.TextField()
    package = models.ForeignKey(Package, db_column="package", on_delete=models.PROTECT)

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

    log = models.TextField(default="init;")
    version = models.IntegerField(default=1)

    class Meta:
        db_table = "item_configuration"

    def __str__(self):
        return self.configuration


class ItemConfigurationDetail(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detail = models.CharField(max_length=50)
    type = models.ForeignKey("ItemType", db_column="type", on_delete=models.CASCADE)
    configuration = models.ForeignKey(
        "ItemConfiguration",
        db_column="configuration",
        to_field="code",
        on_delete=models.CASCADE,
    )
    id_item = models.CharField(max_length=36)
    quantity = models.IntegerField(default=1)  # NUEVA COLUMNA REAL EN DB
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=36)

    class Meta:
        db_table = "item_configuration_detail"
        managed = False
