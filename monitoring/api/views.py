from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from monitoring.repositories import repository_registry

from .serializers import ProductTypeSerializer, StoreSerializer


class ProductTypeViewSet(viewsets.ViewSet):
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_repository(self):
        return repository_registry.product_types

    def list(self, request):
        queryset = self.get_repository().get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self._get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_repository().add(**serializer.validated_data)
        output_serializer = self.serializer_class(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        return self._update(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update(request, pk, partial=True)

    def destroy(self, request, pk=None):
        deleted = self.get_repository().delete(pk)
        if not deleted:
            raise NotFound("Product type not found.")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_object(self, pk):
        instance = self.get_repository().get_by_id(pk)
        if not instance:
            raise NotFound("Product type not found.")
        return instance

    def _update(self, request, pk, partial):
        instance = self._get_object(pk)
        serializer = self.serializer_class(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        updated_instance = self.get_repository().update(
            pk, **serializer.validated_data
        )
        if not updated_instance:
            raise NotFound("Product type not found.")

        output_serializer = self.serializer_class(updated_instance)
        return Response(output_serializer.data)


class StoreViewSet(viewsets.ViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_repository(self):
        return repository_registry.stores

    def list(self, request):
        queryset = self.get_repository().get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self._get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_repository().add(**serializer.validated_data)
        output_serializer = self.serializer_class(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        return self._update(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update(request, pk, partial=True)

    def destroy(self, request, pk=None):
        deleted = self.get_repository().delete(pk)
        if not deleted:
            raise NotFound("Store not found.")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_object(self, pk):
        instance = self.get_repository().get_by_id(pk)
        if not instance:
            raise NotFound("Store not found.")
        return instance

    def _update(self, request, pk, partial):
        instance = self._get_object(pk)
        serializer = self.serializer_class(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        updated_instance = self.get_repository().update(
            pk, **serializer.validated_data
        )
        if not updated_instance:
            raise NotFound("Store not found.")

        output_serializer = self.serializer_class(updated_instance)
        return Response(output_serializer.data)
