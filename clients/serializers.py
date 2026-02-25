from rest_framework import serializers
from .models import Client, ClientBrand, District, Region
from config.models import Status


# -----------------------------------------
# Status Serializer
# -----------------------------------------
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "code", "name", "module"]


# -----------------------------------------
# Client Base Serializer
# -----------------------------------------
class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            "id",
            "code",
            "status",
            "platform",
            "progress",
            "exact_address",
            "observations",
            "district",
            "region",
            "same_address_detected",
            "detection_date",
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
            "estimated_potential_volume",
            "priority",
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
        ]


# -----------------------------------------
# Region & District
# -----------------------------------------
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


# -----------------------------------------
# Client Brand Grid Serializer
# -----------------------------------------
class ClientBrandGridSerializer(serializers.ModelSerializer):

    client_code = serializers.CharField(source="client.code", read_only=True)

    # --- Client fields (FK ids)
    status = serializers.IntegerField(source="client.status")
    district = serializers.IntegerField(source="client.district")
    region = serializers.IntegerField(source="client.region")
    district_name = serializers.SerializerMethodField()
    region_name = serializers.SerializerMethodField()

    # --- Detail fields (FK objects)
    status = serializers.IntegerField(source="client.status")
    district = serializers.IntegerField(source="client.district")
    region = serializers.IntegerField(source="client.region")

    progress = serializers.CharField(
        source="client.progress", allow_null=True, required=False
    )
    exact_address = serializers.CharField(source="client.exact_address")
    observations = serializers.CharField(
        source="client.observations", allow_null=True, required=False
    )

    same_address_detected = serializers.BooleanField(
        source="client.same_address_detected"
    )
    detection_date = serializers.DateField(source="client.detection_date")

    estimated_type = serializers.CharField(
        source="client.estimated_type", allow_null=True, required=False
    )
    operation_schedule = serializers.CharField(
        source="client.operation_schedule", allow_null=True, required=False
    )

    estimated_avg_ticket = serializers.DecimalField(
        source="client.estimated_avg_ticket",
        max_digits=10,
        decimal_places=2,
        allow_null=True,
        required=False,
    )

    has_visible_physical_store = serializers.BooleanField(
        source="client.has_visible_physical_store"
    )

    company_name = serializers.CharField(
        source="client.company_name", allow_null=True, required=False
    )
    company_rut = serializers.CharField(
        source="client.company_rut", allow_null=True, required=False
    )
    owner_name = serializers.CharField(
        source="client.owner_name", allow_null=True, required=False
    )
    owner_position = serializers.CharField(
        source="client.owner_position", allow_null=True, required=False
    )
    linkedin_url = serializers.CharField(
        source="client.linkedin_url", allow_null=True, required=False
    )

    direct_phone = serializers.CharField(
        source="client.direct_phone", allow_null=True, required=False
    )
    direct_email = serializers.EmailField(
        source="client.direct_email", allow_null=True, required=False
    )

    contacted = serializers.BooleanField(source="client.contacted")
    contact_date = serializers.DateField(
        source="client.contact_date", allow_null=True, required=False
    )

    estimated_potential_volume = serializers.DecimalField(
        source="client.estimated_potential_volume",
        max_digits=14,
        decimal_places=2,
        allow_null=True,
        required=False,
    )

    priority = serializers.CharField(
        source="client.priority", allow_null=True, required=False
    )
    is_active = serializers.BooleanField(source="client.is_active")
    is_deleted = serializers.BooleanField(
        source="client.is_deleted", allow_null=True, required=False
    )

    class Meta:
        model = ClientBrand
        fields = [
            "id",
            "client_code",
            "brand_name",
            "status",
            "progress",
            "exact_address",
            "observations",
            "district",
            "district_name",
            "region",
            "region_name",
            "same_address_detected",
            "detection_date",
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
            "estimated_potential_volume",
            "priority",
            "is_active",
            "is_deleted",
        ]

    # -----------------------------------------
    # Update
    # -----------------------------------------
    def update(self, instance, validated_data):
        client_data = validated_data.get("client", {})

        if client_data:
            for attr, value in client_data.items():
                setattr(instance.client, attr, value)
            instance.client.save()

        return instance

    # -----------------------------------------
    # Detail Getters (SIN queries extra)
    # -----------------------------------------
    # -----------------------------------------


    # Detail Getters (COMPATIBLE CON FK INT)
    # -----------------------------------------


    def get_status_detail(self, obj):
        status_id = obj.client.status
        if not status_id:
            return None
        status = Status.objects.filter(id=status_id).first()
        if not status:
            return None
        return {
            "id": status.id,
            "code": status.code,
            "name": status.name,
            "module": status.module,
        }


    def get_district_detail(self, obj):
        district_id = obj.client.district
        if not district_id:
            return None
        district = District.objects.filter(id=district_id).first()
        if not district:
            return None
        return {
            "id": district.id,
            "district": district.district,
        }


    def get_region_detail(self, obj):
        region_id = obj.client.region
        if not region_id:
            return None
        region = Region.objects.filter(id=region_id).first()
        if not region:
            return None
        return {
            "id": region.id,
            "region": region.region,
        }
    def get_district_name(self, obj):
        district_id = obj.client.district
        d = District.objects.filter(id=district_id).only("district").first()
        return d.district if d else None

    def get_region_name(self, obj):
        region_id = obj.client.region
        r = Region.objects.filter(id=region_id).only("region").first()
        return r.region if r else None