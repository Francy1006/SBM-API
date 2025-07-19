from rest_framework import serializers
from .models import FranchiseState, Franchise, FranchiseConfigurationType, FranchiseConfiguration, FranchiseConfigurationDetail


class FranchiseStateSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FranchiseState
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FranchiseState
        fields = ['id', 'state', 'description', 'field_verbose_names']
        read_only_fields = ['id']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FranchiseSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Franchise
    """
    state_name = serializers.CharField(source='state.state', read_only=True)
    field_verbose_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Franchise
        fields = ['id', 'code', 'franchise', 'description', 'state', 'state_name', 'field_verbose_names']
        read_only_fields = ['id', 'code']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FranchiseDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detallado para el modelo Franchise con información del estado
    """
    state = FranchiseStateSerializer(read_only=True)
    
    class Meta:
        model = Franchise
        fields = ['id', 'code', 'franchise', 'description', 'state']
        read_only_fields = ['id', 'code'] 


class FranchiseConfigurationTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FranchiseConfigurationType
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FranchiseConfigurationType
        fields = ['id', 'configuration_type', 'description', 'field_verbose_names']
        read_only_fields = ['id']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FranchiseConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FranchiseConfiguration
    """
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FranchiseConfiguration
        fields = [
            'id', 'code', 'configuration', 'franchise', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by', 'field_verbose_names'
        ]
        read_only_fields = ['id', 'code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'created_by']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


class FranchiseConfigurationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo FranchiseConfigurationDetail
    """
    type_name = serializers.CharField(source='type.configuration_type', read_only=True)
    field_verbose_names = serializers.SerializerMethodField()

    class Meta:
        model = FranchiseConfigurationDetail
        fields = [
            'id', 'code', 'detail', 'description', 'type', 'type_name', 'configuration',
            'index', 'var', 'value', 'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by', 'updated_by',
            'deleted_by', 'field_verbose_names'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'created_by']

    def get_field_verbose_names(self, obj):
        return {field.name: field.verbose_name for field in obj._meta.fields}


