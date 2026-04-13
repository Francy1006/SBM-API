from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FranchiseStateViewSet, FranchiseViewSet, 
    FranchiseConfigurationTypeViewSet, FranchiseConfigurationViewSet, 
    FranchiseConfigurationDetailViewSet,
    FranchiseConfigurationView
)

router = DefaultRouter()
router.register(r'franchise-states', FranchiseStateViewSet, basename='franchise-state')
router.register(r'franchises', FranchiseViewSet, basename='franchise')
router.register(r'franchise-configuration-types', FranchiseConfigurationTypeViewSet, basename='franchise-configuration-type')
router.register(r'franchise-configurations', FranchiseConfigurationViewSet, basename='franchise-configuration')
router.register(r'franchise-configuration-details', FranchiseConfigurationDetailViewSet, basename='franchise-configuration-detail')

app_name = 'franchise'

urlpatterns = [
    path('franchise-configuration/raw/', FranchiseConfigurationView.as_view(), name='franchise-configuration-raw'),
    path('', include(router.urls)),
]