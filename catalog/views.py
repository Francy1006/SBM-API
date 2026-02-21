from django.shortcuts import render  # noqa: F401
from django.db import transaction, connection  # noqa: F401
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Catalog,
    Product,
    Material,
    Service,
    Menu,
    ItemGroup,
    ItemCategory,
    ItemType,
    Restriction,
    Instruction,
    InstructionType,
    ItemConfiguration,
)

from inventory.models import Package, PackageType, TransportType, MeasureUnit
from price.models import Price

from .serializers import (
    CatalogSerializer,
    ProductSerializer,
    MaterialSerializer,
    ServiceSerializer,
    MenuSerializer,
    ItemGroupSerializer,
    ItemCategorySerializer,
    ItemTypeSerializer,
    RestrictionSerializer,
    InstructionSerializer,
    InstructionTypeSerializer,
    ItemConfigurationSerializer,
    PackageSerializer,
    PackageTypeSerializer,
    TransportTypeSerializer,
    MeasureUnitSerializer,
    ProductManageSerializer,
    ProductListSerializer,
    CatalogListSerializer,
)


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()  # type: ignore
    serializer_class = CatalogSerializer
    lookup_field = "sku"
    lookup_value_regex = r"[^/]+"

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = [
        "is_visible",
        "is_deleted",
        "is_confirmed",
        "chef_recommendation",
        "item_group",
        "menu",
    ]

    search_fields = [
        "name",
        "description",
        "sku",
        "code",
        "menu__menu",
        "item_group__group_name",
        "category__category",
        "type__type",
    ]

    ordering_fields = [
        "id",
        "name",
        "sku",
        "created_at",
        "is_visible",
        "is_confirmed",
        "menu__menu",
        "item_group__group_name",
        "category__category",
        "type__type",
    ]

    ordering = ["-id"]

    def get_queryset(self):
        return Catalog.objects.select_related(
            "menu",
            "item_group",
            "category",
            "type",
            "restriction",
            "usage_instructions",
            "configuration",
            "price",
        )

    # Alias para ordenar desde Vue por nombres visibles
    def _apply_ordering_aliases(self, request, qs):
        ordering = request.query_params.get("ordering")
        if not ordering:
            return qs

        alias_map = {
            "menu_name": "menu__menu",
            "category_name": "category__category",
            "group_name": "item_group__group_name",
            "type_name": "type__type",
            "configuration": "configuration__configuration",
        }

        fields = [f.strip() for f in ordering.split(",") if f.strip()]
        translated = []

        for f in fields:
            desc = f.startswith("-")
            key = f[1:] if desc else f
            real_field = alias_map.get(key, key)
            translated.append(f"-{real_field}" if desc else real_field)

        return qs.order_by(*translated)

    @action(detail=False, methods=["post"], url_path="soft_delete")
    def soft_delete(self, request):
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return Response(
                {"detail": "ids debe ser una lista con al menos 1 elemento"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated = Catalog.objects.filter(sku__in=ids).update(
            is_deleted=True, is_visible=False
        )  # code=sku en la lista
        return Response({"deleted": updated}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="list")
    def catalog_list(self, request):
        try:
            qs = self.filter_queryset(self.get_queryset())
            qs = self._apply_ordering_aliases(request, qs)

            page_qs = self.paginate_queryset(qs)
            if page_qs is None:
                page_qs = qs

            # Diccionarios rápidos
            menu_dict = dict(Menu.objects.values_list("id", "menu"))
            category_dict = dict(ItemCategory.objects.values_list("id", "category"))
            group_dict = dict(ItemGroup.objects.values_list("id", "group_name"))
            type_dict = dict(ItemType.objects.values_list("id", "type"))
            config_dict = dict(
                ItemConfiguration.objects.values_list("code", "configuration")
            )

            # Evitar N+1
            price_codes = [c.price_id for c in page_qs if c.price_id]
            price_map = {
                p.code: p
                for p in Price.objects.filter(code__in=price_codes, is_current=True)
            }

            results = []
            for catalog in page_qs:
                price_obj = price_map.get(catalog.price_id)

                results.append(
                    {
                        "code": catalog.sku,
                        "sku": catalog.sku,
                        "cover_image": catalog.cover_image,
                        "menu": catalog.menu_id,
                        "menu_name": menu_dict.get(catalog.menu_id),
                        "category": catalog.category_id,
                        "category_name": category_dict.get(catalog.category_id),
                        "name": catalog.name,
                        "description": catalog.description,
                        "obs": catalog.obs,
                        "chef_recommendation": catalog.chef_recommendation,
                        "item_type": catalog.type_id,
                        "type_name": type_dict.get(catalog.type_id),
                        "item_group": catalog.item_group_id,
                        "group_name": group_dict.get(catalog.item_group_id),
                        "base_net_amount": getattr(price_obj, "base_net_amount", None),
                        "net_amount": getattr(price_obj, "net_amount", None),
                        "gross_amount": getattr(price_obj, "gross_amount", None),
                        "iva_amount": getattr(price_obj, "iva_amount", None),
                        "aditional_tax_amount": getattr(
                            price_obj, "aditional_tax_amount", None
                        ),
                        "retention_amount": getattr(
                            price_obj, "retention_amount", None
                        ),
                        "price_configuration": getattr(
                            price_obj, "price_configuration", None
                        ),
                        "min_quantity_purchase": catalog.min_quantity_purchase,
                        "rations_quantity": catalog.rations_quantity,
                        "item_configuration": catalog.configuration_id,
                        "configuration": config_dict.get(catalog.configuration_id),
                        "is_visible": catalog.is_visible,
                        "is_deleted": catalog.is_deleted,
                        "is_confirmed": catalog.is_confirmed,
                        "created_at": catalog.created_at,
                    }
                )

            verbose_names = {
                "sku": "SKU",
                "menu_name": "Menú",
                "category_name": "Categoría",
                "name": "Nombre",
                "group_name": "Grupo",
                "type_name": "Tipo",
                "base_net_amount": "Valor Base Neto",
                "net_amount": "Valor Neto",
                "gross_amount": "Valor Bruto",
                "is_visible": "Visible",
                "is_confirmed": "Confirmado",
                "created_at": "Creado",
            }

            if hasattr(self, "paginator") and self.paginator is not None:
                return self.get_paginated_response(
                    {"results": results, "verbose_names": verbose_names}
                )

            return Response({"results": results, "verbose_names": verbose_names})

        except Exception as e:
            return Response(
                {"error": f"Error obteniendo lista de catálogos: {str(e)}"},
                status=500,
            )
        # REF: CATALOG_ADV_ENDPOINT_001

    @action(
        detail=False,
        methods=["get"],
        url_path=r"adv/(?P<sku>[^/.]+)",
    )
    def adv(self, request, sku=None):
        """
        GET /api/catalogs/adv/{sku}
        Devuelve campos adicionales (nombres y metadata) resolviendo llaves foráneas.
        """
        try:
            catalog = self.get_queryset().filter(sku=sku).first()
            if not catalog:
                return Response(
                    {"detail": "Catálogo no encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # PRICE (ya viene en select_related('price'))
            price_obj = getattr(catalog, "price", None)

            # INSTRUCTIONS (ya viene select_related('usage_instructions'))
            instr = getattr(catalog, "usage_instructions", None)
            instr_type = getattr(instr, "type", None) if instr else None

            # RESTRICTION (ya viene select_related('restriction'))
            restriction = getattr(catalog, "restriction", None)

            # CONFIGURATION (ya viene select_related('configuration'))
            cfg = getattr(catalog, "configuration", None)
            pkg = getattr(cfg, "package", None) if cfg else None
            pkg_type = getattr(pkg, "package_type", None) if pkg else None
            transport_type = getattr(pkg, "transport_type", None) if pkg else None
            measure_unit = getattr(pkg, "measure_unit", None) if pkg else None
            storage_instr = getattr(pkg, "storage_instructions", None) if pkg else None
            transport_instr = (
                getattr(pkg, "transport_instructions", None) if pkg else None
            )

            advanced = {
                # Catálogo: campos extra útiles
                "code_uuid": getattr(catalog, "code", None),
                "obs": getattr(catalog, "obs", None),
                "secondary_image": getattr(catalog, "secondary_image", None),
                "complementary_image": getattr(catalog, "complementary_image", None),
                "image_gallery": getattr(catalog, "image_gallery", None),
                # Menú / Grupo / Categoría / Tipo (labels extra, aunque ya tengas *_name en list)
                "menu_description": getattr(
                    getattr(catalog, "menu", None), "description", None
                ),
                "group_description": getattr(
                    getattr(catalog, "item_group", None), "description", None
                ),
                "category_description": getattr(
                    getattr(catalog, "category", None), "description", None
                ),
                "type_description": getattr(
                    getattr(catalog, "type", None), "description", None
                ),
                # Restricción
                "restriction_name": getattr(restriction, "restriction", None),
                "restriction_description": getattr(restriction, "description", None),
                # Instrucciones de uso
                "usage_instruction": getattr(instr, "instruction", None),
                "usage_instruction_description": getattr(instr, "description", None),
                "usage_instruction_url": getattr(instr, "url_documentation", None),
                "usage_instruction_type_id": getattr(instr, "type_id", None),
                "usage_instruction_type_name": getattr(instr_type, "type", None),
                # Precio
                "price_code": getattr(price_obj, "code", None),
                "price_configuration": getattr(price_obj, "price_configuration", None),
                "base_net_amount": getattr(price_obj, "base_net_amount", None),
                "net_amount": getattr(price_obj, "net_amount", None),
                "gross_amount": getattr(price_obj, "gross_amount", None),
                "iva_amount": getattr(price_obj, "iva_amount", None),
                "aditional_tax_amount": getattr(
                    price_obj, "aditional_tax_amount", None
                ),
                "retention_amount": getattr(price_obj, "retention_amount", None),
                "price_is_current": getattr(price_obj, "is_current", None),
                # Configuración / Package (para tu sección “Configuración” después)
                "configuration_code": getattr(cfg, "code", None),
                "configuration_name": getattr(cfg, "configuration", None),
                "configuration_description": getattr(cfg, "description", None),
                "package_id": getattr(pkg, "id", None),
                "package_description": getattr(pkg, "description", None),
                "package_type_id": getattr(pkg, "package_type_id", None),
                "package_type_name": getattr(pkg_type, "type", None),
                "transport_type_id": getattr(pkg, "transport_type_id", None),
                "transport_type_name": getattr(transport_type, "type", None),
                "size": getattr(pkg, "size", None),
                "weight": getattr(pkg, "weight", None),
                "measure_unit_id": getattr(pkg, "measure_unit_id", None),
                "measure_unit_name": getattr(measure_unit, "measure_unit", None),
                "quantity_unit": getattr(pkg, "quantity_unit", None),
                "storage_instruction": getattr(storage_instr, "instruction", None),
                "storage_instruction_url": getattr(
                    storage_instr, "url_documentation", None
                ),
                "transport_instruction": getattr(transport_instr, "instruction", None),
                "transport_instruction_url": getattr(
                    transport_instr, "url_documentation", None
                ),
            }

            # Limpia None para que el front no se llene de “-” innecesario si quieres
            advanced = {k: v for k, v in advanced.items() if v is not None}

            verbose_names = {
                "code_uuid": "Código UUID",
                "obs": "Observaciones",
                "secondary_image": "Imagen secundaria",
                "complementary_image": "Imagen complementaria",
                "image_gallery": "Galería de imágenes",
                "menu_description": "Descripción menú",
                "group_description": "Descripción grupo",
                "category_description": "Descripción categoría",
                "type_description": "Descripción tipo",
                "restriction_name": "Restricción",
                "restriction_description": "Descripción restricción",
                "usage_instruction": "Instrucción de uso",
                "usage_instruction_description": "Detalle instrucción",
                "usage_instruction_url": "URL documentación",
                "usage_instruction_type_id": "Tipo instrucción (ID)",
                "usage_instruction_type_name": "Tipo instrucción",
                "price_code": "Código precio",
                "price_configuration": "Config. precio (code)",
                "base_net_amount": "Valor base neto",
                "net_amount": "Valor neto",
                "gross_amount": "Valor bruto",
                "iva_amount": "IVA",
                "aditional_tax_amount": "Impuesto adicional",
                "retention_amount": "Retención",
                "price_is_current": "Precio vigente",
                "configuration_code": "Código configuración",
                "configuration_name": "Configuración",
                "configuration_description": "Detalle configuración",
                "package_id": "Package (ID)",
                "package_description": "Descripción package",
                "package_type_id": "Tipo package (ID)",
                "package_type_name": "Tipo package",
                "transport_type_id": "Tipo transporte (ID)",
                "transport_type_name": "Tipo transporte",
                "size": "Tamaño",
                "weight": "Peso",
                "measure_unit_id": "Unidad medida (ID)",
                "measure_unit_name": "Unidad medida",
                "quantity_unit": "Cantidad unidad",
                "storage_instruction": "Instr. almacenamiento",
                "storage_instruction_url": "URL instr. almacenamiento",
                "transport_instruction": "Instr. transporte",
                "transport_instruction_url": "URL instr. transporte",
            }

            return Response(
                {"results": advanced, "verbose_names": verbose_names},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Error obteniendo avanzado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # type: ignore
    serializer_class = ProductSerializer
    lookup_field = "sku"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "is_active",
        "is_deleted",
        "is_confirmed",
        "provider",
        "type",
        "item_group",
        "category",
    ]
    search_fields = ["description", "sku", "code", "obs"]
    ordering_fields = ["id", "description", "created_at", "updated_at"]
    ordering = ["-id"]

    class _SimplePriceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Price
            fields = "__all__"

    def perform_create(self, serializer):
        if hasattr(self.request.user, "code"):
            product = serializer.save(created_by=self.request.user.code)
        else:
            product = serializer.save(created_by="system")

        try:
            from rest_framework.test import APIRequestFactory
            from price.views import PriceCalculationFormulaView

            factory = APIRequestFactory()
            calculation_request = factory.post(
                "/price/product-price-calculation/",
                {"sku": product.sku},
                format="json",
            )

            if hasattr(self.request, "user") and self.request.user.is_authenticated:
                calculation_request.user = self.request.user

            calculation_view = PriceCalculationFormulaView.as_view()
            calculation_response = calculation_view(calculation_request)

            if calculation_response.status_code != 200:
                print(
                    f"Warning: Price calculation failed for product {product.sku}: {calculation_response.status_code}"
                )

        except Exception as e:
            print(
                f"Error executing price calculation for product {product.sku}: {str(e)}"
            )

    def partial_update(self, request, *args, **kwargs):
        price_data = request.data.get("price_data", None)
        instance = self.get_object()

        if price_data:
            try:
                price_obj = Price.objects.get(code=instance.price)
            except Price.DoesNotExist:
                return Response({"detail": "Precio actual no encontrado."}, status=400)

            base_net_amount_new = price_data.get("base_net_amount")
            price_configuration_new = price_data.get("price_configuration")

            changed = False
            if base_net_amount_new is not None and str(
                price_obj.base_net_amount
            ) != str(base_net_amount_new):
                changed = True
            if price_configuration_new is not None and str(
                price_obj.price_configuration
            ) != str(price_configuration_new):
                changed = True

            if changed:
                with transaction.atomic():
                    price_obj.is_current = False
                    price_obj.save()

                    price_data_new = self._SimplePriceSerializer(price_obj).data
                    price_data_new.pop("id", None)
                    price_data_new.pop("code", None)
                    price_data_new.pop("created_at", None)
                    price_data_new["base_net_amount"] = base_net_amount_new
                    price_data_new["price_configuration"] = price_configuration_new
                    price_data_new["is_current"] = True

                    new_price = Price.objects.create(**price_data_new)
                    new_price.refresh_from_db()

                    instance.price = new_price.code
                    instance.save()

            product_fields = set(request.data.keys()) - {"price_data"}
            for field in product_fields:
                if hasattr(instance, field):
                    setattr(instance, field, request.data[field])

            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="list")
    def product_list(self, request):
        try:
            from price.models import PriceConfiguration

            products = Product.objects.all()

            if request.query_params.get("active_only") == "true":
                products = products.filter(is_active=True, is_deleted=False)

            results = []
            for product in products:
                current_price = Price.objects.filter(
                    code=product.price, is_current=True
                ).first()

                price_config = None
                if current_price:
                    price_config = PriceConfiguration.objects.filter(
                        code=current_price.price_configuration
                    ).first()

                results.append(
                    {
                        "code": product.code,
                        "sku": product.sku,
                        "description": product.description,
                        "base_net_amount": (
                            current_price.base_net_amount if current_price else 0
                        ),
                        "net_amount": current_price.net_amount if current_price else 0,
                        "gross_amount": (
                            current_price.gross_amount if current_price else 0
                        ),
                        "iva_amount": current_price.iva_amount if current_price else 0,
                        "aditional_tax_amount": (
                            getattr(current_price, "aditional_tax_amount", 0)
                            if current_price
                            else 0
                        ),
                        "retention_amount": (
                            current_price.retention_amount if current_price else 0
                        ),
                        "price_configuration": (
                            current_price.price_configuration if current_price else None
                        ),
                        "price_configuration_label": (
                            price_config.price_configuration if price_config else None
                        ),
                        "obs": product.obs,
                        "package_unit": product.package_unit,
                        "min_package_purchase": product.min_package_purchase,
                        "provider": product.provider,
                        "type": product.type,
                        "type_name": None,
                        "item_group": product.item_group,
                        "group_name": None,
                        "category": product.category,
                        "category_name": None,
                        "url": product.url,
                        "package": product.package,
                        "package_description": None,
                        "is_active": product.is_active,
                        "is_deleted": product.is_deleted,
                        "is_confirmed": product.is_confirmed,
                        "created_at": product.created_at,
                    }
                )

            verbose_names = {
                "code": "Código",
                "sku": "SKU",
                "description": "Descripción",
                "base_net_amount": "Valor Base Neto",
                "net_amount": "Valor Neto",
                "gross_amount": "Valor Bruto",
                "iva_amount": "IVA",
                "aditional_tax_amount": "Impuesto Adicional",
                "retention_amount": "Retención",
                "price_configuration": "Configuración de Precio",
                "price_configuration_label": "Configuración Precio",
                "obs": "Observaciones",
                "package_unit": "Unidad de Empaque",
                "min_package_purchase": "Compra Mínima de Empaque",
                "provider": "Proveedor",
                "type": "Tipo",
                "type_name": "Nombre de Tipo",
                "item_group": "Grupo",
                "group_name": "Nombre de Grupo",
                "category": "Categoría",
                "category_name": "Nombre de Categoría",
                "url": "URL",
                "package": "Paquete",
                "package_description": "Descripción del Paquete",
                "is_active": "Está Activo",
                "is_deleted": "Está Eliminado",
                "is_confirmed": "Está Confirmado",
                "created_at": "Fecha de Creación",
            }

            page = self.paginate_queryset(results)
            if page is not None:
                serializer = ProductListSerializer(page, many=True)
                return self.get_paginated_response(
                    {"results": serializer.data, "verbose_names": verbose_names}
                )

            serializer = ProductListSerializer(results, many=True)
            return Response(
                {"results": serializer.data, "verbose_names": verbose_names}
            )

        except Exception as e:
            return Response(
                {"error": f"Error obteniendo lista de productos: {str(e)}"}, status=500
            )

    @action(detail=False, methods=["get"])
    def active(self, request):
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_provider(self, request):
        provider_id = request.query_params.get("provider_id")
        if provider_id:
            queryset = self.get_queryset().filter(provider=provider_id, is_active=True)
        else:
            queryset = self.get_queryset().filter(is_active=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()  # type: ignore
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "is_active",
        "is_deleted",
        "is_confirmed",
        "provider",
        "type",
        "group",
        "category",
    ]
    search_fields = ["description", "sku", "code", "obs"]
    ordering_fields = ["id", "description", "created_at", "updated_at"]
    ordering = ["-id"]

    @action(detail=False, methods=["get"])
    def active(self, request):
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_provider(self, request):
        provider_id = request.query_params.get("provider_id")
        if provider_id:
            queryset = self.get_queryset().filter(provider=provider_id, is_active=True)
        else:
            queryset = self.get_queryset().filter(is_active=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()  # type: ignore
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "is_active",
        "is_deleted",
        "is_confirmed",
        "provider",
        "type",
        "group",
        "category",
    ]
    search_fields = ["description", "sku", "code", "obs"]
    ordering_fields = ["id", "description", "created_at", "updated_at"]
    ordering = ["-id"]

    @action(detail=False, methods=["get"])
    def active(self, request):
        queryset = self.get_queryset().filter(is_active=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_provider(self, request):
        provider_id = request.query_params.get("provider_id")
        if provider_id:
            queryset = self.get_queryset().filter(provider=provider_id, is_active=True)
        else:
            queryset = self.get_queryset().filter(is_active=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()  # type: ignore
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["franchise_only"]
    search_fields = ["menu", "description"]
    ordering_fields = ["id", "menu"]
    ordering = ["menu"]


class ItemGroupViewSet(viewsets.ModelViewSet):
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["group_name", "description"]
    ordering_fields = ["id", "group_name"]
    ordering = ["group_name"]


class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["category", "description"]
    ordering_fields = ["id", "category"]
    ordering = ["category"]


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()  # type: ignore
    serializer_class = ItemTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["type", "description"]
    ordering_fields = ["id", "type"]
    ordering = ["type"]


class RestrictionViewSet(viewsets.ModelViewSet):
    queryset = Restriction.objects.all()
    serializer_class = RestrictionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["restriction", "description"]
    ordering_fields = ["id", "restriction"]
    ordering = ["restriction"]


class InstructionViewSet(viewsets.ModelViewSet):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
    lookup_field = "code"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["instruction", "description"]
    ordering_fields = ["code", "instruction"]
    ordering = ["instruction"]

    def perform_create(self, serializer):
        if hasattr(self.request.user, "code"):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by="system")


class InstructionTypeViewSet(viewsets.ModelViewSet):
    queryset = InstructionType.objects.all()  # type: ignore
    serializer_class = InstructionTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_deleted", "is_confirmed"]
    search_fields = ["type", "description"]
    ordering_fields = ["id", "type", "created_at"]
    ordering = ["type"]

    def perform_create(self, serializer):
        if hasattr(self.request.user, "code"):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by="system")


class ItemConfigurationViewSet(viewsets.ModelViewSet):
    queryset = ItemConfiguration.objects.all()  # type: ignore
    serializer_class = ItemConfigurationSerializer
    lookup_field = "code"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_deleted", "is_confirmed", "package"]
    search_fields = ["configuration", "description", "code"]
    ordering_fields = ["id", "configuration", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        if hasattr(self.request.user, "code"):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by="system")

    @action(detail=False, methods=["get"])
    def active(self, request):
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_package(self, request):
        package_id = request.query_params.get("package_id")
        if package_id:
            queryset = self.get_queryset().filter(package=package_id, is_deleted=False)
        else:
            queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()  # type: ignore
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_deleted", "is_confirmed", "package_type", "transport_type"]
    search_fields = ["description"]
    ordering_fields = ["id", "description", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        if hasattr(self.request.user, "code"):
            serializer.save(created_by=self.request.user.code)
        else:
            serializer.save(created_by="system")

    @action(detail=False, methods=["get"])
    def active(self, request):
        queryset = self.get_queryset().filter(is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PackageTypeViewSet(viewsets.ModelViewSet):
    queryset = PackageType.objects.all()  # type: ignore
    serializer_class = PackageTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["type", "description"]
    ordering_fields = ["id", "type"]
    ordering = ["type"]


class TransportTypeViewSet(viewsets.ModelViewSet):
    queryset = TransportType.objects.all()  # type: ignore
    serializer_class = TransportTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["type", "description"]
    ordering_fields = ["id", "type"]
    ordering = ["type"]


class MeasureUnitViewSet(viewsets.ModelViewSet):
    queryset = MeasureUnit.objects.all()  # type: ignore
    serializer_class = MeasureUnitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["measure_unit", "description"]
    ordering_fields = ["id", "measure_unit"]
    ordering = ["measure_unit"]
