from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SupportTicketViewSet, SupportCategoryViewSet,
    SupportResponseViewSet, SupportAttachmentViewSet
)

router = DefaultRouter()
router.register(r'tickets', SupportTicketViewSet)
router.register(r'categories', SupportCategoryViewSet)
router.register(r'responses', SupportResponseViewSet)
router.register(r'attachments', SupportAttachmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 