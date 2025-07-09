from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def home(request):
    """
    Vista principal que muestra la documentación de la API
    """
    context = {
        'title': 'SBM-API - Documentación',
        'description': 'API REST para gestión de datos del sistema',
        'version': '1.0.0',
        'base_url': 'http://localhost:8082',
        'admin_url': '/admin/',
        'api_endpoints': {
            'Información de la API': {
                'description': 'Endpoints de información del sistema',
                'endpoints': [
                    {'method': 'GET', 'url': '/api/health/', 'description': 'Verificar estado de la API'},
                    {'method': 'GET', 'url': '/api/info/', 'description': 'Información general de la API'},
                    {'method': 'GET', 'url': '/api/', 'description': 'Lista de endpoints disponibles'},
                ]
            },
            'Gestión de Franquicias': {
                'description': 'CRUD completo para franquicias y estados de franquicia',
                'endpoints': [
                    {'method': 'GET', 'url': '/api/franchise-states/', 'description': 'Listar estados de franquicia'},
                    {'method': 'POST', 'url': '/api/franchise-states/', 'description': 'Crear estado de franquicia'},
                    {'method': 'GET', 'url': '/api/franchise-states/{id}/', 'description': 'Obtener estado específico'},
                    {'method': 'PUT', 'url': '/api/franchise-states/{id}/', 'description': 'Actualizar estado'},
                    {'method': 'DELETE', 'url': '/api/franchise-states/{id}/', 'description': 'Eliminar estado'},
                    {'method': 'GET', 'url': '/api/franchises/', 'description': 'Listar franquicias'},
                    {'method': 'POST', 'url': '/api/franchises/', 'description': 'Crear franquicia'},
                    {'method': 'GET', 'url': '/api/franchises/{id}/', 'description': 'Obtener franquicia específica'},
                    {'method': 'PUT', 'url': '/api/franchises/{id}/', 'description': 'Actualizar franquicia'},
                    {'method': 'DELETE', 'url': '/api/franchises/{id}/', 'description': 'Eliminar franquicia'},
                    {'method': 'GET', 'url': '/api/franchises/by_state/', 'description': 'Filtrar por estado'},
                    {'method': 'POST', 'url': '/api/franchises/{id}/change_state/', 'description': 'Cambiar estado'},
                ]
            }
        }
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
        'base_url': 'http://localhost:8082',
        'endpoints': {
            'health': '/api/health/',
            'info': '/api/info/',
            'admin': '/admin/',
            'documentation': '/',
            'franchise_states': '/api/franchise-states/',
            'franchises': '/api/franchises/'
        }
    })


def api_root(request):
    """
    Vista raíz de la API que lista todos los endpoints disponibles
    """
    api_endpoints = {
        "health": {
            "url": "/api/health/",
            "methods": ["GET"],
            "description": "Verificar estado de salud de la API"
        },
        "info": {
            "url": "/api/info/",
            "methods": ["GET"],
            "description": "Información general de la API"
        },
        "franchise_states": {
            "url": "/api/franchise-states/",
            "methods": ["GET", "POST"],
            "description": "CRUD completo para estados de franquicia"
        },
        "franchises": {
            "url": "/api/franchises/",
            "methods": ["GET", "POST"],
            "description": "CRUD completo para franquicias"
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