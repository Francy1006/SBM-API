from django.db import models
import uuid


class Catalog(models.Model):
    """
    Modelo para el catálogo
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="CODE")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    menu = models.ForeignKey('Menu', db_column='menu', on_delete=models.CASCADE, related_name='catalogs', verbose_name="Menú")
    item_group = models.ForeignKey('ItemGroup', db_column='item_group', on_delete=models.CASCADE, related_name='catalogs', verbose_name="Grupo")
    category = models.ForeignKey('ItemCategory', db_column='category', on_delete=models.CASCADE, related_name='catalogs', verbose_name="Categoría")
    type = models.ForeignKey('ItemType', db_column='type', on_delete=models.CASCADE, related_name='catalogs', verbose_name="Tipo")
    restriction = models.ForeignKey('Restriction', db_column='restriction', on_delete=models.CASCADE, related_name='catalogs', verbose_name="Restricción")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    obs = models.TextField(verbose_name="Observaciones")
    chef_recommendation = models.BooleanField(default=False, verbose_name="Recomendación del Chef")  # type: ignore
    usage_instructions = models.TextField(verbose_name="Instrucciones de Uso")
    min_quantity_purchase = models.IntegerField(verbose_name="Cantidad Mínima de Compra")
    rations_quantity = models.IntegerField(verbose_name="Cantidad de Raciones")
    cover_image = models.CharField(max_length=255, null=True, blank=True, verbose_name="Imagen de Portada")
    secondary_image = models.CharField(max_length=255, null=True, blank=True, verbose_name="Imagen Secundaria")
    complementary_image = models.CharField(max_length=255, null=True, blank=True, verbose_name="Imagen Complementaria")
    image_gallery = models.TextField(null=True, blank=True, verbose_name="Galería de Imágenes")
    configuration = models.TextField(null=True, blank=True, verbose_name="Configuración")
    is_visible = models.BooleanField(default=True, verbose_name="Es Visible")  # type: ignore
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Está Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Está Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.CharField(max_length=36, verbose_name="Creado Por")
    confirmed_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Confirmado Por")
    updated_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Actualizado Por")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")  # type: ignore

    class Meta:
        db_table = 'catalog'
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Modelo para productos
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código UUID")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    obs = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Empaque")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Empaque")
    price = models.CharField(max_length=36, verbose_name="Precio")
    provider = models.IntegerField(verbose_name="Proveedor")
    type = models.IntegerField(verbose_name="Tipo")
    group = models.IntegerField(verbose_name="Grupo")
    category = models.IntegerField(verbose_name="Categoría")
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name="URL")
    package = models.IntegerField(verbose_name="Empaque")
    is_active = models.BooleanField(default=True, verbose_name="Está Activo")  # type: ignore
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Está Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Está Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.CharField(max_length=36, verbose_name="Creado Por")
    confirmed_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Confirmado Por")
    updated_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Actualizado Por")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")  # type: ignore

    class Meta:
        db_table = 'product'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class Material(models.Model):
    """
    Modelo para materiales
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código UUID")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    obs = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Empaque")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Empaque")
    price = models.CharField(max_length=36, verbose_name="Precio")
    provider = models.IntegerField(verbose_name="Proveedor")
    type = models.IntegerField(verbose_name="Tipo")
    group = models.IntegerField(verbose_name="Grupo")
    category = models.IntegerField(verbose_name="Categoría")
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name="URL")
    package = models.IntegerField(verbose_name="Empaque")
    is_active = models.BooleanField(default=True, verbose_name="Está Activo")  # type: ignore
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Está Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Está Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.CharField(max_length=36, verbose_name="Creado Por")
    confirmed_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Confirmado Por")
    updated_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Actualizado Por")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión") # type: ignore

    class Meta:
        db_table = 'material'
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ['-created_at']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


class Service(models.Model):
    """
    Modelo para servicios
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="CODE")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    description = models.TextField(verbose_name="Descripción")
    obs = models.TextField(verbose_name="Observaciones")
    package_unit = models.IntegerField(verbose_name="Unidad de Empaque")
    min_package_purchase = models.IntegerField(verbose_name="Compra Mínima de Empaque")
    price = models.CharField(max_length=36, verbose_name="Precio")
    provider = models.IntegerField(verbose_name="Proveedor")
    type = models.IntegerField(verbose_name="Tipo")
    group = models.IntegerField(verbose_name="Grupo")
    category = models.IntegerField(verbose_name="Categoría")
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name="Está Activo")  # type: ignore
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Está Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Está Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.CharField(max_length=36, verbose_name="Creado Por")
    confirmed_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Confirmado Por")
    updated_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Actualizado Por")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")  # type: ignore

    class Meta:
        db_table = 'service'
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['-created_at']

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


# Modelos de referencia sbm_business
class Menu(models.Model):
    """
    Modelo para menús
    """
    id = models.AutoField(primary_key=True)
    menu = models.CharField(max_length=50, verbose_name="Menú")
    description = models.TextField(verbose_name="Descripción")
    franchise_only = models.BooleanField(default=False, verbose_name="Solo Franquicia")  # type: ignore

    class Meta:
        db_table = 'menu'
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ['menu']

    def __str__(self):
        return self.menu


class ItemGroup(models.Model):
    """
    Modelo para grupos de items
    """
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50, verbose_name="Nombre del Grupo")
    description = models.TextField(verbose_name="Descripción")
    catalog_render = models.BooleanField(default=True, verbose_name="Renderizar en Catálogo")  # type: ignore

    class Meta:
        db_table = 'item_group'
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos de Items"
        ordering = ['group_name']

    def __str__(self):
        return self.group_name


class ItemCategory(models.Model):
    """
    Modelo para categorías de items
    """
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, verbose_name="Categoría")
    description = models.TextField(verbose_name="Descripción")
    catalog_render = models.BooleanField(default=True, verbose_name="Renderizar en Catálogo")  # type: ignore

    class Meta:
        db_table = 'item_category'
        verbose_name = "Categoría de Item"
        verbose_name_plural = "Categorías de Items"
        ordering = ['category']

    def __str__(self):
        return self.category


class ItemType(models.Model):
    """
    Modelo para tipos de items
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'item_type'
        verbose_name = "Tipo de Item"
        verbose_name_plural = "Tipos de Items"
        ordering = ['type']

    def __str__(self):
        return self.type


class Restriction(models.Model):
    """
    Modelo para restricciones
    """
    id = models.CharField(max_length=36, primary_key=True, verbose_name="Código UUID")
    restriction = models.CharField(max_length=50, unique=True, verbose_name="Restricción")
    description = models.TextField(verbose_name="Descripción")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Está Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Está Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.CharField(max_length=36, verbose_name="Creado Por")
    confirmed_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Confirmado Por")
    updated_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Actualizado Por")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")  # type: ignore

    class Meta:
        db_table = 'restriction'
        verbose_name = "Restricción"
        verbose_name_plural = "Restricciones"
        ordering = ['restriction']

    def __str__(self):
        return self.restriction

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)


class Instruction(models.Model):
    """
    Modelo para instrucciones
    """
    id = models.CharField(max_length=36, primary_key=True, verbose_name="Código UUID")
    instruction = models.CharField(max_length=50, verbose_name="Instrucción")
    description = models.TextField(verbose_name="Descripción")
    url_documentation = models.CharField(max_length=2083, null=True, blank=True, verbose_name="URL de Documentación")
    type = models.IntegerField(verbose_name="Tipo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Está Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Está Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.CharField(max_length=36, verbose_name="Creado Por")
    confirmed_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Confirmado Por")
    updated_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Actualizado Por")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")

    class Meta:
        db_table = 'instruction'
        verbose_name = "Instrucción"
        verbose_name_plural = "Instrucciones"
        ordering = ['instruction']

    def __str__(self):
        return self.instruction

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)


# Modelos de referencia ditaly_pasta

class Provider(models.Model):
    """
    Modelo para proveedores
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código UUID")
    provider = models.CharField(max_length=50, unique=True, verbose_name="Proveedor")
    type = models.IntegerField(verbose_name="Tipo")
    rating = models.IntegerField(default=0, verbose_name="Calificación")  # type: ignore
    obs_provider = models.TextField(verbose_name="Observaciones del Proveedor")
    contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre de Contacto")
    contact_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Contacto")
    contact_phone = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Contacto")
    contact_phone2 = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Contacto 2")
    website_url = models.TextField(null=True, blank=True, verbose_name="URL del Sitio Web")
    obs_contact = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observaciones de Contacto")
    company_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nombre de la Empresa")
    company_rut = models.CharField(max_length=12, null=True, blank=True, verbose_name="RUT de la Empresa")
    company_activity = models.CharField(max_length=255, null=True, blank=True, verbose_name="Actividad de la Empresa")
    legal_representative = models.CharField(max_length=255, null=True, blank=True, verbose_name="Representante Legal")
    billing_address = models.TextField(null=True, blank=True, verbose_name="Dirección de Facturación")
    billing_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Facturación")
    billing_phone = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Facturación")
    company_bank = models.IntegerField(null=True, blank=True, verbose_name="Banco de la Empresa")
    bank_account_type = models.IntegerField(null=True, blank=True, verbose_name="Tipo de Cuenta Bancaria")
    bank_account_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Número de Cuenta Bancaria")
    bank_account_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Cuenta Bancaria")
    dispatch_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Dirección de Despacho")
    dispatch_maps_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación en Maps")
    obs_dispatch = models.TextField(null=True, blank=True, verbose_name="Observaciones de Despacho")
    dispatch_district = models.IntegerField(null=True, blank=True, verbose_name="Distrito de Despacho")
    dispatch_region = models.IntegerField(null=True, blank=True, verbose_name="Región de Despacho")
    is_active = models.BooleanField(default=True, verbose_name="Está Activo")  # type: ignore
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Está Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Está Confirmado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.CharField(max_length=36, verbose_name="Creado Por")
    confirmed_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Confirmado Por")
    updated_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Actualizado Por")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")

    class Meta:
        db_table = 'provider'
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['provider']

    def __str__(self):
        return self.provider

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)


# Modelos de referencia sbm_business adicionales
class ProviderType(models.Model):
    """
    Modelo para tipos de proveedores
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'provider_type'
        verbose_name = "Tipo de Proveedor"
        verbose_name_plural = "Tipos de Proveedores"
        ordering = ['type']

    def __str__(self):
        return self.type


class Bank(models.Model):
    """
    Modelo para bancos
    """
    id = models.AutoField(primary_key=True)
    bank = models.CharField(max_length=255, verbose_name="Banco")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'bank'
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"
        ordering = ['bank']

    def __str__(self):
        return self.bank


class BankAccountType(models.Model):
    """
    Modelo para tipos de cuenta bancaria
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'bank_account_type'
        verbose_name = "Tipo de Cuenta Bancaria"
        verbose_name_plural = "Tipos de Cuenta Bancaria"
        ordering = ['type']

    def __str__(self):
        return self.type


class Region(models.Model):
    """
    Modelo para regiones
    """
    id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=255, verbose_name="Región")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'region'
        verbose_name = "Región"
        verbose_name_plural = "Regiones"
        ordering = ['region']

    def __str__(self):
        return self.region


class District(models.Model):
    """
    Modelo para distritos
    """
    id = models.AutoField(primary_key=True)
    district = models.CharField(max_length=255, verbose_name="Distrito")
    region = models.IntegerField(verbose_name="Región")
    description = models.TextField(verbose_name="Descripción")

    class Meta:
        db_table = 'district'
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['district']

    def __str__(self):
        return self.district
