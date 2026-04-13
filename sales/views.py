from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from clients.models import Client

from .models import (
    Order,
    FiscalDocumentation,
    FiscalDocumentType,
    OrderDetail,
    OrderFiscalDocumentation,
    OrderType,
)
from .serializers import (
    OrderSerializer,
    ClientSerializer,
    FiscalDocumentationSerializer,
    FiscalDocumentTypeSerializer,
    OrderDetailSerializer,
    OrderFiscalDocumentationSerializer,
    OrderTypeSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.select_related(
        "franchise",
        "status",
        "platform",
    )
    serializer_class = ClientSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "franchise",
        "status",
        "platform",
        "is_active",
        "is_deleted",
        "contacted",
        "same_address_detected",
        "has_visible_physical_store",
        "priority",
    ]
    search_fields = [
        "code",
        "company_name",
        "company_rut",
        "owner_name",
        "owner_position",
        "direct_email",
        "direct_phone",
        "exact_address",
        "observations",
        "progress",
    ]
    ordering_fields = [
        "id",
        "code",
        "detection_date",
        "company_name",
        "owner_name",
        "contact_date",
        "estimated_avg_ticket",
        "estimated_potential_volume",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at"]


class OrderTypeViewSet(viewsets.ModelViewSet):
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "type"]
    search_fields = ["type", "description", "category"]
    ordering_fields = ["id", "type", "category"]
    ordering = ["category", "type"]


class FiscalDocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = FiscalDocumentType.objects.all()
    serializer_class = FiscalDocumentTypeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["type", "description"]
    ordering_fields = ["id", "type"]
    ordering = ["type"]


class FiscalDocumentationViewSet(viewsets.ModelViewSet):
    queryset = FiscalDocumentation.objects.select_related("document_type")
    serializer_class = FiscalDocumentationSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["document_type", "created_by"]
    search_fields = ["code", "document_number", "url"]
    ordering_fields = ["id", "created_at", "issued_at"]
    ordering = ["-id"]


class OrderFiscalDocumentationViewSet(viewsets.ModelViewSet):
    queryset = OrderFiscalDocumentation.objects.select_related(
        "order",
        "fiscal_documentation",
    )
    serializer_class = OrderFiscalDocumentationSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["order", "fiscal_documentation", "is_primary"]
    search_fields = ["description"]
    ordering_fields = ["id", "created_at", "is_primary"]
    ordering = ["order", "-is_primary", "id"]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "status",
        "order_type",
        "parent_order",
        "franchise",
        "client",
        "is_canceled",
        "is_deleted",
        "is_closed",
        "is_processed",
        "requires_fiscal_documentation",
        "fiscal_documentation_error",
    ]
    search_fields = ["name", "code", "description", "client__company_name", "client__owner_name"]
    ordering_fields = [
        "id",
        "code",
        "name",
        "created_at",
        "updated_at",
        "processed_at",
        "closed_at",
        "expected_dispatch_date",
        "expected_delivery_date",
        "dispatch_date",
        "delivery_date",
        "total_net_amount",
        "total_discount",
        "total_surcharge",
        "version",
    ]
    ordering = ["-created_at", "-id"]

    def get_queryset(self):
        qs = Order.objects.select_related(
            "franchise",
            "client",
            "parent_order",
            "order_type",
            "status",
        )
        if self.request.query_params.get("include_deleted") != "true":
            qs = qs.filter(is_deleted=False)

        franchise_code = self.request.query_params.get("franchise_code")
        if franchise_code:
            qs = qs.filter(franchise__code=franchise_code.strip())

        return qs

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        for item in response.data.get('results', response.data):
            order_type_id = item.get('order_type_id')

            if order_type_id:
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT variable_formula
                        FROM sbm_business.module_order_config
                        WHERE order_config_type = %s
                        LIMIT 1
                    """, [order_type_id])
                    row = cursor.fetchone()

                item['module_formula_code'] = row[0] if row else None
            else:
                item['module_formula_code'] = None

        return response

    @action(detail=True, methods=["get"], url_path="details")
    def details(self, request, pk=None):
        order = self.get_object()
        detail_type = request.query_params.get("type")

        qs = OrderDetail.objects.select_related(
            "order",
            "order_type",
            "item_type",
            "fiscal_documentation",
        ).filter(order=order)

        if detail_type:
            if detail_type == "catalog":
                qs = qs.filter(item_type_id=1)
            elif detail_type == "product":
                qs = qs.filter(item_type_id=2)
            elif detail_type == "service":
                qs = qs.filter(item_type_id=3)
            elif detail_type == "ticket":
                qs = qs.filter(item_type_id=4)
            elif detail_type == "material":
                qs = qs.filter(item_type_id=5)

        serializer = OrderDetailSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.select_related(
        "order",
        "order_type",
        "item_type",
        "fiscal_documentation",
    )
    serializer_class = OrderDetailSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "order",
        "order_type",
        "item_type",
        "fiscal_documentation",
        "is_deleted",
        "is_canceled",
        "is_closed",
        "is_processed",
        "requires_fiscal_documentation",
        "fiscal_documentation_error",
    ]
    search_fields = [
        "description",
        "id_item",
        "obs",
        "order__code",
    ]
    ordering_fields = [
        "id",
        "description",
        "quantity",
        "net_amount",
        "created_at",
        "updated_at",
        "processed_at",
        "closed_at",
        "expected_dispatch_date",
        "expected_delivery_date",
        "dispatch_date",
        "delivery_date",
    ]
    ordering = ["order", "id"]


