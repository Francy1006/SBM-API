import uuid
from django.db import models
from django.contrib.auth.models import User


class SupportTicket(models.Model):
    """
    Modelo para tickets de soporte
    """
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Abierto'),
        ('in_progress', 'En Progreso'),
        ('waiting', 'Esperando Respuesta'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_number = models.CharField(max_length=20, unique=True, verbose_name="Número de Ticket")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioridad")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open', verbose_name="Estado")
    
    # Relaciones
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets', verbose_name="Creado por")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets', verbose_name="Asignado a")
    franchise = models.ForeignKey('franchise.Franchise', on_delete=models.CASCADE, related_name='support_tickets', verbose_name="Franquicia")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Resolución")
    
    class Meta:
        db_table = 'support_ticket'
        verbose_name = "Ticket de Soporte"
        verbose_name_plural = "Tickets de Soporte"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.ticket_number} - {self.title}"


class SupportCategory(models.Model):
    """
    Modelo para categorías de soporte
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")  # type: ignore
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'support_category'
        verbose_name = "Categoría de Soporte"
        verbose_name_plural = "Categorías de Soporte"
        ordering = ['name']

    def __str__(self):
        return self.name


class SupportResponse(models.Model):
    """
    Modelo para respuestas a tickets de soporte
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses', verbose_name="Ticket")
    content = models.TextField(verbose_name="Contenido")
    is_internal = models.BooleanField(default=False, verbose_name="Nota Interna")  # type: ignore
    
    # Relaciones
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_responses', verbose_name="Creado por")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        db_table = 'support_response'
        verbose_name = "Respuesta de Soporte"
        verbose_name_plural = "Respuestas de Soporte"
        ordering = ['created_at']

    def __str__(self):
        return f"Respuesta a {self.ticket.ticket_number}"  # type: ignore


class SupportAttachment(models.Model):
    """
    Modelo para archivos adjuntos de soporte
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='attachments', verbose_name="Ticket")
    response = models.ForeignKey(SupportResponse, on_delete=models.CASCADE, null=True, blank=True, related_name='attachments', verbose_name="Respuesta")
    file_name = models.CharField(max_length=255, verbose_name="Nombre del Archivo")
    file_path = models.CharField(max_length=500, verbose_name="Ruta del Archivo")
    file_size = models.IntegerField(verbose_name="Tamaño del Archivo (bytes)")
    mime_type = models.CharField(max_length=100, verbose_name="Tipo MIME")
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_attachments', verbose_name="Subido por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Subida")
    
    class Meta:
        db_table = 'support_attachment'
        verbose_name = "Archivo Adjunto"
        verbose_name_plural = "Archivos Adjuntos"
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name
