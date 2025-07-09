from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import FranchiseState, Franchise
from .serializers import (
    FranchiseStateSerializer, 
    FranchiseSerializer, 
    FranchiseDetailSerializer
)

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
    ordering = ['franchise']

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
