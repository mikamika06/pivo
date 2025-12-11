import concurrent.futures
import multiprocessing
import time
import logging
from typing import List, Dict, Any, Callable
from django.db import connection
from monitoring.repositories.analytics import AnalyticsRepository


logger = logging.getLogger(__name__)


class ParallelDatabaseExecutor:
    
    def __init__(self):
        self.analytics_repo = AnalyticsRepository()
        self.results = []
    
    def execute_queries_multithreading(self, queries: List[Callable], num_threads: int = 4) -> Dict[str, Any]:
        start_time = time.time()
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_query = {executor.submit(query): query for query in queries}
            
            for future in concurrent.futures.as_completed(future_to_query):
                try:
                    result = future.result()
                    results.append(result)
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
    
    def execute_queries_multiprocessing(self, queries: List[Callable], num_processes: int = 4) -> Dict[str, Any]:
        start_time = time.time()
        results = []
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
            future_to_query = {executor.submit(self._execute_query_in_process, query): query for query in queries}
            
            for future in concurrent.futures.as_completed(future_to_query):
                try:
                    result = future.result()
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
    
    @staticmethod
    def _execute_query_in_process(query: Callable):
        from django.db import connection
        connection.close()
        return query()
