
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal

from monitoring.models import Product, ProductType, Store


class AnalyticsAPITestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.beer_type = ProductType.objects.create(
            name='Пиво',
            slug='beer'
        )
        self.snacks_type = ProductType.objects.create(
            name='Снеки',
            slug='snacks'
        )
        
        self.store_kyiv = Store.objects.create(
            name='Сільпо Київ',
            city='Київ',
            address='вул. Тестова 1'
        )
        self.store_lviv = Store.objects.create(
            name='Сільпо Львів',
            city='Львів',
            address='вул. Львівська 2'
        )
        
        Product.objects.create(
            name='Оболонь',
            sku='BEER001',
            product_type=self.beer_type,
            store=self.store_kyiv,
            regular_price=Decimal('45.00'),
            promo_price=Decimal('38.00')
        )
        Product.objects.create(
            name='Львівське',
            sku='BEER002',
            product_type=self.beer_type,
            store=self.store_lviv,
            regular_price=Decimal('50.00')
        )
        Product.objects.create(
            name='Чіпси',
            sku='SNACK001',
            product_type=self.snacks_type,
            store=self.store_kyiv,
            regular_price=Decimal('28.00'),
            promo_price=Decimal('22.00')
        )
    
    def test_avg_prices_by_type_api(self):
        url = reverse('analytics-avg-prices')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('data', response.data)
        self.assertIn('shape', response.data)
        self.assertIn('columns', response.data)
        self.assertIn('statistics', response.data)
        
        self.assertGreater(len(response.data['data']), 0)
        
        self.assertIn('total_product_types', response.data['statistics'])
        self.assertIn('avg_regular_price_overall', response.data['statistics'])
    
    def test_store_statistics_api(self):
        url = reverse('analytics-store-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        
        self.assertIn('statistics', response.data)
        self.assertIn('total_cities', response.data['statistics'])
        self.assertIn('total_stores', response.data['statistics'])
    
    def test_store_statistics_with_city_filter(self):
        url = reverse('analytics-store-stats')
        response = self.client.get(url, {'city': 'Київ'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for item in response.data['data']:
            self.assertIn('Київ', item['city'])
    
    def test_top_expensive_products_api(self):
        url = reverse('analytics-top-expensive')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        
        self.assertIn('statistics', response.data)
        self.assertIn('avg_regular_price', response.data['statistics'])
        self.assertIn('products_with_promo', response.data['statistics'])
    
    def test_top_expensive_products_with_limit(self):
        url = reverse('analytics-top-expensive')
        response = self.client.get(url, {'limit': 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertLessEqual(len(response.data['data']), 2)
    
    def test_products_by_price_ranges_api(self):
        url = reverse('analytics-price-ranges')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        
        self.assertIn('statistics', response.data)
        self.assertIn('total_products', response.data['statistics'])
        self.assertIn('most_popular_range', response.data['statistics'])
    
    def test_promo_analysis_api(self):
        url = reverse('analytics-promo')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        
        self.assertIn('statistics', response.data)
        self.assertIn('total_promo_products', response.data['statistics'])
        self.assertIn('avg_discount_percent', response.data['statistics'])
    
    def test_product_creation_dynamics_api(self):
        url = reverse('analytics-dynamics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        
        self.assertIn('statistics', response.data)
        self.assertIn('total_months', response.data['statistics'])
        self.assertIn('total_products_added', response.data['statistics'])
    
    def test_api_response_shape(self):
        url = reverse('analytics-avg-prices')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIsInstance(response.data['shape'], list)
        self.assertEqual(len(response.data['shape']), 2)
        
        self.assertEqual(response.data['shape'][0], len(response.data['data']))
    
    def test_api_columns_list(self):
        url = reverse('analytics-avg-prices')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIsInstance(response.data['columns'], list)
        
        if len(response.data['data']) > 0:
            self.assertGreater(len(response.data['columns']), 0)
            
            first_record = response.data['data'][0]
            for key in first_record.keys():
                self.assertIn(key, response.data['columns'])
    
    def test_api_error_handling(self):
        url = reverse('analytics-top-expensive')
        response = self.client.get(url, {'limit': 'invalid'})
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
    
    def test_empty_data_response(self):
        Product.objects.all().delete()
        
        url = reverse('analytics-avg-prices')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['data'], [])
        self.assertEqual(response.data['shape'], [0, 0])
        self.assertEqual(response.data['columns'], [])
