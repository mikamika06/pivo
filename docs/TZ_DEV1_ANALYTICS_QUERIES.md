# Технічне завдання для Розробника 1: Аналітичні запити та API ендпоїнти

## Загальна інформація
**Розробник:** Developer 1  
**Напрямок:** Backend розробка - агреговані запити та REST API  
**Термін виконання:** 2 тижні  
**Пріоритет:** Високий

---

## 1. ОСНОВНІ ЗАВДАННЯ

### 1.1. Створення агрегованих запитів (6 запитів)

Необхідно створити 6 складних агрегованих запитів на рівні репозиторія з використанням Django ORM. Всі запити мають працювати з кількома сутностями та включати агрегацію, групування, сортування.

#### Запит 1: Середня ціна товарів за типами продукту
**Опис:** Отримати середню регулярну ціну та середню промо-ціну для кожного типу продукту, відсортовані за середньою регулярною ціною.

**Технічна реалізація:**
- Використовувати `ProductType`, `Product`
- Агрегація: `Avg()` для `regular_price` та `promo_price`
- Групування: за `product_type`
- Сортування: за середньою регулярною ціною (descending)
- Фільтрація: тільки активні продукти (`is_active=True`)

**Приклад структури даних:**
```python
[
    {
        'product_type_id': 1,
        'product_type_name': 'Пиво',
        'avg_regular_price': 45.50,
        'avg_promo_price': 38.20,
        'product_count': 150
    },
    ...
]
```

#### Запит 2: Статистика магазинів за містами
**Опис:** Агрегувати кількість магазинів, кількість товарів та середню ціну товарів для кожного міста.

**Технічна реалізація:**
- Використовувати `Store`, `Product`
- Агрегація: `Count()` для магазинів та продуктів, `Avg()` для цін
- Групування: за містом
- Додатково: підрахувати кількість товарів в акції (де `promo_price IS NOT NULL`)

**Приклад структури даних:**
```python
[
    {
        'city': 'Київ',
        'store_count': 25,
        'total_products': 3500,
        'avg_price': 42.50,
        'promo_products_count': 450
    },
    ...
]
```

#### Запит 3: Топ-10 найдорожчих продуктів з інформацією про магазин
**Опис:** Отримати список 10 найдорожчих товарів з детальною інформацією про магазин та тип продукту.

**Технічна реалізація:**
- Використовувати `Product`, `Store`, `ProductType`
- Джоїни: через `select_related()`
- Сортування: за `regular_price` (descending)
- Ліміт: 10 записів
- Включити: різницю між regular_price та promo_price (якщо є)

**Приклад структури даних:**
```python
[
    {
        'product_name': 'Premium Beer',
        'sku': 'SKU12345',
        'regular_price': 125.00,
        'promo_price': 99.00,
        'discount': 26.00,
        'store_name': 'Сільпо Хрещатик',
        'city': 'Київ',
        'product_type': 'Пиво'
    },
    ...
]
```

#### Запит 4: Розподіл товарів за ціновими діапазонами
**Опис:** Підрахувати кількість товарів у різних цінових категоріях (0-30, 30-60, 60-100, 100+).

**Технічна реалізація:**
- Використовувати `Product`, `ProductType`
- Використати `Case()` та `When()` для створення цінових бакетів
- Групування за ціновими діапазонами та типами продукту
- Агрегація: `Count()`

**Приклад структури даних:**
```python
[
    {
        'price_range': '30-60 грн',
        'product_type': 'Пиво',
        'count': 450,
        'percentage': 35.2
    },
    ...
]
```

#### Запит 5: Аналіз промо-акцій за магазинами
**Опис:** Для кожного магазину підрахувати кількість товарів в акції, середню знижку, загальну економію.

**Технічна реалізація:**
- Використовувати `Store`, `Product`
- Фільтрація: `promo_price IS NOT NULL`
- Агрегація: `Count()`, `Avg()`, `Sum()` для розрахунку знижок
- Обчислювати: `(regular_price - promo_price)` як знижку
- Сортування: за кількістю товарів в акції

**Приклад структури даних:**
```python
[
    {
        'store_id': 1,
        'store_name': 'Сільпо Центр',
        'city': 'Київ',
        'promo_products': 85,
        'avg_discount_percent': 18.5,
        'total_savings': 4250.00
    },
    ...
]
```

#### Запит 6: Часова динаміка створення продуктів за типами
**Опис:** Підрахувати кількість доданих продуктів по місяцях для кожного типу продукту за останній рік.

**Технічна реалізація:**
- Використовувати `Product`, `ProductType`
- Використати `TruncMonth()` для групування по місяцях
- Фільтрація: `created_at >= 1 рік назад`
- Групування: за місяцем та типом продукту
- Агрегація: `Count()`

**Приклад структури даних:**
```python
[
    {
        'month': '2024-11',
        'product_type': 'Пиво',
        'products_added': 45,
        'cumulative_total': 1250
    },
    ...
]
```

---

### 1.2. Створення файлу з репозиторіями для аналітики

**Створити:** `monitoring/repositories/analytics.py`

```python
from django.db.models import Avg, Count, Sum, F, Q, Case, When, Value, IntegerField
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from monitoring.models import Product, ProductType, Store


class AnalyticsRepository:
    """Репозиторій для складних аналітичних запитів"""
    
    def get_avg_prices_by_product_type(self):
        """Запит 1: Середні ціни за типами продукту"""
        pass  # РЕАЛІЗУВАТИ
    
    def get_store_statistics_by_city(self):
        """Запит 2: Статистика магазинів за містами"""
        pass  # РЕАЛІЗУВАТИ
    
    def get_top_expensive_products(self, limit=10):
        """Запит 3: Топ найдорожчих продуктів"""
        pass  # РЕАЛІЗУВАТИ
    
    def get_products_by_price_ranges(self):
        """Запит 4: Розподіл за ціновими діапазонами"""
        pass  # РЕАЛІЗУВАТИ
    
    def get_promo_analysis_by_store(self):
        """Запит 5: Аналіз промо-акцій"""
        pass  # РЕАЛІЗУВАТИ
    
    def get_product_creation_dynamics(self):
        """Запит 6: Динаміка створення продуктів"""
        pass  # РЕАЛІЗУВАТИ
```

---

### 1.3. REST API ендпоїнти

Створити 6 REST API ендпоїнтів для отримання даних з аналітичних запитів та перетворення їх у pandas DataFrame.

**Створити:** `monitoring/api/analytics_views.py`

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from monitoring.repositories.analytics import AnalyticsRepository


analytics_repo = AnalyticsRepository()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def avg_prices_by_product_type_view(request):
    """
    GET /api/analytics/avg-prices-by-type/
    Повертає середні ціни за типами продукту у форматі pandas DataFrame
    """
    data = analytics_repo.get_avg_prices_by_product_type()
    df = pd.DataFrame(list(data))
    
    # Конвертувати DataFrame в dict для JSON response
    response_data = {
        'data': df.to_dict(orient='records'),
        'shape': df.shape,
        'columns': list(df.columns)
    }
    return Response(response_data)


# СТВОРИТИ АНАЛОГІЧНІ VIEW ДЛЯ ІНШИХ 5 ЗАПИТІВ
```

**URL маршрути** (додати в `silpo_monitor/urls.py`):
```python
# Analytics endpoints
path('api/analytics/avg-prices-by-type/', avg_prices_by_product_type_view),
path('api/analytics/store-statistics/', store_statistics_by_city_view),
path('api/analytics/top-expensive-products/', top_expensive_products_view),
path('api/analytics/price-ranges/', products_by_price_ranges_view),
path('api/analytics/promo-analysis/', promo_analysis_by_store_view),
path('api/analytics/product-dynamics/', product_creation_dynamics_view),
```

---

## 2. РОБОТА З PANDAS

### 2.1. Базовий статистичний аналіз

Для кожного з 6 запитів необхідно виконати базовий статистичний аналіз за допомогою pandas.

**Створити:** `monitoring/analytics/statistical_analysis.py`

```python
import pandas as pd


class StatisticalAnalyzer:
    """Клас для статистичного аналізу даних"""
    
    def calculate_basic_statistics(self, df: pd.DataFrame, numeric_columns: list):
        """
        Обчислити базові статистичні показники для вказаних колонок
        
        Повертає:
        - mean (середнє)
        - median (медіана)
        - min (мінімум)
        - max (максимум)
        - std (стандартне відхилення)
        - quantiles (квартилі 25%, 50%, 75%)
        """
        pass  # РЕАЛІЗУВАТИ
    
    def perform_grouping_analysis(self, df: pd.DataFrame, group_by: str, agg_column: str):
        """
        Виконати групування та агрегацію в pandas
        """
        pass  # РЕАЛІЗУВАТИ
```

### 2.2. Порівняння ORM vs Pandas

**Створити:** `docs/ORM_vs_PANDAS_COMPARISON.md`

Необхідно описати:
1. **Продуктивність:** Різниця у швидкості виконання запитів
2. **Синтаксис:** Порівняння коду Django ORM та pandas операцій
3. **Випадки використання:** Коли краще використовувати ORM, а коли pandas
4. **Обмеження:** Що можна зробити в ORM, але складно в pandas і навпаки

**Структура документу:**
```markdown
# Порівняння Django ORM та Pandas для аналітичних запитів

## 1. Запит 1: Середні ціни за типами продукту

### Django ORM реалізація:
\`\`\`python
# Код з ORM
\`\`\`

### Pandas реалізація:
\`\`\`python
# Еквівалентний код в pandas
\`\`\`

### Порівняння:
- Продуктивність: ...
- Складність коду: ...
- Переваги/недоліки: ...

## 2. Запит 2: ...
```

---

## 3. ТЕСТУВАННЯ

### 3.1. Unit тести для репозиторіїв

**Створити:** `monitoring/tests/test_analytics_repository.py`

```python
from django.test import TestCase
from monitoring.repositories.analytics import AnalyticsRepository
from monitoring.models import Product, ProductType, Store


class AnalyticsRepositoryTestCase(TestCase):
    def setUp(self):
        # Створити тестові дані
        self.product_type = ProductType.objects.create(name='Тестове пиво', slug='test-beer')
        self.store = Store.objects.create(name='Тест магазин', city='Київ', address='вул. Тестова 1')
        # ... інші тестові дані
    
    def test_avg_prices_by_product_type(self):
        """Тест запиту середніх цін за типами"""
        pass  # РЕАЛІЗУВАТИ
    
    # ТЕСТИ ДЛЯ ІНШИХ 5 ЗАПИТІВ
```

### 3.2. API тести

**Створити:** `monitoring/tests/test_analytics_api.py`

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AnalyticsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
    
    def test_avg_prices_endpoint(self):
        """Тест ендпоїнту середніх цін"""
        response = self.client.get('/api/analytics/avg-prices-by-type/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('shape', response.data)
    
    # ТЕСТИ ДЛЯ ІНШИХ 5 ЕНДПОЇНТІВ
```

---

## 4. ДОКУМЕНТАЦІЯ

### 4.1. API документація

**Оновити:** `README.md` - додати секцію з аналітичними ендпоїнтами

```markdown
## Analytics API Endpoints

### 1. Average Prices by Product Type
**GET** `/api/analytics/avg-prices-by-type/`

Повертає середні ціни для кожного типу продукту.

**Response:**
\`\`\`json
{
    "data": [...],
    "shape": [10, 5],
    "columns": ["product_type_id", "product_type_name", "avg_regular_price", ...]
}
\`\`\`

### 2. Store Statistics by City
**GET** `/api/analytics/store-statistics/`
...
```

### 4.2. Технічна документація

**Створити:** `docs/ANALYTICS_QUERIES_DOCUMENTATION.md`

Описати:
- Деталі кожного запиту
- SQL запити, які генерує ORM
- Індекси для оптимізації
- Приклади використання

---

## 5. ДОДАТКОВІ ВИМОГИ

### 5.1. Залежності

Додати в `requirements.txt`:
```
pandas>=2.0.0
numpy>=1.24.0
```

### 5.2. Оптимізація запитів

- Використовувати `select_related()` та `prefetch_related()` де необхідно
- Додати індекси для колонок, що часто використовуються в фільтрах
- Оптимізувати N+1 запити

### 5.3. Логування

Додати логування для аналітичних запитів:
```python
import logging

logger = logging.getLogger(__name__)

def get_avg_prices_by_product_type(self):
    logger.info("Executing avg_prices_by_product_type query")
    # ... код
    logger.info(f"Query returned {len(result)} records")
```

---

## 6. ЧЕКЛИСТ ВИКОНАННЯ

- [ ] Створено `monitoring/repositories/analytics.py` з 6 запитами
- [ ] Створено `monitoring/api/analytics_views.py` з 6 ендпоїнтами
- [ ] Додано URL маршрути для аналітичних ендпоїнтів
- [ ] Створено `monitoring/analytics/statistical_analysis.py`
- [ ] Написано документ порівняння ORM vs Pandas
- [ ] Створено unit тести для репозиторіїв (мінімум 12 тестів)
- [ ] Створено API тести (мінімум 6 тестів)
- [ ] Оновлено README.md з описом аналітичних ендпоїнтів
- [ ] Створено технічну документацію запитів
- [ ] Додано необхідні залежності в requirements.txt
- [ ] Виконано оптимізацію запитів
- [ ] Додано логування
- [ ] Всі тести проходять успішно
- [ ] Код відповідає PEP 8

---

## 7. КРИТЕРІЇ ПРИЙНЯТТЯ

1. **Функціональність:**
   - Всі 6 запитів працюють коректно
   - Всі 6 ендпоїнтів повертають дані у форматі pandas DataFrame
   - API повертає коректні HTTP статус-коди

2. **Якість коду:**
   - Код добре структурований та задокументований
   - Дотримуються best practices Django ORM
   - Відсутні дублювання коду

3. **Тестування:**
   - Покриття тестами >= 80%
   - Всі тести проходять успішно

4. **Документація:**
   - Повна документація всіх ендпоїнтів
   - Детальне порівняння ORM vs Pandas
   - Технічна документація запитів

5. **Продуктивність:**
   - Запити виконуються за прийнятний час (< 2 секунди для стандартного набору даних)
   - Оптимізовано використання пам'яті

---

## 8. КОНТАКТНА ІНФОРМАЦІЯ

**Координатор проекту:** [Ім'я]  
**Технічний лід:** [Ім'я]  
**Slack канал:** #pivo-analytics  
**GitHub репозиторій:** https://github.com/mikamika06/pivo

---

**Дата видачі ТЗ:** 11 грудня 2024  
**Дедлайн:** 25 грудня 2024  
**Статус:** В роботі
