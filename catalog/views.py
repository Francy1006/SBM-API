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
    lookup_field = "code"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_visible", "is_deleted", "is_confirmed", "chef_recommendation", "item_group", "menu"]

    # FIX: permitir search por menu_name ("menu__menu"), etc.
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
    ordering_fields = ["id", "name", "created_at", "updated_at"]
    ordering = ["-id"]

    def get_queryset(self):
        return (
            Catalog.objects.select_related(
                "menu",
                "item_group",
                "category",
                "type",
                "restriction",
                "usage_instructions",
                "configuration",
                "price",
            ).all()
        )  # type: ignore

    def perform_create(self, serializer):
        try:
            import uuid
            from django.utils import timezone
            from price.models import PriceConfiguration

            with transaction.atomic():
                package = self.request.data.get("package")
                if not package:
                    raise ValueError("El campo 'package' es requerido para crear el catálogo")

                last_config = ItemConfiguration.objects.filter(configuration__startswith="C-").order_by(
                    "-configuration"
                ).first()

                if last_config:
                    last_number = int(last_config.configuration.split("-")[1])
                    new_number = last_number + 1
                else:
                    new_number = 1

                new_config_code = f"C-{new_number:03d}"

                try:
                    package_instance = Package.objects.get(id=package)
                except Package.DoesNotExist:
                    raise ValueError(f"El package con ID {package} no existe")

                item_config = ItemConfiguration.objects.create(
                    code=str(uuid.uuid4()),
                    configuration=new_config_code,
                    description=serializer.validated_data.get("description", ""),
                    package=package_instance,
                )

                serializer.validated_data["configuration"] = item_config

                price_data = serializer.context.get("price_data")
                if not price_data:
                    price_config = PriceConfiguration.objects.filter(price_type=4).first()
                    if not price_config:
                        raise ValueError(
                            "No se encontró una configuración de precio válida para catálogos (price_type=4)."
                        )
                    price_data = {"base_net_amount": 1, "price_configuration": price_config.code}

                price_code = str(uuid.uuid4())
                price_obj = Price._default_manager.create(
                    code=price_code,
                    base_net_amount=price_data["base_net_amount"],
                    gross_amount=0,
                    iva_amount=0,
                    retention_amount=0,
                    price_configuration=price_data["price_configuration"],
                    created_by="5fbf2886-4ad0-11f0-8ce6-0242ac120002",
                    created_at=timezone.now(),
                    price_record_type=4,
                )

                serializer.validated_data["price"] = price_obj

                catalog = serializer.save(created_by="5fbf2886-4ad0-11f0-8ce6-0242ac120002")

                price_obj.record_item_code = catalog.code
                price_obj.save()

        except Exception as e:
            print(f"Error creando item-configuration y price: {str(e)}")
            raise

    @action(detail=False, methods=["get"])
    def visible(self, request):
        queryset = self.get_queryset().filter(is_visible=True, is_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def chef_recommendations(self, request):
        queryset = self.get_queryset().filter(chef_recommendation=True, is_visible=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="foreign-keys-by-code")
    def foreign_keys_by_code(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"detail": "code param is required."}, status=400)
        try:
            catalog = Catalog.objects.get(code=code)  # type: ignore
        except Catalog.DoesNotExist:  # type: ignore
            return Response({"detail": "Catalog not found."}, status=404)

        data = {
            "menu_id": catalog.menu_id,
            "item_group_id": catalog.item_group_id,
            "category_id": catalog.category_id,
            "type_id": catalog.type_id,
            "restriction_id": catalog.restriction_id,
        }
        return Response(data)

    @action(detail=False, methods=["get"], url_path="list")
    def catalog_list(self, request):
        try:
            catalogs = self.filter_queryset(self.get_queryset())

            # map dicts (ids -> names)
            menu_dict = {m.id: m.menu for m in Menu.objects.all()}
            category_dict = {c.id: c.category for c in ItemCategory.objects.all()}
            group_dict = {g.id: g.group_name for g in ItemGroup.objects.all()}
            type_dict = {t.id: t.type for t in ItemType.objects.all()}
            config_dict = {c.code: c.configuration for c in ItemConfiguration.objects.all()}

            results = []
            for catalog in catalogs:
                price_obj = Price.objects.filter(code=catalog.price_id, is_current=True).first()

                results.append(
                    {
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
                        "base_net_amount": price_obj.base_net_amount if price_obj else None,
                        "net_amount": price_obj.net_amount if price_obj else None,
                        "gross_amount": price_obj.gross_amount if price_obj else None,
                        "iva_amount": price_obj.iva_amount if price_obj else None,
                        "aditional_tax_amount": getattr(price_obj, "aditional_tax_amount", None) if price_obj else None,
                        "retention_amount": price_obj.retention_amount if price_obj else None,
                        "price_configuration": price_obj.price_configuration if price_obj else None,
                        "min_quantity_purchase": catalog.min_quantity_purchase,
                        "rations_quantity": catalog.rations_quantity,
                        "item_configuration": catalog.configuration_id,
                        "configuration": config_dict.get(catalog.configuration_id),
                        "is_visible": catalog.is_visible,
                        "is_confirmed": catalog.is_confirmed,
                        "created_at": catalog.created_at,
                    }
                )

            verbose_names = {
                "sku": "SKU",
                "cover_image": "Imagen",
                "menu": "Menú (ID)",
                "menu_name": "Menú",
                "category": "Categoría (ID)",
                "category_name": "Categoría",
                "name": "Nombre",
                "description": "Descripción",
                "obs": "Obs",
                "chef_recommendation": "Recomendación Chef",
                "item_type": "Tipo (ID)",
                "type_name": "Tipo",
                "item_group": "Grupo (ID)",
                "group_name": "Grupo",
                "base_net_amount": "Valor Base Neto",
                "net_amount": "Valor Neto",
                "gross_amount": "Valor Bruto",
                "iva_amount": "IVA",
                "aditional_tax_amount": "Impuesto Adicional",
                "retention_amount": "Retención",
                "price_configuration": "Configuración Precio",
                "min_quantity_purchase": "Compra Mínima",
                "rations_quantity": "Raciones",
                "item_configuration": "Item Config (Code)",
                "configuration": "Configuración",
                "is_visible": "Visible",
                "is_confirmed": "Confirmado",
                "created_at": "Creado",
            }

            page = self.paginate_queryset(results)
            if page is not None:
                ser = CatalogListSerializer(page, many=True)
                return self.get_paginated_response({"results": ser.data, "verbose_names": verbose_names})

            ser = CatalogListSerializer(results, many=True)
            return Response({"results": ser.data, "verbose_names": verbose_names})

        except Exception as e:
            return Response({"error": f"Error obteniendo lista de catálogos: {str(e)}"}, status=500)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # type: ignore
    serializer_class = ProductSerializer
    lookup_field = "sku"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active", "is_deleted", "is_confirmed", "provider", "type", "item_group", "category"]
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
            print(f"Error executing price calculation for product {product.sku}: {str(e)}")

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
            if base_net_amount_new is not None and str(price_obj.base_net_amount) != str(base_net_amount_new):
                changed = True
            if price_configuration_new is not None and str(price_obj.price_configuration) != str(price_configuration_new):
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
                current_price = Price.objects.filter(code=product.price, is_current=True).first()

                price_config = None
                if current_price:
                    price_config = PriceConfiguration.objects.filter(code=current_price.price_configuration).first()

                results.append(
                    {
                        "code": product.code,
                        "sku": product.sku,
                        "description": product.description,
                        "base_net_amount": current_price.base_net_amount if current_price else 0,
                        "net_amount": current_price.net_amount if current_price else 0,
                        "gross_amount": current_price.gross_amount if current_price else 0,
                        "iva_amount": current_price.iva_amount if current_price else 0,
                        "aditional_tax_amount": getattr(current_price, "aditional_tax_amount", 0) if current_price else 0,
                        "retention_amount": current_price.retention_amount if current_price else 0,
                        "price_configuration": current_price.price_configuration if current_price else None,
                        "price_configuration_label": price_config.price_configuration if price_config else None,
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
                return self.get_paginated_response({"results": serializer.data, "verbose_names": verbose_names})

            serializer = ProductListSerializer(results, many=True)
            return Response({"results": serializer.data, "verbose_names": verbose_names})

        except Exception as e:
            return Response({"error": f"Error obteniendo lista de productos: {str(e)}"}, status=500)

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
    filterset_fields = ["is_active", "is_deleted", "is_confirmed", "provider", "type", "group", "category"]
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
    filterset_fields = ["is_active", "is_deleted", "is_confirmed", "provider", "type", "group", "category"]
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
    queryset = ItemGroup.objects.all()  # type: ignore
    serializer_class = ItemGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["catalog_render"]
    search_fields = ["group_name", "description"]
    ordering_fields = ["id", "group_name"]
    ordering = ["group_name"]


class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()  # type: ignore
    serializer_class = ItemCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["catalog_render"]
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
    queryset = Restriction.objects.all()  # type: ignore
    serializer_class = RestrictionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_deleted", "is_confirmed"]
    search_fields = ["restriction", "description"]
    ordering_fields = ["id", "restriction", "created_at"]
    ordering = ["restriction"]


class InstructionViewSet(viewsets.ModelViewSet):
    queryset = Instruction.objects.all()  # type: ignore
    serializer_class = InstructionSerializer
    lookup_field = "code"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_deleted", "is_confirmed", "type"]
    search_fields = ["instruction", "description"]
    ordering_fields = ["code", "instruction", "created_at"]
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