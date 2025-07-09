from rest_framework import serializers
from .models import SupportTicket, SupportCategory, SupportResponse, SupportAttachment


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SupportTicket
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    assigned_to_name = serializers.SerializerMethodField(help_text="Asignado a")
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    responses_count = serializers.SerializerMethodField(help_text="Número de Respuestas")
    attachments_count = serializers.SerializerMethodField(help_text="Número de Archivos")

    class Meta:
        model = SupportTicket
        fields = [
            'id', 'ticket_number', 'title', 'description', 'priority', 'status',
            'created_by', 'assigned_to', 'franchise', 'created_at', 'updated_at',
            'resolved_at', 'field_verbose_names', 'created_by_name', 'assigned_to_name',
            'franchise_name', 'responses_count', 'attachments_count'
        ]
        read_only_fields = ['id', 'ticket_number', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'created_by_name': 'Creado por',
            'assigned_to_name': 'Asignado a',
            'franchise_name': 'Franquicia',
            'responses_count': 'Número de Respuestas',
            'attachments_count': 'Número de Archivos'
        })
        return verbose_names

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_assigned_to_name(self, obj):
        return obj.assigned_to.get_full_name() if obj.assigned_to else None

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_responses_count(self, obj):
        return obj.responses.count()

    def get_attachments_count(self, obj):
        return obj.attachments.count()


class SupportCategorySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SupportCategory
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = SupportCategory
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at', 'field_verbose_names']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class SupportResponseSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SupportResponse
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")
    ticket_number = serializers.SerializerMethodField(help_text="Número de Ticket")

    class Meta:
        model = SupportResponse
        fields = [
            'id', 'ticket', 'content', 'is_internal', 'created_by', 'created_at',
            'updated_at', 'field_verbose_names', 'created_by_name', 'ticket_number'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'created_by_name': 'Creado por',
            'ticket_number': 'Número de Ticket'
        })
        return verbose_names

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_ticket_number(self, obj):
        return obj.ticket.ticket_number if obj.ticket else None


class SupportAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SupportAttachment
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    created_by_name = serializers.SerializerMethodField(help_text="Subido por")
    ticket_number = serializers.SerializerMethodField(help_text="Número de Ticket")

    class Meta:
        model = SupportAttachment
        fields = [
            'id', 'ticket', 'response', 'file_name', 'file_path', 'file_size',
            'mime_type', 'created_by', 'created_at', 'field_verbose_names',
            'created_by_name', 'ticket_number'
        ]
        read_only_fields = ['id', 'created_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'created_by_name': 'Subido por',
            'ticket_number': 'Número de Ticket'
        })
        return verbose_names

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_ticket_number(self, obj):
        return obj.ticket.ticket_number if obj.ticket else None 