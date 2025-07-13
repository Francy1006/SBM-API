from rest_framework import serializers
from .models import UserProfile, UserPermission, UserSession, UserActivity, UserNotification, User, UserToken


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


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User (sbm_business.user)
    """
    field_verbose_names = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField(help_text="Nombre Completo")

    class Meta:
        model = User
        fields = [
            'id', 'code', 'type', 'google_id', 'mail', 'phone', 'name', 'last_name',
            'is_active', 'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'deleted_by', 'log', 'version',
            'field_verbose_names', 'full_name'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'full_name': 'Nombre Completo'
        })
        return verbose_names

    def get_full_name(self, obj):
        return f"{obj.name} {obj.last_name}"


class UserTokenSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserToken (sbm_business.user_token)
    """
    field_verbose_names = serializers.SerializerMethodField()
    
    # Campos relacionados
    user_name = serializers.SerializerMethodField(help_text="Usuario")

    class Meta:
        model = UserToken
        fields = [
            'id', 'user_id', 'token', 'ip_address', 'user_agent',
            'created_at', 'expires_at', 'revoked_at',
            'field_verbose_names', 'user_name'
        ]
        read_only_fields = ['id', 'created_at']

    def get_field_verbose_names(self, obj):
        verbose_names = {field.name: field.verbose_name for field in obj._meta.fields}
        verbose_names.update({
            'user_name': 'Usuario'
        })
        return verbose_names

    def get_user_name(self, obj):
        return f"User {obj.user_id}" 