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
from price.models import Price
from .serializers import (
    CatalogSerializer, ProductSerializer, MaterialSerializer, ServiceSerializer,
    MenuSerializer, ItemGroupSerializer, ItemCategorySerializer, ItemTypeSerializer,
    RestrictionSerializer, InstructionSerializer, ProviderSerializer,
    ProviderTypeSerializer, BankSerializer, BankAccountTypeSerializer, DistrictSerializer, RegionSerializer,
    ProductManageSerializer, ProviderListSerializer, ProductListSerializer
)
from django.db import connection
from django.db import transaction
from rest_framework import serializers


class CatalogViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Catalog
    Proporciona operaciones CRUD completas para el catálogo
    """
    queryset = Catalog.objects.all()  # type: ignore
    serializer_class = CatalogSerializer
    lookup_field = 'code'
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
    lookup_field = 'sku'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_deleted', 'is_confirmed', 'provider', 'type', 'item_group', 'category']
    search_fields = ['description', 'sku', 'code', 'obs']
    ordering_fields = ['id', 'description', 'created_at', 'updated_at']
    ordering = ['-id']

    class _SimplePriceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Price
            fields = '__all__'

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')

    def partial_update(self, request, *args, **kwargs):
        price_data = request.data.get('price_data', None)
        instance = self.get_object()
        if price_data:
            # Obtener el price actual
            try:
                price_obj = Price.objects.get(code=instance.price)
            except Price.DoesNotExist:
                return Response({'detail': 'Precio actual no encontrado.'}, status=400)
            # Detectar cambios en base_net_amount o price_configuration
            base_net_amount_new = price_data.get('base_net_amount')
            price_configuration_new = price_data.get('price_configuration')
            changed = False
            if base_net_amount_new is not None and str(price_obj.base_net_amount) != str(base_net_amount_new):
                changed = True
            if price_configuration_new is not None and str(price_obj.price_configuration) != str(price_configuration_new):
                changed = True
            if changed:
                with transaction.atomic():
                    # 1. Marcar el price actual como is_current=False
                    price_obj.is_current = False
                    price_obj.save()
                    # 2. Crear un nuevo price
                    price_data_new = self._SimplePriceSerializer(price_obj).data
                    price_data_new.pop('id', None)
                    price_data_new.pop('code', None)
                    price_data_new.pop('created_at', None)
                    price_data_new['base_net_amount'] = base_net_amount_new
                    price_data_new['price_configuration'] = price_configuration_new
                    price_data_new['is_current'] = True
                    new_price = Price.objects.create(**price_data_new)
                    new_price.refresh_from_db()
                    # 3. Actualizar el producto para que apunte al nuevo price
                    instance.price = new_price.code
                    instance.save()
            # Actualizar el resto de campos del producto si hay otros en el PATCH
            product_fields = set(request.data.keys()) - {'price_data'}
            for field in product_fields:
                if hasattr(instance, field):
                    setattr(instance, field, request.data[field])
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        # Si no hay price_data, hacer el update normal
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='product-list')
    def product_list(self, request):
        sql = '''
        SELECT 
          p.code, p.sku, p.description, pr.base_net_amount, pr.net_amount, pr.gross_amount, 
          pr.iva_amount, pr.aditional_tax_amount, pr.retention_amount, pr.price_configuration, pc.price_configuration as price_configuration_label, 
          p.obs, p.package_unit, p.min_package_purchase, p.provider, p.type, it."type" as type_name, 
          p.item_group, ig.group_name, p.category, ic.category as category_name, p.url, 
          p.package, pa.description as package_description, p.is_active, p.is_deleted, p.is_confirmed, p.created_at
        FROM ditaly_pasta.product p
        LEFT JOIN LATERAL (
            SELECT pr.*
            FROM ditaly_pasta.price pr
            WHERE p.price = pr.code AND pr.is_current = true
            ORDER BY pr.created_at DESC
            LIMIT 1
        ) pr ON true
        LEFT JOIN sbm_business.item_type it ON p.type = it.id
        LEFT JOIN sbm_business.item_group ig ON p.item_group = ig.id
        LEFT JOIN sbm_business.item_category ic ON p.category = ic.id 
        LEFT JOIN sbm_business.package pa ON p.package = pa.id
        left join ditaly_pasta.price_configuration pc on pr.price_configuration = pc.code 
        '''
        verbose_names = {
            'code': 'Código',
            'sku': 'SKU',
            'description': 'Descripción',
            'base_net_amount': 'Valor Base Neto',
            'net_amount': 'Valor Neto',
            'gross_amount': 'Valor Bruto',
            'iva_amount': 'IVA',
            'aditional_tax_amount': 'Impuesto Adicional',
            'retention_amount': 'Retención',
            'price_configuration': 'Configuración de Precio',
            'price_configuration_label': 'Configuración Precio',
            'obs': 'Observaciones',
            'package_unit': 'Unidad de Empaque',
            'min_package_purchase': 'Compra Mínima de Empaque',
            'provider': 'Proveedor',
            'type': 'Tipo',
            'type_name': 'Nombre de Tipo',
            'item_group': 'Grupo',
            'group_name': 'Nombre de Grupo',
            'category': 'Categoría',
            'category_name': 'Nombre de Categoría',
            'url': 'URL',
            'package': 'Paquete',
            'package_description': 'Descripción del Paquete',
            'is_active': 'Está Activo',
            'is_deleted': 'Está Eliminado',
            'is_confirmed': 'Está Confirmado',
            'created_at': 'Fecha de Creación',
        }
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response({'results': serializer.data, 'verbose_names': verbose_names})
        serializer = ProductListSerializer(results, many=True)
        return Response({'results': serializer.data, 'verbose_names': verbose_names})

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

    def list(self, request, *args, **kwargs):
        # Restaurar el comportamiento original: select * from ditaly_pasta.provider
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list')
    def provider_list(self, request):
        sql = '''
        select p.id, p.provider, p.type, pt."type" as type_name, p.rating, p.obs_provider, p.contact_name, p.contact_mail, p.contact_phone, p.contact_phone2, p.obs_contact,  p.website_url, p.company_name, p.company_rut, p.company_activity,
        p.legal_representative, p.billing_address, p.billing_mail, p.billing_phone, p.company_bank, b.bank, p.bank_account_number, p.bank_account_type, bat."type" as bank_account_type_name, p.bank_account_mail, p.dispatch_address,
        p.dispatch_maps_location,
        p.obs_dispatch, p.dispatch_district, d.district, p.dispatch_region, r.region, p.is_active, p.is_deleted, p.is_confirmed
        from ditaly_pasta.provider p 
        left join sbm_business.provider_type pt on p.type = pt.id
        left join sbm_business.bank b on p.company_bank = b.id
        left join sbm_business.bank_account_type bat on p.bank_account_type = bat.id
        left join sbm_business.district d on p.dispatch_district = d.id 
        left join sbm_business.region r on p.dispatch_region = r.id 
        '''
        verbose_names = {
            'id': 'ID',
            'provider': 'Proveedor',
            'type': 'Tipo',
            'type_name': 'Tipo de Proveedor',
            'rating': 'Calificación',
            'obs_provider': 'Observaciones del Proveedor',
            'contact_name': 'Nombre de Contacto',
            'contact_mail': 'Email de Contacto',
            'contact_phone': 'Teléfono de Contacto',
            'contact_phone2': 'Teléfono de Contacto 2',
            'obs_contact': 'Observaciones de Contacto',
            'website_url': 'URL del Sitio Web',
            'company_name': 'Nombre de la Empresa',
            'company_rut': 'RUT de la Empresa',
            'company_activity': 'Actividad de la Empresa',
            'legal_representative': 'Representante Legal',
            'billing_address': 'Dirección de Facturación',
            'billing_mail': 'Email de Facturación',
            'billing_phone': 'Teléfono de Facturación',
            'company_bank': 'Banco de la Empresa',
            'bank': 'Banco',
            'bank_account_number': 'Número de Cuenta Bancaria',
            'bank_account_type': 'Tipo de Cuenta Bancaria',
            'bank_account_type_name': 'Tipo de Cuenta Bancaria',
            'bank_account_mail': 'Email de Cuenta Bancaria',
            'dispatch_address': 'Dirección de Despacho',
            'dispatch_maps_location': 'Ubicación en Maps',
            'obs_dispatch': 'Observaciones de Despacho',
            'dispatch_district': 'Distrito de Despacho',
            'district': 'Distrito',
            'dispatch_region': 'Región de Despacho',
            'region': 'Región',
            'is_active': 'Está Activo',
            'is_deleted': 'Está Eliminado',
            'is_confirmed': 'Está Confirmado',
        }
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        page = self.paginate_queryset(results)
        if page is not None:
            serializer = ProviderListSerializer(page, many=True)
            return self.get_paginated_response({'results': serializer.data, 'verbose_names': verbose_names})
        serializer = ProviderListSerializer(results, many=True)
        return Response({'results': serializer.data, 'verbose_names': verbose_names})

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')

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
