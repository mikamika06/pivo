from rest_framework import serializers

from monitoring.models import ProductType, Store, Product


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "description": {"required": False, "allow_blank": True},
            "is_active": {"required": False},
        }


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "description",
            "is_active",
            "address",
            "city",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {
            "description": {"required": False, "allow_blank": True},
            "is_active": {"required": False},
        }


class ProductSerializer(serializers.ModelSerializer):
    product_type_info = ProductTypeSerializer(source="product_type", read_only=True)
    store_info = StoreSerializer(source="store", read_only=True)
    
    product_type = serializers.PrimaryKeyRelatedField(
        queryset=ProductType.objects.all(),
        write_only=False
    )
    store = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(),
        write_only=False
    )
    
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "sku",
            "description",
            "product_type",
            "product_type_info",
            "store",
            "store_info",
            "regular_price",
            "promo_price",
            "promo_ends_at",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "product_type_info",
            "store_info",
        )
        extra_kwargs = {
            "description": {"required": False, "allow_blank": True},
            "promo_price": {"required": False, "allow_null": True},
            "promo_ends_at": {"required": False, "allow_null": True},
            "is_active": {"required": False},
        }
