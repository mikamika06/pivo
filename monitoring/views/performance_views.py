from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from monitoring.performance.optimization_experiments import DatabaseOptimizationExperiments
from monitoring.charts.performance_charts import PerformanceChartsGenerator
import pandas as pd


@login_required
def performance_dashboard_view(request):
    experiments = DatabaseOptimizationExperiments()
    charts_generator = PerformanceChartsGenerator()
    
    num_queries = int(request.GET.get('num_queries', 50))
    max_workers = int(request.GET.get('max_workers', 10))
    
    df = experiments.run_full_experiment(num_queries=num_queries, max_workers=max_workers)
    
    exec_time_script, exec_time_div = charts_generator.create_execution_time_chart(df)
    throughput_script, throughput_div = charts_generator.create_throughput_chart(df)
    heatmap_script, heatmap_div = charts_generator.create_heatmap_chart(df)
    
    optimal_params = experiments.find_optimal_parameters()
    
    context = {
        'exec_time_script': exec_time_script,
        'exec_time_div': exec_time_div,
        'throughput_script': throughput_script,
        'throughput_div': throughput_div,
        'heatmap_script': heatmap_script,
        'heatmap_div': heatmap_div,
        'optimal_params': optimal_params,
        'num_queries': num_queries,
        'max_workers': max_workers,
    }
    
    return render(request, 'monitoring/performance_dashboard.html', context)
