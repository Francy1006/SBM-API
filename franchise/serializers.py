from rest_framework import serializers
from .models import FranchiseState, Franchise


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


