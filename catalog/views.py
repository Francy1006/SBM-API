from django.db import models, transaction
from django.utils import timezone
from django.shortcuts import render  # noqa: F401

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

import uuid
from price.models import Price, PriceConfiguration
from catalog.models import ItemConfigurationDetail
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
)

from inventory.models import Package, PackageType, TransportType, MeasureUnit


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

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        raw_user_code = getattr(getattr(request, "user", None), "code", None)
        created_by = str(raw_user_code).strip() if raw_user_code is not None else ""
        if not created_by:
            return Response(
                {"detail": "Usuario inválido para created_by."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for k in ("created_by", "updated_by", "deleted_by", "confirmed_by"):
            data.pop(k, None)
        data["created_by"] = created_by

        with transaction.atomic():
            if not data.get("configuration"):
                sku = data.get("sku")
                if not sku:
                    return Response(
                        {"detail": "sku es requerido."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                package_id = data.get("package")
                if package_id in ("", None):
                    return Response(
                        {"detail": "package es requerido."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    package_id = int(package_id)
                except Exception:
                    return Response(
                        {"detail": "package debe ser int."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                cfg_code = str(uuid.uuid4())

                ItemConfiguration.objects.create(
                    code=cfg_code,
                    configuration=str(sku)[:50],
                    description=(data.get("description") or "Auto"),
                    package_id=package_id,
                    created_by=created_by,
                )
                data["configuration"] = cfg_code

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

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
        )
        return Response({"deleted": updated}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="list")
    def catalog_list(self, request):
        try:
            qs = self.filter_queryset(self.get_queryset())
            qs = self._apply_ordering_aliases(request, qs)

            page_qs = self.paginate_queryset(qs)
            if page_qs is None:
                page_qs = qs

            menu_dict = {
                m.id: {
                    "menu": m.menu,
                    "background_color": m.background_color,
                    "text_color": m.text_color,
                }
                for m in Menu.objects.only(
                    "id", "menu", "background_color", "text_color"
                )
            }
            category_dict = dict(ItemCategory.objects.values_list("id", "category"))
            group_dict = dict(ItemGroup.objects.values_list("id", "group_name"))
            type_dict = dict(ItemType.objects.values_list("id", "type"))
            config_dict = dict(
                ItemConfiguration.objects.values_list("code", "configuration")
            )

            price_codes = [c.price_id for c in page_qs if c.price_id is not None]
            price_map = {
                p.code: p
                for p in Price.objects.filter(
                    code__in=price_codes, is_current=True
                ).select_related("price_configuration")
            }

            results = []
            for catalog in page_qs:
                price_obj = price_map.get(catalog.price_id)
                pc = (
                    getattr(price_obj, "price_configuration", None)
                    if price_obj
                    else None
                )

                results.append(
                    {
                        "sku": catalog.sku,
                        "cover_image": catalog.cover_image,
                        "menu": catalog.menu_id,
                        "menu_name": menu_dict.get(catalog.menu_id, {}).get("menu"),
                        "menu_background_color": menu_dict.get(catalog.menu_id, {}).get(
                            "background_color"
                        ),
                        "menu_text_color": menu_dict.get(catalog.menu_id, {}).get(
                            "text_color"
                        ),
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
                        # ✅ NUNCA devolver objetos (PriceConfiguration) en JSON
                        "base_net_amount": getattr(price_obj, "base_net_amount", None),
                        "net_amount": getattr(price_obj, "net_amount", None),
                        "gross_amount": getattr(price_obj, "gross_amount", None),
                        "iva_amount": getattr(price_obj, "iva_amount", None),
                        "price_configuration": getattr(pc, "code", None),
                        "price_configuration_label": getattr(
                            pc, "price_configuration", None
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

            if getattr(self, "paginator", None) is not None:
                return self.get_paginated_response(
                    {"results": results, "verbose_names": {}}
                )

            return Response({"results": results, "verbose_names": {}})

        except Exception as e:
            return Response(
                {"error": f"Error obteniendo lista de catálogos: {str(e)}"},
                status=500,
            )

    # ===============================
    # HISTORICAL PRICES (CATALOG)
    # ===============================

    @action(detail=True, methods=["get"], url_path="prices")
    def prices(self, request, sku=None):
        catalog = self.get_object()

        prices = (
            Price.objects.filter(record_item_code=catalog.code)  # 🔥 CLAVE
            .order_by("created_at")
            .values(
                "code",
                "base_net_amount",
                "created_at",
                "is_current",
            )
        )

        return Response(list(prices))

    # ===============================
    # UPDATE WITH VERSIONED PRICE (CATALOG)
    # ===============================

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        price_data = request.data.get("price_data")

        if not price_data:
            return super().partial_update(request, *args, **kwargs)

        price_obj = instance.price

        if not price_obj:
            return Response(
                {"detail": "Precio actual no encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base_net_amount_new = price_data.get("base_net_amount")
        price_configuration_new = price_data.get("price_configuration")

        try:
            base_net_amount_new = int(base_net_amount_new)
        except Exception:
            return Response(
                {"detail": "base_net_amount inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_pc = (
            price_obj.price_configuration.code
            if price_obj.price_configuration
            else None
        )

        changed = int(
            price_obj.base_net_amount
        ) != base_net_amount_new or current_pc != str(price_configuration_new)

        if not changed:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        with transaction.atomic():

            price_obj.is_current = False
            price_obj.save(update_fields=["is_current"])

            price_conf_obj = PriceConfiguration.objects.filter(
                code=str(price_configuration_new).strip()
            ).first()

            if not price_conf_obj:
                return Response(
                    {"detail": "PriceConfiguration inválido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_price = Price.objects.create(
                base_net_amount=base_net_amount_new,
                net_amount=base_net_amount_new,
                gross_amount=price_obj.gross_amount,
                iva_amount=price_obj.iva_amount,
                aditional_tax_amount=price_obj.aditional_tax_amount,
                retention_amount=price_obj.retention_amount,
                price_configuration=price_conf_obj,
                record_item_code=instance.code,  # 🔥 importante
                price_record_type=1,
                is_current=True,
                created_by=getattr(request.user, "code", "system"),
                created_at=timezone.now(),
            )

            instance.price = new_price
            instance.save(update_fields=["price"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path=r"adv/(?P<sku>[^/.]+)")
    def adv(self, request, sku=None):
        try:
            catalog = self.get_queryset().filter(sku=sku).first()
            if not catalog:
                return Response(
                    {"detail": "Catálogo no encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ asegurar select_related price_configuration para no devolver objeto crudo
            price_obj = (
                Price.objects.filter(code=catalog.price_id, is_current=True)
                .select_related("price_configuration")
                .first()
            )
            pc = getattr(price_obj, "price_configuration", None) if price_obj else None

            instr = getattr(catalog, "usage_instructions", None)
            instr_type = getattr(instr, "type", None) if instr else None
            restriction = getattr(catalog, "restriction", None)

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
                "code_uuid": getattr(catalog, "code", None),
                "obs": getattr(catalog, "obs", None),
                "secondary_image": getattr(catalog, "secondary_image", None),
                "complementary_image": getattr(catalog, "complementary_image", None),
                "image_gallery": getattr(catalog, "image_gallery", None),
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
                "restriction_name": getattr(restriction, "restriction", None),
                "restriction_description": getattr(restriction, "description", None),
                "usage_instruction": getattr(instr, "instruction", None),
                "usage_instruction_description": getattr(instr, "description", None),
                "usage_instruction_url": getattr(instr, "url_documentation", None),
                "usage_instruction_type_id": getattr(instr, "type_id", None),
                "usage_instruction_type_name": getattr(instr_type, "type", None),
                "price_code": getattr(price_obj, "code", None),
                # ✅ NO objeto
                "price_configuration": getattr(pc, "code", None),
                "price_configuration_label": getattr(pc, "price_configuration", None),
                "base_net_amount": getattr(price_obj, "base_net_amount", None),
                "net_amount": getattr(price_obj, "net_amount", None),
                "gross_amount": getattr(price_obj, "gross_amount", None),
                "iva_amount": getattr(price_obj, "iva_amount", None),
                "aditional_tax_amount": getattr(
                    price_obj, "aditional_tax_amount", None
                ),
                "retention_amount": getattr(price_obj, "retention_amount", None),
                "price_is_current": getattr(price_obj, "is_current", None),
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
                "price_configuration_label": "Config. precio (nombre)",
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

    def _safe_float(self, v, default=0.0):
        try:
            if v is None or v == "":
                return default
            return float(v)
        except Exception:
            return default

    def _sum_rows(self, rows):
        count = 0
        sub_net = 0.0
        sub_gross = 0.0
        sub_iva = 0.0

        for r in rows:
            count += 1
            sub_net += self._safe_float(r.get("net_amount"), 0.0)
            sub_gross += self._safe_float(r.get("gross_amount"), 0.0)
            sub_iva += self._safe_float(r.get("iva_amount"), 0.0)

        return {
            "count": count,
            "sub_total_net": sub_net,
            "sub_total_gross": sub_gross,
            "sub_total_iva": sub_iva,
        }

    def _serialize_detail_row(self, d, obj=None, item_kind=None):

        from accounting.models import FiscalDirective

        q = self._safe_float(getattr(d, "quantity", 1), 1.0)
        if q <= 0:
            q = 1.0

        price_obj = getattr(obj, "price", None)

        unit_net = float(price_obj.base_net_amount or 0) if price_obj else 0.0

        iva_directive = (
            FiscalDirective.objects.filter(fiscal_directive="IVA")
            .filter(Q(is_deleted__isnull=True) | Q(is_deleted=False))
            .order_by("-year")
            .first()
        )

        iva_rate = float(iva_directive.value) if iva_directive else 0.0

        unit_iva = unit_net * iva_rate
        unit_gross = unit_net + unit_iva

        return {
            "detail_code": getattr(d, "code", None),
            "detail": getattr(d, "detail", None),
            "type_id": getattr(d, "type_id", None),
            "item_kind": item_kind,
            "item_code": getattr(d, "id_item", None),
            "item_sku": getattr(obj, "sku", None),
            "description": getattr(obj, "description", None),
            "obs": getattr(obj, "obs", None),
            "quantity": q,
            "unit_net": unit_net,
            "unit_iva": unit_iva,
            "unit_gross": unit_gross,
            "net_amount": unit_net * q,
            "iva_amount": unit_iva * q,
            "gross_amount": unit_gross * q,
        }

    @action(detail=True, methods=["get", "post"], url_path="config")
    def config(self, request, sku=None):

        from accounting.models import FiscalDirective

        catalog = self.get_queryset().filter(sku=sku).first()
        if not catalog:
            return Response(
                {"detail": "Catálogo no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cfg = getattr(catalog, "configuration", None)

        # ==========================================
        # 🔥 POST → GUARDAR CONFIGURACIÓN
        # ==========================================
        if request.method == "POST":

            if not cfg:
                return Response(
                    {"detail": "Configuración no encontrada."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ItemConfigurationDetail.objects.filter(configuration_id=cfg.code).delete()

            products = request.data.get("products", [])
            materials = request.data.get("materials", [])
            services = request.data.get("services", [])

            def create_details(rows, type_id):
                for r in rows:
                    item_sku = r.get("item_sku")
                    if not item_sku:
                        continue

                    # 🔥 buscar el objeto real
                    obj = None
                    if type_id == 1:
                        obj = Product.objects.filter(sku=item_sku).first()
                    elif type_id == 2:
                        obj = Material.objects.filter(sku=item_sku).first()
                    elif type_id == 3:
                        obj = Service.objects.filter(sku=item_sku).first()

                    if not obj:
                        continue

                    ItemConfigurationDetail.objects.create(
                        configuration_id=cfg.code,
                        id_item=obj.code,  # 🔥 guardar UUID real
                        detail=r.get("detail", ""),
                        quantity=int(r.get("quantity") or 1),
                        type_id=type_id,
                        created_by=getattr(request.user, "code", "system"),
                    )

            create_details(products, 1)
            create_details(materials, 2)
            create_details(services, 3)

            return Response(
                {"detail": "Configuración actualizada correctamente."},
                status=status.HTTP_200_OK,
            )

        # ==========================================
        # 🟢 GET → DEVOLVER CONFIGURACIÓN
        # ==========================================

        price_obj = (
            Price.objects.filter(code=catalog.price_id, is_current=True)
            .select_related("price_configuration")
            .first()
        )

        pc = getattr(price_obj, "price_configuration", None) if price_obj else None

        from accounting.models import FiscalDirective

        iva_directive = (
            FiscalDirective.objects.filter(fiscal_directive="IVA", is_confirmed=True)
            .filter(Q(is_deleted__isnull=True) | Q(is_deleted=False))
            .order_by("-year", "-month", "-id")
            .first()
        )

        if not iva_directive:
            return Response(
                {"detail": "IVA no encontrado en fiscal_directive."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        iva_rate = float(iva_directive.value)

        # ------------------------
        # INFORMATIVE
        # ------------------------
        informativa_data = {
            "item_configuration_code": getattr(cfg, "code", None),
            "item_configuration_name": getattr(cfg, "configuration", None),
            "price_code": getattr(price_obj, "code", None),
            "price_configuration": getattr(pc, "code", None),
            "price_configuration_label": getattr(pc, "price_configuration", None),
            "base_net_amount": getattr(price_obj, "base_net_amount", None),
            "price_is_current": getattr(price_obj, "is_current", None),
        }

        # ------------------------
        # LINKING
        # ------------------------
        products_rows = []
        materials_rows = []
        services_rows = []

        if cfg and getattr(cfg, "code", None):

            details = ItemConfigurationDetail.objects.filter(
                configuration_id=cfg.code
            ).order_by("created_at")

            id_items = [d.id_item for d in details if d.id_item]

            prod_map = {
                p.code: p
                for p in Product.objects.filter(code__in=id_items).select_related(
                    "price"
                )
            }

            mat_map = {m.code: m for m in Material.objects.filter(code__in=id_items)}
            srv_map = {s.code: s for s in Service.objects.filter(code__in=id_items)}

            for d in details:
                item_code = d.id_item
                if not item_code:
                    continue

                if item_code in prod_map:
                    products_rows.append(
                        self._serialize_detail_row(d, prod_map[item_code], "product")
                    )
                elif item_code in mat_map:
                    materials_rows.append(
                        self._serialize_detail_row(d, mat_map[item_code], "material")
                    )
                elif item_code in srv_map:
                    services_rows.append(
                        self._serialize_detail_row(d, srv_map[item_code], "service")
                    )

        subtotals_products = self._sum_rows(products_rows)
        subtotals_materials = self._sum_rows(materials_rows)
        subtotals_services = self._sum_rows(services_rows)

        totals = {
            "count": (
                subtotals_products["count"]
                + subtotals_materials["count"]
                + subtotals_services["count"]
            ),
            "sub_total_net": (
                subtotals_products["sub_total_net"]
                + subtotals_materials["sub_total_net"]
                + subtotals_services["sub_total_net"]
            ),
            "sub_total_gross": (
                subtotals_products["sub_total_gross"]
                + subtotals_materials["sub_total_gross"]
                + subtotals_services["sub_total_gross"]
            ),
            "sub_total_iva": (
                subtotals_products["sub_total_iva"]
                + subtotals_materials["sub_total_iva"]
                + subtotals_services["sub_total_iva"]
            ),
        }

        # ------------------------
        # CALCULATION VARIABLES (NO RESULTADOS)
        # ------------------------
        calculation_props = {
            "code": getattr(pc, "code", None),
            "baseNetAmount": getattr(price_obj, "base_net_amount", None),
            "iva": iva_rate,
            "total_neto_productos": subtotals_products["sub_total_net"],
            "total_neto_materiales": subtotals_materials["sub_total_net"],
            "total_neto_servicios": subtotals_services["sub_total_net"],
            "costo_neto": totals["sub_total_net"],
            "iva_costo": totals["sub_total_iva"],
        }

        linking = {
            "header": {
                "item_configuration_code": getattr(cfg, "code", None),
                "item_configuration_name": getattr(cfg, "configuration", None),
                "base_net_amount": getattr(price_obj, "base_net_amount", None),
            },
            "totals": totals,
            "products": {
                "links": products_rows,
                "subtotals": subtotals_products,
                "searchBaseUrl": "/products/?search=",
            },
            "materials": {
                "links": materials_rows,
                "subtotals": subtotals_materials,
                "searchBaseUrl": "/materials/?search=",
            },
            "services": {
                "links": services_rows,
                "subtotals": subtotals_services,
                "searchBaseUrl": "/services/?search=",
            },
        }

        return Response(
            {
                "informativa": {
                    "data": informativa_data,
                    "verbose_names": {},
                },
                "calculation": {"props": calculation_props},
                "linking": linking,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="cost-prices")
    def cost_prices(self, request, sku=None):
        """
        Devuelve histórico de costo_neto basado en precios versionados de items vinculados.
        - Junta todas las fechas de cambios de precios de items.
        - Para cada fecha, toma el último precio <= fecha por item y suma (base_net_amount * qty).
        """
        catalog = self.get_queryset().filter(sku=sku).first()
        if not catalog:
            return Response(
                {"detail": "Catálogo no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        cfg = getattr(catalog, "configuration", None)
        if not cfg:
            return Response([], status=status.HTTP_200_OK)

        details = ItemConfigurationDetail.objects.filter(
            configuration_id=cfg.code
        ).order_by("created_at")

        item_codes = [d.id_item for d in details if d.id_item]
        if not item_codes:
            return Response([], status=status.HTTP_200_OK)

        # Mapa qty por item
        qty_map = {}
        for d in details:
            if not d.id_item:
                continue
            try:
                qty_map[d.id_item] = float(d.quantity or 1)
            except Exception:
                qty_map[d.id_item] = 1.0

        # Traer TODOS los precios versionados de esos items (por record_item_code)
        # Nota: aquí asumimos que el versionado usa record_item_code=item.code (como en Product/Catalog)
        price_rows = (
            Price.objects.filter(record_item_code__in=item_codes)
            .values("record_item_code", "base_net_amount", "created_at", "is_current")
            .order_by("created_at")
        )

        price_rows = list(price_rows)
        if not price_rows:
            # Si no hay históricos, devolvemos 1 punto (costo actual = 0)
            return Response([], status=status.HTTP_200_OK)

        # Timeline = todas las fechas de cambios
        timeline = sorted({p["created_at"] for p in price_rows if p.get("created_at")})

        # Indexar precios por item, ordenados
        by_item = {}
        for p in price_rows:
            code = p["record_item_code"]
            by_item.setdefault(code, []).append(p)

        # helper: último precio <= t
        def latest_price_at(item_code, t):
            arr = by_item.get(item_code) or []
            last = None
            for p in arr:
                if p["created_at"] <= t:
                    last = p
                else:
                    break
            return last

        out = []
        for t in timeline:
            total = 0.0
            for item_code in item_codes:
                lp = latest_price_at(item_code, t)
                if not lp:
                    continue
                try:
                    unit = float(lp.get("base_net_amount") or 0)
                except Exception:
                    unit = 0.0
                q = qty_map.get(item_code, 1.0)
                total += unit * q

            out.append(
                {
                    "created_at": t,
                    "costo_neto": round(total, 2),
                }
            )

        # marcar último como current (para pintar verde)
        if out:
            out[-1]["is_current"] = True
            for i in range(len(out) - 1):
                out[i]["is_current"] = False

        return Response(out, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        "provider",
        "type",
        "item_group",
        "category",
        "package",
        "price",
        "price__price_configuration",
    )
    serializer_class = ProductSerializer
    lookup_field = "code"

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
    ordering_fields = "__all__"
    ordering = ["-id"]

    # ===============================
    # CREATE
    # ===============================

    def perform_create(self, serializer):
        serializer.save(created_by=getattr(self.request.user, "code", "system"))

    # ===============================
    # UPDATE WITH VERSIONED PRICE
    # ===============================

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        price_data = request.data.get("price_data")

        # 🔵 Si no viene price_data → update normal
        if not price_data:
            return super().partial_update(request, *args, **kwargs)

        price_obj = instance.price

        if not price_obj:
            return Response(
                {"detail": "Precio actual no encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base_net_amount_new = price_data.get("base_net_amount")
        price_configuration_new = price_data.get("price_configuration")

        try:
            base_net_amount_new = int(base_net_amount_new)
        except Exception:
            return Response(
                {"detail": "base_net_amount inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_pc = (
            price_obj.price_configuration.code
            if price_obj.price_configuration
            else None
        )

        changed = int(
            price_obj.base_net_amount
        ) != base_net_amount_new or current_pc != str(price_configuration_new)

        if not changed:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        with transaction.atomic():

            # 🔴 Desactivar precio actual
            price_obj.is_current = False
            price_obj.save(update_fields=["is_current"])

            # 🔵 Buscar nueva configuración
            price_conf_obj = PriceConfiguration.objects.filter(
                code=str(price_configuration_new).strip()
            ).first()

            if not price_conf_obj:
                return Response(
                    {"detail": "PriceConfiguration inválido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 🟢 Crear nueva versión
            new_price = Price.objects.create(
                base_net_amount=base_net_amount_new,
                net_amount=0,
                gross_amount=0,
                iva_amount=0,
                aditional_tax_amount=0,
                retention_amount=0,
                price_configuration=price_conf_obj,
                record_item_code=instance.code,
                price_record_type=1,
                is_current=True,
                created_by=getattr(request.user, "code", "system"),
                created_at=timezone.now(),
            )

            formula_obj = getattr(price_conf_obj, "variable_formula", None)

            if formula_obj and formula_obj.price_variables:

                formula = formula_obj.price_variables

                from accounting.models import FiscalConfigurationDetail, FiscalDirective

                context = {"base_net_amount": new_price.base_net_amount}

                fiscal_details = FiscalConfigurationDetail.objects.filter(
                    price_configuration=price_conf_obj.code
                )

                directive_codes = fiscal_details.values_list(
                    "fiscal_directive", flat=True
                )
                directives = FiscalDirective.objects.filter(code__in=directive_codes)
                directive_map = {d.code: d for d in directives}

                for detail in fiscal_details:
                    directive = directive_map.get(detail.fiscal_directive)
                    if directive and detail.var:
                        context[detail.var] = float(directive.value)

                results = {}

                for line in formula.split(";"):

                    if "=" not in line:
                        continue

                    key, expr = line.split("=")
                    key = key.strip()
                    expr = expr.strip()

                    for var, val in context.items():
                        expr = expr.replace(var, str(val))

                    results[key] = eval(expr)

                new_price.net_amount = int(results.get("net_amount", 0))
                new_price.iva_amount = int(results.get("iva_amount", 0))
                new_price.gross_amount = int(results.get("gross_amount", 0))
                new_price.aditional_tax_amount = int(
                    results.get("aditional_tax_amount", 0)
                )
                new_price.retention_amount = int(results.get("retention_amount", 0))

                new_price.save()

            # 🔗 Vincular nuevo price
            instance.price = new_price
            instance.save(update_fields=["price"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ===============================
    # QUERYSET OPTIMIZED
    # ===============================

    def get_queryset(self):
        return Product.objects.select_related(
            "provider",
            "type",
            "item_group",
            "category",
            "package",
            "price",
            "price__price_configuration",
        )

    # ===============================
    # HISTORICAL PRICES
    # ===============================

    @action(detail=True, methods=["get"], url_path="prices")
    def prices(self, request, code=None):
        product = self.get_object()

        prices = (
            Price.objects.filter(record_item_code=product.code)
            .order_by("created_at")
            .values(
                "code",
                "base_net_amount",
                "created_at",
                "is_current",  # 🔥 necesario para pintar verde/amarillo
            )
        )

        return Response(list(prices))

    # ===============================
    # CONFIG VIEW
    # ===============================

    @action(detail=True, methods=["get"], url_path="config")
    def config(self, request, code=None):

        product = self.get_object()
        price_obj = product.price
        pc = getattr(price_obj, "price_configuration", None) if price_obj else None

        informativa_data = {
            "product_code": product.code,
            "product_sku": product.sku,
            "price_code": getattr(price_obj, "code", None),
            "price_configuration": getattr(pc, "code", None),
            "price_configuration_label": getattr(pc, "price_configuration", None),
            "base_net_amount": getattr(price_obj, "base_net_amount", None),
            "price_is_current": getattr(price_obj, "is_current", None),
        }

        calculation_props = {
            "code": getattr(pc, "code", None),
            "baseNetAmount": getattr(price_obj, "base_net_amount", None),
            "additionalTaxAmount": getattr(price_obj, "aditional_tax_amount", None),
            "retentionAmount": getattr(price_obj, "retention_amount", None),
            "selectedProductSku": product.sku,
        }

        return Response(
            {
                "informativa": {
                    "data": informativa_data,
                    "verbose_names": {},
                },
                "calculation": {"props": calculation_props},
                "linking": None,
            },
            status=status.HTTP_200_OK,
        )

    # ===============================
    # LOOKUP
    # ===============================

    @action(detail=False, methods=["get"], url_path="lookup")
    def lookup(self, request):
        q = (request.query_params.get("q") or "").strip()

        if not q:
            return Response({"results": []})

        qs = Product.objects.filter(
            Q(sku__icontains=q)
            | models.Q(description__icontains=q)
            | models.Q(obs__icontains=q)
        ).order_by("description")[:20]

        results = [
            {"sku": p.sku, "description": p.description, "obs": p.obs} for p in qs
        ]

        return Response({"results": results})


class MaterialViewSet(viewsets.ModelViewSet):

    queryset = Material.objects.select_related(
        "provider",
        "type",
        "item_group",
        "category",
        "package",
        "price",
        "price__price_configuration",
    )

    serializer_class = MaterialSerializer
    lookup_field = "code"

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

    search_fields = [
        "description",
        "sku",
        "code",
        "obs",
    ]

    ordering_fields = "__all__"
    ordering = ["-id"]

    # ===============================
    # CREATE
    # ===============================

    def perform_create(self, serializer):
        serializer.save(created_by=getattr(self.request.user, "code", "system"))

    # ===============================
    # UPDATE WITH VERSIONED PRICE
    # ===============================

    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()
        price_data = request.data.get("price_data")

        if not price_data:
            return super().partial_update(request, *args, **kwargs)

        price_obj = instance.price

        if not price_obj:
            return Response(
                {"detail": "Precio actual no encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base_net_amount_new = price_data.get("base_net_amount")
        price_configuration_new = price_data.get("price_configuration")

        try:
            base_net_amount_new = int(base_net_amount_new)
        except Exception:
            return Response(
                {"detail": "base_net_amount inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_pc = (
            price_obj.price_configuration.code
            if price_obj.price_configuration
            else None
        )

        changed = int(price_obj.base_net_amount) != base_net_amount_new or current_pc != str(price_configuration_new)

        if not changed:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        with transaction.atomic():

            price_obj.is_current = False
            price_obj.save(update_fields=["is_current"])

            price_conf_obj = PriceConfiguration.objects.filter(
                code=str(price_configuration_new).strip()
            ).first()

            if not price_conf_obj:
                return Response(
                    {"detail": "PriceConfiguration inválido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_price = Price.objects.create(
                base_net_amount=base_net_amount_new,
                net_amount=0,
                gross_amount=0,
                iva_amount=0,
                aditional_tax_amount=0,
                retention_amount=0,
                price_configuration=price_conf_obj,
                record_item_code=instance.code,
                price_record_type=1,
                is_current=True,
                created_by=getattr(request.user, "code", "system"),
                created_at=timezone.now(),
            )

            formula_obj = getattr(price_conf_obj, "variable_formula", None)

            if formula_obj and formula_obj.price_variables:

                formula = formula_obj.price_variables

                from accounting.models import FiscalConfigurationDetail, FiscalDirective

                context = {"base_net_amount": new_price.base_net_amount}

                fiscal_details = FiscalConfigurationDetail.objects.filter(
                    price_configuration=price_conf_obj.code
                )

                directive_codes = fiscal_details.values_list("fiscal_directive", flat=True)
                directives = FiscalDirective.objects.filter(code__in=directive_codes)

                directive_map = {d.code: d for d in directives}

                for detail in fiscal_details:
                    directive = directive_map.get(detail.fiscal_directive)
                    if directive and detail.var:
                        context[detail.var] = float(directive.value)

                results = {}

                for line in formula.split(";"):

                    if "=" not in line:
                        continue

                    key, expr = line.split("=")
                    key = key.strip()
                    expr = expr.strip()

                    for var, val in context.items():
                        expr = expr.replace(var, str(val))

                    results[key] = eval(expr)

                new_price.net_amount = int(results.get("net_amount", 0))
                new_price.iva_amount = int(results.get("iva_amount", 0))
                new_price.gross_amount = int(results.get("gross_amount", 0))
                new_price.aditional_tax_amount = int(results.get("aditional_tax_amount", 0))
                new_price.retention_amount = int(results.get("retention_amount", 0))

                new_price.save()

            instance.price = new_price
            instance.save(update_fields=["price"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ===============================
    # HISTORICAL PRICES
    # ===============================

    @action(detail=True, methods=["get"], url_path="prices")
    def prices(self, request, code=None):

        material = self.get_object()

        prices = (
            Price.objects.filter(record_item_code=material.code)
            .order_by("created_at")
            .values(
                "code",
                "base_net_amount",
                "created_at",
                "is_current",
            )
        )

        return Response(list(prices))

    # ===============================
    # CONFIG VIEW
    # ===============================

    @action(detail=True, methods=["get"], url_path="config")
    def config(self, request, code=None):

        material = self.get_object()

        price_obj = material.price
        pc = getattr(price_obj, "price_configuration", None) if price_obj else None

        informativa_data = {
            "material_code": material.code,
            "material_sku": material.sku,
            "price_code": getattr(price_obj, "code", None),
            "price_configuration": getattr(pc, "code", None),
            "price_configuration_label": getattr(pc, "price_configuration", None),
            "base_net_amount": getattr(price_obj, "base_net_amount", None),
            "price_is_current": getattr(price_obj, "is_current", None),
        }

        calculation_props = {
            "code": getattr(pc, "code", None),
            "baseNetAmount": getattr(price_obj, "base_net_amount", None),
            "additionalTaxAmount": getattr(price_obj, "aditional_tax_amount", None),
            "retentionAmount": getattr(price_obj, "retention_amount", None),
            "selectedMaterialSku": material.sku,
        }

        return Response(
            {
                "informativa": {
                    "data": informativa_data,
                    "verbose_names": {},
                },
                "calculation": {"props": calculation_props},
                "linking": None,
            },
            status=status.HTTP_200_OK,
        )


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.select_related(
        "provider",
        "type",
        "item_group",
        "category",
        "price",
        "price__price_configuration",
    )
    serializer_class = ServiceSerializer
    lookup_field = "code"
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
    ordering_fields = "__all__"
    ordering = ["-id"]

    def perform_create(self, serializer):
        serializer.save(created_by=getattr(self.request.user, "code", "system"))

    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()
        price_data = request.data.get("price_data")

        if not price_data:
            return super().partial_update(request, *args, **kwargs)

        price_obj = instance.price

        if not price_obj:
            return Response(
                {"detail": "Precio actual no encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base_net_amount_new = price_data.get("base_net_amount")
        price_configuration_new = price_data.get("price_configuration")

        try:
            base_net_amount_new = int(base_net_amount_new)
        except Exception:
            return Response(
                {"detail": "base_net_amount inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_pc = (
            price_obj.price_configuration.code
            if price_obj.price_configuration
            else None
        )

        changed = int(price_obj.base_net_amount) != base_net_amount_new or current_pc != str(price_configuration_new)

        if not changed:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        with transaction.atomic():

            price_obj.is_current = False
            price_obj.save(update_fields=["is_current"])

            price_conf_obj = PriceConfiguration.objects.filter(
                code=str(price_configuration_new).strip()
            ).first()

            if not price_conf_obj:
                return Response(
                    {"detail": "PriceConfiguration inválido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_price = Price.objects.create(
                base_net_amount=base_net_amount_new,
                net_amount=0,
                gross_amount=0,
                iva_amount=0,
                aditional_tax_amount=0,
                retention_amount=0,
                price_configuration=price_conf_obj,
                record_item_code=instance.code,
                price_record_type=3,
                is_current=True,
                created_by=getattr(request.user, "code", "system"),
                created_at=timezone.now(),
            )

            formula_obj = getattr(price_conf_obj, "variable_formula", None)

            if formula_obj and formula_obj.price_variables:

                formula = formula_obj.price_variables

                from accounting.models import FiscalConfigurationDetail, FiscalDirective

                context = {"base_net_amount": new_price.base_net_amount}

                fiscal_details = FiscalConfigurationDetail.objects.filter(
                    price_configuration=price_conf_obj.code
                )

                directive_codes = fiscal_details.values_list("fiscal_directive", flat=True)
                directives = FiscalDirective.objects.filter(code__in=directive_codes)

                directive_map = {d.code: d for d in directives}

                for detail in fiscal_details:
                    directive = directive_map.get(detail.fiscal_directive)
                    if directive and detail.var:
                        context[detail.var] = float(directive.value)

                results = {}

                for line in formula.split(";"):

                    if "=" not in line:
                        continue

                    key, expr = line.split("=")
                    key = key.strip()
                    expr = expr.strip()

                    for var, val in context.items():
                        expr = expr.replace(var, str(val))

                    results[key] = eval(expr)

                new_price.net_amount = int(results.get("net_amount", 0))
                new_price.iva_amount = int(results.get("iva_amount", 0))
                new_price.gross_amount = int(results.get("gross_amount", 0))
                new_price.aditional_tax_amount = int(results.get("aditional_tax_amount", 0))
                new_price.retention_amount = int(results.get("retention_amount", 0))

                new_price.save()

            instance.price = new_price
            instance.save(update_fields=["price"])

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="prices")
    def prices(self, request, code=None):

        service = self.get_object()

        prices = (
            Price.objects.filter(record_item_code=service.code)
            .order_by("created_at")
            .values(
                "code",
                "base_net_amount",
                "created_at",
                "is_current",
            )
        )

        return Response(list(prices))

    @action(detail=True, methods=["get"], url_path="config")
    def config(self, request, code=None):

        service = self.get_object()

        price_obj = service.price
        pc = getattr(price_obj, "price_configuration", None) if price_obj else None

        informativa_data = {
            "service_code": service.code,
            "service_sku": service.sku,
            "price_code": getattr(price_obj, "code", None),
            "price_configuration": getattr(pc, "code", None),
            "price_configuration_label": getattr(pc, "price_configuration", None),
            "base_net_amount": getattr(price_obj, "base_net_amount", None),
            "price_is_current": getattr(price_obj, "is_current", None),
        }

        calculation_props = {
            "code": getattr(pc, "code", None),
            "baseNetAmount": getattr(price_obj, "base_net_amount", None),
            "additionalTaxAmount": getattr(price_obj, "aditional_tax_amount", None),
            "retentionAmount": getattr(price_obj, "retention_amount", None),
            "selectedServiceSku": service.sku,
        }

        return Response(
            {
                "informativa": {
                    "data": informativa_data,
                    "verbose_names": {},
                },
                "calculation": {"props": calculation_props},
                "linking": None,
            },
            status=status.HTTP_200_OK,
        )


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
