from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import FranchiseState, Franchise, FranchiseConfigurationType, FranchiseConfiguration, FranchiseConfigurationDetail
from .serializers import (
    FranchiseStateSerializer, 
    FranchiseSerializer, 
    FranchiseDetailSerializer,
    FranchiseConfigurationTypeSerializer,
    FranchiseConfigurationSerializer,
    FranchiseConfigurationDetailSerializer
)
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# Create your views here.

class FranchiseStateViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FranchiseState
    Proporciona operaciones CRUD completas para los estados de franquicia
    """
    queryset = FranchiseState.objects.all()# type: ignore
    serializer_class = FranchiseStateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['state']
    search_fields = ['state', 'description']
    ordering_fields = ['id', 'state']
    ordering = ['state']

    def get_serializer_class(self):
        return FranchiseStateSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo estados activos
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FranchiseViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Franchise
    Proporciona operaciones CRUD completas para las franquicias
    """
    queryset = Franchise.objects.select_related('state').all()# type: ignore
    serializer_class = FranchiseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['state', 'franchise']
    search_fields = ['franchise', 'description', 'code']
    ordering_fields = ['id', 'franchise', 'code', 'state']
    ordering = ['-id']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FranchiseDetailSerializer
        return FranchiseSerializer

    def create(self, request, *args, **kwargs):
        """
        Crear una nueva franquicia
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Actualizar una franquicia existente
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo franquicias activas
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_state(self, request):
        """
        Endpoint para filtrar franquicias por estado
        """
        state_id = request.query_params.get('state_id')
        if state_id:
            queryset = self.get_queryset().filter(state_id=state_id)
        else:
            queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_state(self, request, pk=None):
        """
        Endpoint para cambiar el estado de una franquicia
        """
        franchise = self.get_object()
        new_state_id = request.data.get('state_id')
        
        if not new_state_id:
            return Response(
                {'error': 'state_id es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_state = FranchiseState.objects.get(id=new_state_id)
            franchise.state = new_state
            franchise.save()
            serializer = self.get_serializer(franchise)
            return Response(serializer.data)
        except FranchiseState.DoesNotExist:
            return Response(
                {'error': 'Estado no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def soft_delete(self, request):
        """
        Endpoint para hacer soft delete de una franquicia por código
        Cambia el estado a 2 (desactivado)
        """
        code = request.data.get('code')
        
        if not code:
            return Response(
                {'error': 'code es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            franchise = Franchise.objects.get(code=code)  # type: ignore
            # Cambiar estado a 2 (desactivado)
            franchise.state_id = 2
            franchise.save()
            serializer = self.get_serializer(franchise)
            return Response(
                {
                    'message': 'Franquicia desactivada exitosamente',
                    'franchise': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Franchise.DoesNotExist:  # type: ignore
            return Response(
                {'error': 'Franquicia no encontrada con el código proporcionado'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class FranchiseConfigurationTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FranchiseConfigurationType
    """
    queryset = FranchiseConfigurationType.objects.all()  # type: ignore
    serializer_class = FranchiseConfigurationTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['configuration_type']
    search_fields = ['configuration_type', 'description']
    ordering_fields = ['id', 'configuration_type']
    ordering = ['configuration_type']


class FranchiseConfigurationViewSet(viewsets.ModelViewSet):
    queryset = FranchiseConfiguration.objects.all()  # type: ignore
    serializer_class = FranchiseConfigurationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['franchise', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'configuration']
    ordering_fields = ['id', 'code', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')

    @action(detail=False, methods=['get'])
    def active(self, request):
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_franchise(self, request):
        franchise_code = request.query_params.get('franchise_code')
        if franchise_code:
            queryset = self.get_queryset().filter(franchise=franchise_code)
        else:
            queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_franchise_code(self, request):
        franchise_code = request.query_params.get('franchise_code')
        type_id = request.query_params.get('type')
        
        if not franchise_code:
            return Response({'error': 'franchise_code es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not type_id:
            return Response({'error': 'type es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            franchise=franchise_code
        ).filter(
            models.Q(is_deleted=False) | models.Q(is_deleted__isnull=True)
        ).filter(
            models.Q(is_confirmed=True) | models.Q(is_confirmed__isnull=True)
        )
        
        config_codes = FranchiseConfigurationDetail.objects.filter(
            type_id=type_id,
            configuration__in=queryset.values_list('code', flat=True)
        ).values_list('configuration', flat=True).distinct()
        
        queryset = queryset.filter(code__in=config_codes)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FranchiseConfigurationView(APIView):
    """
    Endpoint que retorna detail, description, var y value de franchise_configuration_detail para una franquicia dada y type=2.
    """
    def get(self, request):
        franchise = request.query_params.get('franchise')
        if not franchise:
            return Response({'error': 'El parámetro franchise es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT fcd.detail, fcd.description, fcd.var, fcd.value
                FROM sbm_business.franchise f
                LEFT JOIN ditaly_pasta.franchise_configuration fc
                  ON f.code = fc.franchise
                LEFT JOIN ditaly_pasta.franchise_configuration_detail fcd
                  ON fc.code = fcd.configuration
                WHERE f.code = %s AND fcd.type = 2
            ''', [franchise])
            results = cursor.fetchall()
        data = [
            {'detail': row[0], 'description': row[1], 'var': row[2], 'value': row[3]} for row in results
        ]
        return Response(data)


class FranchiseConfigurationDetailViewSet(viewsets.ModelViewSet):
    queryset = FranchiseConfigurationDetail.objects.select_related('type').all()  # type: ignore
    serializer_class = FranchiseConfigurationDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'configuration', 'index', 'is_deleted', 'is_confirmed']
    search_fields = ['code', 'detail', 'var', 'description', 'type__configuration_type']
    ordering_fields = ['id', 'code', 'detail', 'index', 'created_at', 'updated_at']
    ordering = ['configuration', 'type', 'index', 'detail']

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')

    @action(detail=False, methods=['get'])
    def active(self, request):
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_configuration(self, request):
        configuration_code = request.query_params.get('configuration_code')
        if configuration_code:
            queryset = self.get_queryset().filter(configuration=configuration_code)
        else:
            queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        type_id = request.query_params.get('type_id')
        if type_id:
            queryset = self.get_queryset().filter(type_id=type_id)
        else:
            queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)