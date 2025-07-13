import uuid
from django.db import models
from django.contrib.auth.models import User as AuthUser


class UserProfile(models.Model):
    """
    Modelo para perfiles de usuario extendidos
    """
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('manager', 'Gerente'),
        ('employee', 'Empleado'),
        ('cashier', 'Cajero'),
        ('kitchen', 'Cocina'),
        ('delivery', 'Delivery'),
        ('customer', 'Cliente'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile', verbose_name="Usuario")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee', verbose_name="Rol")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    address = models.TextField(blank=True, verbose_name="Dirección")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    hire_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Contratación")
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salario")
    is_active = models.BooleanField(verbose_name="Activo")
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='user_profiles', verbose_name="Franquicia")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        db_table = 'user_profile'
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ['user__username']

    def __str__(self):
        if self.user:
            return f"{str(self.user)} - {self.role}"
        return f"Perfil de Usuario {self.pk}"


class UserPermission(models.Model):
    """
    Modelo para permisos específicos de usuario
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission_name = models.CharField(max_length=100, verbose_name="Nombre del Permiso")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(verbose_name="Activo")
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='custom_permissions', verbose_name="Usuario")
    created_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='created_user_permissions', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        db_table = 'user_permission'
        verbose_name = "Permiso de Usuario"
        verbose_name_plural = "Permisos de Usuario"
        unique_together = ['user', 'permission_name']
        ordering = ['user', 'permission_name']

    def __str__(self):
        username = getattr(self.user, 'username', str(self.user))
        return f"{username} - {self.permission_name}"


class UserSession(models.Model):
    """
    Modelo para sesiones de usuario
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_key = models.CharField(max_length=40, verbose_name="Clave de Sesión")
    ip_address = models.GenericIPAddressField(verbose_name="Dirección IP")
    user_agent = models.TextField(verbose_name="User Agent")
    login_time = models.DateTimeField(verbose_name="Hora de Inicio de Sesión")
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name="Hora de Cierre de Sesión")
    is_active = models.BooleanField(verbose_name="Sesión Activa")
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='sessions', verbose_name="Usuario")
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='user_sessions', verbose_name="Franquicia")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        db_table = 'user_session'
        verbose_name = "Sesión de Usuario"
        verbose_name_plural = "Sesiones de Usuario"
        ordering = ['-login_time']

    def __str__(self):
        username = getattr(self.user, 'username', str(self.user))
        return f"{username} - {self.login_time}"


class UserActivity(models.Model):
    """
    Modelo para actividades de usuario
    """
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Inicio de Sesión'),
        ('logout', 'Cierre de Sesión'),
        ('create', 'Crear'),
        ('update', 'Actualizar'),
        ('delete', 'Eliminar'),
        ('view', 'Ver'),
        ('export', 'Exportar'),
        ('import', 'Importar'),
        ('print', 'Imprimir'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, verbose_name="Tipo de Actividad")
    description = models.TextField(verbose_name="Descripción")
    ip_address = models.GenericIPAddressField(verbose_name="Dirección IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    activity_date = models.DateTimeField(verbose_name="Fecha de Actividad")
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='activities', verbose_name="Usuario")
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='user_activities', verbose_name="Franquicia")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        db_table = 'user_activity'
        verbose_name = "Actividad de Usuario"
        verbose_name_plural = "Actividades de Usuario"
        ordering = ['-activity_date']

    def __str__(self):
        username = getattr(self.user, 'username', str(self.user))
        return f"{username} - {self.activity_type} - {self.activity_date}"


class UserNotification(models.Model):
    """
    Modelo para notificaciones de usuario
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Información'),
        ('success', 'Éxito'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('alert', 'Alerta'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name="Título")
    message = models.TextField(verbose_name="Mensaje")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info', verbose_name="Tipo de Notificación")
    is_read = models.BooleanField(verbose_name="Leída")
    read_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Lectura")
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='notifications', verbose_name="Usuario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        db_table = 'user_notification'
        verbose_name = "Notificación de Usuario"
        verbose_name_plural = "Notificaciones de Usuario"
        ordering = ['-created_at']

    def __str__(self):
        username = getattr(self.user, 'username', str(self.user))
        return f"{username} - {self.title}"


# --- MODELO PROPIO DE USUARIO DEL NEGOCIO ---
class User(models.Model):
    """
    Modelo para usuarios del sistema (tabla sbm_business.user)
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código UUID")
    type = models.IntegerField(verbose_name="Tipo de Usuario")
    google_id = models.CharField(max_length=255, unique=True, verbose_name="Google ID")
    mail = models.EmailField(unique=True, verbose_name="Email")
    phone = models.BigIntegerField(verbose_name="Teléfono")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    last_name = models.CharField(max_length=255, verbose_name="Apellido")
    is_active = models.BooleanField(default=True, verbose_name="Activo")  # type: ignore
    is_deleted = models.BooleanField(default=False, verbose_name="Eliminado")  # type: ignore
    is_confirmed = models.BooleanField(default=False, verbose_name="Confirmado")  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado Por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")  # type: ignore

    class Meta:
        db_table = 'user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['name', 'last_name']

    def __str__(self):
        return f"{self.name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True


class UserToken(models.Model):
    """
    Modelo para tokens de usuario (tabla sbm_business.user_token)
    """
    id = models.CharField(max_length=36, primary_key=True, verbose_name="Token UUID")
    user_id = models.CharField(max_length=36, verbose_name="ID de Usuario")
    token = models.TextField(verbose_name="Token")
    ip_address = models.CharField(max_length=45, verbose_name="Dirección IP")
    user_agent = models.TextField(null=True, blank=True, verbose_name="User Agent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Expiración")
    revoked_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Revocación")

    class Meta:
        db_table = 'user_token'
        verbose_name = "Token de Usuario"
        verbose_name_plural = "Tokens de Usuario"
        ordering = ['-created_at']

    def __str__(self):
        return f"Token {self.id} - {self.user_id}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)
