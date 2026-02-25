from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Client, ClientBrand, District, Region
from .serializers import (
    ClientSerializer,
    ClientBrandGridSerializer,
    DistrictSerializer,
    RegionSerializer,
)

# 🔹 CRUD real de Client (necesario para PATCH /clients/{code}/)
class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.filter(is_deleted__isnull=True)
    serializer_class = ClientSerializer

    lookup_field = "code"      # 🔥 CLAVE para usar UUID
    lookup_url_kwarg = "code"


# 🔹 GRID (lista ClientBrand)
class ClientBrandViewSet(viewsets.ModelViewSet):

    queryset = ClientBrand.objects.select_related("client").all()
    serializer_class = ClientBrandGridSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = [
        "client__status",
        "client__platform",
        "client__priority",
        "client__contacted",
        "client__is_active",
    ]

    search_fields = [
        "brand_name",
        "client__company_name",
        "client__owner_name",
        "client__direct_email",
        "client__exact_address",
    ]

    ordering_fields = [
        "id",
        "client__estimated_potential_volume",
        "client__detection_date",
    ]

    ordering = ["-id"]


    


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["district"]
    ordering_fields = ["id", "district"]
    ordering = ["district"]


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["region"]
    ordering_fields = ["id", "region"]
    ordering = ["region"]