from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def home(request):
    """
    Vista principal que muestra la documentación de la API
    """
    api_endpoints = {
        'Menús': {
            'description': 'Gestión de menús del sistema',
            'endpoints': [
                {'method': 'GET', 'url': '/api/menus/', 'description': 'Listar todos los menús'},
                {'method': 'POST', 'url': '/api/menus/', 'description': 'Crear un nuevo menú'},
                {'method': 'GET', 'url': '/api/menus/{id}/', 'description': 'Obtener un menú específico'},
                {'method': 'PUT', 'url': '/api/menus/{id}/', 'description': 'Actualizar un menú'},
                {'method': 'DELETE', 'url': '/api/menus/{id}/', 'description': 'Eliminar un menú'},
            ]
        },
        'Categorías de Items': {
            'description': 'Gestión de categorías de items con opción de renderizado en catálogo',
            'endpoints': [
                {'method': 'GET', 'url': '/api/item-categories/', 'description': 'Listar todas las categorías'},
                {'method': 'POST', 'url': '/api/item-categories/', 'description': 'Crear una nueva categoría'},
                {'method': 'GET', 'url': '/api/item-categories/{id}/', 'description': 'Obtener una categoría específica'},
                {'method': 'PUT', 'url': '/api/item-categories/{id}/', 'description': 'Actualizar una categoría'},
                {'method': 'DELETE', 'url': '/api/item-categories/{id}/', 'description': 'Eliminar una categoría'},
                {'method': 'GET', 'url': '/api/item-categories/catalog_categories/', 'description': 'Solo categorías para catálogo'},
                {'method': 'POST', 'url': '/api/item-categories/{id}/toggle_catalog_render/', 'description': 'Alternar renderizado en catálogo'},
            ]
        },
        'Tipos de Items': {
            'description': 'Gestión de tipos de items',
            'endpoints': [
                {'method': 'GET', 'url': '/api/item-types/', 'description': 'Listar todos los tipos'},
                {'method': 'POST', 'url': '/api/item-types/', 'description': 'Crear un nuevo tipo'},
                {'method': 'GET', 'url': '/api/item-types/{id}/', 'description': 'Obtener un tipo específico'},
                {'method': 'PUT', 'url': '/api/item-types/{id}/', 'description': 'Actualizar un tipo'},
                {'method': 'DELETE', 'url': '/api/item-types/{id}/', 'description': 'Eliminar un tipo'},
            ]
        },
        'Grupos de Items': {
            'description': 'Gestión de grupos de items con opción de renderizado en catálogo',
            'endpoints': [
                {'method': 'GET', 'url': '/api/item-groups/', 'description': 'Listar todos los grupos'},
                {'method': 'POST', 'url': '/api/item-groups/', 'description': 'Crear un nuevo grupo'},
                {'method': 'GET', 'url': '/api/item-groups/{id}/', 'description': 'Obtener un grupo específico'},
                {'method': 'PUT', 'url': '/api/item-groups/{id}/', 'description': 'Actualizar un grupo'},
                {'method': 'DELETE', 'url': '/api/item-groups/{id}/', 'description': 'Eliminar un grupo'},
                {'method': 'GET', 'url': '/api/item-groups/catalog_groups/', 'description': 'Solo grupos para catálogo'},
                {'method': 'POST', 'url': '/api/item-groups/{id}/toggle_catalog_render/', 'description': 'Alternar renderizado en catálogo'},
            ]
        },
        'Tipos de Instrucciones': {
            'description': 'Gestión de tipos de instrucciones',
            'endpoints': [
                {'method': 'GET', 'url': '/api/instruction-types/', 'description': 'Listar todos los tipos de instrucciones'},
                {'method': 'POST', 'url': '/api/instruction-types/', 'description': 'Crear un nuevo tipo de instrucción'},
                {'method': 'GET', 'url': '/api/instruction-types/{id}/', 'description': 'Obtener un tipo específico'},
                {'method': 'PUT', 'url': '/api/instruction-types/{id}/', 'description': 'Actualizar un tipo'},
                {'method': 'DELETE', 'url': '/api/instruction-types/{id}/', 'description': 'Eliminar un tipo'},
            ]
        },
        'Instrucciones': {
            'description': 'Gestión de instrucciones con control de estado y auditoría completa',
            'endpoints': [
                {'method': 'GET', 'url': '/api/instructions/', 'description': 'Listar todas las instrucciones activas'},
                {'method': 'POST', 'url': '/api/instructions/', 'description': 'Crear una nueva instrucción'},
                {'method': 'GET', 'url': '/api/instructions/{id}/', 'description': 'Obtener una instrucción específica'},
                {'method': 'PUT', 'url': '/api/instructions/{id}/', 'description': 'Actualizar una instrucción'},
                {'method': 'DELETE', 'url': '/api/instructions/{id}/', 'description': 'Eliminación lógica de instrucción'},
                {'method': 'GET', 'url': '/api/instructions/active/', 'description': 'Solo instrucciones activas'},
                {'method': 'GET', 'url': '/api/instructions/confirmed/', 'description': 'Solo instrucciones confirmadas'},
                {'method': 'POST', 'url': '/api/instructions/{id}/confirm/', 'description': 'Confirmar una instrucción'},
                {'method': 'POST', 'url': '/api/instructions/{id}/soft_delete/', 'description': 'Eliminación lógica'},
                {'method': 'POST', 'url': '/api/instructions/{id}/restore/', 'description': 'Restaurar instrucción eliminada'},
            ]
        }
    }
    
    context = {
        'title': 'SBM-API - Documentación',
        'description': 'API REST para gestión de datos del sistema',
        'version': '1.0.0',
        'base_url': 'http://localhost:8081',
        'admin_url': '/admin/',
        'api_endpoints': api_endpoints
    }
    
    return render(request, 'home.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Endpoint de verificación de salud de la API
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'SBM-API is running successfully',
        'version': '1.0.0'
    })


@csrf_exempt
@require_http_methods(["GET"])
def api_info(request):
    """
    Endpoint para obtener información general de la API
    """
    return JsonResponse({
        'name': 'SBM-API',
        'version': '1.0.0',
        'description': 'API REST para gestión de datos del sistema',
        'base_url': 'http://localhost:8081',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
            'admin': '/admin/',
            'documentation': '/'
        },
        'models': [
            'Menu',
            'ItemCategory', 
            'ItemType',
            'ItemGroup',
            'InstructionType',
            'Instruction'
        ]
    })


def api_root(request):
    """
    Vista raíz de la API que lista todos los endpoints disponibles
    """
    api_endpoints = {
        "item_groups": {
            "url": "/store/api/item-groups/",
            "methods": ["GET", "POST"],
            "description": "CRUD completo para grupos de items"
        },
        "item_categories": {
            "url": "/store/api/item-categories/",
            "methods": ["GET", "POST"],
            "description": "CRUD completo para categorías de items"
        },
        "item_types": {
            "url": "/store/api/item-types/",
            "methods": ["GET", "POST"],
            "description": "CRUD completo para tipos de items"
        },
        "menus": {
            "url": "/store/api/menus/",
            "methods": ["GET", "POST"],
            "description": "CRUD completo para menús del sistema"
        },
        "catalog_groups": {
            "url": "/store/api/item-groups/catalog_groups/",
            "methods": ["GET"],
            "description": "Solo grupos que se renderizan en catálogo"
        },
        "catalog_categories": {
            "url": "/store/api/item-categories/catalog_categories/",
            "methods": ["GET"],
            "description": "Solo categorías que se renderizan en catálogo"
        },
        "admin": {
            "url": "/admin/",
            "methods": ["GET"],
            "description": "Panel de administración de Django"
        },
        "auth": {
            "url": "/api-token-auth/",
            "methods": ["POST"],
            "description": "Autenticación por token"
        }
    }
    
    return JsonResponse(api_endpoints, json_dumps_params={'indent': 2}) 