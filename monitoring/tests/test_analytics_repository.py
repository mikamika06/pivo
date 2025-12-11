
from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from monitoring.models import Product, ProductType, Store
from monitoring.repositories.analytics import AnalyticsRepository


class AnalyticsRepositoryTestCase(TestCase):
    
    def setUp(self):
        self.beer_type = ProductType.objects.create(
            name='Пиво',
            slug='beer',
            description='Пивні напої'
        )
        self.snacks_type = ProductType.objects.create(
            name='Снеки',
            slug='snacks',
            description='Снеки та закуски'
        )
        
        self.store_kyiv_1 = Store.objects.create(
            name='Сільпо Хрещатик',
            city='Київ',
            address='вул. Хрещатик 1'
        )
        self.store_kyiv_2 = Store.objects.create(
            name='Сільпо Оболонь',
            city='Київ',
            address='пр. Оболонський 5'
        )
        self.store_lviv = Store.objects.create(
            name='Сільпо Львів Центр',
            city='Львів',
            address='пл. Ринок 1'
        )
        
        self.product_beer_1 = Product.objects.create(
            name='Оболонь Світле',
            sku='BEER001',
            product_type=self.beer_type,
            store=self.store_kyiv_1,
            regular_price=Decimal('45.00'),
            promo_price=Decimal('38.00')
        )
        self.product_beer_2 = Product.objects.create(
            name='Львівське 1715',
            sku='BEER002',
            product_type=self.beer_type,
            store=self.store_kyiv_1,
            regular_price=Decimal('55.00'),
            promo_price=None
        )
        self.product_beer_3 = Product.objects.create(
            name='Чернігівське',
            sku='BEER003',
            product_type=self.beer_type,
            store=self.store_lviv,
            regular_price=Decimal('42.00'),
            promo_price=Decimal('35.00')
        )
        self.product_snack_1 = Product.objects.create(
            name='Чіпси Лейс',
            sku='SNACK001',
            product_type=self.snacks_type,
            store=self.store_kyiv_2,
            regular_price=Decimal('28.00'),
            promo_price=Decimal('22.00')
        )
        self.product_snack_2 = Product.objects.create(
            name='Горішки',
            sku='SNACK002',
            product_type=self.snacks_type,
            store=self.store_kyiv_2,
            regular_price=Decimal('65.00'),
            promo_price=None
        )
        
        self.repo = AnalyticsRepository()
    
    def test_get_avg_prices_by_product_type(self):
        result = list(self.repo.get_avg_prices_by_product_type())
        
        self.assertEqual(len(result), 2)
        
        beer_result = next((r for r in result if r['product_type_name'] == 'Пиво'), None)
        self.assertIsNotNone(beer_result)
        
        self.assertAlmostEqual(float(beer_result['avg_regular_price']), 47.33, places=2)
        
        self.assertEqual(beer_result['product_count'], 3)
        
        self.assertAlmostEqual(float(beer_result['avg_promo_price']), 36.50, places=2)
    
    def test_get_avg_prices_by_product_type_ordering(self):
        result = list(self.repo.get_avg_prices_by_product_type())
        
        if len(result) > 1:
            for i in range(len(result) - 1):
                self.assertGreaterEqual(
                    result[i]['avg_regular_price'],
                    result[i + 1]['avg_regular_price']
                )
    
    def test_get_store_statistics_by_city(self):
        result = list(self.repo.get_store_statistics_by_city())
        
        cities = [r['city'] for r in result]
        self.assertIn('Київ', cities)
        self.assertIn('Львів', cities)
        
        kyiv_stats = next((r for r in result if r['city'] == 'Київ'), None)
        self.assertIsNotNone(kyiv_stats)
        
        self.assertEqual(kyiv_stats['store_count'], 2)
        
        self.assertEqual(kyiv_stats['total_products'], 4)
        
        self.assertEqual(kyiv_stats['promo_products_count'], 2)
    
    def test_get_top_expensive_products_default_limit(self):
        result = list(self.repo.get_top_expensive_products())
        
        self.assertLessEqual(len(result), 10)
        
        if len(result) > 0:
            self.assertEqual(result[0]['product_name'], 'Горішки')
            self.assertEqual(result[0]['regular_price'], Decimal('65.00'))
    
    def test_get_top_expensive_products_custom_limit(self):
        result = list(self.repo.get_top_expensive_products(limit=3))
        
        self.assertEqual(len(result), 3)
        
        for i in range(len(result) - 1):
            self.assertGreaterEqual(
                result[i]['regular_price'],
                result[i + 1]['regular_price']
            )
    
    def test_get_top_expensive_products_discount_calculation(self):
        result = list(self.repo.get_top_expensive_products())
        
        beer1 = next((p for p in result if p['sku'] == 'BEER001'), None)
        self.assertIsNotNone(beer1)
        
        self.assertEqual(beer1['discount'], Decimal('7.00'))
        
        beer2 = next((p for p in result if p['sku'] == 'BEER002'), None)
        self.assertIsNotNone(beer2)
        
        self.assertEqual(beer2['discount'], Decimal('0'))
    
    def test_get_products_by_price_ranges(self):
        result = list(self.repo.get_products_by_price_ranges())
        
        self.assertGreater(len(result), 0)
        
        price_ranges = set(r['price_range'] for r in result)
        
        self.assertIn('0-30 грн', price_ranges)
        
        self.assertIn('30-60 грн', price_ranges)
    
    def test_get_products_by_price_ranges_count(self):
        result = list(self.repo.get_products_by_price_ranges())
        
        range_30_60_beer = next(
            (r for r in result if r['price_range'] == '30-60 грн' and r['product_type_name'] == 'Пиво'),
            None
        )
        
        if range_30_60_beer:
            self.assertEqual(range_30_60_beer['count'], 3)
    
    def test_get_promo_analysis_by_store(self):
        result = list(self.repo.get_promo_analysis_by_store())
        
        self.assertGreater(len(result), 0)
        
        store_khreschatyk = next(
            (s for s in result if s['store_name'] == 'Сільпо Хрещатик'),
            None
        )
        
        if store_khreschatyk:
            self.assertEqual(store_khreschatyk['promo_products'], 1)
            
            self.assertEqual(store_khreschatyk['total_savings'], Decimal('7.00'))
    
    def test_get_promo_analysis_ordering(self):
        result = list(self.repo.get_promo_analysis_by_store())
        
        if len(result) > 1:
            for i in range(len(result) - 1):
                self.assertGreaterEqual(
                    result[i]['promo_products'],
                    result[i + 1]['promo_products']
                )
    
    def test_get_product_creation_dynamics(self):
        result = list(self.repo.get_product_creation_dynamics())
        
        self.assertGreater(len(result), 0)
        
        if len(result) > 0:
            first_record = result[0]
            self.assertIn('month', first_record)
            self.assertIn('product_type_name', first_record)
            self.assertIn('products_added', first_record)
    
    def test_get_product_creation_dynamics_filtering(self):
        old_product = Product.objects.create(
            name='Старий продукт',
            sku='OLD001',
            product_type=self.beer_type,
            store=self.store_kyiv_1,
            regular_price=Decimal('100.00')
        )
        old_product.created_at = timezone.now() - timedelta(days=400)
        old_product.save()
        
        result = list(self.repo.get_product_creation_dynamics())
        
        for record in result:
            if record['product_type_name'] == 'Пиво':
                month_date = record['month']
                self.assertGreaterEqual(
                    month_date,
                    timezone.now() - timedelta(days=365)
                )
