# Технічне завдання для Розробника 3: Візуалізація даних Bokeh та Паралельні обчислення

## Загальна інформація
**Розробник:** Developer 3  
**Напрямок:** Backend/Frontend розробка - візуалізація даних Bokeh та оптимізація продуктивності  
**Термін виконання:** 2 тижні  
**Пріоритет:** Високий

---

## 1. ОСНОВНІ ЗАВДАННЯ (ЧАСТИНА 1: BOKEH)

### 1.1. Візуалізація даних за допомогою Bokeh

Необхідно створити 6 інтерактивних графіків з використанням бібліотеки Bokeh для візуалізації даних з аналітичних запитів.

#### Графік 1: Середні ціни за типами продукту (Grouped Bar Chart)

**Приклад коду:**
```python
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import dodge
from bokeh.palettes import Category20_3
from bokeh.embed import components

def create_avg_prices_chart_bokeh(df):
    source = ColumnDataSource(df)
    product_types = df['product_type_name'].tolist()
    
    p = figure(
        x_range=product_types,
        height=400,
        title="Середні ціни за типами продукту",
        toolbar_location="above",
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )
    
    p.vbar(
        x=dodge('product_type_name', -0.15, range=p.x_range),
        top='avg_regular_price',
        width=0.25,
        source=source,
        color='#c9d9d3',
        legend_label="Регулярна ціна"
    )
    
    p.vbar(
        x=dodge('product_type_name', 0.15, range=p.x_range),
        top='avg_promo_price',
        width=0.25,
        source=source,
        color='#718dbf',
        legend_label="Промо ціна"
    )
    
    hover = HoverTool(tooltips=[
        ("Тип", "@product_type_name"),
        ("Регулярна ціна", "@avg_regular_price{0.2f} грн"),
        ("Промо ціна", "@avg_promo_price{0.2f} грн"),
        ("Кількість товарів", "@product_count")
    ])
    p.add_tools(hover)
    
    p.xaxis.axis_label = "Тип продукту"
    p.yaxis.axis_label = "Ціна (грн)"
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    
    script, div = components(p)
    return script, div
```

#### Графіки 2-6: (аналогічно створити для інших візуалізацій)
- Статистика магазинів за містами (Multi-line Chart)
- Топ-10 найдорожчих продуктів (Horizontal Bar Chart)
- Розподіл товарів за ціновими діапазонами (Stacked Bar + Pie)
- Аналіз промо-акцій (Scatter Plot)
- Часова динаміка створення продуктів (Time Series)

---

## 2. ОСНОВНІ ЗАВДАННЯ (ЧАСТИНА 2: ПАРАЛЕЛЬНІ ОБЧИСЛЕННЯ)

### 2.1. Реалізація паралельного доступу до БД

**Створити:** `monitoring/performance/parallel_db_access.py`

```python
import concurrent.futures
import multiprocessing
import time
import logging
from typing import List, Dict, Any, Callable
from django.db import connection
from monitoring.repositories.analytics import AnalyticsRepository


logger = logging.getLogger(__name__)


class ParallelDatabaseExecutor:
    """
    Клас для паралельного виконання запитів до БД
    з використанням багатопотоковості та багатопроцесності
    """
    
    def __init__(self):
        self.analytics_repo = AnalyticsRepository()
        self.results = []
    
    def execute_queries_multithreading(self, queries: List[Callable], num_threads: int = 4) -> Dict[str, Any]:
        """
        Виконати запити з використанням багатопотоковості (ThreadPoolExecutor)
        
        Args:
            queries: список функцій-запитів для виконання
            num_threads: кількість потоків
        
        Returns:
            dict з результатами: час виконання, результати запитів
        """
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
        """
        Виконати запити з використанням багатопроцесності (ProcessPoolExecutor)
        """
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
        """Виконати запит в окремому процесі"""
        from django.db import connection
        connection.close()
        return query()
```

---

### 2.2. Пошук оптимальних параметрів

**Створити:** `monitoring/performance/optimization_experiments.py`

```python
import pandas as pd
from monitoring.performance.parallel_db_access import ParallelDatabaseExecutor


class DatabaseOptimizationExperiments:
    """
    Клас для проведення експериментів з метою знаходження
    оптимальних параметрів доступу до БД
    """
    
    def __init__(self):
        self.executor = ParallelDatabaseExecutor()
        self.experiment_results = []
    
    def run_full_experiment(self, num_queries: int = 100, max_workers: int = 20) -> pd.DataFrame:
        """
        Запустити повний експеримент з різними параметрами
        
        Args:
            num_queries: кількість запитів для виконання (100-200)
            max_workers: максимальна кількість воркерів для тестування
        
        Returns:
            pandas DataFrame з результатами експериментів
        """
        queries = self._prepare_queries(num_queries)
        
        # Експерименти з різною кількістю потоків
        for num_threads in range(1, max_workers + 1):
            result = self._run_experiment_threads(queries, num_threads)
            self.experiment_results.append(result)
        
        # Експерименти з різною кількістю процесів
        for num_processes in range(1, min(multiprocessing.cpu_count() + 1, max_workers)):
            result = self._run_experiment_processes(queries, num_processes)
            self.experiment_results.append(result)
        
        df = pd.DataFrame(self.experiment_results)
        return df
    
    def find_optimal_parameters(self) -> Dict[str, Any]:
        """Знайти оптимальні параметри на основі результатів експериментів"""
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
```

---

### 2.3. Візуалізація результатів оптимізації

**Створити:** `monitoring/charts/performance_charts.py`

```python
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components
from bokeh.palettes import Category10
import pandas as pd


class PerformanceChartsGenerator:
    """Генератор графіків для аналізу продуктивності"""
    
    def create_execution_time_chart(self, df: pd.DataFrame):
        """Створити графік залежності часу виконання від кількості воркерів"""
        p = figure(
            title="Час виконання запитів vs Кількість воркерів",
            x_axis_label="Кількість воркерів",
            y_axis_label="Час виконання (секунди)",
            height=400,
            width=800
        )
        
        methods = df['method'].unique()
        colors = Category10[max(3, len(methods))]
        
        for method, color in zip(methods, colors):
            df_filtered = df[df['method'] == method]
            source = ColumnDataSource(df_filtered)
            
            p.line('num_workers', 'execution_time', source=source, 
                   line_width=2, color=color, legend_label=method)
            p.circle('num_workers', 'execution_time', source=source, 
                     size=8, color=color)
        
        p.legend.location = "top_right"
        p.legend.click_policy = "hide"
        
        script, div = components(p)
        return script, div
    
    def create_throughput_chart(self, df: pd.DataFrame):
        """Створити графік пропускної здатності"""
        # TODO: РЕАЛІЗУВАТИ
        pass
    
    def create_heatmap_chart(self, df: pd.DataFrame):
        """Створити теплову карту часу виконання"""
        # TODO: РЕАЛІЗУВАТИ
        pass
```

---

## 3. ТЕСТУВАННЯ

### 3.1. Unit тести для Bokeh графіків

**Створити:** `monitoring/tests/test_bokeh_charts.py`

### 3.2. Тести паралельних обчислень

**Створити:** `monitoring/tests/test_parallel_execution.py`

---

## 4. ДОКУМЕНТАЦІЯ

### 4.1. Документація Bokeh графіків

**Створити:** `docs/BOKEH_CHARTS_DOCUMENTATION.md`

### 4.2. Документація оптимізації продуктивності

**Створити:** `docs/PERFORMANCE_OPTIMIZATION_GUIDE.md`

---

## 5. ДОДАТКОВІ ВИМОГИ

### 5.1. Залежності

Додати в `requirements.txt`:
```
bokeh>=3.3.0
pandas>=2.0.0
numpy>=1.24.0
```

### 5.2. URL маршрути

Додати в `silpo_monitor/urls.py`:
```python
from monitoring.views.dashboard_bokeh_views import dashboard_v2_view
from monitoring.views.performance_views import performance_dashboard_view

urlpatterns += [
    path('dashboard/v2/', dashboard_v2_view, name='dashboard_v2'),
    path('dashboard/performance/', performance_dashboard_view, name='performance_dashboard'),
]
```

---

## 6. ЧЕКЛИСТ ВИКОНАННЯ

### Частина 1: Bokeh
- [ ] Створено `monitoring/charts/bokeh_charts.py` з 6 графіками
- [ ] Створено `monitoring/views/dashboard_bokeh_views.py`
- [ ] Створено HTML шаблон `dashboard_v2.html`
- [ ] Реалізовано всі 6 типів графіків Bokeh
- [ ] Графіки інтерактивні та працюють коректно
- [ ] Створено unit тести для графіків (мінімум 6 тестів)

### Частина 2: Паралельні обчислення
- [ ] Створено `monitoring/performance/parallel_db_access.py`
- [ ] Створено `monitoring/performance/optimization_experiments.py`
- [ ] Реалізовано multithreading виконання
- [ ] Реалізовано multiprocessing виконання
- [ ] Проведено експерименти зі 100-200 запитами
- [ ] Створено `monitoring/charts/performance_charts.py`
- [ ] Реалізовано 3 графіки для аналізу продуктивності
- [ ] Створено `monitoring/views/performance_views.py`
- [ ] Інтегровано графіки в дашборд
- [ ] Створено тести паралельних обчислень (мінімум 5 тестів)

### Загальне
- [ ] Додано URL маршрути
- [ ] Створено документацію Bokeh графіків
- [ ] Створено посібник з оптимізації продуктивності
- [ ] Додано необхідні залежності
- [ ] Всі тести проходять успішно
- [ ] Код відповідає PEP 8

---

**Дата видачі ТЗ:** 11 грудня 2024  
**Дедлайн:** 25 грудня 2024  
**Статус:** В роботі
