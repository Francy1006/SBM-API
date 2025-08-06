from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    Catalog, Product, Material, Service,
    Menu, ItemGroup, ItemCategory, ItemType, Restriction, Instruction, InstructionType,
    Provider, ProviderType, Bank, BankAccountType, District, Region,
    ItemConfiguration
)
from inventory.models import Package, PackageType, TransportType, MeasureUnit
from price.models import Price
from .serializers import (
    CatalogSerializer, ProductSerializer, MaterialSerializer, ServiceSerializer,
    MenuSerializer, ItemGroupSerializer, ItemCategorySerializer, ItemTypeSerializer,
    RestrictionSerializer, InstructionSerializer, InstructionTypeSerializer, ProviderSerializer,
    ProviderTypeSerializer, BankSerializer, BankAccountTypeSerializer, DistrictSerializer, RegionSerializer,
    ProductManageSerializer, ProviderListSerializer, ProductListSerializer, CatalogListSerializer,
    ItemConfigurationSerializer, PackageSerializer, PackageTypeSerializer, TransportTypeSerializer, MeasureUnitSerializer
)

from django.db import transaction, connection
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
        'name', 'description', 'sku', 'code'
    ]
    ordering_fields = ['id', 'name', 'created_at', 'updated_at']
    ordering = ['-id']

    def get_queryset(self):
        """
        Optimizar consultas con select_related para datos relacionados
        """
        return Catalog.objects.select_related('usage_instructions').all()  # type: ignore

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

    @action(detail=False, methods=['get'], url_path='list')
    def catalog_list(self, request):
        try:
            from django.db.models import Q
            from price.models import Price
            
            # Obtener catálogos usando ORM con select_related para optimizar consultas
            catalogs = Catalog.objects.select_related('usage_instructions').all()
            
            # Obtener datos de las tablas relacionadas para los JOINs
            from .models import Menu, ItemCategory, ItemGroup, ItemType, ItemConfiguration
            
            # Crear diccionarios para mapear IDs a nombres
            menu_dict = {menu.id: menu.menu for menu in Menu.objects.all()}
            category_dict = {cat.id: cat.category for cat in ItemCategory.objects.all()}
            group_dict = {group.id: group.group_name for group in ItemGroup.objects.all()}
            type_dict = {type_obj.id: type_obj.type for type_obj in ItemType.objects.all()}
            config_dict = {config.code: config.configuration for config in ItemConfiguration.objects.all()}
            
            # Filtrar catálogos visibles si es necesario
            if request.query_params.get('visible_only') == 'true':
                catalogs = catalogs.filter(is_visible=True, is_deleted=False)
            
            results = []
            for catalog in catalogs:
                # Obtener el precio asociado
                try:
                    price_obj = Price.objects.filter(
                        code=catalog.price,
                        is_current=True
                    ).first()
                    
                    # Construir el resultado
                    result = {
                        'sku': catalog.sku,
                        'cover_image': catalog.cover_image,
                        'menu': catalog.menu,
                        'menu_name': menu_dict.get(catalog.menu),
                        'category': catalog.category,
                        'category_name': category_dict.get(catalog.category),
                        'name': catalog.name,
                        'description': catalog.description,
                        'obs': catalog.obs,
                        'chef_recommendation': catalog.chef_recommendation,
                        'item_type': catalog.type,
                        'type_name': type_dict.get(catalog.type),
                        'item_group': catalog.item_group,
                        'group_name': group_dict.get(catalog.item_group),
                        'base_net_amount': price_obj.base_net_amount if price_obj else None,
                        'net_amount': price_obj.net_amount if price_obj else None,
                        'gross_amount': price_obj.gross_amount if price_obj else None,
                        'iva_amount': price_obj.iva_amount if price_obj else None,
                        'aditional_tax_amount': price_obj.aditional_tax_amount if price_obj else None,
                        'retention_amount': price_obj.retention_amount if price_obj else None,
                        'price_configuration': price_obj.price_configuration if price_obj else None,
                        'min_quantity_purchase': catalog.min_quantity_purchase,
                        'rations_quantity': catalog.rations_quantity,
                        'item_configuration': catalog.configuration,
                        'configuration': config_dict.get(catalog.configuration),
                        'is_visible': catalog.is_visible,
                        'is_confirmed': catalog.is_confirmed,
                        'created_at': catalog.created_at,
                    }
                    results.append(result)
                    
                except Exception as e:
                    # Si hay error con un catálogo específico, continuar con el siguiente
                    print(f"Error procesando catálogo {catalog.sku}: {str(e)}")
                    continue
            
            verbose_names = CatalogListSerializer.get_verbose_names()
            
            page = self.paginate_queryset(results)
            if page is not None:
                serializer = CatalogListSerializer(page, many=True)
                return self.get_paginated_response({'results': serializer.data, 'verbose_names': verbose_names})
            serializer = CatalogListSerializer(results, many=True)
            return Response({'results': serializer.data, 'verbose_names': verbose_names})
            
        except Exception as e:
            return Response({'error': f'Error obteniendo lista de catálogos: {str(e)}'}, status=500)


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
            product = serializer.save(created_by=self.request.user.code)
        else:
            product = serializer.save(created_by='system')
        
        # Ejecutar automáticamente el cálculo de precio después de crear el producto
        try:
            from rest_framework.test import APIRequestFactory
            from price.views import PriceCalculationFormulaView
            from rest_framework.response import Response
            
            # Crear una request interna para el cálculo de precio
            factory = APIRequestFactory()
            calculation_request = factory.post('/price/product-price-calculation/', 
                                             {'sku': product.sku}, 
                                             format='json')
            
            # Agregar autenticación a la request interna
            if hasattr(self.request, 'user') and self.request.user.is_authenticated:
                calculation_request.user = self.request.user
            
            # Ejecutar el cálculo de precio
            calculation_view = PriceCalculationFormulaView.as_view()
            calculation_response = calculation_view(calculation_request)
            
            # Log del resultado (opcional)
            if calculation_response.status_code != 200:
                print(f"Warning: Price calculation failed for product {product.sku}: {calculation_response.status_code}")
            else:
                print(f"Price calculation completed successfully for product {product.sku}")
                
        except Exception as e:
            print(f"Error executing price calculation for product {product.sku}: {str(e)}")
            # No fallar la creación del producto si el cálculo falla

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

    @action(detail=False, methods=['get'], url_path='list')
    def product_list(self, request):
        try:
            from django.db.models import Q
            from price.models import Price, PriceConfiguration
            from catalog.models import ItemType, ItemGroup, ItemCategory
            from inventory.models import Package
            
            # Obtener productos usando ORM
            products = Product.objects.all()
            
            # Filtrar productos activos si es necesario
            if request.query_params.get('active_only') == 'true':
                products = products.filter(is_active=True, is_deleted=False)
            
            results = []
            for product in products:
                # Obtener el precio actual (is_current=True)
                try:
                    current_price = Price.objects.filter(
                        code=product.price,
                        is_current=True
                    ).first()
                    
                    # Obtener la configuración de precio
                    price_config = None
                    if current_price:
                        price_config = PriceConfiguration.objects.filter(
                            code=current_price.price_configuration
                        ).first()
                    
                    # Construir el resultado
                    result = {
                        'code': product.code,
                        'sku': product.sku,
                        'description': product.description,
                        'base_net_amount': current_price.base_net_amount if current_price else 0,
                        'net_amount': current_price.net_amount if current_price else 0,
                        'gross_amount': current_price.gross_amount if current_price else 0,
                        'iva_amount': current_price.iva_amount if current_price else 0,
                        'aditional_tax_amount': current_price.aditional_tax_amount if current_price else 0,
                        'retention_amount': current_price.retention_amount if current_price else 0,
                        'price_configuration': current_price.price_configuration if current_price else None,
                        'price_configuration_label': price_config.price_configuration if price_config else None,
                        'obs': product.obs,
                        'package_unit': product.package_unit,
                        'min_package_purchase': product.min_package_purchase,
                        'provider': product.provider,
                        'type': product.type,
                        'type_name': None,  # Se puede obtener consultando ItemType por ID si es necesario
                        'item_group': product.item_group,
                        'group_name': None,  # Se puede obtener consultando ItemGroup por ID si es necesario
                        'category': product.category,
                        'category_name': None,  # Se puede obtener consultando ItemCategory por ID si es necesario
                        'url': product.url,
                        'package': product.package,
                        'package_description': None,  # Se puede obtener consultando Package por ID si es necesario
                        'is_active': product.is_active,
                        'is_deleted': product.is_deleted,
                        'is_confirmed': product.is_confirmed,
                        'created_at': product.created_at,
                    }
                    results.append(result)
                    
                except Exception as e:
                    # Si hay error con un producto específico, continuar con el siguiente
                    print(f"Error procesando producto {product.sku}: {str(e)}")
                    continue
            
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
            
            page = self.paginate_queryset(results)
            if page is not None:
                serializer = ProductListSerializer(page, many=True)
                return self.get_paginated_response({'results': serializer.data, 'verbose_names': verbose_names})
            serializer = ProductListSerializer(results, many=True)
            return Response({'results': serializer.data, 'verbose_names': verbose_names})
            
        except Exception as e:
            return Response({'error': f'Error obteniendo lista de productos: {str(e)}'}, status=500)

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
    lookup_field = 'code'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed', 'type']
    search_fields = ['instruction', 'description']
    ordering_fields = ['code', 'instruction', 'created_at']
    ordering = ['instruction']

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')



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


class ItemConfigurationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo ItemConfiguration
    Proporciona operaciones CRUD completas para configuraciones de items
    """
    queryset = ItemConfiguration.objects.all()  # type: ignore
    serializer_class = ItemConfigurationSerializer
    lookup_field = 'code'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed', 'package']
    search_fields = ['configuration', 'description', 'code']
    ordering_fields = ['id', 'configuration', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo configuraciones activas
        """
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_package(self, request):
        """
        Endpoint para filtrar configuraciones por paquete
        """
        package_id = request.query_params.get('package_id')
        if package_id:
            queryset = self.get_queryset().filter(package=package_id, is_deleted=False)
        else:
            queryset = self.get_queryset().filter(is_deleted=False)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PackageViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Package
    Proporciona operaciones CRUD completas para paquetes
    """
    queryset = Package.objects.all()  # type: ignore
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed', 'package_type', 'transport_type']
    search_fields = ['description']
    ordering_fields = ['id', 'description', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Endpoint para obtener solo paquetes activos
        """
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PackageTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo PackageType
    """
    queryset = PackageType.objects.all()  # type: ignore
    serializer_class = PackageTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['id', 'type']
    ordering = ['type']


class TransportTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo TransportType
    """
    queryset = TransportType.objects.all()  # type: ignore
    serializer_class = TransportTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['type', 'description']
    ordering_fields = ['id', 'type']
    ordering = ['type']


class MeasureUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo MeasureUnit
    """
    queryset = MeasureUnit.objects.all()  # type: ignore
    serializer_class = MeasureUnitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['measure_unit', 'description']
    ordering_fields = ['id', 'measure_unit']
    ordering = ['measure_unit']


class InstructionTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo InstructionType
    """
    queryset = InstructionType.objects.all()  # type: ignore
    serializer_class = InstructionTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_deleted', 'is_confirmed']
    search_fields = ['type', 'description']
    ordering_fields = ['id', 'type', 'created_at']
    ordering = ['type']

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'code'):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by='system')
