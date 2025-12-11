from django.test import TestCase
from monitoring.charts.bokeh_charts import BokehChartsGenerator
from decimal import Decimal


class BokehChartsTest(TestCase):
    
    def setUp(self):
        self.charts_generator = BokehChartsGenerator()
    
    def test_create_avg_prices_chart_bokeh(self):
        data = [
            {
                'product_type_name': 'Пиво',
                'avg_regular_price': Decimal('45.50'),
                'avg_promo_price': Decimal('38.00'),
                'product_count': 100
            },
            {
                'product_type_name': 'Вино',
                'avg_regular_price': Decimal('120.00'),
                'avg_promo_price': Decimal('95.00'),
                'product_count': 50
            }
        ]
        
        script, div = self.charts_generator.create_avg_prices_chart_bokeh(data)
        
        self.assertIsNotNone(script)
        self.assertIsNotNone(div)
        self.assertIn('Bokeh', script)
        self.assertIn('div', div)
    
    def test_create_store_statistics_chart(self):
        data = [
            {
                'city': 'Київ',
                'store_count': 50,
                'total_products': 5000,
                'promo_products_count': 1200,
                'avg_price': Decimal('65.00')
            },
            {
                'city': 'Львів',
                'store_count': 30,
                'total_products': 3500,
                'promo_products_count': 800,
                'avg_price': Decimal('60.00')
            }
        ]
        
        script, div = self.charts_generator.create_store_statistics_chart(data)
        
        self.assertIsNotNone(script)
        self.assertIsNotNone(div)
        self.assertIn('Bokeh', script)
    
    def test_create_top_expensive_products_chart(self):
        data = [
            {
                'product_name': 'Віскі Johnnie Walker',
                'regular_price': Decimal('1500.00'),
                'promo_price': Decimal('1200.00'),
                'store_name': 'Сільпо Центр',
                'city': 'Київ'
            }
        ]
        
        script, div = self.charts_generator.create_top_expensive_products_chart(data)
        
        self.assertIsNotNone(script)
        self.assertIsNotNone(div)
    
    def test_create_price_ranges_chart(self):
        data = [
            {
                'price_range': '0-30 грн',
                'product_type_name': 'Пиво',
                'count': 150
            },
            {
                'price_range': '30-60 грн',
                'product_type_name': 'Пиво',
                'count': 200
            }
        ]
        
        script, div = self.charts_generator.create_price_ranges_chart(data)
        
        self.assertIsNotNone(script)
        self.assertIsNotNone(div)
    
    def test_create_promo_analysis_chart(self):
        data = [
            {
                'store_name': 'Сільпо Центр',
                'city': 'Київ',
                'promo_products': 500,
                'avg_discount_percent': Decimal('15.5'),
                'total_savings': Decimal('25000.00')
            }
        ]
        
        script, div = self.charts_generator.create_promo_analysis_chart(data)
        
        self.assertIsNotNone(script)
        self.assertIsNotNone(div)
    
    def test_create_product_creation_dynamics_chart(self):
        from datetime import datetime
        data = [
            {
                'month': datetime(2024, 1, 1),
                'product_type_name': 'Пиво',
                'products_added': 50
            },
            {
                'month': datetime(2024, 2, 1),
                'product_type_name': 'Пиво',
                'products_added': 75
            }
        ]
        
        script, div = self.charts_generator.create_product_creation_dynamics_chart(data)
        
        self.assertIsNotNone(script)
        self.assertIsNotNone(div)
    
    def test_empty_data_handling(self):
        script, div = self.charts_generator.create_avg_prices_chart_bokeh([])
        
        self.assertIsNotNone(script)
        self.assertIsNotNone(div)
