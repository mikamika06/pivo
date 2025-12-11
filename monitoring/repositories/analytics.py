
from django.db.models import Avg, Count, Sum, F, Q, Case, When, Value, DecimalField, CharField
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from monitoring.models import Product, ProductType, Store
import logging


logger = logging.getLogger(__name__)


class AnalyticsRepository:
    
    def get_avg_prices_by_product_type(self):
        logger.info("Executing avg_prices_by_product_type query")
        
        result = ProductType.objects.filter(
            products__is_active=True
        ).annotate(
            product_type_name=F('name'),
            avg_regular_price=Avg('products__regular_price'),
            avg_promo_price=Avg('products__promo_price'),
            product_count=Count('products', filter=Q(products__is_active=True))
        ).values(
            'id',
            'product_type_name',
            'avg_regular_price',
            'avg_promo_price',
            'product_count'
        ).order_by('-avg_regular_price')
        
        logger.info(f"Query returned {len(result)} product types")
        return result
    
    def get_store_statistics_by_city(self):
        logger.info("Executing store_statistics_by_city query")
        from django.db.models import OuterRef, Subquery
        
        products_per_store = Product.objects.filter(
            store=OuterRef('pk'),
            is_active=True
        ).values('store').annotate(
            count=Count('id')
        ).values('count')
        
        promo_products_per_store = Product.objects.filter(
            store=OuterRef('pk'),
            is_active=True,
            promo_price__isnull=False
        ).values('store').annotate(
            count=Count('id')
        ).values('count')
        
        avg_price_per_store = Product.objects.filter(
            store=OuterRef('pk'),
            is_active=True
        ).values('store').annotate(
            avg=Avg('regular_price')
        ).values('avg')
        
        from django.db.models import CharField
        from django.db.models.functions import Coalesce
        
        stores_data = Store.objects.filter(
            is_active=True
        ).values('city').annotate(
            store_count=Count('id', distinct=True),
            total_products=Count('products', filter=Q(products__is_active=True)),
            avg_price=Avg('products__regular_price', filter=Q(products__is_active=True)),
            promo_products_count=Count(
                'products',
                filter=Q(products__is_active=True, products__promo_price__isnull=False)
            )
        ).order_by('-store_count')
        
        logger.info(f"Query returned {len(stores_data)} cities")
        return stores_data
    
    def get_top_expensive_products(self, limit=10):
        logger.info(f"Executing top_expensive_products query with limit={limit}")
        
        products = Product.objects.filter(
            is_active=True
        ).select_related('store', 'product_type').annotate(
            product_name=F('name'),
            store_name=F('store__name'),
            city=F('store__city'),
            product_type_name=F('product_type__name'),
            discount=Case(
                When(
                    promo_price__isnull=False,
                    then=F('regular_price') - F('promo_price')
                ),
                default=Value(0),
                output_field=DecimalField()
            )
        ).values(
            'product_name',
            'sku',
            'regular_price',
            'promo_price',
            'discount',
            'store_name',
            'city',
            'product_type_name'
        ).order_by('-regular_price')[:limit]
        
        logger.info(f"Query returned {len(products)} products")
        return products
    
    def get_products_by_price_ranges(self):
        logger.info("Executing products_by_price_ranges query")
        
        total_products = Product.objects.filter(is_active=True).count()
        
        products = Product.objects.filter(
            is_active=True
        ).annotate(
            price_range=Case(
                When(regular_price__lt=30, then=Value('0-30 грн')),
                When(regular_price__gte=30, regular_price__lt=60, then=Value('30-60 грн')),
                When(regular_price__gte=60, regular_price__lt=100, then=Value('60-100 грн')),
                When(regular_price__gte=100, then=Value('100+ грн')),
                output_field=CharField()
            ),
            product_type_name=F('product_type__name')
        ).values('price_range', 'product_type_name').annotate(
            count=Count('id')
        ).annotate(
            percentage=Case(
                When(count__gt=0, then=F('count') * 100.0 / total_products),
                default=Value(0.0),
                output_field=DecimalField()
            )
        ).order_by('price_range', 'product_type_name')
        
        logger.info(f"Query returned {len(products)} price range groups")
        return products
    
    def get_promo_analysis_by_store(self):
        logger.info("Executing promo_analysis_by_store query")
        
        stores = Store.objects.filter(
            is_active=True,
            products__promo_price__isnull=False,
            products__is_active=True
        ).annotate(
            store_name=F('name'),
            promo_products=Count('products', filter=Q(
                products__promo_price__isnull=False,
                products__is_active=True
            )),
            avg_discount_amount=Avg(
                F('products__regular_price') - F('products__promo_price'),
                filter=Q(products__promo_price__isnull=False, products__is_active=True)
            ),
            avg_discount_percent=Avg(
                (F('products__regular_price') - F('products__promo_price')) * 100.0 / F('products__regular_price'),
                filter=Q(products__promo_price__isnull=False, products__is_active=True),
                output_field=DecimalField()
            ),
            total_savings=Sum(
                F('products__regular_price') - F('products__promo_price'),
                filter=Q(products__promo_price__isnull=False, products__is_active=True)
            )
        ).values(
            'id',
            'store_name',
            'city',
            'promo_products',
            'avg_discount_percent',
            'total_savings'
        ).order_by('-promo_products')
        
        logger.info(f"Query returned {len(stores)} stores with promo products")
        return stores
    
    def get_product_creation_dynamics(self):
        logger.info("Executing product_creation_dynamics query")
        
        one_year_ago = timezone.now() - timedelta(days=365)
        
        products = Product.objects.filter(
            created_at__gte=one_year_ago,
            is_active=True
        ).annotate(
            month=TruncMonth('created_at'),
            product_type_name=F('product_type__name')
        ).values('month', 'product_type_name').annotate(
            products_added=Count('id')
        ).order_by('month', 'product_type_name')
        
        logger.info(f"Query returned {len(products)} time period records")
        return products
