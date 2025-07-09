from rest_framework import serializers
from .models import UserProfile, UserPermission, UserSession, UserActivity, UserNotification


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserProfile
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    user_name = serializers.SerializerMethodField(help_text="Usuario")
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'role', 'phone', 'address', 'birth_date', 'hire_date',
            'salary', 'is_active', 'franchise', 'created_at', 'updated_at',
            'field_verbose_names', 'user_name', 'franchise_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'user_name': 'Usuario',
            'franchise_name': 'Franquicia'
        })
        return verbose_names

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None


class UserPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserPermission
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    user_name = serializers.SerializerMethodField(help_text="Usuario")
    created_by_name = serializers.SerializerMethodField(help_text="Creado por")

    class Meta:
        model = UserPermission
        fields = [
            'id', 'permission_name', 'description', 'is_active', 'user',
            'created_by', 'created_at', 'updated_at', 'field_verbose_names',
            'user_name', 'created_by_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'user_name': 'Usuario',
            'created_by_name': 'Creado por'
        })
        return verbose_names

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class UserSessionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserSession
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    user_name = serializers.SerializerMethodField(help_text="Usuario")
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")

    class Meta:
        model = UserSession
        fields = [
            'id', 'session_key', 'ip_address', 'user_agent', 'login_time',
            'logout_time', 'is_active', 'user', 'franchise', 'created_at',
            'field_verbose_names', 'user_name', 'franchise_name'
        ]
        read_only_fields = ['id', 'created_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'user_name': 'Usuario',
            'franchise_name': 'Franquicia'
        })
        return verbose_names

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserActivity
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    user_name = serializers.SerializerMethodField(help_text="Usuario")
    franchise_name = serializers.SerializerMethodField(help_text="Franquicia")

    class Meta:
        model = UserActivity
        fields = [
            'id', 'activity_type', 'description', 'ip_address', 'user_agent',
            'activity_date', 'user', 'franchise', 'created_at',
            'field_verbose_names', 'user_name', 'franchise_name'
        ]
        read_only_fields = ['id', 'created_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'user_name': 'Usuario',
            'franchise_name': 'Franquicia'
        })
        return verbose_names

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

    def get_franchise_name(self, obj):
        return obj.franchise.name if obj.franchise else None


class UserNotificationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserNotification
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    user_name = serializers.SerializerMethodField(help_text="Usuario")

    class Meta:
        model = UserNotification
        fields = [
            'id', 'title', 'message', 'notification_type', 'is_read',
            'read_date', 'user', 'created_at', 'field_verbose_names', 'user_name'
        ]
        read_only_fields = ['id', 'created_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'user_name': 'Usuario'
        })
        return verbose_names

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None 