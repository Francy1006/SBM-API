from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemConfigViewSet, FranchiseConfigViewSet,
    NotificationTemplateViewSet, AuditLogViewSet,
    StatusByModuleView
)

router = DefaultRouter()
router.register(r'system', SystemConfigViewSet)
router.register(r'franchise', FranchiseConfigViewSet)
router.register(r'templates', NotificationTemplateViewSet)
router.register(r'audit', AuditLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('status/<str:module>/', StatusByModuleView.as_view(), name='status-by-module'),
]