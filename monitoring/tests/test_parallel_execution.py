from django.test import TestCase
from monitoring.performance.parallel_db_access import ParallelDatabaseExecutor
from monitoring.repositories.analytics import AnalyticsRepository


class ParallelExecutionTest(TestCase):
    
    def setUp(self):
        self.executor = ParallelDatabaseExecutor()
        self.analytics_repo = AnalyticsRepository()
    
    def test_execute_queries_multithreading(self):
        queries = [
            self.analytics_repo.get_avg_prices_by_product_type,
            self.analytics_repo.get_store_statistics_by_city
        ]
        
        result = self.executor.execute_queries_multithreading(queries, num_threads=2)
        
        self.assertEqual(result['method'], 'multithreading')
        self.assertEqual(result['num_workers'], 2)
        self.assertIsInstance(result['execution_time'], float)
    
    def test_execute_queries_multiprocessing(self):
        queries = [
            self.analytics_repo.get_avg_prices_by_product_type
        ]
        
        result = self.executor.execute_queries_multiprocessing(queries, num_processes=2)
        
        self.assertEqual(result['method'], 'multiprocessing')
        self.assertIsInstance(result['execution_time'], float)
    
    def test_parallel_executor_initialization(self):
        self.assertIsNotNone(self.executor.analytics_repo)
        self.assertIsInstance(self.executor.results, list)
    
    def test_single_thread_execution(self):
        queries = [self.analytics_repo.get_avg_prices_by_product_type]
        result = self.executor.execute_queries_multithreading(queries, num_threads=1)
        
        self.assertEqual(result['num_workers'], 1)
        self.assertGreater(result['execution_time'], 0)
    
    def test_multiple_queries_execution(self):
        queries = [
            self.analytics_repo.get_avg_prices_by_product_type,
            self.analytics_repo.get_store_statistics_by_city,
            self.analytics_repo.get_top_expensive_products
        ]
        
        result = self.executor.execute_queries_multithreading(queries, num_threads=3)
        
        self.assertEqual(result['num_queries'], 3)
