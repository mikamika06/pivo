import pandas as pd
import multiprocessing
from typing import Dict, Any, List, Callable
from monitoring.performance.parallel_db_access import ParallelDatabaseExecutor
from monitoring.repositories.analytics import AnalyticsRepository


class DatabaseOptimizationExperiments:
    
    def __init__(self):
        self.executor = ParallelDatabaseExecutor()
        self.experiment_results = []
        self.analytics_repo = AnalyticsRepository()
    
    def run_full_experiment(self, num_queries: int = 100, max_workers: int = 20) -> pd.DataFrame:
        queries = self._prepare_queries(num_queries)
        
        for num_threads in range(1, max_workers + 1):
            result = self._run_experiment_threads(queries, num_threads)
            self.experiment_results.append(result)
        
        for num_processes in range(1, min(multiprocessing.cpu_count() + 1, max_workers)):
            result = self._run_experiment_processes(queries, num_processes)
            self.experiment_results.append(result)
        
        df = pd.DataFrame(self.experiment_results)
        return df
    
    def find_optimal_parameters(self) -> Dict[str, Any]:
        df = pd.DataFrame(self.experiment_results)
        
        optimal_threads = df[df['method'] == 'threads'].nsmallest(1, 'execution_time')
        optimal_processes = df[df['method'] == 'processes'].nsmallest(1, 'execution_time')
        
        return {
            'optimal_threads': {
                'num_workers': int(optimal_threads['num_workers'].values[0]),
                'execution_time': float(optimal_threads['execution_time'].values[0]),
                'throughput': float(optimal_threads['throughput'].values[0])
            },
            'optimal_processes': {
                'num_workers': int(optimal_processes['num_workers'].values[0]),
                'execution_time': float(optimal_processes['execution_time'].values[0]),
                'throughput': float(optimal_processes['throughput'].values[0])
            }
        }
    
    def _prepare_queries(self, num_queries: int) -> List[Callable]:
        queries = []
        query_methods = [
            self.analytics_repo.get_avg_prices_by_product_type,
            self.analytics_repo.get_store_statistics_by_city,
            self.analytics_repo.get_top_expensive_products,
            self.analytics_repo.get_products_by_price_ranges,
            self.analytics_repo.get_promo_analysis_by_store,
            self.analytics_repo.get_product_creation_dynamics
        ]
        
        for i in range(num_queries):
            queries.append(query_methods[i % len(query_methods)])
        
        return queries
    
    def _run_experiment_threads(self, queries: List[Callable], num_threads: int) -> Dict[str, Any]:
        result = self.executor.execute_queries_multithreading(queries, num_threads)
        return {
            'method': 'threads',
            'num_workers': num_threads,
            'execution_time': result['execution_time'],
            'num_queries': result['num_queries'],
            'success_count': result['success_count'],
            'throughput': result['num_queries'] / result['execution_time'] if result['execution_time'] > 0 else 0
        }
    
    def _run_experiment_processes(self, queries: List[Callable], num_processes: int) -> Dict[str, Any]:
        result = self.executor.execute_queries_multiprocessing(queries, num_processes)
        return {
            'method': 'processes',
            'num_workers': num_processes,
            'execution_time': result['execution_time'],
            'num_queries': result['num_queries'],
            'success_count': result['success_count'],
            'throughput': result['num_queries'] / result['execution_time'] if result['execution_time'] > 0 else 0
        }
