from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    Catalog, Product, Material, Service,
    Menu, ItemGroup, ItemCategory, ItemType, Restriction, Instruction,
    Provider, ProviderType, Bank, BankAccountType, District, Region
)
from .serializers import (
    CatalogSerializer, ProductSerializer, MaterialSerializer, ServiceSerializer,
    MenuSerializer, ItemGroupSerializer, ItemCategorySerializer, ItemTypeSerializer,
    RestrictionSerializer, InstructionSerializer, ProviderSerializer,
    ProviderTypeSerializer, BankSerializer, BankAccountTypeSerializer, DistrictSerializer, RegionSerializer
)


class CatalogViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Catalog
    Proporciona operaciones CRUD completas para el catálogo
    """
    queryset = Catalog.objects.all()  # type: ignore
    serializer_class = CatalogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'is_visible', 'is_deleted', 'is_confirmed', 'chef_recommendation', 'item_group', 'menu'
    ]
    search_fields = [
        'name', 'description', 'sku', 'code', 'menu__menu'
    ]
    ordering_fields = ['id', 'name', 'created_at', 'updated_at']
    ordering = ['-id']

    def get_queryset(self):
        """
        Optimizar consultas con select_related para datos relacionados
        """
        return Catalog.objects.select_related().all()  # type: ignore

    @action(detail=False, methods=['get'])
    def visible(self, request):
        """
        Endpoint para obtener solo elementos visibles
        """
        queryset = self.get_queryset().filter(is_visible=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def chef_recommendations(self, request):
        """
        Endpoint para obtener solo recomendaciones del chef
        """
        queryset = self.get_queryset().filter(chef_recommendation=True, is_visible=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='foreign-keys-by-code')
    def foreign_keys_by_code(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'detail': 'code param is required.'}, status=400)
        try:
            catalog = Catalog.objects.get(code=code)  # type: ignore
        except Catalog.DoesNotExist:  # type: ignore
            return Response({'detail': 'Catalog not found.'}, status=404)
        data = {
            'menu_id': catalog.menu_id,
            'item_group_id': catalog.item_group_id,
            'category_id': catalog.category_id,
            'type_id': catalog.type_id,
            'restriction_id': catalog.restriction_id,
        }
        return Response(data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Product
    Proporciona operaciones CRUD completas para productos
    """
    queryset = Product.objects.all()  # type: ignore
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_deleted', 'is_confirmed', 'provider', 'type', 'group', 'category']
    search_fields = ['description', 'sku', 'code', 'obs']
    ordering_fields = ['id', 'description', 'created_at', 'updated_at']
    ordering = ['-id']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo productos activos
        """
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_provider(self, request):
        """
        Endpoint para filtrar productos por proveedor
        """
        provider_id = request.query_params.get('provider_id')
        if provider_id:
            queryset = self.get_queryset().filter(provider=provider_id, is_active=True)
        else:
            queryset = self.get_queryset().filter(is_active=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Material
    Proporciona operaciones CRUD completas para materiales
    """
    queryset = Material.objects.all()  # type: ignore
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_deleted', 'is_confirmed', 'provider', 'type', 'group', 'category']
    search_fields = ['description', 'sku', 'code', 'obs']
    ordering_fields = ['id', 'description', 'created_at', 'updated_at']
    ordering = ['-id']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo materiales activos
        """
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_provider(self, request):
        """
        Endpoint para filtrar materiales por proveedor
        """
        provider_id = request.query_params.get('provider_id')
        if provider_id:
            queryset = self.get_queryset().filter(provider=provider_id, is_active=True)
        else:
            queryset = self.get_queryset().filter(is_active=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Service
    Proporciona operaciones CRUD completas para servicios
    """
    queryset = Service.objects.all()  # type: ignore
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_deleted', 'is_confirmed', 'provider', 'type', 'group', 'category']
    search_fields = ['description', 'sku', 'code', 'obs']
    ordering_fields = ['id', 'description', 'created_at', 'updated_at']
    ordering = ['-id']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo servicios activos
        """
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_provider(self, request):
        """
        Endpoint para filtrar servicios por proveedor
        """
        provider_id = request.query_params.get('provider_id')
        if provider_id:
            queryset = self.get_queryset().filter(provider=provider_id, is_active=True)
        else:
            queryset = self.get_queryset().filter(is_active=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# ViewSets para modelos de referencia
class MenuViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Menu
    """
    queryset = Menu.objects.all()  # type: ignore
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['franchise_only']
    search_fields = ['menu', 'description']
    ordering_fields = ['id', 'menu']
    ordering = ['menu']


class ItemGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo ItemGroup
    """
    queryset = ItemGroup.objects.all()  # type: ignore
    serializer_class = ItemGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['catalog_render']
    search_fields = ['group_name', 'description']
    ordering_fields = ['id', 'group_name']
    ordering = ['group_name']


class ItemCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo ItemCategory
    """
    queryset = ItemCategory.objects.all()  # type: ignore
    serializer_class = ItemCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['catalog_render']
    search_fields = ['category', 'description']
    ordering_fields = ['id', 'category']
    ordering = ['category']


class ItemTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo ItemType
    """
    queryset = ItemType.objects.all()  # type: ignore
    serializer_class = ItemTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['id', 'type']
    ordering = ['type']


class RestrictionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Restriction
    """
    queryset = Restriction.objects.all()  # type: ignore
    serializer_class = RestrictionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['restriction', 'description']
    ordering_fields = ['id', 'restriction', 'created_at']
    ordering = ['restriction']


class InstructionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Instruction
    """
    queryset = Instruction.objects.all()  # type: ignore
    serializer_class = InstructionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed', 'type']
    search_fields = ['instruction', 'description']
    ordering_fields = ['id', 'instruction', 'created_at']
    ordering = ['instruction']



class ProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Provider
    """
    queryset = Provider.objects.all()  # type: ignore
    serializer_class = ProviderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_deleted', 'is_confirmed', 'type']
    search_fields = ['provider', 'company_name', 'contact_name', 'code']
    ordering_fields = ['id', 'provider', 'created_at']
    ordering = ['provider']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo proveedores activos
        """
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProviderTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo ProviderType
    """
    queryset = ProviderType.objects.all()  # type: ignore
    serializer_class = ProviderTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['id', 'type']
    ordering = ['type']


class BankViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Bank
    """
    queryset = Bank.objects.all()  # type: ignore
    serializer_class = BankSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['bank', 'description']
    ordering_fields = ['id', 'bank']
    ordering = ['bank']


class BankAccountTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo BankAccountType
    """
    queryset = BankAccountType.objects.all()  # type: ignore
    serializer_class = BankAccountTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['id', 'type']
    ordering = ['type']


class RegionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Region
    """
    queryset = Region.objects.all()  # type: ignore
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['region', 'description']
    ordering_fields = ['id', 'region']
    ordering = ['region']


class DistrictViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo District
    """
    queryset = District.objects.all()  # type: ignore
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['region']
    search_fields = ['district', 'description']
    ordering_fields = ['id', 'district']
    ordering = ['district']

    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """
        Endpoint para filtrar distritos por región
        """
        region_id = request.query_params.get('region_id')
        if region_id:
            queryset = self.get_queryset().filter(region=region_id)
        else:
            queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
