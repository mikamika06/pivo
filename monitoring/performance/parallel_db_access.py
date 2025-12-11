import concurrent.futures
import multiprocessing
import time
import logging
import os
import django
from typing import List, Dict, Any, Callable
from django.db import connection

logger = logging.getLogger(__name__)


def _execute_query_wrapper(query_name: str):
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'silpo_monitor.settings')
        django.setup()
        
        from monitoring.repositories.analytics import AnalyticsRepository
        from django.db import connection
        
        connection.close()
        repo = AnalyticsRepository()
        
        query_methods = {
            'avg_prices': repo.get_avg_prices_by_product_type,
            'store_stats': repo.get_store_statistics_by_city,
            'top_products': repo.get_top_expensive_products,
            'price_ranges': repo.get_products_by_price_ranges,
            'promo_analysis': repo.get_promo_analysis_by_store,
            'dynamics': repo.get_product_creation_dynamics
        }
        
        method = query_methods.get(query_name)
        if method:
            return list(method())
        return []
    except Exception as e:
        logger.error(f"Error in subprocess query {query_name}: {e}")
        return None


class ParallelDatabaseExecutor:
    
    def __init__(self):
        self.results = []
    
    def execute_queries_multithreading(self, queries: List[str], num_threads: int = 4) -> Dict[str, Any]:
        from monitoring.repositories.analytics import AnalyticsRepository
        from django.db import connection
        
        start_time = time.time()
        results = []
        
        def execute_single_query(query_name):
            try:
                connection.close()
                repo = AnalyticsRepository()
                query_methods = {
                    'avg_prices': repo.get_avg_prices_by_product_type,
                    'store_stats': repo.get_store_statistics_by_city,
                    'top_products': repo.get_top_expensive_products,
                    'price_ranges': repo.get_products_by_price_ranges,
                    'promo_analysis': repo.get_promo_analysis_by_store,
                    'dynamics': repo.get_product_creation_dynamics
                }
                method = query_methods.get(query_name)
                if method:
                    return list(method())
                return []
            except Exception as e:
                logger.error(f"Query failed: {e}")
                return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(execute_single_query, qname): qname for qname in queries}
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result(timeout=15)
                    results.append(result)
                except concurrent.futures.TimeoutError:
                    logger.error(f"Query timeout")
                    results.append(None)
                except Exception as e:
                    logger.error(f"Query failed: {e}")
                    results.append(None)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            'method': 'multithreading',
            'num_workers': num_threads,
            'execution_time': execution_time,
            'num_queries': len(queries),
            'success_count': len([r for r in results if r is not None]),
            'results': results
        }
    
    def execute_queries_multiprocessing(self, queries: List[str], num_processes: int = 4) -> Dict[str, Any]:
        start_time = time.time()
        results = []
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = [executor.submit(_execute_query_wrapper, query_name) for query_name in queries]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result(timeout=10)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Query failed in process: {e}")
                    results.append(None)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            'method': 'multiprocessing',
            'num_workers': num_processes,
            'execution_time': execution_time,
            'num_queries': len(queries),
            'success_count': len([r for r in results if r is not None]),
            'results': results
        }
