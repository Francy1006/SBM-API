from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FranchiseStateViewSet, FranchiseViewSet

# Crear el router para los ViewSets
router = DefaultRouter()
router.register(r'franchise-states', FranchiseStateViewSet, basename='franchise-state')
router.register(r'franchises', FranchiseViewSet, basename='franchise')

app_name = 'franchise'

urlpatterns = [
    # Incluir todas las rutas del router
    path('', include(router.urls)),
] 