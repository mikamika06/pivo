from django.test import TestCase
from monitoring.charts.plotly_charts import PlotlyChartsGenerator
import pandas as pd


class PlotlyChartsTestCase(TestCase):
    
    def setUp(self):
        self.chart_generator = PlotlyChartsGenerator()
        
        self.test_data_avg_prices = pd.DataFrame({
            'product_type_name': ['Пиво', 'Вино', 'Горілка'],
            'avg_regular_price': [50.0, 120.0, 180.0],
            'avg_promo_price': [40.0, 100.0, 150.0],
            'product_count': [100, 50, 30]
        })
        
        self.test_data_store_stats = pd.DataFrame({
            'city': ['Київ', 'Львів', 'Одеса'],
            'store_count': [10, 5, 7],
            'total_products': [500, 250, 350],
            'promo_products_count': [100, 50, 70],
            'avg_price': [75.5, 80.2, 70.3]
        })
        
        self.test_data_top_expensive = pd.DataFrame({
            'product_name': ['Продукт A', 'Продукт B', 'Продукт C'],
            'sku': ['SKU001', 'SKU002', 'SKU003'],
            'regular_price': [500.0, 450.0, 400.0],
            'store_name': ['Магазин 1', 'Магазин 2', 'Магазин 3'],
            'city': ['Київ', 'Львів', 'Одеса'],
            'discount_percent': [10.0, 15.0, 5.0]
        })
        
        self.test_data_price_ranges = pd.DataFrame({
            'price_range': ['0-50', '50-100', '100-200'],
            'product_type_name': ['Пиво', 'Вино', 'Горілка'],
            'product_count': [100, 50, 30]
        })
        
        self.test_data_promo_analysis = pd.DataFrame({
            'store_name': ['Магазин 1', 'Магазин 2', 'Магазин 3'],
            'city': ['Київ', 'Львів', 'Одеса'],
            'promo_products_count': [50, 30, 40],
            'avg_discount_percent': [15.0, 12.0, 18.0],
            'total_savings': [1000.0, 600.0, 800.0]
        })
        
        self.test_data_product_dynamics = pd.DataFrame({
            'month': ['2024-01', '2024-02', '2024-03'],
            'product_type_name': ['Пиво', 'Пиво', 'Вино'],
            'products_added': [20, 25, 15]
        })
    
    def test_create_avg_prices_chart(self):
        chart_html = self.chart_generator.create_avg_prices_chart(self.test_data_avg_prices)
        
        self.assertIsInstance(chart_html, str)
        self.assertIn('plotly', chart_html.lower())
        self.assertIn('chart1', chart_html)
        self.assertGreater(len(chart_html), 100)
        self.assertIn('Середні ціни', chart_html)
    
    def test_create_store_statistics_chart(self):
        chart_html = self.chart_generator.create_store_statistics_chart(self.test_data_store_stats)
        
        self.assertIsInstance(chart_html, str)
        self.assertIn('plotly', chart_html.lower())
        self.assertIn('chart2', chart_html)
        self.assertGreater(len(chart_html), 100)
        self.assertIn('Статистика магазинів', chart_html)
    
    def test_create_top_expensive_products_chart(self):
        chart_html = self.chart_generator.create_top_expensive_products_chart(self.test_data_top_expensive)
        
        self.assertIsInstance(chart_html, str)
        self.assertIn('plotly', chart_html.lower())
        self.assertIn('chart3', chart_html)
        self.assertGreater(len(chart_html), 100)
        self.assertIn('найдорожчих', chart_html)
    
    def test_create_price_ranges_chart(self):
        chart_html = self.chart_generator.create_price_ranges_chart(self.test_data_price_ranges)
        
        self.assertIsInstance(chart_html, str)
        self.assertIn('plotly', chart_html.lower())
        self.assertIn('chart4', chart_html)
        self.assertGreater(len(chart_html), 100)
        self.assertIn('Розподіл товарів', chart_html)
    
    def test_create_promo_analysis_chart(self):
        chart_html = self.chart_generator.create_promo_analysis_chart(self.test_data_promo_analysis)
        
        self.assertIsInstance(chart_html, str)
        self.assertIn('plotly', chart_html.lower())
        self.assertIn('chart5', chart_html)
        self.assertGreater(len(chart_html), 100)
        self.assertIn('Аналіз промо-акцій', chart_html)
    
    def test_create_product_dynamics_chart(self):
        chart_html = self.chart_generator.create_product_dynamics_chart(self.test_data_product_dynamics)
        
        self.assertIsInstance(chart_html, str)
        self.assertIn('plotly', chart_html.lower())
        self.assertIn('chart6', chart_html)
        self.assertGreater(len(chart_html), 100)
        self.assertIn('Динаміка', chart_html)
    
    def test_empty_dataframe(self):
        empty_df = pd.DataFrame()
        
        chart_html = self.chart_generator.create_avg_prices_chart(empty_df)
        
        self.assertIsInstance(chart_html, str)
        self.assertIn('Немає даних', chart_html)
    
    def test_chart_generator_initialization(self):
        self.assertIsNotNone(self.chart_generator.default_layout)
        self.assertIsNotNone(self.chart_generator.color_scheme)
        self.assertIn('template', self.chart_generator.default_layout)
        self.assertIn('regular', self.chart_generator.color_scheme)
    
    def test_apply_default_layout(self):
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig = self.chart_generator._apply_default_layout(fig)
        
        self.assertIsNotNone(fig.layout)
        self.assertEqual(fig.layout.template, 'plotly_white')
    
    def test_chart_responsiveness(self):
        chart_html = self.chart_generator.create_avg_prices_chart(self.test_data_avg_prices)
        
        self.assertIn('responsive', chart_html.lower())
        self.assertIn('config', chart_html.lower())


class PlotlyChartsIntegrationTestCase(TestCase):
    
    def setUp(self):
        self.chart_generator = PlotlyChartsGenerator()
    
    def test_all_charts_generation(self):
        test_datasets = {
            'avg_prices': pd.DataFrame({
                'product_type_name': ['Тип 1'],
                'avg_regular_price': [100.0],
                'avg_promo_price': [80.0],
                'product_count': [10]
            }),
            'store_stats': pd.DataFrame({
                'city': ['Місто'],
                'store_count': [5],
                'total_products': [100],
                'promo_products_count': [20],
                'avg_price': [75.0]
            }),
            'top_expensive': pd.DataFrame({
                'product_name': ['Продукт'],
                'sku': ['SKU001'],
                'regular_price': [500.0],
                'store_name': ['Магазин'],
                'city': ['Місто'],
                'discount_percent': [10.0]
            }),
            'price_ranges': pd.DataFrame({
                'price_range': ['0-50'],
                'product_type_name': ['Тип'],
                'product_count': [50]
            }),
            'promo_analysis': pd.DataFrame({
                'store_name': ['Магазин'],
                'city': ['Місто'],
                'promo_products_count': [30],
                'avg_discount_percent': [15.0],
                'total_savings': [500.0]
            }),
            'product_dynamics': pd.DataFrame({
                'month': ['2024-01'],
                'product_type_name': ['Тип'],
                'products_added': [20]
            })
        }
        
        charts = [
            self.chart_generator.create_avg_prices_chart(test_datasets['avg_prices']),
            self.chart_generator.create_store_statistics_chart(test_datasets['store_stats']),
            self.chart_generator.create_top_expensive_products_chart(test_datasets['top_expensive']),
            self.chart_generator.create_price_ranges_chart(test_datasets['price_ranges']),
            self.chart_generator.create_promo_analysis_chart(test_datasets['promo_analysis']),
            self.chart_generator.create_product_dynamics_chart(test_datasets['product_dynamics'])
        ]
        
        for chart in charts:
            self.assertIsInstance(chart, str)
            self.assertGreater(len(chart), 50)
    
    def test_chart_with_special_characters(self):
        test_data = pd.DataFrame({
            'product_type_name': ['Пиво "Міцне"', 'Вино & Шампанське'],
            'avg_regular_price': [50.0, 120.0],
            'avg_promo_price': [40.0, 100.0],
            'product_count': [100, 50]
        })
        
        chart_html = self.chart_generator.create_avg_prices_chart(test_data)
        
        self.assertIsInstance(chart_html, str)
        self.assertGreater(len(chart_html), 100)
    
    def test_chart_with_large_dataset(self):
        large_data = pd.DataFrame({
            'product_type_name': [f'Тип {i}' for i in range(100)],
            'avg_regular_price': [float(i * 10) for i in range(100)],
            'avg_promo_price': [float(i * 8) for i in range(100)],
            'product_count': [i * 5 for i in range(100)]
        })
        
        chart_html = self.chart_generator.create_avg_prices_chart(large_data)
        
        self.assertIsInstance(chart_html, str)
        self.assertGreater(len(chart_html), 100)
