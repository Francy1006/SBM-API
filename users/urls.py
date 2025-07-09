from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import UserProfileViewSet, UserPermissionViewSet, UserSessionViewSet, UserActivityViewSet, UserNotificationViewSet

router = DefaultRouter()
# router.register(r'profiles', UserProfileViewSet)
# router.register(r'permissions', UserPermissionViewSet)
# router.register(r'sessions', UserSessionViewSet)
# router.register(r'activities', UserActivityViewSet)
# router.register(r'notifications', UserNotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 