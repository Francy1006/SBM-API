# Calavera Pirata Digital

                                                       █                                                       █──▄────▄▄▄▄▄▄▄────▄───
                                                       █─▀▀▄─▄█████████▄─▄▀▀──
                                                       █─────██─▀███▀─██──────
                                                       █───▄─▀████▀████▀─▄────
                                                       █─▀█────██▀█▀██────█▀──
        ▄████▄   ▒█████   ███▄    █  ██ ██░██████ ▄▄▄  █    
       ▒██▀ ▀█  ▒██▒  ██▒ ██ ▀█   █  ██ █░ ▓█   ▀▒████▄█    
       ▒▓█    ▄ ▒██░  ██▒ ██  ▀█ █▒  ████░ ▒███  ▒██   █▄   
       ▒▓▓▄ ▄██ ▒██   ██░ ██▒  ▐▌█▒  ██ █▄ ▒▓█  ▄░████████  
       ▒ ▓███▀ ░░ ████▓▒  ██░   ▓█░  █▒ ██▄░▒████▒▓█  █▒ 
       ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒  ▒▒ ▓▒░░ ▒░ ░▒▒   ▓▒█░ 
         ░  ▒     ░ ▒ ▒░ ░ ░░   ░ ▒  ░▒ ▒░ ░ ░  ░ ▒   ▒▒ ░ 
       ░        ░ ░ ░ ▒     ░   ░ ░ ░ ░░ ░    ░    ░   ▒    
       ░ ░          ░ ░           ░ ░  ░      ░  ░     ░  ░ 
       ░                                                           
       ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄
      █ ▄▄▄ █ ▀▀ ▄▀ ▀▄▀ █ ▄▄▄ █ ▄▀ ▀▄▀ █ ▄▄▄ █ ▄▄▄ █ ▀▀ ▄▀ ▀▄
      █ ███ █ ▀ ▀▄█ ▄ ▀ █ ███ █ ▀▄█ ▄ ▀ █ ███ █ ███ █ ▀ ▀▄█ ▄
      █▄▄▄█ █ █▄▀ █ ▀█ █ █▄▄▄█ █▄▀ █ ▀█ █▄▄▄█ █▄▄▄█ █ █▄▀ █ ▀
      ▄▄▄▄▄▄█ ▀▄█▄▀ ▀ █▄█▄▄▄▄▄█ ▀▄█▄▀ ▀ █▄▄▄▄▄█▄▄▄▄▄█ ▀▄█▄▀ ▀

    ████████████████████████████████████████████████████████████████
    ██  ║                                                       ║  ██
    ██  ║               ░▒▓ SBM - API ▓▒░                       ║  ██
    ██  ║                                                       ║  ██
    ██  ║    ┌─────────────────────────────────────────────┐    ║  ██
    ██  ║    │  > SBM Official API                         │    ║  ██
    ██  ║    │  > Users, Finance, Operational, Providers   │    ║  ██
    ██  ║    │  > BASIC CRUD                               │    ║  ██
    ██  ║    │  > users, login and token validation        │    ║  ██
    ██  ║    │  > STATUS: ACTIVE                           │    ║  ██
    ██  ║    └─────────────────────────────────────────────┘    ║  ██
    ██  ║                                                       ║  ██
    ██  ║         ░▒▓ SBM-ADMIN ACCESS GRANTED ▓▒░              ║  ██
    ██  ║                                                       ║  ██
    ██  ╚═══════════════════════════════════════════════════════╝  ██
    ██                                                             ██
    ████████████████████████████████████████████████████████████████



## Símbolo Digital de los Mares Cibernéticos

**Advertencia:** *Este símbolo marca territorio peligroso en el ciberespacio*

---

*"En las profundidades de la red, donde los datos son tesoros y la información es poder..."*


# SBM-API - Documentación Técnica Completa

## Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Configuración del Proyecto](#configuración-del-proyecto)
4. [Base de Datos](#base-de-datos)
5. [Aplicaciones Django](#aplicaciones-django)
6. [Modelos de Datos](#modelos-de-datos)
7. [API Endpoints](#api-endpoints)
8. [Autenticación y Permisos](#autenticación-y-permisos)
9. [Configuración de Docker](#configuración-de-docker)
10. [Despliegue](#despliegue)
11. [Guías de Desarrollo](#guías-de-desarrollo)
12. [Troubleshooting](#troubleshooting)
13. [Referencias](#referencias)

---

## 1. Descripción General

**SBM-API** es una API REST desarrollada en Django que proporciona servicios para la gestión de catálogos, productos, proveedores y usuarios. La API está diseñada para ser consumida por aplicaciones frontend y otros servicios.

### Características Principales
- ✅ API REST completa con Django REST Framework
- ✅ Autenticación por token y sesión
- ✅ Gestión de catálogos y productos
- ✅ Sistema de proveedores
- ✅ Gestión de usuarios y roles
- ✅ Base de datos PostgreSQL con múltiples esquemas
- ✅ Documentación automática con Django Jazzmin
- ✅ Configuración Docker completa

---

## 2. Arquitectura del Sistema

### Estructura del Proyecto
```
SBM-API/
├── core/                    # Proyecto principal Django
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs principales
│   ├── views.py            # Vistas del proyecto
│   ├── wsgi.py             # Configuración WSGI
│   ├── asgi.py             # Configuración ASGI
│   ├── Dockerfile          # Imagen Docker (PostgreSQL)
│   ├── entrypoint.sh       # Script de inicio
│   └── requirements.txt    # Dependencias Python
├── users/                   # Gestión de usuarios
│   ├── models.py           # Modelos de usuarios
│   ├── views.py            # ViewSets de usuarios
│   ├── serializers.py      # Serializers de usuarios
│   ├── urls.py             # URLs de usuarios
│   └── admin.py            # Admin de usuarios
├── authz/                   # Autorización y permisos
│   ├── models.py           # Modelos de roles y permisos
│   ├── views.py            # ViewSets de autorización
│   ├── serializers.py      # Serializers de autorización
│   ├── urls.py             # URLs de autorización
│   └── admin.py            # Admin de autorización
├── products/                # Gestión de productos
│   ├── models.py           # Modelos de productos
│   ├── views.py            # ViewSets de productos
│   ├── serializers.py      # Serializers de productos
│   ├── urls.py             # URLs de productos
│   └── admin.py            # Admin de productos
├── providers/               # Gestión de proveedores
│   ├── models.py           # Modelos de proveedores
│   ├── views.py            # ViewSets de proveedores
│   ├── serializers.py      # Serializers de proveedores
│   ├── urls.py             # URLs de proveedores
│   └── admin.py            # Admin de proveedores
├── pricing/                 # Gestión de precios
│   ├── models.py           # Modelos de precios
│   ├── views.py            # ViewSets de precios
│   ├── serializers.py      # Serializers de precios
│   ├── urls.py             # URLs de precios
│   └── admin.py            # Admin de precios
├── documentation/           # Gestión de documentación
│   ├── models.py           # Modelos de documentación
│   ├── views.py            # ViewSets de documentación
│   ├── serializers.py      # Serializers de documentación
│   ├── urls.py             # URLs de documentación
│   └── admin.py            # Admin de documentación
├── sales/                   # Gestión de ventas (placeholder)
│   ├── models.py           # Modelos de ventas
│   ├── views.py            # ViewSets de ventas
│   ├── serializers.py      # Serializers de ventas
│   ├── urls.py             # URLs de ventas
│   └── admin.py            # Admin de ventas
├── templates/               # Templates HTML
├── manage.py                # Comando Django (raíz)
├── docker-compose.yml       # Configuración Docker
└── .env                     # Variables de entorno
```

### Tecnologías Utilizadas
- **Backend**: Django 4.2.16, Django REST Framework
- **Base de Datos**: PostgreSQL 13+
- **Autenticación**: Django REST Framework Token Auth
- **Admin**: Django Jazzmin
- **Contenedores**: Docker & Docker Compose
- **Filtros**: Django Filter
- **CORS**: django-cors-headers

---

## 3. Configuración del Proyecto

### Variables de Entorno (.env)
```bash
# Django settings
DEBUG=0
SECRET_KEY=MysecretKey
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:9000
STATIC_URL=static/

# Internationalization
LANGUAGE_CODE=es-ar
TIME_ZONE=America/Santiago
USE_I18N=1
USE_TZ=1

# PostgreSQL connection
DB_NAME=sbm_db
DB_USER=sbm_admin
DB_PASSWORD=FrancY1
DB_HOST=postgres
DB_PORT=5432

# Media files
MEDIA_URL=/media/
MEDIA_ROOT=os.path.join(BASE_DIR, "media")

# Django Superuser Credentials
DJANGO_SUPERUSER_USERNAME=sbm-admin
DJANGO_SUPERUSER_EMAIL=operacione@ditalypasta.cl
DJANGO_SUPERUSER_PASSWORD=sbm123
```

### Configuración Django (core/settings.py)

#### Aplicaciones Instaladas
```python
INSTALLED_APPS = [
    'jazzmin',                    # Admin moderno
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',             # API REST
    'corsheaders',                # CORS
    'django_filters',             # Filtros
    'users',                      # Gestión de usuarios
    'authz',                      # Autorización y permisos
    'products',                   # Gestión de productos
    'providers',                  # Gestión de proveedores
    'pricing',                    # Gestión de precios
    'documentation',              # Gestión de documentación
    'sales',                      # Gestión de ventas (placeholder)
]
```

#### Configuración de Base de Datos
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
        'OPTIONS': {
            'options': '-c search_path=ditaly_pasta,sbm_business,public',
            'connect_timeout': 10,
        },
    }
}
```

#### Configuración REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

#### Configuración CORS
```python
CORS_ALLOW_ALL_ORIGINS = True  # Solo para desarrollo
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = str(env("CORS_ALLOWED_ORIGINS")).split(",")
```

#### Deshabilitación de Migraciones
```python
# Disable Django migrations for business apps - using Flyway instead
# Enable migrations only for Django system apps
MIGRATION_MODULES = {
    'users': None,
    'authz': None,
    'products': None,
    'providers': None,
    'pricing': None,
    'documentation': None,
    'sales': None,
    # Django system apps - migrations enabled
    # 'admin': None,  # Comentado para permitir migraciones
    # 'auth': None,   # Comentado para permitir migraciones  
    # 'contenttypes': None,  # Comentado para permitir migraciones
    # 'sessions': None,  # Comentado para permitir migraciones
}
```

---

## 4. Base de Datos

### Esquemas de Base de Datos
El proyecto utiliza PostgreSQL con múltiples esquemas:

- **`sbm_business`**: Tablas principales del negocio
- **`ditaly_pasta`**: Tablas específicas de productos y catálogos
- **`public`**: Esquema por defecto

### Configuración de Search Path
```sql
SET search_path TO ditaly_pasta, sbm_business, public;
```

### Tablas Principales

#### Esquema sbm_business
- `menu` - Menús del sistema
- `item_group` - Grupos de items
- `item_category` - Categorías de items
- `item_type` - Tipos de items
- `user` - Usuarios del sistema
- `user_type` - Tipos de usuario
- `provider_type` - Tipos de proveedor
- `instruction` - Instrucciones del sistema
- `instruction_type` - Tipos de instrucción
- `package` - Paquetes
- `package_type` - Tipos de paquete
- `transport_type` - Tipos de transporte
- `measure_unit` - Unidades de medida
- `bank` - Bancos
- `bank_account_type` - Tipos de cuenta bancaria
- `region` - Regiones
- `district` - Distritos
- `role` - Roles del sistema
- `permission` - Permisos
- `restriction` - Restricciones

#### Esquema ditaly_pasta
- `catalog` - Catálogo de productos
- `provider` - Proveedores
- `product` - Productos
- `material` - Materiales
- `service` - Servicios
- `price` - Precios
- `item_configuration` - Configuraciones de items

---

## 5. Aplicaciones Django

### Organización de Aplicaciones

El proyecto está organizado en 7 aplicaciones Django especializadas, cada una responsable de un dominio específico del negocio:

#### 1. **users** - Gestión de Usuarios
- **Responsabilidad**: Gestión de usuarios del sistema
- **Modelos principales**: `User`, `UserType`
- **Endpoints**: `/api/users/`, `/api/user-types/`
- **Funcionalidades**: CRUD de usuarios, tipos de usuario, autenticación

#### 2. **authz** - Autorización y Permisos
- **Responsabilidad**: Gestión de roles, permisos y restricciones
- **Modelos principales**: `Role`, `Permission`, `Restriction`
- **Endpoints**: `/api/roles/`, `/api/permissions/`, `/api/restrictions/`
- **Funcionalidades**: Control de acceso, gestión de permisos

#### 3. **products** - Gestión de Productos
- **Responsabilidad**: Gestión de catálogos y productos
- **Modelos principales**: `Menu`, `ItemGroup`, `ItemCategory`, `ItemType`, `Catalog`, `Product`, `Package`, `PackageType`, `TransportType`, `MeasureUnit`
- **Endpoints**: `/api/menus/`, `/api/item-groups/`, `/api/item-categories/`, `/api/item-types/`, `/api/catalogs/`, `/api/products/`, `/api/packages/`, `/api/package-types/`, `/api/transport-types/`, `/api/measure-units/`
- **Funcionalidades**: CRUD de productos, catálogos, organización de productos, categorización

#### 4. **providers** - Gestión de Proveedores
- **Responsabilidad**: Gestión de proveedores y sus datos
- **Modelos principales**: `Provider`, `ProviderType`, `Region`, `District`, `Bank`, `BankAccountType`
- **Endpoints**: `/api/providers/`, `/api/provider-types/`, `/api/regions/`, `/api/districts/`, `/api/banks/`, `/api/bank-account-types/`
- **Funcionalidades**: CRUD de proveedores, información de contacto, datos bancarios, regiones y distritos

#### 5. **pricing** - Gestión de Precios
- **Responsabilidad**: Gestión de precios y configuraciones fiscales
- **Modelos principales**: `Price`, `FiscalDirective`, `FiscalDirectiveType`, `FiscalFormula`, `PriceFiscalConfiguration`, `FiscalConfigurationDetail`
- **Endpoints**: `/api/prices/`, `/api/fiscal-directives/`, `/api/fiscal-directive-types/`, `/api/fiscal-formulas/`, `/api/price-fiscal-configurations/`, `/api/fiscal-configuration-details/`
- **Funcionalidades**: Gestión de precios, directivas fiscales, configuraciones de precios

#### 6. **documentation** - Gestión de Documentación
- **Responsabilidad**: Gestión de instrucciones y documentación
- **Modelos principales**: `Instruction`, `InstructionType`
- **Endpoints**: `/api/instructions/`, `/api/instruction-types/`
- **Funcionalidades**: CRUD de instrucciones, tipos de instrucción

#### 7. **sales** - Gestión de Ventas (Placeholder)
- **Responsabilidad**: Gestión de ventas (preparado para futuras implementaciones)
- **Modelos principales**: `SalesBase` (abstracto)
- **Endpoints**: Placeholder - funcionalidad futura
- **Funcionalidades**: Preparado para futuras implementaciones de ventas

### Estructura de Cada Aplicación

Cada aplicación sigue la estructura estándar de Django:

```
app_name/
├── __init__.py              # Inicialización de la app
├── admin.py                 # Configuración del admin Django
├── apps.py                  # Configuración de la aplicación
├── models.py                # Modelos de datos
├── serializers.py           # Serializers de DRF
├── views.py                 # ViewSets y vistas
├── urls.py                  # URLs de la aplicación
└── tests.py                 # Tests unitarios
```

### Configuración de URLs

Las URLs están organizadas jerárquicamente:

```python
# core/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('authz.urls')),
    path('api/', include('products.urls')),
    path('api/', include('providers.urls')),
    path('api/', include('pricing.urls')),
    path('api/', include('documentation.urls')),
    path('api/', include('sales.urls')),
]
```

### Convenciones de Nomenclatura

- **Aplicaciones**: Nombres en minúsculas, descriptivos del dominio
- **Modelos**: PascalCase (ej: `User`, `Product`)
- **ViewSets**: PascalCase + ViewSet (ej: `UserViewSet`)
- **Serializers**: PascalCase + Serializer (ej: `UserSerializer`)
- **URLs**: kebab-case (ej: `/api/users/`, `/api/user-types/`)

---

## 6. Modelos de Datos

### Modelos Principales

#### Menu
```python
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.CharField(max_length=50, verbose_name="Menú")
    description = models.TextField(verbose_name="Descripción")
    franchise_only = models.BooleanField(default=False, verbose_name="Solo Franquicia")
    
    class Meta:
        db_table = 'menu'
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ['menu']
```

#### ItemGroup
```python
class ItemGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50, verbose_name="Nombre del Grupo")
    description = models.TextField(verbose_name="Descripción")
    catalog_render = models.BooleanField(default=True, verbose_name="Renderizar en Catálogo")
    
    class Meta:
        db_table = 'item_group'
        verbose_name = "Grupo de Items"
        verbose_name_plural = "Grupos de Items"
        ordering = ['group_name']
```

#### ItemCategory
```python
class ItemCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, verbose_name="Categoría")
    description = models.TextField(verbose_name="Descripción")
    catalog_render = models.BooleanField(default=True, verbose_name="Renderizar en Catálogo")
    
    class Meta:
        db_table = 'item_category'
        verbose_name = "Categoría de Items"
        verbose_name_plural = "Categorías de Items"
        ordering = ['category']
```

#### ItemType
```python
class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")
    
    class Meta:
        db_table = 'item_type'
        verbose_name = "Tipo de Item"
        verbose_name_plural = "Tipos de Items"
        ordering = ['type']
```

#### User
```python
class User(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    type = models.ForeignKey(UserType, on_delete=models.CASCADE, db_column='type')
    google_id = models.CharField(max_length=255, unique=True, verbose_name="Google ID")
    mail = models.CharField(max_length=255, unique=True, verbose_name="Email")
    phone = models.BigIntegerField(verbose_name="Teléfono")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    last_name = models.CharField(max_length=255, verbose_name="Apellido")
    is_active = models.BooleanField(null=True, blank=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")
    
    class Meta:
        db_table = 'user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['name']
```

#### Catalog
```python
class Catalog(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column='menu')
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, db_column='item_group')
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, db_column='category')
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, db_column='type')
    restriction = models.CharField(max_length=36, verbose_name="Restricción")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    obs = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observaciones")
    chef_recommendation = models.BooleanField(default=False, verbose_name="Recomendación del Chef")
    usage_instructions = models.ForeignKey(Instruction, on_delete=models.CASCADE, db_column='usage_instructions')
    price = models.CharField(max_length=36, verbose_name="Precio", db_column='base_gross_price')
    min_quantity_purchase = models.IntegerField(default=1, verbose_name="Cantidad Mínima de Compra")
    rations_quantity = models.IntegerField(default=1, verbose_name="Cantidad de Raciones")
    cover_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen de Portada")
    secondary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Secundaria")
    complementary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Complementaria")
    image_gallery = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Galería de Imágenes")
    configuration = models.CharField(max_length=36, verbose_name="Configuración")
    is_visible = models.BooleanField(default=True, verbose_name="Visible")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='catalogs_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='catalogs_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='catalogs_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='catalogs_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")
    
    class Meta:
        db_table = 'catalog'
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"
        ordering = ['-created_at']
```

#### Provider
```python
class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    provider = models.CharField(max_length=50, unique=True, verbose_name="Proveedor")
    type = models.ForeignKey(ProviderType, on_delete=models.CASCADE, db_column='type')
    rating = models.IntegerField(default=0, verbose_name="Calificación")
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
    company_bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True, db_column='company_bank')
    bank_account_type = models.ForeignKey(BankAccountType, on_delete=models.SET_NULL, null=True, blank=True, db_column='bank_account_type')
    bank_account_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Número de Cuenta Bancaria")
    bank_account_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Cuenta Bancaria")
    dispatch_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Dirección de Despacho")
    dispatch_maps_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación en Maps")
    obs_dispatch = models.TextField(null=True, blank=True, verbose_name="Observaciones de Despacho")
    dispatch_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, db_column='dispatch_district')
    dispatch_region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, db_column='dispatch_region')
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='providers_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='providers_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='providers_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='providers_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")
    
    class Meta:
        db_table = 'provider'
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['provider']
```

---

## 7. API Endpoints

### Base URL
```
http://localhost:8081/api/
```

### Endpoints por Aplicación

#### **users** - Gestión de Usuarios
```
GET    /api/users/                       # Listar usuarios
POST   /api/users/                       # Crear usuario
GET    /api/users/{id}/                  # Obtener usuario específico
PUT    /api/users/{id}/                  # Actualizar usuario
DELETE /api/users/{id}/                  # Eliminar usuario
GET    /api/users/active/                # Solo usuarios activos
GET    /api/users/confirmed/             # Solo usuarios confirmados

GET    /api/user-types/                  # Listar tipos de usuario
POST   /api/user-types/                  # Crear tipo de usuario
GET    /api/user-types/{id}/             # Obtener tipo específico
PUT    /api/user-types/{id}/             # Actualizar tipo
DELETE /api/user-types/{id}/             # Eliminar tipo
```

#### **authz** - Autorización y Permisos
```
GET    /api/roles/                       # Listar roles
POST   /api/roles/                       # Crear rol
GET    /api/roles/{id}/                  # Obtener rol específico
PUT    /api/roles/{id}/                  # Actualizar rol
DELETE /api/roles/{id}/                  # Eliminar rol

GET    /api/permissions/                 # Listar permisos
POST   /api/permissions/                 # Crear permiso
GET    /api/permissions/{id}/            # Obtener permiso específico
PUT    /api/permissions/{id}/            # Actualizar permiso
DELETE /api/permissions/{id}/            # Eliminar permiso

GET    /api/restrictions/                # Listar restricciones
POST   /api/restrictions/                # Crear restricción
GET    /api/restrictions/{id}/           # Obtener restricción específica
PUT    /api/restrictions/{id}/           # Actualizar restricción
DELETE /api/restrictions/{id}/           # Eliminar restricción
```

#### **products** - Gestión de Productos
```
GET    /api/menus/                       # Listar menús
POST   /api/menus/                       # Crear menú
GET    /api/menus/{id}/                  # Obtener menú específico
PUT    /api/menus/{id}/                  # Actualizar menú
DELETE /api/menus/{id}/                  # Eliminar menú

GET    /api/item-groups/                 # Listar grupos
POST   /api/item-groups/                 # Crear grupo
GET    /api/item-groups/{id}/            # Obtener grupo específico
PUT    /api/item-groups/{id}/            # Actualizar grupo
DELETE /api/item-groups/{id}/            # Eliminar grupo
GET    /api/item-groups/catalog_groups/  # Solo grupos de catálogo

GET    /api/item-categories/             # Listar categorías
POST   /api/item-categories/             # Crear categoría
GET    /api/item-categories/{id}/        # Obtener categoría específica
PUT    /api/item-categories/{id}/        # Actualizar categoría
DELETE /api/item-categories/{id}/        # Eliminar categoría
GET    /api/item-categories/catalog_categories/  # Solo categorías de catálogo

GET    /api/item-types/                  # Listar tipos
POST   /api/item-types/                  # Crear tipo
GET    /api/item-types/{id}/             # Obtener tipo específico
PUT    /api/item-types/{id}/             # Actualizar tipo
DELETE /api/item-types/{id}/             # Eliminar tipo

GET    /api/catalogs/                    # Listar catálogos
POST   /api/catalogs/                    # Crear catálogo
GET    /api/catalogs/{id}/               # Obtener catálogo específico
PUT    /api/catalogs/{id}/               # Actualizar catálogo
DELETE /api/catalogs/{id}/               # Eliminar catálogo
GET    /api/catalogs/visible/            # Solo catálogos visibles
GET    /api/catalogs/chef_recommendations/  # Solo recomendaciones del chef
GET    /api/catalogs/salsas/             # Solo catálogos de salsas
GET    /api/catalogs/pastas/             # Solo catálogos de pastas
GET    /api/catalogs/franchise_only_catalogs/ # Solo catálogos de franquicia (confirmados, activos, no eliminados)
POST   /api/catalogs/{id}/toggle_visibility/  # Alternar visibilidad

GET    /api/products/                    # Listar productos
POST   /api/products/                    # Crear producto
GET    /api/products/{id}/               # Obtener producto específico
PUT    /api/products/{id}/               # Actualizar producto
DELETE /api/products/{id}/               # Eliminar producto

GET    /api/packages/                    # Listar paquetes
POST   /api/packages/                    # Crear paquete
GET    /api/packages/{id}/               # Obtener paquete específico
PUT    /api/packages/{id}/               # Actualizar paquete
DELETE /api/packages/{id}/               # Eliminar paquete

GET    /api/package-types/               # Listar tipos de paquete
POST   /api/package-types/               # Crear tipo de paquete
GET    /api/package-types/{id}/          # Obtener tipo específico
PUT    /api/package-types/{id}/          # Actualizar tipo
DELETE /api/package-types/{id}/          # Eliminar tipo

GET    /api/transport-types/             # Listar tipos de transporte
POST   /api/transport-types/             # Crear tipo de transporte
GET    /api/transport-types/{id}/        # Obtener tipo específico
PUT    /api/transport-types/{id}/        # Actualizar tipo
DELETE /api/transport-types/{id}/        # Eliminar tipo

GET    /api/measure-units/               # Listar unidades de medida
POST   /api/measure-units/               # Crear unidad de medida
GET    /api/measure-units/{id}/          # Obtener unidad específica
PUT    /api/measure-units/{id}/          # Actualizar unidad
DELETE /api/measure-units/{id}/          # Eliminar unidad
```

#### **providers** - Gestión de Proveedores
```
GET    /api/providers/                   # Listar proveedores
POST   /api/providers/                   # Crear proveedor
GET    /api/providers/{id}/              # Obtener proveedor específico
PUT    /api/providers/{id}/              # Actualizar proveedor
DELETE /api/providers/{id}/              # Eliminar proveedor
GET    /api/providers/active/            # Solo proveedores activos

GET    /api/provider-types/              # Listar tipos de proveedor
POST   /api/provider-types/              # Crear tipo de proveedor
GET    /api/provider-types/{id}/         # Obtener tipo específico
PUT    /api/provider-types/{id}/         # Actualizar tipo
DELETE /api/provider-types/{id}/         # Eliminar tipo

GET    /api/regions/                     # Listar regiones
POST   /api/regions/                     # Crear región
GET    /api/regions/{id}/                # Obtener región específica
PUT    /api/regions/{id}/                # Actualizar región
DELETE /api/regions/{id}/                # Eliminar región

GET    /api/districts/                   # Listar distritos
POST   /api/districts/                   # Crear distrito
GET    /api/districts/{id}/              # Obtener distrito específico
PUT    /api/districts/{id}/              # Actualizar distrito
DELETE /api/districts/{id}/              # Eliminar distrito

GET    /api/banks/                       # Listar bancos
POST   /api/banks/                       # Crear banco
GET    /api/banks/{id}/                  # Obtener banco específico
PUT    /api/banks/{id}/                  # Actualizar banco
DELETE /api/banks/{id}/                  # Eliminar banco

GET    /api/bank-account-types/          # Listar tipos de cuenta bancaria
POST   /api/bank-account-types/          # Crear tipo de cuenta
GET    /api/bank-account-types/{id}/     # Obtener tipo específico
PUT    /api/bank-account-types/{id}/     # Actualizar tipo
DELETE /api/bank-account-types/{id}/     # Eliminar tipo
```

#### **pricing** - Gestión de Precios
```
GET    /api/prices/                      # Listar precios
POST   /api/prices/                      # Crear precio
GET    /api/prices/{id}/                 # Obtener precio específico
PUT    /api/prices/{id}/                 # Actualizar precio
DELETE /api/prices/{id}/                 # Eliminar precio

GET    /api/fiscal-directives/           # Listar directivas fiscales
POST   /api/fiscal-directives/           # Crear directiva fiscal
GET    /api/fiscal-directives/{id}/      # Obtener directiva específica
PUT    /api/fiscal-directives/{id}/      # Actualizar directiva
DELETE /api/fiscal-directives/{id}/      # Eliminar directiva

GET    /api/fiscal-directive-types/      # Listar tipos de directiva fiscal
POST   /api/fiscal-directive-types/      # Crear tipo de directiva
GET    /api/fiscal-directive-types/{id}/ # Obtener tipo específico
PUT    /api/fiscal-directive-types/{id}/ # Actualizar tipo
DELETE /api/fiscal-directive-types/{id}/ # Eliminar tipo

GET    /api/fiscal-formulas/             # Listar fórmulas fiscales
POST   /api/fiscal-formulas/             # Crear fórmula fiscal
GET    /api/fiscal-formulas/{id}/        # Obtener fórmula específica
PUT    /api/fiscal-formulas/{id}/        # Actualizar fórmula
DELETE /api/fiscal-formulas/{id}/        # Eliminar fórmula

GET    /api/price-fiscal-configurations/ # Listar configuraciones fiscales de precios
POST   /api/price-fiscal-configurations/ # Crear configuración
GET    /api/price-fiscal-configurations/{id}/  # Obtener configuración específica
PUT    /api/price-fiscal-configurations/{id}/  # Actualizar configuración
DELETE /api/price-fiscal-configurations/{id}/  # Eliminar configuración

GET    /api/fiscal-configuration-details/ # Listar detalles de configuración fiscal
POST   /api/fiscal-configuration-details/ # Crear detalle
GET    /api/fiscal-configuration-details/{id}/  # Obtener detalle específico
PUT    /api/fiscal-configuration-details/{id}/  # Actualizar detalle
DELETE /api/fiscal-configuration-details/{id}/  # Eliminar detalle
```

#### **documentation** - Gestión de Documentación
```
GET    /api/instructions/                # Listar instrucciones
POST   /api/instructions/                # Crear instrucción
GET    /api/instructions/{id}/           # Obtener instrucción específica
PUT    /api/instructions/{id}/           # Actualizar instrucción
DELETE /api/instructions/{id}/           # Eliminar instrucción
GET    /api/instructions/active/         # Solo instrucciones activas
GET    /api/instructions/confirmed/      # Solo instrucciones confirmadas

GET    /api/instruction-types/           # Listar tipos de instrucción
POST   /api/instruction-types/           # Crear tipo de instrucción
GET    /api/instruction-types/{id}/      # Obtener tipo específico
PUT    /api/instruction-types/{id}/      # Actualizar tipo
DELETE /api/instruction-types/{id}/      # Eliminar tipo
```

#### **sales** - Gestión de Ventas (Placeholder)
```
# Esta aplicación está preparada para futuras implementaciones
# Los endpoints se agregarán cuando se implemente la funcionalidad de ventas
```

### Endpoints de Información
```
GET    /api/                             # Información general de la API
GET    /api/health/                      # Estado de salud
GET    /api/info/                        # Información del sistema
```

### Endpoints de Autenticación
```
POST   /api-token-auth/                  # Obtener token de autenticación
GET    /api-auth/                        # Autenticación por sesión
```

### Filtros y Búsqueda
Todos los endpoints soportan:
- **Filtros**: `?field=value`
- **Búsqueda**: `?search=texto`
- **Ordenamiento**: `?ordering=field` o `?ordering=-field`
- **Paginación**: `?page=1`

### Endpoints de Filtros Personalizados

#### **Catálogos - Filtros Especializados**
```
GET    /api/catalogs/visible/                    # Solo catálogos visibles
GET    /api/catalogs/chef_recommendations/       # Solo recomendaciones del chef
GET    /api/catalogs/salsas/                     # Solo catálogos de salsas (categoría=2)
GET    /api/catalogs/pastas/                     # Solo catálogos de pastas (categoría=1)
GET    /api/catalogs/franchise_only_catalogs/    # Solo catálogos de franquicia
POST   /api/catalogs/{id}/toggle_visibility/     # Alternar visibilidad
```

#### **Criterios de Filtrado**
- **visible**: `is_visible=True`
- **chef_recommendations**: `chef_recommendation=True, is_visible=True, is_confirmed=True, is_deleted=null`
- **salsas**: `is_visible=True, is_confirmed=True, is_deleted=null, category_id=2`
- **pastas**: `is_visible=True, is_confirmed=True, is_deleted=null, category_id=1`
- **franchise_only_catalogs**: `is_confirmed=True, is_visible=True, is_deleted=null, menu__franchise_only=True`

#### **Otros Filtros Personalizados**
```
GET    /api/item-categories/catalog_categories/  # Solo categorías de catálogo
GET    /api/item-groups/catalog_groups/          # Solo grupos de catálogo
GET    /api/products/active/                     # Solo productos activos
GET    /api/materials/active/                    # Solo materiales activos
GET    /api/services/active/                     # Solo servicios activos
GET    /api/providers/active/                    # Solo proveedores activos
GET    /api/instructions/active/                 # Solo instrucciones activas
GET    /api/instructions/confirmed/              # Solo instrucciones confirmadas
```

### Ejemplos de Uso

#### Obtener catálogos con filtros
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/catalogs/?is_visible=true&search=pasta"
```

#### Obtener recomendaciones del chef
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/catalogs/chef_recommendations/"
```

#### Obtener catálogos de salsas
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/catalogs/salsas/"
```

#### Obtener catálogos de pastas
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/catalogs/pastas/"
```

#### Obtener catálogos de franquicia
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/catalogs/franchise_only_catalogs/"
```

#### Obtener solo categorías de catálogo
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/item-categories/catalog_categories/"
```

#### Obtener solo grupos de catálogo
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/item-groups/catalog_groups/"
```

#### Obtener productos activos
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/products/active/"
```

#### Obtener proveedores activos
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/providers/active/"
```

---

## 8. Autenticación y Permisos

### Tipos de Autenticación

#### 1. Autenticación por Token
```bash
# Obtener token
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}' \
     "http://localhost:8081/api-token-auth/"

# Usar token
curl -H "Authorization: Token tu_token_aqui" \
     "http://localhost:8081/api/catalogs/"
```

#### 2. Autenticación por Sesión
```bash
# Loguearse en el admin
# Ir a http://localhost:8081/admin/
# Luego acceder a la API desde el navegador
```

#### 3. Autenticación Básica
```bash
curl -u username:password \
     "http://localhost:8081/api/catalogs/"
```

### Permisos
- **IsAuthenticated**: Requiere autenticación para todos los endpoints
- **IsAuthenticatedOrReadOnly**: Permite lectura pública, escritura solo autenticada
- **IsAdminUser**: Solo usuarios administradores

### Crear Superusuario
```bash
docker-compose exec core python manage.py createsuperuser
```

---

## 9. Configuración de Docker

### Docker Compose (docker-compose.yml)
```yaml
version: '3.8'

services:
  api:
    container_name: core
    build: ./core
    command: sh -c "sleep 10s; python manage.py runserver 0.0.0.0:8000"
    ports:
      - "8081:8000"
    env_file:
      - ./.env
    volumes:
      - ./core:/usr/src/app/core
      - ./users:/usr/src/app/users
      - ./authz:/usr/src/app/authz
      - ./products:/usr/src/app/products
      - ./providers:/usr/src/app/providers
      - ./pricing:/usr/src/app/pricing
      - ./documentation:/usr/src/app/documentation
      - ./sales:/usr/src/app/sales
      - ./templates:/usr/src/app/templates
      - ./manage.py:/usr/src/app/manage.py
    networks:
      - sbm-network

networks:
  sbm-network:
    external: true
    name: sbm-db_sbm-network
```

### Dockerfile (core/Dockerfile)
```dockerfile
FROM python:3.9-slim

WORKDIR /usr/src/app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Entrypoint (entrypoint.sh)
```bash
#!/bin/sh 

echo "Starting Django application"

exec "$@"
```

### Comandos Docker

#### Iniciar servicios
```bash
docker-compose up -d
```

#### Ver logs
```bash
docker-compose logs
```

#### Ejecutar comandos en el contenedor
```bash
docker-compose exec core python manage.py shell
docker-compose exec core python manage.py createsuperuser
```

#### Reiniciar servicios
```bash
docker-compose restart
```

#### Detener servicios
```bash
docker-compose down
```

---

## 10. Despliegue

### Requisitos del Sistema
- Docker 20.10+
- Docker Compose 2.0+
- PostgreSQL 13+
- 2GB RAM mínimo
- 10GB espacio en disco

### Pasos de Despliegue

#### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd SBM-API
```

#### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con los valores correctos
```

#### 3. Construir y ejecutar
```bash
docker-compose up -d --build
```

#### 4. Crear superusuario
```bash
docker-compose exec core python manage.py createsuperuser
```

#### 5. Verificar funcionamiento
```bash
curl http://localhost:8081/api/health/
```

### Configuración de Producción

#### Variables de entorno para producción
```bash
DEBUG=0
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
CORS_ALLOWED_ORIGINS=https://tu-dominio.com
SECRET_KEY=tu-secret-key-seguro
```

#### Configuración de base de datos para producción
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'production_db',
        'USER': 'production_user',
        'PASSWORD': 'secure_password',
        'HOST': 'production_host',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=ditaly_pasta,sbm_business,public',
            'connect_timeout': 10,
        },
    }
}
```

---

## 11. Guías de Desarrollo

### Estructura de Desarrollo

#### Agregar un nuevo modelo en una aplicación existente
1. Definir el modelo en `app_name/models.py`
2. Crear el serializer en `app_name/serializers.py`
3. Crear el ViewSet en `app_name/views.py`
4. Registrar las URLs en `app_name/urls.py`
5. Configurar el admin en `app_name/admin.py`

### Convenciones de Código

#### Nombres de archivos
- Modelos: `models.py`
- Serializers: `serializers.py`
- Views: `views.py`
- URLs: `urls.py`
- Admin: `admin.py`

#### Nombres de clases
- Modelos: `PascalCase` (ej: `User`, `Product`)
- Serializers: `PascalCase + Serializer` (ej: `UserSerializer`)
- ViewSets: `PascalCase + ViewSet` (ej: `UserViewSet`)

#### Nombres de URLs
- Endpoints: `kebab-case` (ej: `/api/users/`)
- Acciones: `snake_case` (ej: `/api/users/active/`)

#### Organización por Dominio
- **users**: Todo lo relacionado con usuarios y tipos de usuario
- **authz**: Roles, permisos y restricciones
- **products**: Catálogos, productos, menús, grupos, categorías, tipos, paquetes, transporte, unidades de medida
- **providers**: Proveedores, tipos de proveedor, regiones, distritos, bancos
- **pricing**: Precios, directivas fiscales, fórmulas fiscales, configuraciones
- **documentation**: Instrucciones y tipos de instrucción
- **sales**: Placeholder para futuras implementaciones de ventas

---

## 12. Troubleshooting

### Problemas Comunes

#### Error de conexión a base de datos
```bash
# Verificar que PostgreSQL esté ejecutándose
docker ps | grep postgres

# Verificar variables de entorno
cat .env

# Probar conexión
docker-compose exec core python manage.py dbshell
```

#### Error de migraciones
```bash
# Verificar configuración de MIGRATION_MODULES
# Las migraciones están deshabilitadas por diseño
```

#### Error de permisos
```bash
# Verificar que el usuario tenga permisos en PostgreSQL
# Verificar configuración de search_path
```

#### Error de CORS
```bash
# Verificar CORS_ALLOWED_ORIGINS en settings.py
# Verificar configuración de CORS en el frontend
```

### Comandos de Diagnóstico

#### Verificar estado de servicios
```bash
docker-compose ps
docker-compose logs
```

#### Verificar conectividad de red
```bash
docker network ls
docker network inspect sbm-db_sbm-network
```

#### Verificar configuración de base de datos
```bash
docker-compose exec core python manage.py check
```

---

## 13. Referencias

### Documentación Oficial
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

### Recursos Adicionales
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/api-stability/)
- [REST API Design](https://restfulapi.net/)
- [PostgreSQL Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)

---

**Última actualización**: Enero 2025
**Versión**: 3.2.0
**Mantenido por**: Equipo de Desarrollo SBM-API 

### Cambios en la Versión 3.2.0
- ✅ Agregado campo `franchise_only` al modelo Menu
- ✅ Actualizado MenuSerializer para incluir el nuevo campo
- ✅ Actualizado MenuAdmin para mostrar y filtrar por `franchise_only`
- ✅ Creado endpoint `franchise_only_catalogs` para filtrar catálogos de franquicia
- ✅ Configuración de migraciones del sistema Django (auth, admin, contenttypes, sessions)
- ✅ Eliminación de endpoint redundante `selectall` para menús
- ✅ Actualización completa de documentación técnica
- ✅ Nuevos ejemplos de uso para endpoints de filtros personalizados

### Cambios en la Versión 3.1.0
- ✅ Limpieza completa de archivos duplicados
- ✅ Eliminación de Dockerfile duplicado (mantenido el de core/ con PostgreSQL)
- ✅ Eliminación de entrypoint.sh duplicado
- ✅ Eliminación de requirements.txt duplicado
- ✅ Eliminación de manage.py duplicado (mantenido el de raíz)
- ✅ Eliminación de templates duplicados
- ✅ Eliminación de db.sqlite3 duplicado
- ✅ Eliminación de flask-docker-compose.yml (no necesario)
- ✅ Corrección de configuración Docker Compose con volúmenes específicos
- ✅ Actualización de documentación técnica

### Cambios en la Versión 3.0.0
- ✅ Reorganización completa de aplicaciones Django
- ✅ Eliminación de la aplicación `store` (funcionalidad integrada en `products`)
- ✅ Aplicación `sales` convertida en placeholder para futuras implementaciones
- ✅ Actualización de modelos y endpoints según la nueva estructura
- ✅ Corrección de importaciones y referencias en todas las aplicaciones
- ✅ Actualización de documentación técnica completa
- ✅ Configuración de `verbose_name` en español para todas las aplicaciones

### Gestión de Migraciones

#### Estrategia de Migraciones
- **Aplicaciones de Negocio**: Las migraciones están deshabilitadas para usar Flyway
- **Aplicaciones del Sistema Django**: Las migraciones están habilitadas para crear tablas del sistema

#### Comando para Ejecutar Migraciones del Sistema
```bash
# Ejecutar migraciones solo para tablas del sistema Django
docker-compose exec api python manage.py migrate --run-syncdb
```

#### Tablas del Sistema Creadas
- `django_admin_log` - Logs del admin
- `django_content_type` - Tipos de contenido
- `django_session` - Sesiones de usuario
- `auth_group` - Grupos de usuarios
- `auth_group_permissions` - Permisos de grupos
- `auth_permission` - Permisos del sistema
- `auth_user` - Usuarios del sistema Django
- `auth_user_groups` - Grupos de usuarios
- `auth_user_user_permissions` - Permisos de usuarios