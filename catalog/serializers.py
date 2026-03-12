from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from catalog.models import ItemConfiguration


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


class CatalogSerializer(serializers.ModelSerializer):

    field_verbose_names = serializers.SerializerMethodField()

    menu_name = serializers.SerializerMethodField()
    menu_background_color = serializers.CharField(
        source="menu.background_color", read_only=True
    )
    menu_text_color = serializers.CharField(source="menu.text_color", read_only=True)

    item_group_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()
    restriction_name = serializers.SerializerMethodField()
    usage_instructions_name = serializers.SerializerMethodField()
    configuration_name = serializers.SerializerMethodField()

    price_data = serializers.DictField(write_only=True, required=False)

    base_net_amount = serializers.IntegerField(
        source="price.base_net_amount", read_only=True
    )
    net_amount = serializers.IntegerField(source="price.net_amount", read_only=True)
    gross_amount = serializers.IntegerField(source="price.gross_amount", read_only=True)
    iva_amount = serializers.IntegerField(source="price.iva_amount", read_only=True)

    aditional_tax_amount = serializers.IntegerField(
        source="price.aditional_tax_amount", read_only=True
    )

    retention_amount = serializers.IntegerField(
        source="price.retention_amount", read_only=True
    )

    price_configuration = serializers.CharField(
        source="price.price_configuration.code", read_only=True
    )

    # ==============================
    # GETTERS
    # ==============================

    def get_menu_name(self, obj):
        return obj.menu.menu if obj.menu else None

    def get_item_group_name(self, obj):
        return obj.item_group.group_name if obj.item_group else None

    def get_category_name(self, obj):
        return obj.category.category if obj.category else None

    def get_type_name(self, obj):
        return obj.type.type if obj.type else None

    def get_restriction_name(self, obj):
        return obj.restriction.restriction if obj.restriction else None

    def get_usage_instructions_name(self, obj):
        return obj.usage_instructions.instruction if obj.usage_instructions else None

    def get_configuration_name(self, obj):
        return obj.configuration.configuration if obj.configuration else None

    def get_field_verbose_names(self, obj):
        field_names = [
            "code",
            "sku",
            "menu",
            "name",
            "description",
            "item_group",
            "category",
            "type",
            "chef_recommendation",
            "min_quantity_purchase",
            "rations_quantity",
            "cover_image",
            "is_visible",
            "is_deleted",
            "is_confirmed",
            "restriction",
        ]
        return {field: obj._meta.get_field(field).verbose_name for field in field_names}

    # ==============================
    # CREATE
    # ==============================

    def create(self, validated_data):

        request = self.context.get("request")
        user_code = getattr(getattr(request, "user", None), "code", None)
        now = timezone.now()

        price_data = validated_data.pop("price_data", None)

        if not price_data:
            price_data = {
                "base_net_amount": validated_data.pop("base_net_amount", None),
                "price_configuration": validated_data.pop("price_configuration", None),
            }

        if not price_data:
            raise serializers.ValidationError({"price_data": "Requerido."})

        base_net = price_data.get("base_net_amount")
        price_conf_value = price_data.get("price_configuration")

        if base_net in [None, ""] or price_conf_value in [None, ""]:
            raise serializers.ValidationError({"price_data": "Datos incompletos."})

        from price.models import PriceConfiguration

        price_conf_obj = PriceConfiguration.objects.filter(
            code=str(price_conf_value).strip()
        ).first()

        if not price_conf_obj:
            price_conf_obj = PriceConfiguration.objects.filter(
                price_configuration=str(price_conf_value).strip()
            ).first()

        if not price_conf_obj:
            raise serializers.ValidationError(
                {"price_configuration": "No existe PriceConfiguration válido."}
            )

        with transaction.atomic():

            price = Price.objects.create(
                base_net_amount=base_net,
                price_configuration=price_conf_obj,
                is_current=True,
                created_by=user_code,
                created_at=now,
            )

            formula_obj = price_conf_obj.variable_formula
            formula = formula_obj.formula_translate

            context = {
                "base_net_amount": price.base_net_amount,
            }

            try:

                result = eval(formula, {}, context)

                price.net_amount = int(result.get("net_amount", 0))
                price.iva_amount = int(result.get("iva_amount", 0))
                price.gross_amount = int(result.get("gross_amount", 0))
                price.aditional_tax_amount = int(result.get("aditional_tax_amount", 0))
                price.retention_amount = int(result.get("retention_amount", 0))

            except Exception:

                price.net_amount = 0
                price.iva_amount = 0
                price.gross_amount = 0
                price.aditional_tax_amount = 0
                price.retention_amount = 0

            price.save()

            catalog = Catalog.objects.create(
                price=price, created_by=user_code, created_at=now, **validated_data
            )

        return catalog

    # ==============================
    # UPDATE
    # ==============================

    def update(self, instance, validated_data):

        request = self.context.get("request")
        user_code = getattr(getattr(request, "user", None), "code", None)
        now = timezone.now()

        price_data = validated_data.pop("price_data", None)
        direct_price_code = validated_data.pop("price", None)

        from price.models import PriceConfiguration

        with transaction.atomic():

            if price_data:

                base_net = price_data.get("base_net_amount")
                price_conf_value = price_data.get("price_configuration")

                current_price = instance.price

                if not current_price:
                    raise serializers.ValidationError(
                        {"price": "El catálogo no tiene Price asociado."}
                    )

                if base_net is not None and int(base_net) != int(
                    current_price.base_net_amount
                ):

                    current_price.is_current = False
                    current_price.save()

                    price_conf_obj = None

                    if price_conf_value:

                        price_conf_obj = PriceConfiguration.objects.filter(
                            code=str(price_conf_value).strip()
                        ).first()

                        if not price_conf_obj:

                            price_conf_obj = PriceConfiguration.objects.filter(
                                price_configuration=str(price_conf_value).strip()
                            ).first()

                        if not price_conf_obj:

                            raise serializers.ValidationError(
                                {
                                    "price_configuration": "No existe PriceConfiguration válido."
                                }
                            )

                    else:

                        price_conf_obj = current_price.price_configuration

                    new_price = Price.objects.create(
                        base_net_amount=base_net,
                        price_configuration=price_conf_obj,
                        record_item_code=instance.code,
                        price_record_type=1,
                        is_current=True,
                        created_by=user_code,
                        created_at=now,
                    )

                    formula_obj = price_conf_obj.variable_formula
                    formula = formula_obj.formula_translate

                    context = {
                        "base_net_amount": new_price.base_net_amount,
                    }

                    try:

                        result = eval(formula, {}, context)

                        new_price.net_amount = int(result.get("net_amount", 0))
                        new_price.iva_amount = int(result.get("iva_amount", 0))
                        new_price.gross_amount = int(result.get("gross_amount", 0))
                        new_price.aditional_tax_amount = int(
                            result.get("aditional_tax_amount", 0)
                        )
                        new_price.retention_amount = int(
                            result.get("retention_amount", 0)
                        )

                    except Exception:

                        new_price.net_amount = 0
                        new_price.iva_amount = 0
                        new_price.gross_amount = 0
                        new_price.aditional_tax_amount = 0
                        new_price.retention_amount = 0

                    new_price.save()

                    instance.price = new_price

            elif direct_price_code:

                new_price = Price.objects.filter(
                    code=str(direct_price_code).strip()
                ).first()

                if not new_price:
                    raise serializers.ValidationError(
                        {"price": "No existe Price con ese code."}
                    )

                instance.price = new_price

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.updated_by = user_code
            instance.updated_at = now
            instance.save()

        return instance

    class Meta:
        model = Catalog
        fields = [
            "code",
            "sku",
            "cover_image",
            "menu",
            "menu_name",
            "menu_background_color",
            "menu_text_color",
            "name",
            "description",
            "item_group",
            "item_group_name",
            "category",
            "category_name",
            "type",
            "type_name",
            "chef_recommendation",
            "usage_instructions",
            "usage_instructions_name",
            "min_quantity_purchase",
            "rations_quantity",
            "is_visible",
            "is_deleted",
            "is_confirmed",
            "restriction",
            "restriction_name",
            "configuration",
            "configuration_name",
            "field_verbose_names",
            "price_data",
            "price",
            "base_net_amount",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "price_configuration",
        ]

        read_only_fields = [
            "code",
            "created_at",
            "updated_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "price",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
        ]


class ProductSerializer(serializers.ModelSerializer):

    field_verbose_names = serializers.SerializerMethodField()

    # 🔹 Nombres relacionados
    type_name = serializers.SerializerMethodField()
    item_group_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    provider_name = serializers.SerializerMethodField()
    package_description = serializers.SerializerMethodField()

    # 🔹 Price info
    base_net_amount = serializers.IntegerField(
        source="price.base_net_amount", read_only=True
    )
    base_net_amount_input = serializers.IntegerField(write_only=True)
    net_amount = serializers.IntegerField(source="price.net_amount", read_only=True)
    gross_amount = serializers.IntegerField(source="price.gross_amount", read_only=True)
    iva_amount = serializers.IntegerField(source="price.iva_amount", read_only=True)
    aditional_tax_amount = serializers.IntegerField(
        source="price.aditional_tax_amount", read_only=True
    )
    retention_amount = serializers.IntegerField(
        source="price.retention_amount", read_only=True
    )
    price_configuration = serializers.CharField(
        source="price.price_configuration.code", read_only=True
    )
    price_configuration_input = serializers.CharField(write_only=True)

    # ==============================
    # GETTERS NOMBRES
    # ==============================

    def get_type_name(self, obj):
        return obj.type.type if obj.type else None

    def get_item_group_name(self, obj):
        return obj.item_group.group_name if obj.item_group else None

    def get_category_name(self, obj):
        return obj.category.category if obj.category else None

    def get_provider_name(self, obj):
        return obj.provider.provider if obj.provider else None

    def get_package_description(self, obj):
        return obj.package.description if obj.package else None

    # ==============================
    # VERBOSE
    # ==============================

    def get_field_verbose_names(self, obj):
        field_names = [
            "id",
            "code",
            "sku",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "price",
            "provider",
            "type",
            "item_group",
            "category",
            "url",
            "package",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
        ]
        return {
            field: (
                obj._meta.get_field(field).verbose_name
                if field in [f.name for f in obj._meta.fields]
                else field
            )
            for field in field_names
        }

    # ==============================
    # CREATE
    # ==============================

    def create(self, validated_data):
        request = self.context.get("request", None)
        price_data = validated_data.pop("price_data", None)

        # permitir formato directo desde el frontend
        if not price_data:
            base_net = validated_data.pop("base_net_amount_input", None)
            price_conf = validated_data.pop("price_configuration_input", None)

            if base_net is None or price_conf is None:
                raise serializers.ValidationError(
                    {"price_data": "Este campo es requerido."}
                )

            price_data = {
                "base_net_amount": base_net,
                "price_configuration": price_conf,
            }

        base_net = price_data.get("base_net_amount")
        price_conf_value = price_data.get("price_configuration")

        if base_net in [None, ""] or price_conf_value in [None, ""]:
            raise serializers.ValidationError({"price_data": "Datos incompletos."})

        from price.models import PriceConfiguration

        price_conf_obj = PriceConfiguration.objects.filter(
            code=str(price_conf_value).strip()
        ).first()

        if not price_conf_obj:
            price_conf_obj = PriceConfiguration.objects.filter(
                price_configuration=str(price_conf_value).strip()
            ).first()

        if not price_conf_obj:
            raise serializers.ValidationError(
                {"price_configuration": "No existe PriceConfiguration válido."}
            )

        validated_data.pop("price", None)
        validated_data.pop("created_by", None)

        user_code = getattr(getattr(request, "user", None), "code", "system")
        now = timezone.now()

        import uuid

        with transaction.atomic():

            # 🔹 generar código de producto
            product_code = str(uuid.uuid4())

            # 🔹 crear price primero
            price_code = str(uuid.uuid4())

            price_obj = Price._default_manager.create(
                code=price_code,
                base_net_amount=base_net,
                net_amount=0,
                gross_amount=0,
                iva_amount=0,
                aditional_tax_amount=0,
                retention_amount=0,
                price_configuration=price_conf_obj,
                record_item_code=product_code,
                price_record_type=1,
                is_current=True,
                created_by=user_code,
                created_at=now,
            )

            # 🔥 CALCULAR FÓRMULA (igual que Catalog)
            formula_obj = getattr(price_conf_obj, "variable_formula", None)

            if formula_obj and formula_obj.price_variables:
                formula = formula_obj.price_variables

                from accounting.models import FiscalConfigurationDetail, FiscalDirective

                context = {"base_net_amount": price_obj.base_net_amount}

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

                try:
                    results = {}

                    for line in [l.strip() for l in formula.split(";") if l.strip()]:
                        if "=" not in line:
                            continue

                        key, expr = line.split("=")
                        key = key.strip()
                        expr = expr.strip()

                        for var, val in context.items():
                            expr = expr.replace(var, str(val))

                        results[key] = eval(expr)

                    price_obj.net_amount = int(results.get("net_amount", 0))
                    price_obj.iva_amount = int(results.get("iva_amount", 0))
                    price_obj.gross_amount = int(results.get("gross_amount", 0))
                    price_obj.aditional_tax_amount = int(
                        results.get("aditional_tax_amount", 0)
                    )
                    price_obj.retention_amount = int(results.get("retention_amount", 0))

                except Exception:
                    price_obj.net_amount = 0
                    price_obj.iva_amount = 0
                    price_obj.gross_amount = 0
                    price_obj.aditional_tax_amount = 0
                    price_obj.retention_amount = 0

            price_obj.save()

            # 🔹 crear producto con price
            product = Product._default_manager.create(
                **validated_data,
                code=product_code,
                price=price_obj,
                created_by=user_code,
                created_at=now,
            )

        return product

    class Meta:
        model = Product
        fields = [
            "id",
            "code",
            "sku",
            "description",
            "base_net_amount",
            "base_net_amount_input",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "obs",
            "package_unit",
            "min_package_purchase",
            "provider",
            "provider_name",
            "type",
            "type_name",
            "item_group",
            "item_group_name",
            "category",
            "category_name",
            "url",
            "package",
            "package_description",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
            "price_configuration",
            "price_configuration_input",
            "field_verbose_names",
            "price",
        ]

        read_only_fields = [
            "id",
            "code",
            "sku",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "price",
            # seguridad API
            "base_net_amount",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "price_configuration",
        ]


class ProductManageSerializer(serializers.Serializer):
    code = serializers.CharField()
    sku = serializers.CharField()
    description = serializers.CharField()
    base_net_amount = serializers.IntegerField()
    obs = serializers.CharField()
    package_unit = serializers.IntegerField()
    min_package_purchase = serializers.IntegerField()
    provider = serializers.IntegerField()
    type = serializers.IntegerField()
    type_name = serializers.CharField()
    item_group = serializers.IntegerField()
    group_name = serializers.CharField()
    category = serializers.IntegerField()
    category_name = serializers.CharField()
    url = serializers.CharField(allow_null=True, allow_blank=True)
    package = serializers.IntegerField()
    package_description = serializers.CharField()
    is_active = serializers.BooleanField()
    is_deleted = serializers.BooleanField(allow_null=True)
    is_confirmed = serializers.BooleanField(allow_null=True)
    created_at = serializers.DateTimeField()

    @staticmethod
    def get_verbose_names():
        return {
            "code": "Código UUID",
            "sku": "SKU",
            "description": "Descripción",
            "base_net_amount": "Valor Neto Base",
            "obs": "Observaciones",
            "package_unit": "Unidad de Empaque",
            "min_package_purchase": "Compra Mínima de Empaque",
            "provider": "Proveedor",
            "type": "Tipo (ID)",
            "type_name": "Tipo",
            "item_group": "Grupo (ID)",
            "group_name": "Nombre del Grupo",
            "category": "Categoría (ID)",
            "category_name": "Categoría",
            "url": "URL",
            "package": "Empaque (ID)",
            "package_description": "Descripción de Empaque",
            "is_active": "Está Activo",
            "is_deleted": "Está Eliminado",
            "is_confirmed": "Está Confirmado",
            "created_at": "Fecha de Creación",
        }


class ProductListSerializer(serializers.Serializer):
    code = serializers.CharField()
    sku = serializers.CharField()
    description = serializers.CharField()
    base_net_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True
    )
    net_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True
    )
    gross_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True
    )
    iva_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True
    )
    aditional_tax_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True
    )
    retention_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True
    )
    price_configuration = serializers.CharField(allow_null=True)
    price_configuration_label = serializers.CharField(allow_null=True)
    obs = serializers.CharField(allow_null=True)
    package_unit = serializers.IntegerField(allow_null=True)
    min_package_purchase = serializers.IntegerField(allow_null=True)
    provider = serializers.IntegerField(allow_null=True)
    type = serializers.IntegerField(allow_null=True)
    type_name = serializers.CharField(allow_null=True)
    item_group = serializers.IntegerField(allow_null=True)
    group_name = serializers.CharField(allow_null=True)
    category = serializers.IntegerField(allow_null=True)
    category_name = serializers.CharField(allow_null=True)
    url = serializers.CharField(allow_null=True)
    package = serializers.IntegerField(allow_null=True)
    package_description = serializers.CharField(allow_null=True)
    is_active = serializers.BooleanField()
    is_deleted = serializers.BooleanField(allow_null=True)
    is_confirmed = serializers.BooleanField(allow_null=True)
    created_at = serializers.DateTimeField()


class MaterialSerializer(serializers.ModelSerializer):

    field_verbose_names = serializers.SerializerMethodField()

    type_name = serializers.SerializerMethodField()
    item_group_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    provider_name = serializers.SerializerMethodField()
    package_description = serializers.SerializerMethodField()

    base_net_amount = serializers.IntegerField(
        source="price.base_net_amount", read_only=True
    )
    base_net_amount_input = serializers.IntegerField(write_only=True)

    net_amount = serializers.IntegerField(source="price.net_amount", read_only=True)
    gross_amount = serializers.IntegerField(source="price.gross_amount", read_only=True)
    iva_amount = serializers.IntegerField(source="price.iva_amount", read_only=True)

    aditional_tax_amount = serializers.IntegerField(
        source="price.aditional_tax_amount", read_only=True
    )
    retention_amount = serializers.IntegerField(
        source="price.retention_amount", read_only=True
    )

    price_configuration = serializers.CharField(
        source="price.price_configuration.code", read_only=True
    )
    price_configuration_input = serializers.CharField(write_only=True)

    def get_type_name(self, obj):
        return obj.type.type if obj.type else None

    def get_item_group_name(self, obj):
        return obj.item_group.group_name if obj.item_group else None

    def get_category_name(self, obj):
        return obj.category.category if obj.category else None

    def get_provider_name(self, obj):
        return obj.provider.provider if obj.provider else None

    def get_package_description(self, obj):
        return obj.package.description if obj.package else None

    def get_field_verbose_names(self, obj):

        fields = [
            "id",
            "code",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "provider",
            "type",
            "item_group",
            "category",
            "url",
            "package",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
        ]

        return {
            f: (
                obj._meta.get_field(f).verbose_name
                if f in [x.name for x in obj._meta.fields]
                else f
            )
            for f in fields
        }

    def create(self, validated_data):

        request = self.context.get("request", None)

        validated_data.pop("created_by", None)
        validated_data.pop("created_at", None)
        validated_data.pop("updated_by", None)
        validated_data.pop("deleted_by", None)
        validated_data.pop("confirmed_by", None)

        base_net = validated_data.pop("base_net_amount_input")
        price_conf_value = validated_data.pop("price_configuration_input")

        from price.models import PriceConfiguration
        import uuid

        price_conf_obj = PriceConfiguration.objects.filter(
            code=str(price_conf_value).strip()
        ).first()

        if not price_conf_obj:
            price_conf_obj = PriceConfiguration.objects.filter(
                price_configuration=str(price_conf_value).strip()
            ).first()

        if not price_conf_obj:
            raise serializers.ValidationError(
                {"price_configuration": "No existe PriceConfiguration válido."}
            )

        user_code = getattr(getattr(request, "user", None), "code", "system")
        now = timezone.now()

        with transaction.atomic():

            material_code = str(uuid.uuid4())
            price_code = str(uuid.uuid4())

            price_obj = Price.objects.create(
                code=price_code,
                base_net_amount=base_net,
                net_amount=0,
                gross_amount=0,
                iva_amount=0,
                aditional_tax_amount=0,
                retention_amount=0,
                price_configuration=price_conf_obj,
                record_item_code=material_code,
                price_record_type=2,
                is_current=True,
                created_by=user_code,
                created_at=now,
            )

            formula_obj = getattr(price_conf_obj, "variable_formula", None)

            if formula_obj and formula_obj.price_variables:

                formula = formula_obj.price_variables

                from accounting.models import FiscalConfigurationDetail, FiscalDirective

                context = {
                    "base_net_amount": price_obj.base_net_amount,
                }

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

                try:

                    results = {}

                    for line in [l.strip() for l in formula.split(";") if l.strip()]:

                        if "=" not in line:
                            continue

                        key, expr = line.split("=")

                        key = key.strip()
                        expr = expr.strip()

                        for var, val in context.items():
                            expr = expr.replace(var, str(val))

                        results[key] = eval(expr)

                    price_obj.net_amount = int(results.get("net_amount", 0))
                    price_obj.iva_amount = int(results.get("iva_amount", 0))
                    price_obj.gross_amount = int(results.get("gross_amount", 0))
                    price_obj.aditional_tax_amount = int(
                        results.get("aditional_tax_amount", 0)
                    )
                    price_obj.retention_amount = int(
                        results.get("retention_amount", 0)
                    )

                except Exception:

                    price_obj.net_amount = 0
                    price_obj.iva_amount = 0
                    price_obj.gross_amount = 0
                    price_obj.aditional_tax_amount = 0
                    price_obj.retention_amount = 0

            price_obj.save()

            material = Material.objects.create(
                **validated_data,
                code=material_code,
                price=price_obj,
                created_by=user_code,
                created_at=now,
            )

        return material

    class Meta:
        model = Material

        fields = [
            "id",
            "code",
            "sku",
            "description",
            "base_net_amount",
            "base_net_amount_input",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "obs",
            "package_unit",
            "min_package_purchase",
            "provider",
            "provider_name",
            "type",
            "type_name",
            "item_group",
            "item_group_name",
            "category",
            "category_name",
            "url",
            "package",
            "package_description",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "price_configuration",
            "price_configuration_input",
            "field_verbose_names",
        ]

        read_only_fields = [
            "id",
            "code",
            "sku",
            "created_at",
            "base_net_amount",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "price_configuration",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    type_name = serializers.SerializerMethodField()
    item_group_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    provider_name = serializers.SerializerMethodField()

    base_net_amount = serializers.IntegerField(
        source="price.base_net_amount", read_only=True
    )
    base_net_amount_input = serializers.IntegerField(write_only=True)

    net_amount = serializers.IntegerField(source="price.net_amount", read_only=True)
    gross_amount = serializers.IntegerField(source="price.gross_amount", read_only=True)
    iva_amount = serializers.IntegerField(source="price.iva_amount", read_only=True)

    aditional_tax_amount = serializers.IntegerField(
        source="price.aditional_tax_amount", read_only=True
    )
    retention_amount = serializers.IntegerField(
        source="price.retention_amount", read_only=True
    )

    price_configuration = serializers.CharField(
        source="price.price_configuration.code", read_only=True
    )
    price_configuration_input = serializers.CharField(write_only=True)

    def get_type_name(self, obj):
        return obj.type.type if obj.type else None

    def get_item_group_name(self, obj):
        return obj.item_group.group_name if obj.item_group else None

    def get_category_name(self, obj):
        return obj.category.category if obj.category else None

    def get_provider_name(self, obj):
        return obj.provider.provider if obj.provider else None

    def get_field_verbose_names(self, obj):

        fields = [
            "id",
            "code",
            "description",
            "obs",
            "package_unit",
            "min_package_purchase",
            "provider",
            "type",
            "item_group",
            "category",
            "url",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
        ]

        return {
            f: (
                obj._meta.get_field(f).verbose_name
                if f in [x.name for x in obj._meta.fields]
                else f
            )
            for f in fields
        }

    def create(self, validated_data):

        request = self.context.get("request", None)

        validated_data.pop("created_by", None)
        validated_data.pop("created_at", None)
        validated_data.pop("updated_by", None)
        validated_data.pop("deleted_by", None)
        validated_data.pop("confirmed_by", None)

        base_net = validated_data.pop("base_net_amount_input")
        price_conf_value = validated_data.pop("price_configuration_input")

        from price.models import PriceConfiguration
        import uuid

        price_conf_obj = PriceConfiguration.objects.filter(
            code=str(price_conf_value).strip()
        ).first()

        if not price_conf_obj:
            price_conf_obj = PriceConfiguration.objects.filter(
                price_configuration=str(price_conf_value).strip()
            ).first()

        if not price_conf_obj:
            raise serializers.ValidationError(
                {"price_configuration": "No existe PriceConfiguration válido."}
            )

        user_code = getattr(getattr(request, "user", None), "code", "system")
        now = timezone.now()

        with transaction.atomic():

            service_code = str(uuid.uuid4())
            price_code = str(uuid.uuid4())

            price_obj = Price.objects.create(
                code=price_code,
                base_net_amount=base_net,
                net_amount=0,
                gross_amount=0,
                iva_amount=0,
                aditional_tax_amount=0,
                retention_amount=0,
                price_configuration=price_conf_obj,
                record_item_code=service_code,
                price_record_type=3,
                is_current=True,
                created_by=user_code,
                created_at=now,
            )

            formula_obj = getattr(price_conf_obj, "variable_formula", None)

            if formula_obj and formula_obj.price_variables:

                formula = formula_obj.price_variables

                from accounting.models import FiscalConfigurationDetail, FiscalDirective

                context = {
                    "base_net_amount": price_obj.base_net_amount,
                }

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

                try:

                    results = {}

                    for line in [l.strip() for l in formula.split(";") if l.strip()]:

                        if "=" not in line:
                            continue

                        key, expr = line.split("=")

                        key = key.strip()
                        expr = expr.strip()

                        for var, val in context.items():
                            expr = expr.replace(var, str(val))

                        results[key] = eval(expr)

                    price_obj.net_amount = int(results.get("net_amount", 0))
                    price_obj.iva_amount = int(results.get("iva_amount", 0))
                    price_obj.gross_amount = int(results.get("gross_amount", 0))
                    price_obj.aditional_tax_amount = int(
                        results.get("aditional_tax_amount", 0)
                    )
                    price_obj.retention_amount = int(
                        results.get("retention_amount", 0)
                    )

                except Exception:

                    price_obj.net_amount = 0
                    price_obj.iva_amount = 0
                    price_obj.gross_amount = 0
                    price_obj.aditional_tax_amount = 0
                    price_obj.retention_amount = 0

            price_obj.save()

            service = Service.objects.create(
                **validated_data,
                code=service_code,
                price=price_obj,
                created_by=user_code,
                created_at=now,
            )

        return service

    class Meta:
        model = Service
        fields = [
            "id",
            "code",
            "sku",
            "description",
            "base_net_amount",
            "base_net_amount_input",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "obs",
            "package_unit",
            "min_package_purchase",
            "provider",
            "provider_name",
            "type",
            "type_name",
            "item_group",
            "item_group_name",
            "category",
            "category_name",
            "url",
            "is_active",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "price_configuration",
            "price_configuration_input",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "code",
            "sku",
            "created_at",
            "base_net_amount",
            "net_amount",
            "gross_amount",
            "iva_amount",
            "aditional_tax_amount",
            "retention_amount",
            "price_configuration",
        ]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",
            "menu",
            "description",
            "franchise_only",
            "background_color",
            "text_color",
        ]
        read_only_fields = ["id"]


class ItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemGroup
        fields = ["id", "group_name", "description"]
        read_only_fields = ["id"]


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ["id", "category", "description"]
        read_only_fields = ["id"]


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class RestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restriction
        fields = ["id", "restriction", "description"]
        read_only_fields = ["id"]


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = "__all__"


class CatalogListSerializer(serializers.Serializer):
    sku = serializers.CharField()
    cover_image = serializers.CharField(allow_null=True, required=False)
    menu = serializers.IntegerField(allow_null=True, required=False)
    menu_name = serializers.CharField(allow_null=True, required=False)
    category = serializers.IntegerField(allow_null=True, required=False)
    category_name = serializers.CharField(allow_null=True, required=False)
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
    obs = serializers.CharField(allow_null=True, required=False)
    chef_recommendation = serializers.BooleanField()
    item_type = serializers.IntegerField(allow_null=True, required=False)
    type_name = serializers.CharField(allow_null=True, required=False)
    item_group = serializers.IntegerField(allow_null=True, required=False)
    group_name = serializers.CharField(allow_null=True, required=False)

    base_net_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True, required=False
    )
    net_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True, required=False
    )
    gross_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True, required=False
    )
    iva_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True, required=False
    )
    aditional_tax_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True, required=False
    )
    retention_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, allow_null=True, required=False
    )

    price_configuration = serializers.CharField(allow_null=True, required=False)
    min_quantity_purchase = serializers.IntegerField(allow_null=True, required=False)
    rations_quantity = serializers.IntegerField(allow_null=True, required=False)

    item_configuration = serializers.CharField(allow_null=True, required=False)
    configuration = serializers.CharField(allow_null=True, required=False)

    is_visible = serializers.BooleanField()
    is_confirmed = serializers.BooleanField(allow_null=True, required=False)
    created_at = serializers.DateTimeField()


class ItemConfigurationSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    def get_field_verbose_names(self, obj):
        field_names = [
            "id",
            "code",
            "configuration",
            "description",
            "package",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
            "updated_by",
            "deleted_by",
            "log",
            "version",
        ]
        return {
            field: (
                obj._meta.get_field(field).verbose_name
                if hasattr(obj._meta, "get_field")
                else field
            )
            for field in field_names
        }

    def create(self, validated_data):
        request = self.context.get("request", None)

        # Si el front manda estos campos, los controlamos acá
        validated_data.pop("created_by", None)
        validated_data.pop("updated_by", None)
        validated_data.pop("confirmed_by", None)
        validated_data.pop("deleted_by", None)

        user_code = getattr(getattr(request, "user", None), "code", "system")
        now = timezone.now()

        item_config = ItemConfiguration._default_manager.create(
            **validated_data,
            created_by=user_code,
            created_at=now,
        )
        return item_config

    def update(self, instance, validated_data):
        request = self.context.get("request", None)
        user_code = getattr(getattr(request, "user", None), "code", "system")
        now = timezone.now()

        # Evitar que el front pise auditoría sensible
        validated_data.pop("created_by", None)
        validated_data.pop("created_at", None)
        validated_data.pop("deleted_by", None)
        validated_data.pop("deleted_at", None)
        validated_data.pop("confirmed_by", None)
        validated_data.pop("confirmed_at", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.updated_by = user_code
        instance.updated_at = now
        instance.save()
        return instance

    class Meta:
        model = ItemConfiguration
        fields = [
            "id",
            "code",
            "configuration",
            "description",
            "package",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "created_by",
            "confirmed_by",
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
            "created_by",
            "updated_at",
            "updated_by",
            "confirmed_at",
            "confirmed_by",
            "deleted_at",
            "deleted_by",
        ]


class PackageSerializer(serializers.ModelSerializer):
    field_verbose_names = serializers.SerializerMethodField()

    def get_field_verbose_names(self, obj):
        field_names = [
            "id",
            "description",
            "package_type",
            "transport_type",
            "size",
            "weight",
            "measure_unit",
            "quantity_unit",
            "storage_instructions",
            "transport_instructions",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]
        return {
            field: (
                obj._meta.get_field(field).verbose_name
                if hasattr(obj._meta, "get_field")
                else field
            )
            for field in field_names
        }

    class Meta:
        model = Package
        fields = [
            "id",
            "description",
            "package_type",
            "transport_type",
            "size",
            "weight",
            "measure_unit",
            "quantity_unit",
            "storage_instructions",
            "transport_instructions",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "field_verbose_names",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
            "field_verbose_names",
        ]


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = ["id", "type", "description"]
        read_only_fields = ["id"]


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = ["id", "measure_unit", "description"]
        read_only_fields = ["id"]


class InstructionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionType
        fields = [
            "id",
            "type",
            "description",
            "is_deleted",
            "is_confirmed",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "confirmed_at",
            "deleted_at",
        ]
