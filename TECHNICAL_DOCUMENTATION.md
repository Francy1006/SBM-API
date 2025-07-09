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
5. [Aplicación Core](#aplicación-core)
6. [API Endpoints](#api-endpoints)
7. [Autenticación y Permisos](#autenticación-y-permisos)
8. [Configuración de Docker](#configuración-de-docker)
9. [Despliegue](#despliegue)
10. [Guías de Desarrollo](#guías-de-desarrollo)
11. [Troubleshooting](#troubleshooting)
12. [Referencias](#referencias)

---

## 1. Descripción General

**SBM-API** es una API REST desarrollada en Django que proporciona servicios básicos del sistema. La API está diseñada para ser consumida por aplicaciones frontend y otros servicios.

### Características Principales
- ✅ API REST completa con Django REST Framework
- ✅ Autenticación por token y sesión
- ✅ Base de datos PostgreSQL con múltiples esquemas
- ✅ Documentación automática con Django Jazzmin
- ✅ Configuración Docker completa
- ✅ Endpoints de información y salud del sistema

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

---

## 4. Base de Datos

### Configuración PostgreSQL
- **Motor**: PostgreSQL 13+
- **Esquemas**: `ditaly_pasta`, `sbm_business`, `public`
- **Conexión**: Configurada para Docker con red externa

### Tablas del Sistema Django
- `django_admin_log` - Logs del admin
- `django_content_type` - Tipos de contenido
- `django_session` - Sesiones de usuario
- `auth_group` - Grupos de usuarios
- `auth_group_permissions` - Permisos de grupos
- `auth_permission` - Permisos del sistema
- `auth_user` - Usuarios del sistema Django
- `auth_user_groups` - Grupos de usuarios
- `auth_user_user_permissions` - Permisos de usuarios

---

## 5. Aplicación Core

### Funcionalidades Principales
- **Gestión de configuración**: Configuración centralizada del proyecto
- **URLs principales**: Enrutamiento de endpoints básicos
- **Vistas del sistema**: Endpoints de información y salud
- **Admin personalizado**: Interfaz de administración con Jazzmin

### Archivos Principales
- `settings.py`: Configuración completa del proyecto
- `urls.py`: Enrutamiento de URLs principales
- `views.py`: Vistas y endpoints del sistema
- `wsgi.py`: Configuración WSGI para producción
- `asgi.py`: Configuración ASGI para async

---

## 6. API Endpoints

### Endpoints Disponibles

#### Información del Sistema
```
GET    /api/health/              # Verificar estado de salud de la API
GET    /api/info/                # Información general de la API
GET    /api/                     # Lista de endpoints disponibles
```

#### Autenticación
```
POST   /api-token-auth/          # Autenticación por token
GET    /api-auth/                # Autenticación REST Framework
```

#### Administración
```
GET    /admin/                   # Panel de administración Django
```

#### Documentación
```
GET    /                         # Página principal con documentación
```

### Ejemplos de Uso

#### Verificar estado de la API
```bash
curl http://localhost:8082/api/health/
```

**Respuesta:**
```json
{
    "status": "healthy",
    "message": "SBM-API is running successfully",
    "version": "1.0.0"
}
```

#### Obtener información de la API
```bash
curl http://localhost:8082/api/info/
```

**Respuesta:**
```json
{
    "name": "SBM-API",
    "version": "1.0.0",
    "description": "API REST para gestión de datos del sistema",
    "base_url": "http://localhost:8082",
    "endpoints": {
        "health": "/api/health/",
        "info": "/api/info/",
        "admin": "/admin/",
        "documentation": "/"
    }
}
```

---

## 7. Autenticación y Permisos

### Tipos de Autenticación
- **Token Authentication**: Para APIs y servicios
- **Session Authentication**: Para el admin de Django
- **Basic Authentication**: Para desarrollo y testing

### Configuración de Permisos
- **Admin**: Acceso completo al panel de administración
- **API**: Autenticación requerida para endpoints protegidos
- **Documentación**: Acceso público a endpoints de información

---

## 8. Configuración de Docker

### Docker Compose
```yaml
version: '3.8'

services:
  api:
    container_name: sbm-core
    build: ./core
    command: sh -c "sleep 10s; python manage.py runserver 0.0.0.0:8000"
    ports:
      - "8082:8000"
    env_file:
      - ./.env
    volumes:
      - ./core:/usr/src/app/core
      - ./templates:/usr/src/app/templates
      - ./manage.py:/usr/src/app/manage.py
    networks:
      - sbm-network

networks:
  sbm-network:
    external: true
    name: sbm-db_sbm-network
```

### Comandos Docker
```bash
# Construir y levantar
docker-compose up -d --build

# Ver logs
docker-compose logs api

# Ejecutar comandos Django
docker-compose exec api python manage.py check
docker-compose exec api python manage.py createsuperuser

# Detener servicios
docker-compose down
```

---

## 9. Despliegue

### Requisitos del Sistema
- Docker y Docker Compose
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
docker-compose exec api python manage.py createsuperuser
```

#### 5. Verificar funcionamiento
```bash
curl http://localhost:8082/api/health/
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

## 10. Guías de Desarrollo

### Estructura de Desarrollo

#### Agregar nuevas funcionalidades
1. Crear nuevas vistas en `core/views.py`
2. Agregar URLs en `core/urls.py`
3. Configurar serializers si es necesario
4. Actualizar documentación

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

---

## 11. Troubleshooting

### Problemas Comunes

#### Error de conexión a base de datos
```bash
# Verificar que PostgreSQL esté ejecutándose
docker ps | grep postgres

# Verificar variables de entorno
cat .env

# Probar conexión
docker-compose exec api python manage.py dbshell
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
docker-compose exec api python manage.py check
```

---

## 12. Referencias

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
**Versión**: 4.0.0
**Mantenido por**: Equipo de Desarrollo SBM-API 

### Cambios en la Versión 4.0.0
- ✅ Limpieza completa del proyecto - solo aplicación core
- ✅ Eliminación de todas las aplicaciones de negocio
- ✅ Simplificación de endpoints y configuración
- ✅ Actualización de documentación técnica
- ✅ Configuración Docker optimizada
- ✅ Endpoints básicos de información y salud del sistema

### Gestión de Migraciones

#### Estrategia de Migraciones
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