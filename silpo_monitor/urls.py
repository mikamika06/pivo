from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from web_interface.views import home_redirect_view

from monitoring.api.views import ProductTypeViewSet, StoreViewSet, ProductViewSet
from monitoring.api.analytics_views import (
    avg_prices_by_product_type_view,
    store_statistics_by_city_view,
    top_expensive_products_view,
    products_by_price_ranges_view,
    promo_analysis_by_store_view,
    product_creation_dynamics_view
)

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
    path("api/analytics/avg-prices-by-type/", avg_prices_by_product_type_view, name="analytics-avg-prices"),
    path("api/analytics/store-statistics/", store_statistics_by_city_view, name="analytics-store-stats"),
    path("api/analytics/top-expensive-products/", top_expensive_products_view, name="analytics-top-expensive"),
    path("api/analytics/products-by-price-ranges/", products_by_price_ranges_view, name="analytics-price-ranges"),
    path("api/analytics/promo-analysis/", promo_analysis_by_store_view, name="analytics-promo"),
    path("api/analytics/product-creation-dynamics/", product_creation_dynamics_view, name="analytics-dynamics"),
]

handler404 = 'web_interface.views.custom_404_view'
