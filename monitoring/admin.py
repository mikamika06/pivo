from django.contrib import admin
from .models import ProductType, Store, Product, BeerProduct


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address', 'is_active', 'created_at')
    list_filter = ('is_active', 'city')
    search_fields = ('name', 'city', 'address')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'product_type', 'store', 'regular_price', 'promo_price', 'is_active')
    list_filter = ('is_active', 'product_type', 'store')
    search_fields = ('name', 'sku', 'description')
    list_select_related = ('product_type', 'store')


@admin.register(BeerProduct)
class BeerProductAdmin(ProductAdmin):
    pass
