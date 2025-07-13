from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FranchiseStateViewSet, FranchiseViewSet, 
    FranchiseConfigurationTypeViewSet, FranchiseConfigurationViewSet, 
    FranchiseConfigurationDetailViewSet
)

# Crear el router para los ViewSets
router = DefaultRouter()
router.register(r'franchise-states', FranchiseStateViewSet, basename='franchise-state')
router.register(r'franchises', FranchiseViewSet, basename='franchise')
router.register(r'franchise-configuration-types', FranchiseConfigurationTypeViewSet, basename='franchise-configuration-type')
router.register(r'franchise-configurations', FranchiseConfigurationViewSet, basename='franchise-configuration')
router.register(r'franchise-configuration-details', FranchiseConfigurationDetailViewSet, basename='franchise-configuration-detail')

app_name = 'franchise'

urlpatterns = [
    # Incluir todas las rutas del router
    path('', include(router.urls)),
] 