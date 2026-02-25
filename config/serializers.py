from rest_framework import serializers
from .models import (
    SystemConfig,
    FranchiseConfig,
    NotificationTemplate,
    AuditLog,
    Status,
)


class SystemConfigSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SystemConfig
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = SystemConfig
        fields = [
            "id",
            "key",
            "value",
            "description",
            "is_active",
            "created_by",
            "created_at",
            "updated_at",
            "field_verbose_names",
            "created_by_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({"created_by_name": "Creado por"})
        return verbose_names

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class FranchiseConfigSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FranchiseConfig
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = FranchiseConfig
        fields = [
            "id",
            "key",
            "value",
            "description",
            "is_active",
            "franchise",
            "created_by",
            "created_at",
            "updated_at",
            "field_verbose_names",
            "franchise_name",
            "created_by_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update(
            {"franchise_name": "Franquicia", "created_by_name": "Creado por"}
        )
        return verbose_names

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo NotificationTemplate
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = NotificationTemplate
        fields = [
            "id",
            "name",
            "template_type",
            "subject",
            "content",
            "variables",
            "is_active",
            "created_by",
            "created_at",
            "updated_at",
            "field_verbose_names",
            "created_by_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({"created_by_name": "Creado por"})
        return verbose_names

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class AuditLogSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo AuditLog
    """

    field_verbose_names = serializers.SerializerMethodField()

    # Campos relacionados
    user_name = serializers.SerializerMethodField(help_text="Usuario")
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "action",
            "model_name",
            "object_id",
            "details",
            "ip_address",
            "user_agent",
            "user",
            "franchise",
            "created_at",
            "field_verbose_names",
            "user_name",
            "franchise_name",
        ]
        read_only_fields = ["id", "created_at"]

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({"user_name": "Usuario", "franchise_name": "Franquicia"})
        return verbose_names

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
