import pandas as pd
import multiprocessing
import psutil
import time
from typing import Dict, Any, List
from monitoring.performance.parallel_db_access import ParallelDatabaseExecutor
from monitoring.repositories.analytics import AnalyticsRepository


class DatabaseOptimizationExperiments:
    
    def __init__(self):
        self.executor = ParallelDatabaseExecutor()
        self.experiment_results = []
        self.analytics_repo = AnalyticsRepository()
    
    def run_full_experiment(self, num_queries: int = 100, max_workers: int = 20) -> pd.DataFrame:
        self.experiment_results = []
        queries = self._prepare_queries(num_queries)
        
        for num_threads in range(1, max_workers + 1):
            result = self._run_experiment_threads(queries, num_threads)
            self.experiment_results.append(result)
        
        for num_processes in range(1, max_workers + 1):
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
                'num_workers': int(optimal_threads['num_workers'].values[0]) if not optimal_threads.empty else 1,
                'execution_time': float(optimal_threads['execution_time'].values[0]) if not optimal_threads.empty else 0,
                'throughput': float(optimal_threads['throughput'].values[0]) if not optimal_threads.empty else 0
            },
            'optimal_processes': {
                'num_workers': int(optimal_processes['num_workers'].values[0]) if not optimal_processes.empty else 1,
                'execution_time': float(optimal_processes['execution_time'].values[0]) if not optimal_processes.empty else 0,
                'throughput': float(optimal_processes['throughput'].values[0]) if not optimal_processes.empty else 0
            }
        }
    
    def _prepare_queries(self, num_queries: int) -> List[str]:
        query_names = [
            'avg_prices',
            'store_stats',
            'top_products',
            'price_ranges',
            'promo_analysis',
            'dynamics'
        ]
        
        queries = []
        for i in range(num_queries):
            queries.append(query_names[i % len(query_names)])
        
        return queries
    
    def _run_experiment_threads(self, queries: List[str], num_threads: int) -> Dict[str, Any]:
        process = psutil.Process()
        process.cpu_percent()
        mem_before = process.memory_info().rss / 1024 / 1024
        cpu_before = psutil.cpu_percent(interval=0.1)
        
        result = self.executor.execute_queries_multithreading(queries, num_threads)
        
        cpu_after = psutil.cpu_percent(interval=0.1)
        mem_after = process.memory_info().rss / 1024 / 1024
        
        return {
            'method': 'threads',
            'num_workers': num_threads,
            'execution_time': result['execution_time'],
            'num_queries': result['num_queries'],
            'success_count': result['success_count'],
            'throughput': result['num_queries'] / result['execution_time'] if result['execution_time'] > 0 else 0,
            'cpu_usage': (cpu_before + cpu_after) / 2,
            'memory_mb': (mem_before + mem_after) / 2
        }
    
    def _run_experiment_processes(self, queries: List[str], num_processes: int) -> Dict[str, Any]:
        process = psutil.Process()
        process.cpu_percent()
        mem_before = process.memory_info().rss / 1024 / 1024
        cpu_before = psutil.cpu_percent(interval=0.1)
        
        result = self.executor.execute_queries_multiprocessing(queries, num_processes)
        
        cpu_after = psutil.cpu_percent(interval=0.1)
        mem_after = process.memory_info().rss / 1024 / 1024
        
        return {
            'method': 'processes',
            'num_workers': num_processes,
            'execution_time': result['execution_time'],
            'num_queries': result['num_queries'],
            'success_count': result['success_count'],
            'throughput': result['num_queries'] / result['execution_time'] if result['execution_time'] > 0 else 0,
            'cpu_usage': (cpu_before + cpu_after) / 2,
            'memory_mb': (mem_before + mem_after) / 2
        }
