import uuid
from typing import Optional

from django.db import transaction
from django.utils import timezone
from franchise.models import Franchise
from config.models import Status
from rest_framework import serializers

from clients.models import Client
from catalog.models import Catalog, Product, Material, Service, Ticket

from .models import (
    Order,
    OrderDetail,
    OrderType,
    FiscalDocumentation,
    FiscalDocumentType,
    OrderFiscalDocumentation,
)


def _user_code_from_context(serializer) -> Optional[str]:
    request = serializer.context.get("request")
    if not request:
        return None
    code = getattr(request.user, "code", None)
    if code is None:
        return None
    s = str(code).strip()
    return s or None


class ClientSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()
    franchise_code = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()
    platform_name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            "id",
            "code",
            "franchise",
            "franchise_code",
            "detection_date",
            "status",
            "status_name",
            "platform",
            "platform_name",
            "exact_address",
            "district",
            "region",
            "same_address_detected",
            "estimated_type",
            "operation_schedule",
            "estimated_avg_ticket",
            "has_visible_physical_store",
            "company_name",
            "company_rut",
            "owner_name",
            "owner_position",
            "linkedin_url",
            "direct_phone",
            "direct_email",
            "contacted",
            "contact_date",
            "progress",
            "estimated_potential_volume",
            "priority",
            "observations",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
        ]

    def get_field_verbose_names(self, obj):
        return {
            "id": "ID",
            "code": "Código",
            "franchise": "Franquicia",
            "franchise_code": "Código Franquicia",
            "detection_date": "Fecha de detección",
            "status": "Estado",
            "status_name": "Nombre estado",
            "platform": "Plataforma",
            "platform_name": "Nombre plataforma",
            "exact_address": "Dirección exacta",
            "district": "Comuna",
            "region": "Región",
            "same_address_detected": "Misma dirección detectada",
            "estimated_type": "Tipo estimado",
            "operation_schedule": "Horario de operación",
            "estimated_avg_ticket": "Ticket promedio estimado",
            "has_visible_physical_store": "Tiene local visible",
            "company_name": "Razón social",
            "company_rut": "RUT empresa",
            "owner_name": "Nombre dueño",
            "owner_position": "Cargo dueño",
            "linkedin_url": "LinkedIn",
            "direct_phone": "Teléfono directo",
            "direct_email": "Email directo",
            "contacted": "Contactado",
            "contact_date": "Fecha de contacto",
            "progress": "Progreso",
            "estimated_potential_volume": "Volumen potencial estimado",
            "priority": "Prioridad",
            "observations": "Observaciones",
            "is_active": "Activo",
            "is_deleted": "Eliminado",
            "created_at": "Creado en",
            "updated_at": "Actualizado en",
            "deleted_at": "Eliminado en",
            "created_by": "Creado por",
            "updated_by": "Actualizado por",
            "deleted_by": "Eliminado por",
            "log": "Log",
            "version": "Versión",
        }

    def get_franchise_code(self, obj):
        return obj.franchise.code if getattr(obj, "franchise", None) else None

    def get_status_name(self, obj):
        return obj.status.name if getattr(obj, "status", None) else None

    def get_platform_name(self, obj):
        return obj.platform.platform if getattr(obj, "platform", None) else None

    def create(self, validated_data):
        user_code = _user_code_from_context(self)
        if not user_code:
            raise serializers.ValidationError(
                {"created_by": "Usuario autenticado sin código válido."}
            )
        validated_data["created_by"] = user_code
        validated_data.setdefault("created_at", timezone.now())
        validated_data.setdefault("is_active", True)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user_code = _user_code_from_context(self)
        if user_code:
            validated_data["updated_by"] = user_code
        validated_data["updated_at"] = timezone.now()
        return super().update(instance, validated_data)


class FiscalDocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalDocumentType
        fields = ["id", "type", "description"]


class FiscalDocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalDocumentation
        fields = [
            "id",
            "code",
            "document_type",
            "document_number",
            "url",
            "issued_at",
            "created_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "created_by"]

    def create(self, validated_data):
        user_code = _user_code_from_context(self)
        if not user_code:
            raise serializers.ValidationError(
                {"created_by": "Usuario autenticado sin código válido."}
            )
        validated_data["created_by"] = user_code
        if not validated_data.get("code"):
            validated_data["code"] = str(uuid.uuid4())
        validated_data.setdefault("created_at", timezone.now())
        return super().create(validated_data)


class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ["id", "type", "description", "category"]


class OrderDetailSerializer(serializers.ModelSerializer):
    sku = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = [
            "id",
            "order",
            "order_type",
            "item_type",
            "id_item",
            "sku",
            "description",
            "quantity",
            "percent",
            "net_amount",
            "fiscal_documentation",
            "obs",
            "url_evidence",
            "is_delayed",
            "is_partial",
            "is_canceled",
            "is_non_conforming",
            "requires_cold_chain",
            "requires_fiscal_documentation",
            "fiscal_documentation_error",
            "is_processed",
            "is_closed",
            "is_deleted",
            "expected_dispatch_date",
            "expected_delivery_date",
            "dispatch_date",
            "delivery_date",
            "processed_at",
            "closed_at",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
        ]
        read_only_fields = [
            "id",
            "sku",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
        ]

    def get_sku(self, obj):
        if not obj.id_item:
            return None

        item_type_id = getattr(obj, "item_type_id", None)
        if item_type_id is None and getattr(obj, "item_type", None):
            item_type_id = getattr(obj.item_type, "id", None)

        model_map = {
            1: Catalog,
            2: Product,
            3: Service,
            4: Ticket,
            5: Material,
        }

        model_class = model_map.get(item_type_id)
        if not model_class:
            return obj.id_item

        item = model_class.objects.filter(code=obj.id_item).only("sku").first()
        return item.sku if item else obj.id_item

    def validate(self, attrs):
        order = attrs.get("order") or getattr(self.instance, "order", None)
        item_type = attrs.get("item_type") or getattr(self.instance, "item_type", None)
        id_item = attrs.get("id_item") or getattr(self.instance, "id_item", None)

        if order and item_type and id_item:
            qs = OrderDetail.objects.filter(
                order=order,
                item_type=item_type,
                id_item=id_item,
                is_canceled=False,
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"id_item": "Este registro ya existe en la orden para ese tipo."}
                )
        return attrs

    def create(self, validated_data):
        user_code = _user_code_from_context(self)
        if not user_code:
            raise serializers.ValidationError(
                {"created_by": "Usuario autenticado sin código válido."}
            )
        validated_data["created_by"] = user_code
        validated_data.setdefault("created_at", timezone.now())
        return super().create(validated_data)

class OrderFiscalDocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFiscalDocumentation
        fields = [
            "id",
            "order",
            "fiscal_documentation",
            "description",
            "is_primary",
            "created_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "created_by"]

    def create(self, validated_data):
        user_code = _user_code_from_context(self)
        if not user_code:
            raise serializers.ValidationError(
                {"created_by": "Usuario autenticado sin código válido."}
            )
        validated_data["created_by"] = user_code
        validated_data.setdefault("created_at", timezone.now())
        return super().create(validated_data)


class OrderDetailNestedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            "order_type",
            "item_type",
            "id_item",
            "description",
            "quantity",
            "percent",
            "net_amount",
            "fiscal_documentation",
            "obs",
            "url_evidence",
            "is_delayed",
            "is_partial",
            "is_canceled",
            "is_non_conforming",
            "requires_cold_chain",
            "requires_fiscal_documentation",
            "fiscal_documentation_error",
            "is_processed",
            "is_closed",
            "is_deleted",
            "expected_dispatch_date",
            "expected_delivery_date",
            "dispatch_date",
            "delivery_date",
            "processed_at",
            "closed_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    franchise_code = serializers.SlugRelatedField(
        source="franchise",
        slug_field="code",
        queryset=Franchise.objects.all(),
    )
    client = serializers.SlugRelatedField(
        slug_field="code",
        queryset=Client.objects.all(),
        required=False,
        allow_null=True,
    )
    parent_order_id = serializers.PrimaryKeyRelatedField(
        source="parent_order",
        queryset=Order.objects.all(),
        required=False,
        allow_null=True,
    )
    order_type_id = serializers.PrimaryKeyRelatedField(
        source="order_type",
        queryset=OrderType.objects.all(),
    )
    status_id = serializers.PrimaryKeyRelatedField(
        source="status",
        queryset=Status.objects.all(),
    )
    details = OrderDetailNestedCreateSerializer(
        many=True, required=False, write_only=True
    )
    

    class Meta:
        model = Order
        fields = [
            "id",
            "code",
            "name",
            "franchise_code",
            "client",
            "parent_order_id",
            "order_type_id",
            "status_id",
            "description",
            "is_partial",
            "is_canceled",
            "is_non_conforming",
            "requires_cold_chain",
            "requires_fiscal_documentation",
            "fiscal_documentation_error",
            "is_processed",
            "is_closed",
            "expected_dispatch_date",
            "expected_delivery_date",
            "dispatch_date",
            "delivery_date",
            "delivery_route",
            "delivery_window",
            "delivery_comments",
            "total_net_amount",
            "total_discount",
            "total_surcharge",
            "processed_at",
            "closed_at",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "is_deleted",
            "log",
            "version",
            "details",
        ]
        read_only_fields = [
            "id",
            "code",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "updated_by",
            "log",
            "version",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["code"] = (instance.code or "").strip()
        data["details"] = []
        data["parent_order_id"] = instance.parent_order_id
        data["order_type_id"] = instance.order_type_id
        data["status_id"] = instance.status_id
        data["franchise_code"] = instance.franchise.code if instance.franchise else None
        data["client"] = instance.client.code if instance.client else None
        return data

    def validate(self, attrs):
        if self.instance is None and not attrs.get("franchise"):
            raise serializers.ValidationError(
                {"franchise_code": "Este campo es obligatorio."}
            )
        return attrs

    def create(self, validated_data):
        details_data = validated_data.pop("details", [])
        user_code = _user_code_from_context(self)
        if not user_code:
            raise serializers.ValidationError(
                {"created_by": "Usuario autenticado sin código válido."}
            )

        validated_data["created_by"] = user_code
        validated_data.setdefault("created_at", timezone.now())
        validated_data.setdefault("is_deleted", False)

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for row in details_data:
                payload = dict(row)
                OrderDetail.objects.create(
                    order=order,
                    created_by=user_code,
                    created_at=timezone.now(),
                    **payload,
                )
        return order

    def update(self, instance, validated_data):
        validated_data.pop("details", None)
        user_code = _user_code_from_context(self)
        if user_code:
            validated_data["updated_by"] = user_code
        validated_data["updated_at"] = timezone.now()
        return super().update(instance, validated_data)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            "id",
            "code",
            "name",
            "description",
            "module",
            "is_active",
        ]
