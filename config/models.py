import uuid
from django.db import models
from django.contrib.auth.models import User


class SystemConfig(models.Model):
    """
    Modelo para configuración del sistema
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100, unique=True, verbose_name="Clave")
    value = models.TextField(verbose_name="Valor")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")  # type: ignore
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_system_configs', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'system_config'
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.value}"


class FranchiseConfig(models.Model):
    """
    Modelo para configuración específica de franquicias
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100, verbose_name="Clave")
    value = models.TextField(verbose_name="Valor")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")  # type: ignore
    
    # Relaciones
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='configs', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_franchise_configs', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'franchise_config'
        verbose_name = "Configuración de Franquicia"
        verbose_name_plural = "Configuraciones de Franquicia"
        unique_together = ['franchise', 'key']
        ordering = ['franchise', 'key']

    def __str__(self):
        return f"{self.franchise.name} - {self.key}: {self.value}"


class NotificationTemplate(models.Model):
    """
    Modelo para plantillas de notificaciones
    """
    TEMPLATE_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'Notificación en App'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    template_type = models.CharField(max_length=10, choices=TEMPLATE_TYPE_CHOICES, default='email', verbose_name="Tipo de Plantilla")
    subject = models.CharField(max_length=200, blank=True, verbose_name="Asunto")
    content = models.TextField(verbose_name="Contenido")
    variables = models.JSONField(default=dict, blank=True, verbose_name="Variables")
    is_active = models.BooleanField(default=True, verbose_name="Activo")  # type: ignore
    
    # Campos de auditoría
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notification_templates', verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'notification_template'
        verbose_name = "Plantilla de Notificación"
        verbose_name_plural = "Plantillas de Notificación"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"  # type: ignore


class AuditLog(models.Model):
    """
    Modelo para registro de auditoría
    """
    ACTION_CHOICES = [
        ('create', 'Crear'),
        ('update', 'Actualizar'),
        ('delete', 'Eliminar'),
        ('login', 'Iniciar Sesión'),
        ('logout', 'Cerrar Sesión'),
        ('export', 'Exportar'),
        ('import', 'Importar'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Acción")
    model_name = models.CharField(max_length=100, verbose_name="Modelo")
    object_id = models.CharField(max_length=100, verbose_name="ID del Objeto")
    details = models.JSONField(default=dict, blank=True, verbose_name="Detalles")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    # Relaciones
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs', verbose_name="Usuario")
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, null=True, blank=True, related_name='audit_logs', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        db_table = 'audit_log'
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.model_name}"  # type: ignore



class Status(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    module = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'status'
        managed = False
        ordering = ["id"]

    def __str__(self):
        return f"{self.module} - {self.name}"


        