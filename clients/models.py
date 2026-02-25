from django.db import models


# 🔹 1️⃣ PRIMERO Client
class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    detection_date = models.DateField()
    status = models.IntegerField()
    platform = models.IntegerField()

    exact_address = models.CharField(max_length=255)
    district = models.IntegerField()
    region = models.IntegerField()
    same_address_detected = models.BooleanField(default=False)

    estimated_type = models.CharField(max_length=150, null=True, blank=True)
    operation_schedule = models.CharField(max_length=150, null=True, blank=True)
    estimated_avg_ticket = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    has_visible_physical_store = models.BooleanField(default=False)

    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_rut = models.CharField(max_length=20, null=True, blank=True)
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    owner_position = models.CharField(max_length=150, null=True, blank=True)
    linkedin_url = models.CharField(max_length=255, null=True, blank=True)

    direct_phone = models.CharField(max_length=50, null=True, blank=True)
    direct_email = models.EmailField(null=True, blank=True)
    contacted = models.BooleanField(default=False)
    contact_date = models.DateField(null=True, blank=True)
    progress = models.TextField(null=True, blank=True)

    estimated_potential_volume = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    priority = models.CharField(max_length=20, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.CharField(max_length=36)
    updated_by = models.CharField(max_length=36, null=True, blank=True)
    deleted_by = models.CharField(max_length=36, null=True, blank=True)

    log = models.TextField(default="init;")
    version = models.IntegerField(default=1)

    class Meta:
        db_table = "client"
        managed = False


# 🔹 2️⃣ DESPUÉS ClientBrand
class ClientBrand(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)

    client = models.ForeignKey(
        "Client",  # usar string evita NameError
        to_field="code",  # 🔥 FK apunta a code, no a id
        db_column="client",  # nombre real columna
        on_delete=models.DO_NOTHING,
        related_name="brands",
    )

    brand_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=36)

    class Meta:
        db_table = "client_brand"
        managed = False


class Region(models.Model):
    id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "region"
        managed = False
        ordering = ["id"]

    def __str__(self):
        return self.region


class District(models.Model):
    id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=255)
    region = models.ForeignKey(
        Region,
        on_delete=models.DO_NOTHING,
        db_column="region",
        related_name="districts",
    )
    description = models.TextField()

    class Meta:
        db_table = "district"
        managed = False
        ordering = ["id"]

    def __str__(self):
        return self.district
