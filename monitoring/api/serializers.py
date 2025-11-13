from rest_framework import serializers

from monitoring.models import ProductType


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
