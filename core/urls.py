"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_views
# from rest_framework.documentation import include_docs_urls
from . import views

urlpatterns = [
    # Vista principal
    path('', views.home, name='home'),
    
    # Vista raíz de la API
    path('api/', views.api_root, name='api-root'),
    
    # Endpoints de información de la API
    path('api/health/', views.health_check, name='health-check'),
    path('api/info/', views.api_info, name='api-info'),
    
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # Autenticación REST Framework
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', auth_views.obtain_auth_token),
    
    path('api/', include('users.urls')),
    path('api/', include('authz.urls')),
    path('api/', include('products.urls')),
    path('api/', include('providers.urls')),
    path('api/', include('pricing.urls')),
    path('api/', include('documentation.urls')),
    path('api/', include('sales.urls')),
    # path('docs/', include_docs_urls(title='SBM API Documentation')),
]
