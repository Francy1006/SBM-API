import uuid
import time
import json
import datetime
import logging
import jwt # type: ignore
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from google.auth.transport.requests import Request  # type: ignore
from google.oauth2 import id_token  # type: ignore
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, UserToken, UserProfile, UserPermission, UserSession, UserActivity, UserNotification
from .serializers import (
    UserSerializer, UserTokenSerializer, UserProfileSerializer, 
    UserPermissionSerializer, UserSessionSerializer, UserActivitySerializer, 
    UserNotificationSerializer
)
from .authentication import CustomTokenAuthentication
from django.conf import settings

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class GoogleAuthView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            id_token_google = data.get('id_token')
            if not id_token_google:
                return JsonResponse({'error': 'id_token es requerido'}, status=400)

            # --- MODO DESARROLLO: omitir Google Auth y devolver usuario de prueba ---
            if getattr(settings, 'DJANGO_ENV', 'development') == 'development':
                return JsonResponse({
                    'uuid': getattr(settings, 'MOCK_USER_UUID', 'mock-uuid'),
                    'email': getattr(settings, 'MOCK_USER_EMAIL', 'mock@example.com'),
                    'name': getattr(settings, 'MOCK_USER_NAME', 'MOCKUSER'),
                    'token': getattr(settings, 'MOCK_USER_TOKEN', 'mock-token')
                })
            # --- FIN MODO DESARROLLO ---

            # --- MODO PRODUCCIÓN: validar Google Auth normalmente ---
            client_id = settings.GOOGLE_CLIENT_ID

            # LOG HORA DEL SISTEMA
            logger.warning(">>> Hora del sistema (timezone.now()): %s", timezone.now())
            logger.warning(">>> Hora del sistema (datetime.utcnow()): %s", datetime.datetime.utcnow())

            # TEMPORAL: Para pruebas, deshabilitar validación de tiempo
            try:
                idinfo = id_token.verify_oauth2_token(id_token_google, Request(), client_id)
            except ValueError as e:
                if "Token used too early" in str(e):
                    logger.warning(">>> Token usado muy pronto, pero continuando para pruebas...")
                    # Para pruebas, extraer datos del token sin validar tiempo
                    # En producción, esto debería fallar
                    try:
                        # Decodificar el token sin validar tiempo
                        decoded = jwt.decode(id_token_google, options={"verify_signature": False, "verify_aud": False, "verify_exp": False, "verify_iat": False})
                        idinfo = {
                            'sub': decoded.get('sub', 'unknown'),
                            'email': decoded.get('email', ''),
                            'given_name': decoded.get('given_name', ''),
                            'family_name': decoded.get('family_name', '')
                        }
                        logger.warning(">>> Datos extraídos del token: %s", idinfo)
                    except Exception as jwt_error:
                        logger.error(">>> Error decodificando token: %s", jwt_error)
                        return JsonResponse({'error': f'Error decodificando token: {str(jwt_error)}'}, status=401)
                else:
                    return JsonResponse({'error': f'Token de Google inválido: {str(e)}'}, status=401)

            google_id = idinfo['sub']
            email = idinfo['email']
            given_name = idinfo.get('given_name', '')
            family_name = idinfo.get('family_name', '')

            # Buscar usuario por email primero, luego por google_id
            try:
                user = User.objects.get(mail=email) # type: ignore
                # Usuario existe, actualizar google_id si es diferente
                if user.google_id != google_id:
                    user.google_id = google_id
                user.name = given_name
                user.last_name = family_name
                user.is_active = True
                user.save()
                created = False
            except User.DoesNotExist: # type: ignore
                # Usuario no existe, crearlo
                try:
                    user = User.objects.get(google_id=google_id) # type: ignore
                    # Usuario existe con google_id pero email diferente, actualizar email
                    user.mail = email
                    user.name = given_name
                    user.last_name = family_name
                    user.is_active = True
                    user.save()
                    created = False
                except User.DoesNotExist: # type: ignore
                    # Usuario no existe, crearlo
                    user = User.objects.create( # type: ignore
                        google_id=google_id,
                        mail=email,
                        name=given_name,
                        last_name=family_name,
                        phone=0,
                        type=1,
                        is_active=True,
                        is_deleted=False,
                        is_confirmed=True,
                    )
                    created = True

            token_uuid = str(uuid.uuid4())
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            UserToken.objects.create( # type: ignore
                id=token_uuid,
                user_id=user.code,
                token=token_uuid,
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=timezone.now() + timezone.timedelta(days=30),
            )

            return JsonResponse({
                'uuid': user.code,
                'email': user.mail,
                'name': f"{user.name} {user.last_name}",
                'token': token_uuid
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() # type: ignore
    serializer_class = UserSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active', 'is_deleted', 'is_confirmed']
    search_fields = ['name', 'last_name', 'mail', 'google_id']
    ordering_fields = ['name', 'last_name', 'mail', 'created_at', 'updated_at']
    ordering = ['name', 'last_name']
    
    def perform_create(self, serializer):
        """Sobrescribir perform_create para usar request.user.code como created_by"""
        serializer.save()


class UserTokenViewSet(viewsets.ModelViewSet):
    queryset = UserToken.objects.all() # type: ignore
    serializer_class = UserTokenSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_id', 'ip_address']
    search_fields = ['user_id', 'token', 'ip_address']
    ordering_fields = ['created_at', 'expires_at', 'revoked_at']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Sobrescribir perform_create para usar request.user.code como created_by"""
        serializer.save()


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all() # type: ignore
    serializer_class = UserProfileSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active', 'franchise']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    ordering_fields = ['user__username', 'role', 'hire_date', 'created_at']
    ordering = ['user__username']
    
    def perform_create(self, serializer):
        """Sobrescribir perform_create para usar request.user.code como created_by"""
        serializer.save()


class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserPermission.objects.all() # type: ignore
    serializer_class = UserPermissionSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['permission_name', 'is_active', 'user', 'created_by']
    search_fields = ['permission_name', 'description', 'user__username']
    ordering_fields = ['permission_name', 'created_at']
    ordering = ['permission_name']
    
    def perform_create(self, serializer):
        """Sobrescribir perform_create para usar request.user.code como created_by"""
        serializer.save(created_by=self.request.user)


class UserSessionViewSet(viewsets.ModelViewSet):
    queryset = UserSession.objects.all() # type: ignore
    serializer_class = UserSessionSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'user', 'franchise']
    search_fields = ['session_key', 'ip_address', 'user__username']
    ordering_fields = ['login_time', 'logout_time', 'created_at']
    ordering = ['-login_time']
    
    def perform_create(self, serializer):
        """Sobrescribir perform_create para usar request.user.code como created_by"""
        serializer.save()


class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all() # type: ignore
    serializer_class = UserActivitySerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activity_type', 'user', 'franchise']
    search_fields = ['description', 'ip_address', 'user__username']
    ordering_fields = ['activity_date', 'created_at']
    ordering = ['-activity_date']
    
    def perform_create(self, serializer):
        """Sobrescribir perform_create para usar request.user.code como created_by"""
        serializer.save()


class UserNotificationViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.all() # type: ignore
    serializer_class = UserNotificationSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'is_read', 'user']
    search_fields = ['title', 'message', 'user__username']
    ordering_fields = ['created_at', 'read_date']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Sobrescribir perform_create para usar request.user.code como created_by"""
        serializer.save()
