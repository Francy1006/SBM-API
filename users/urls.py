from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GoogleAuthView, UserViewSet, UserTokenViewSet, UserProfileViewSet, 
    UserPermissionViewSet, UserSessionViewSet, UserActivityViewSet, 
    UserNotificationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tokens', UserTokenViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'permissions', UserPermissionViewSet)
router.register(r'sessions', UserSessionViewSet)
router.register(r'activities', UserActivityViewSet)
router.register(r'notifications', UserNotificationViewSet)

urlpatterns = [
    path('auth/google/', GoogleAuthView.as_view(), name='google-auth'),
    path('', include(router.urls)),
] 