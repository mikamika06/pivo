from django.db import models


class MonitoredObject(models.Model):

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str: 
        return self.name


class ProductType(MonitoredObject):
    slug = models.SlugField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Product type"
        verbose_name_plural = "Product types"


class Store(MonitoredObject):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"


class Product(MonitoredObject):
    product_type = models.ForeignKey(
        ProductType, related_name="products", on_delete=models.PROTECT
    )
    store = models.ForeignKey(
        Store, related_name="products", on_delete=models.CASCADE
    )
    sku = models.CharField(max_length=32, unique=True)
    regular_price = models.DecimalField(max_digits=8, decimal_places=2)
    promo_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    promo_ends_at = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class BeerProduct(Product):
    class Meta:
        proxy = True
        verbose_name = "Beer product"
        verbose_name_plural = "Beer products"
