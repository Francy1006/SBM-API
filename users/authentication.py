from rest_framework import authentication
from rest_framework import exceptions
from django.utils import timezone
from django.utils.timezone import make_aware, is_naive
from .models import UserToken, User


class CustomTokenAuthentication(authentication.BaseAuthentication):
    """
    Autenticación personalizada usando tokens UUID del modelo UserToken
    """
    
    def authenticate(self, request):
        # Obtener el token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return None
        
        # Extraer el token (remover 'Bearer ' del inicio)
        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else None
        
        if not token:
            return None
        
        try:
            # Buscar el token en la base de datos
            user_token = UserToken.objects.get( # type: ignore
                token=token,
                revoked_at__isnull=True  # Token no está revocado
            )
            
            # Verificar que el token no haya expirado
            now = timezone.now()
            expires_at = user_token.expires_at
            if is_naive(expires_at):
                expires_at = make_aware(expires_at, timezone.get_current_timezone())
            if expires_at <= now:
                raise exceptions.AuthenticationFailed('Token expirado')
            
            # Obtener el usuario asociado
            user = User.objects.get(code=user_token.user_id) # type: ignore
            
            return (user, user_token)
            
        except UserToken.DoesNotExist: # type: ignore
            raise exceptions.AuthenticationFailed('Token inválido o expirado')
        except User.DoesNotExist: # type: ignore
            raise exceptions.AuthenticationFailed('Usuario no encontrado')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Error de autenticación: {str(e)}')
    
    def authenticate_header(self, request):
        return 'Bearer realm="api"' 