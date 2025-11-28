from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from web_interface.views import home_redirect_view

from monitoring.api.views import ProductTypeViewSet, StoreViewSet, ProductViewSet

router = DefaultRouter()
router.register("product-types", ProductTypeViewSet, basename="product-type")
router.register("stores", StoreViewSet, basename="store")
router.register("products", ProductViewSet, basename="product")

urlpatterns = [
    path("", home_redirect_view, name="home"),  
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("products/", include("web_interface.urls")),
]

handler404 = 'web_interface.views.custom_404_view'
