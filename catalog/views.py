from django.shortcuts import render  # noqa: F401
from django.db import transaction, connection  # noqa: F401
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models
from catalog.models import ItemConfigurationDetail
from django.utils import timezone

import uuid

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

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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


import uuid
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from inventory.models import Package
from price.models import Price

from .models import (
    Catalog,
    Menu,
    ItemGroup,
    ItemCategory,
    ItemType,
    ItemConfiguration,
)
from .serializers import CatalogSerializer


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

            menu_dict = dict(Menu.objects.values_list("id", "menu"))
            category_dict = dict(ItemCategory.objects.values_list("id", "category"))
            group_dict = dict(ItemGroup.objects.values_list("id", "group_name"))
            type_dict = dict(ItemType.objects.values_list("id", "type"))
            config_dict = dict(
                ItemConfiguration.objects.values_list("code", "configuration")
            )

            price_codes = [c.price_id for c in page_qs if c.price_id]
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
            q = self._safe_float(r.get("quantity"), 1.0)
            n = self._safe_float(r.get("net_amount"), 0.0)
            g = self._safe_float(r.get("gross_amount"), 0.0)
            i = self._safe_float(r.get("iva_amount"), 0.0)

            count += 1
            sub_net += n * q
            sub_gross += g * q
            sub_iva += i * q

        return {
            "count": count,
            "sub_total_net": sub_net,
            "sub_total_gross": sub_gross,
            "sub_total_iva": sub_iva,
        }

    def _serialize_detail_row(self, d, obj=None, item_kind=None):
        q = self._safe_float(getattr(d, "quantity", 1), 1.0)
        if q <= 0:
            q = 1.0

        price_obj = None
        if obj and getattr(obj, "price", None):
            price_obj = (
                Price.objects.filter(code=obj.price).order_by("-created_at").first()
            )

        if price_obj:
            net_u = float(price_obj.net_amount or 0)
            iva_u = float(price_obj.iva_amount or 0)
            gross_u = float(price_obj.gross_amount or 0)
        else:
            net_u = 0.0
            iva_u = 0.0
            gross_u = 0.0

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
            "unit_net": net_u,
            "unit_iva": iva_u,
            "unit_gross": gross_u,
            "net_amount": net_u * q,
            "iva_amount": iva_u * q,
            "gross_amount": gross_u * q,
        }

    @action(detail=True, methods=["get", "post"], url_path="config")
    def config(self, request, sku=None):
        catalog = self.get_queryset().filter(sku=sku).first()
        if not catalog:
            return Response(
                {"detail": "Catálogo no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ✅ traer Price real + FK lista
        price_obj = (
            Price.objects.filter(code=catalog.price_id, is_current=True)
            .select_related("price_configuration")
            .first()
        )
        pc = getattr(price_obj, "price_configuration", None) if price_obj else None

        cfg = getattr(catalog, "configuration", None)

        if request.method == "POST":
            raw_user_code = getattr(getattr(request, "user", None), "code", None)
            created_by = str(raw_user_code).strip() if raw_user_code is not None else ""
            if not created_by:
                return Response(
                    {"detail": "Usuario inválido para created_by."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = request.data or {}

            products_in = data.get("products", None)
            materials_in = data.get("materials", None)
            services_in = data.get("services", None)
            links_in = data.get("links", None)

            links_payload = []

            def add_rows(kind, rows):
                if not isinstance(rows, list):
                    return
                for r in rows:
                    if not isinstance(r, dict):
                        continue
                    links_payload.append(
                        {
                            "item_kind": kind,
                            "item_sku": (r.get("item_sku") or "").strip(),
                            "item_code": (r.get("item_code") or "").strip(),
                            "detail": (r.get("detail") or "").strip()[:50],
                            "quantity": r.get("quantity", 1),
                            "net_amount": r.get("net_amount"),
                            "iva_amount": r.get("iva_amount"),
                            "gross_amount": r.get("gross_amount"),
                        }
                    )

            if isinstance(links_in, list):
                for r in links_in:
                    if not isinstance(r, dict):
                        continue
                    kind = (
                        (r.get("item_type") or r.get("item_kind") or "").strip().lower()
                    )
                    if kind not in ("product", "material", "service"):
                        continue
                    add_rows(kind, [r])
            else:
                add_rows("product", products_in or [])
                add_rows("material", materials_in or [])
                add_rows("service", services_in or [])

            if not cfg or not getattr(cfg, "code", None):
                return Response(
                    {"detail": "Catálogo sin ItemConfiguration."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                now = timezone.now()

                sku_products = [
                    x["item_sku"]
                    for x in links_payload
                    if x["item_kind"] == "product" and x["item_sku"]
                ]
                sku_materials = [
                    x["item_sku"]
                    for x in links_payload
                    if x["item_kind"] == "material" and x["item_sku"]
                ]
                sku_services = [
                    x["item_sku"]
                    for x in links_payload
                    if x["item_kind"] == "service" and x["item_sku"]
                ]

                prod_by_sku = {
                    p.sku: p for p in Product.objects.filter(sku__in=sku_products)
                }
                mat_by_sku = {
                    m.sku: m for m in Material.objects.filter(sku__in=sku_materials)
                }
                srv_by_sku = {
                    s.sku: s for s in Service.objects.filter(sku__in=sku_services)
                }

                existing = list(
                    ItemConfigurationDetail.objects.filter(configuration_id=cfg.code)
                )
                existing_by_item = {
                    e.id_item: e for e in existing if getattr(e, "id_item", None)
                }

                desired = []
                for r in links_payload:
                    kind = r["item_kind"]
                    item_code = (r.get("item_code") or "").strip()
                    item_sku = (r.get("item_sku") or "").strip()

                    obj = None
                    if not item_code:
                        if kind == "product":
                            obj = prod_by_sku.get(item_sku)
                        elif kind == "material":
                            obj = mat_by_sku.get(item_sku)
                        elif kind == "service":
                            obj = srv_by_sku.get(item_sku)

                        if not obj:
                            continue
                        item_code = getattr(obj, "code", None)

                    if not item_code:
                        continue

                    if obj is None:
                        if kind == "product":
                            obj = Product.objects.filter(code=item_code).first()
                        elif kind == "material":
                            obj = Material.objects.filter(code=item_code).first()
                        elif kind == "service":
                            obj = Service.objects.filter(code=item_code).first()

                    type_id = getattr(obj, "type", None) if obj else None
                    if not type_id:
                        continue

                    desired.append(
                        {
                            "item_code": item_code,
                            "detail": (r.get("detail") or "")[:50],
                            "type_id": int(type_id),
                            "quantity": r.get("quantity", 1),
                        }
                    )

                desired_codes = {d["item_code"] for d in desired}

                to_delete = [
                    e.id_item for e in existing if e.id_item not in desired_codes
                ]
                if to_delete:
                    ItemConfigurationDetail.objects.filter(
                        configuration_id=cfg.code, id_item__in=to_delete
                    ).delete()

                to_create = []
                for d in desired:
                    existing_obj = existing_by_item.get(d["item_code"])
                    if not existing_obj:
                        to_create.append(
                            ItemConfigurationDetail(
                                code=str(uuid.uuid4()),
                                detail=d["detail"],
                                type_id=d["type_id"],
                                configuration_id=cfg.code,
                                id_item=d["item_code"],
                                quantity=d["quantity"],
                                created_at=now,
                                created_by=created_by,
                            )
                        )
                    else:
                        updated = False
                        if existing_obj.detail != d["detail"]:
                            existing_obj.detail = d["detail"]
                            updated = True
                        if existing_obj.type_id != d["type_id"]:
                            existing_obj.type_id = d["type_id"]
                            updated = True
                        if float(getattr(existing_obj, "quantity", 1) or 1) != float(
                            d["quantity"] or 1
                        ):
                            existing_obj.quantity = d["quantity"]
                            updated = True
                        if updated:
                            existing_obj.save(
                                update_fields=["detail", "type_id", "quantity"]
                            )

                if to_create:
                    ItemConfigurationDetail.objects.bulk_create(to_create)

            return Response(
                {"detail": "Configuración guardada."}, status=status.HTTP_200_OK
            )

        try:
            # ✅ serializable
            informativa_data = {
                "item_configuration_code": getattr(cfg, "code", None),
                "item_configuration_name": getattr(cfg, "configuration", None),
                "price_code": getattr(price_obj, "code", None),
                "price_configuration": getattr(pc, "code", None),
                "price_configuration_label": getattr(pc, "price_configuration", None),
                "base_net_amount": getattr(price_obj, "base_net_amount", None),
                "price_is_current": getattr(price_obj, "is_current", None),
            }

            informativa_verbose = {
                "item_configuration_code": "Item Configuration (code)",
                "item_configuration_name": "Item Configuration (configuration)",
                "price_code": "Price (code)",
                "price_configuration": "Price Configuration (code)",
                "price_configuration_label": "Price Configuration (nombre)",
                "base_net_amount": "Valor Neto Base",
                "price_is_current": "Precio Vigente",
            }

            calculation_props = {
                "code": getattr(pc, "code", None),
                "baseNetAmount": getattr(price_obj, "base_net_amount", None),
                "netAmount": getattr(price_obj, "net_amount", None),
                "grossAmount": getattr(price_obj, "gross_amount", None),
                "ivaAmount": getattr(price_obj, "iva_amount", None),
                "additionalTaxAmount": getattr(price_obj, "aditional_tax_amount", None),
                "retentionAmount": getattr(price_obj, "retention_amount", None),
                "selectedProductSku": catalog.sku,
            }

            products_rows, materials_rows, services_rows = [], [], []

            if cfg and getattr(cfg, "code", None):
                details = list(
                    ItemConfigurationDetail.objects.only(
                        "code",
                        "detail",
                        "type_id",
                        "configuration",
                        "id_item",
                        "quantity",
                        "created_at",
                        "created_by",
                    )
                    .filter(configuration_id=cfg.code)
                    .order_by("created_at")
                )

                id_items = [d.id_item for d in details if getattr(d, "id_item", None)]
                prod_map = {
                    p.code: p for p in Product.objects.filter(code__in=id_items)
                }
                mat_map = {
                    m.code: m for m in Material.objects.filter(code__in=id_items)
                }
                srv_map = {s.code: s for s in Service.objects.filter(code__in=id_items)}

                for d in details:
                    item_code = getattr(d, "id_item", None)
                    if not item_code:
                        continue
                    if item_code in prod_map:
                        products_rows.append(
                            self._serialize_detail_row(
                                d, prod_map[item_code], "product"
                            )
                        )
                    elif item_code in mat_map:
                        materials_rows.append(
                            self._serialize_detail_row(
                                d, mat_map[item_code], "material"
                            )
                        )
                    elif item_code in srv_map:
                        services_rows.append(
                            self._serialize_detail_row(d, srv_map[item_code], "service")
                        )

            subtotals_products = self._sum_rows(products_rows)
            subtotals_materials = self._sum_rows(materials_rows)
            subtotals_services = self._sum_rows(services_rows)

            totals = {
                "count": subtotals_products["count"]
                + subtotals_materials["count"]
                + subtotals_services["count"],
                "sub_total_net": subtotals_products["sub_total_net"]
                + subtotals_materials["sub_total_net"]
                + subtotals_services["sub_total_net"],
                "sub_total_gross": subtotals_products["sub_total_gross"]
                + subtotals_materials["sub_total_gross"]
                + subtotals_services["sub_total_gross"],
                "sub_total_iva": subtotals_products["sub_total_iva"]
                + subtotals_materials["sub_total_iva"]
                + subtotals_services["sub_total_iva"],
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
                        "verbose_names": informativa_verbose,
                    },
                    "calculation": {"props": calculation_props},
                    "linking": linking,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": f"Error obteniendo configuración: {str(e)}"},
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
                "/product-price-calculation/",
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

            if price_configuration_new is not None and (
                str(
                    getattr(
                        price_obj.price_configuration,
                        "code",
                        price_obj.price_configuration,
                    )
                )
                != str(price_configuration_new)
            ):
                changed = True

            if changed:
                from price.models import PriceConfiguration

                with transaction.atomic():
                    price_obj.is_current = False
                    price_obj.save()

                    # 🔥 Resolver FK correctamente
                    price_conf_obj = None

                    if price_configuration_new:
                        price_conf_obj = PriceConfiguration.objects.filter(
                            code=str(price_configuration_new).strip()
                        ).first()

                        if not price_conf_obj:
                            price_conf_obj = PriceConfiguration.objects.filter(
                                price_configuration=str(price_configuration_new).strip()
                            ).first()

                        if not price_conf_obj:
                            return Response(
                                {"detail": "PriceConfiguration inválido."},
                                status=400,
                            )
                    else:
                        price_conf_obj = price_obj.price_configuration

                    price_data_new = self._SimplePriceSerializer(price_obj).data
                    price_data_new.pop("id", None)
                    price_data_new.pop("code", None)
                    price_data_new.pop("created_at", None)

                    price_data_new["base_net_amount"] = base_net_amount_new
                    price_data_new["price_configuration"] = price_conf_obj
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

    def get_queryset(self):
        qs = Product.objects.select_related(
            "provider",
            "type",
            "item_group",
            "category",
            "package",
            "price",
            "price__price_configuration",
        )

        franchise = self.request.query_params.get("franchise")

        if franchise:
            qs = qs.filter(
                price__price_configuration__franchise_configuration__franchise=franchise
            )

        return qs

    @action(detail=False, methods=["get"], url_path="list")
    def product_list(self, request):
        try:
            from price.models import PriceConfiguration

            products = self.get_queryset()

            if request.query_params.get("active_only") == "true":
                products = products.filter(is_active=True, is_deleted=False)

            results = []
            for product in products:
                current_price = (
                    product.price
                    if product.price and product.price.is_current
                    else None
                )

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
                        "price_configuration_label": (
                            current_price.price_configuration.price_configuration
                            if current_price and current_price.price_configuration
                            else None
                        ),
                        "obs": product.obs,
                        "package_unit": product.package_unit,
                        "min_package_purchase": product.min_package_purchase,
                        "provider": product.provider,
                        "type": product.type,
                        "type_name": product.type.type if product.type else None,
                        "item_group": product.item_group,
                        "group_name": product.item_group.group_name if product.item_group else None,
                        "category": product.category,
                        "category_name": product.category.category if product.category else None,
                        "url": product.url,
                        "package": product.package,
                        "package_description": product.package.description if product.package else None,
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

    @action(detail=False, methods=["get"], url_path="lookup")
    def lookup(self, request):
        """
        Autocomplete liviano:
        GET /products/lookup/?q=pollo&limit=10
        Retorna [{sku, description, obs}]
        """
        q = (request.query_params.get("q") or "").strip()
        limit = request.query_params.get("limit") or "10"

        try:
            limit = int(limit)
        except Exception:
            limit = 10

        limit = max(1, min(limit, 50))

        if not q:
            return Response({"results": []}, status=status.HTTP_200_OK)

        qs = Product.objects.all()

        # búsqueda simple y rápida
        qs = qs.filter(
            models.Q(sku__icontains=q)
            | models.Q(description__icontains=q)
            | models.Q(obs__icontains=q)
        ).order_by("description")[:limit]

        results = [
            {
                "sku": p.sku,
                "description": p.description,
                "obs": p.obs,
            }
            for p in qs
        ]

        return Response({"results": results}, status=status.HTTP_200_OK)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = [
        "is_active",
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

    ordering_fields = [
        "id",
        "description",
        "created_at",
    ]

    ordering = ["-id"]

    @action(detail=False, methods=["get"])
    def active(self, request):
        queryset = self.get_queryset().filter(is_active=True)
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
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = [
        "is_active",
        "provider",
        "type",
        "item_group",
        "category",
    ]

    search_fields = ["description", "sku", "code", "obs"]
    ordering_fields = ["id", "description"]
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

    @action(detail=False, methods=["get"], url_path="lookup")
    def lookup(self, request):
        """
        GET /materials/lookup/?q=pollo&limit=10
        Retorna [{sku, description, obs}]
        """
        q = (request.query_params.get("q") or "").strip()
        limit = request.query_params.get("limit") or "10"

        try:
            limit = int(limit)
        except Exception:
            limit = 10

        limit = max(1, min(limit, 50))

        if not q:
            return Response({"results": []}, status=status.HTTP_200_OK)

        qs = (
            Material.objects.all()
            .filter(
                models.Q(sku__icontains=q)
                | models.Q(description__icontains=q)
                | models.Q(obs__icontains=q)
            )
            .order_by("description")[:limit]
        )

        results = [
            {"sku": m.sku, "description": m.description, "obs": m.obs} for m in qs
        ]
        return Response({"results": results}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="lookup")
    def lookup(self, request):
        """
        GET /services/lookup/?q=pollo&limit=10
        Retorna [{sku, description, obs}]
        """
        q = (request.query_params.get("q") or "").strip()
        limit = request.query_params.get("limit") or "10"

        try:
            limit = int(limit)
        except Exception:
            limit = 10

        limit = max(1, min(limit, 50))

        if not q:
            return Response({"results": []}, status=status.HTTP_200_OK)

        qs = (
            Service.objects.all()
            .filter(
                models.Q(sku__icontains=q)
                | models.Q(description__icontains=q)
                | models.Q(obs__icontains=q)
            )
            .order_by("description")[:limit]
        )

        results = [
            {"sku": s.sku, "description": s.description, "obs": s.obs} for s in qs
        ]
        return Response({"results": results}, status=status.HTTP_200_OK)


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
