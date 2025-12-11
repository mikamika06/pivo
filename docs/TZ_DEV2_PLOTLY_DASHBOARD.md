# Технічне завдання для Розробника 2: Візуалізація даних та Дашборди (Plotly)

## Загальна інформація
**Розробник:** Developer 2  
**Напрямок:** Frontend/Backend розробка - візуалізація даних та інтерактивні дашборди  
**Термін виконання:** 2 тижні  
**Пріоритет:** Високий

---

## 1. ОСНОВНІ ЗАВДАННЯ

### 1.1. Візуалізація даних за допомогою Plotly

Необхідно створити 6 інтерактивних графіків з використанням бібліотеки Plotly для візуалізації даних з аналітичних запитів.

#### Графік 1: Середні ціни за типами продукту (Bar Chart)
**Опис:** Стовпчикова діаграма, що показує середні регулярні та промо-ціни для кожного типу продукту.

**Технічна реалізація:**
- Тип графіка: Grouped Bar Chart
- Вісь X: Назви типів продукту
- Вісь Y: Ціна (грн)
- Дві серії даних: regular_price та promo_price
- Колір: різні кольори для regular та promo
- Інтерактивність: hover з детальною інформацією (кількість товарів, точна ціна)

**Приклад коду:**
```python
import plotly.graph_objects as go

def create_avg_prices_chart(data):
    fig = go.Figure(data=[
        go.Bar(name='Регулярна ціна', x=..., y=..., marker_color='indianred'),
        go.Bar(name='Промо ціна', x=..., y=..., marker_color='lightsalmon')
    ])
    
    fig.update_layout(
        title='Середні ціни за типами продукту',
        xaxis_title='Тип продукту',
        yaxis_title='Ціна (грн)',
        barmode='group',
        hovermode='x unified'
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id='chart1')
```

#### Графік 2: Статистика магазинів за містами (Stacked Bar Chart)
**Опис:** Стовпчикова діаграма з накопиченням, що показує кількість магазинів та товарів по містах.

**Технічна реалізація:**
- Тип графіка: Stacked Bar Chart
- Вісь X: Міста
- Вісь Y: Кількість
- Три серії: store_count, total_products, promo_products_count
- Додатково: лінія середньої ціни на вторинній осі Y

#### Графік 3: Топ-10 найдорожчих продуктів (Horizontal Bar Chart)
**Опис:** Горизонтальна стовпчикова діаграма з топ-10 найдорожчих товарів.

**Технічна реалізація:**
- Тип графіка: Horizontal Bar Chart
- Вісь Y: Назви товарів + SKU
- Вісь X: Ціна (грн)
- Колір: градієнт від темного до світлого залежно від ціни
- Інтерактивність: hover з інформацією про магазин, місто, знижку

#### Графік 4: Розподіл товарів за ціновими діапазонами (Pie Chart + Sunburst)
**Опис:** Кругова діаграма з вкладеними рівнями для показу розподілу товарів за ціновими діапазонами та типами.

**Технічна реалізація:**
- Тип графіка: Sunburst Chart
- Зовнішній рівень: цінові діапазони
- Внутрішній рівень: типи продуктів
- Показувати: кількість та відсоток
- Інтерактивність: click для drill-down

#### Графік 5: Аналіз промо-акцій (Scatter Plot)
**Опис:** Точкова діаграма для аналізу співвідношення кількості товарів в акції та середньої знижки по магазинах.

**Технічна реалізація:**
- Тип графіка: Scatter Plot
- Вісь X: Кількість товарів в акції
- Вісь Y: Середній відсоток знижки
- Розмір точок: загальна економія
- Колір: за містами
- Інтерактивність: hover з назвою магазину та деталями

#### Графік 6: Часова динаміка створення продуктів (Line Chart)
**Опис:** Лінійний графік для показу динаміки додавання нових товарів по місяцях.

**Технічна реалізація:**
- Тип графіка: Multi-line Chart
- Вісь X: Місяці
- Вісь Y: Кількість доданих товарів
- Кожна лінія: окремий тип продукту
- Інтерактивність: можливість вимкнути/ввімкнути лінії типів продуктів
- Додатково: область (area) для кумулятивного показника

---

### 1.2. Створення дашборду Django

Створити інтерактивний дашборд для відображення всіх 6 графіків з можливістю фільтрації та взаємодії.

**Створити файли:**
1. `monitoring/views/dashboard_views.py` - view для дашборду
2. `monitoring/templates/monitoring/dashboard_v1.html` - шаблон дашборду
3. `monitoring/static/monitoring/css/dashboard.css` - стилі
4. `monitoring/static/monitoring/js/dashboard_plotly.js` - JavaScript для інтерактивності

#### 1.2.1. Django View

**Файл:** `monitoring/views/dashboard_views.py`

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from monitoring.repositories.analytics import AnalyticsRepository
from monitoring.charts.plotly_charts import PlotlyChartsGenerator
import pandas as pd


analytics_repo = AnalyticsRepository()


@login_required
def dashboard_v1_view(request):
    """
    Дашборд версії 1 (Plotly)
    
    Фільтри:
    - city: місто (спадний список)
    - product_type: тип продукту (спадний список)
    - date_from, date_to: діапазон дат (date pickers)
    - price_min, price_max: ціновий діапазон (слайдер)
    """
    
    # Отримання параметрів фільтрів
    city = request.GET.get('city', None)
    product_type_id = request.GET.get('product_type', None)
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 1000)
    
    # Отримання даних з репозиторію
    data1 = analytics_repo.get_avg_prices_by_product_type()
    data2 = analytics_repo.get_store_statistics_by_city()
    data3 = analytics_repo.get_top_expensive_products(limit=10)
    data4 = analytics_repo.get_products_by_price_ranges()
    data5 = analytics_repo.get_promo_analysis_by_store()
    data6 = analytics_repo.get_product_creation_dynamics()
    
    # Застосування фільтрів до даних
    # TODO: Реалізувати фільтрацію pandas DataFrame
    
    # Генерація графіків
    chart_generator = PlotlyChartsGenerator()
    
    chart1 = chart_generator.create_avg_prices_chart(pd.DataFrame(list(data1)))
    chart2 = chart_generator.create_store_statistics_chart(pd.DataFrame(list(data2)))
    chart3 = chart_generator.create_top_expensive_products_chart(pd.DataFrame(list(data3)))
    chart4 = chart_generator.create_price_ranges_chart(pd.DataFrame(list(data4)))
    chart5 = chart_generator.create_promo_analysis_chart(pd.DataFrame(list(data5)))
    chart6 = chart_generator.create_product_dynamics_chart(pd.DataFrame(list(data6)))
    
    # Отримання списків для фільтрів
    cities = Store.objects.values_list('city', flat=True).distinct()
    product_types = ProductType.objects.all()
    
    context = {
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'chart5': chart5,
        'chart6': chart6,
        'cities': cities,
        'product_types': product_types,
        'selected_city': city,
        'selected_product_type': product_type_id,
        'date_from': date_from,
        'date_to': date_to,
        'price_min': price_min,
        'price_max': price_max,
    }
    
    return render(request, 'monitoring/dashboard_v1.html', context)
```

---

### 1.3. Створення класу генератора графіків

**Створити:** `monitoring/charts/plotly_charts.py`

```python
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any


class PlotlyChartsGenerator:
    """Генератор інтерактивних графіків з використанням Plotly"""
    
    def __init__(self):
        self.default_layout = {
            'template': 'plotly_white',
            'font': {'family': 'Arial, sans-serif', 'size': 12},
            'hovermode': 'closest',
            'showlegend': True
        }
    
    def create_avg_prices_chart(self, df: pd.DataFrame) -> str:
        """Графік 1: Середні ціни за типами продукту"""
        # TODO: РЕАЛІЗУВАТИ
        pass
    
    def create_store_statistics_chart(self, df: pd.DataFrame) -> str:
        """Графік 2: Статистика магазинів за містами"""
        # TODO: РЕАЛІЗУВАТИ
        pass
    
    def create_top_expensive_products_chart(self, df: pd.DataFrame) -> str:
        """Графік 3: Топ-10 найдорожчих продуктів"""
        # TODO: РЕАЛІЗУВАТИ
        pass
    
    def create_price_ranges_chart(self, df: pd.DataFrame) -> str:
        """Графік 4: Розподіл товарів за ціновими діапазонами"""
        # TODO: РЕАЛІЗУВАТИ
        pass
    
    def create_promo_analysis_chart(self, df: pd.DataFrame) -> str:
        """Графік 5: Аналіз промо-акцій"""
        # TODO: РЕАЛІЗУВАТИ
        pass
    
    def create_product_dynamics_chart(self, df: pd.DataFrame) -> str:
        """Графік 6: Динаміка створення продуктів"""
        # TODO: РЕАЛІЗУВАТИ
        pass
    
    def _apply_default_layout(self, fig: go.Figure) -> go.Figure:
        """Застосувати стандартні налаштування до графіка"""
        fig.update_layout(**self.default_layout)
        return fig
```

---

## 2. ІНТЕРАКТИВНІСТЬ ТА ФІЛЬТРАЦІЯ

### 2.1. JavaScript для динамічної взаємодії

**Створити:** `monitoring/static/monitoring/js/dashboard_plotly.js`

```javascript
// Оновлення відображення цінового діапазону
document.addEventListener('DOMContentLoaded', function() {
    const priceMinInput = document.getElementById('price_min');
    const priceMaxInput = document.getElementById('price_max');
    const priceDisplay = document.getElementById('price_range_display');
    
    function updatePriceDisplay() {
        priceDisplay.textContent = `${priceMinInput.value} - ${priceMaxInput.value} грн`;
    }
    
    priceMinInput.addEventListener('input', updatePriceDisplay);
    priceMaxInput.addEventListener('input', updatePriceDisplay);
    
    // Автоматичне застосування фільтрів при зміні
    const form = document.getElementById('filters-form');
    const selects = form.querySelectorAll('select');
    
    selects.forEach(select => {
        select.addEventListener('change', function() {
            form.submit();
        });
    });
});

function resetFilters() {
    window.location.href = window.location.pathname;
}

// Синхронізація графіків при взаємодії
// TODO: Реалізувати cross-filtering між графіками
```

---

## 3. ТЕСТУВАННЯ

### 3.1. Unit тести для графіків

**Створити:** `monitoring/tests/test_plotly_charts.py`

```python
from django.test import TestCase
from monitoring.charts.plotly_charts import PlotlyChartsGenerator
import pandas as pd


class PlotlyChartsTestCase(TestCase):
    def setUp(self):
        self.chart_generator = PlotlyChartsGenerator()
        # Створити тестові DataFrame
        self.test_data = pd.DataFrame({
            'product_type_name': ['Пиво', 'Вино'],
            'avg_regular_price': [50.0, 120.0],
            'avg_promo_price': [40.0, 100.0],
            'product_count': [100, 50]
        })
    
    def test_create_avg_prices_chart(self):
        """Тест генерації графіка середніх цін"""
        chart_html = self.chart_generator.create_avg_prices_chart(self.test_data)
        self.assertIsInstance(chart_html, str)
        self.assertIn('plotly', chart_html.lower())
        self.assertIn('chart1', chart_html)
    
    # TODO: ТЕСТИ ДЛЯ ІНШИХ 5 ГРАФІКІВ
```

---

## 4. ДОКУМЕНТАЦІЯ

### 4.1. Документація візуалізацій

**Створити:** `docs/PLOTLY_CHARTS_DOCUMENTATION.md`

---

## 5. ДОДАТКОВІ ВИМОГИ

### 5.1. Залежності

Додати в `requirements.txt`:
```
plotly>=5.18.0
kaleido>=0.2.1
```

### 5.2. URL маршрути

Додати в `silpo_monitor/urls.py`:
```python
from monitoring.views.dashboard_views import dashboard_v1_view

urlpatterns += [
    path('dashboard/v1/', dashboard_v1_view, name='dashboard_v1'),
]
```

---

## 6. ЧЕКЛИСТ ВИКОНАННЯ

- [ ] Створено `monitoring/charts/plotly_charts.py` з 6 графіками
- [ ] Створено `monitoring/views/dashboard_views.py`
- [ ] Створено HTML шаблон `dashboard_v1.html`
- [ ] Створено CSS стилі `dashboard.css`
- [ ] Створено JavaScript `dashboard_plotly.js`
- [ ] Реалізовано всі 6 типів графіків
- [ ] Реалізовано панель фільтрів (5 фільтрів)
- [ ] Фільтри працюють коректно
- [ ] Графіки оновлюються при застосуванні фільтрів
- [ ] Додано URL маршрути
- [ ] Створено unit тести (мінімум 6 тестів)
- [ ] Створено інтеграційні тести (мінімум 5 тестів)
- [ ] Створено документацію графіків
- [ ] Створено посібник користувача
- [ ] Додано необхідні залежності
- [ ] Дашборд адаптивний (responsive design)
- [ ] Всі графіки інтерактивні
- [ ] Код відповідає PEP 8

---

**Дата видачі ТЗ:** 11 грудня 2024  
**Дедлайн:** 25 грудня 2024  
**Статус:** В роботі
