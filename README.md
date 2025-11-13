# Django REST API для моніторингу цін пива

## Структура проекту

Проект складається з двох основних компонентів:
1. **Repository Pattern** (частина 1) — доступ до даних через класи-репозиторії
2. **REST API** (частина 2/3) — повнофункціональне API з CRUD операціями та звітами

---

## 1. Встановлення та налаштування

### 1.1 Встановити залежності

```bash
pip install Django==5.2.7 sqlparse==0.5.3 djangorestframework==3.14.0
```

### 1.2 Налаштувати базу даних (SQLite)

У файлі `silpo_monitor/settings.py` перевірити конфігурацію:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

INSTALLED_APPS = [
    # ...
    "rest_framework",
    "monitoring.apps.MonitoringConfig",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

### 1.3 Виконати міграції та створити суперкористувача

```bash
python manage.py migrate
python manage.py createsuperuser
```

Введіть ім'я користувача, email та пароль для доступу до API.

### 1.4 Запустити розробницький сервер

```bash
python manage.py runserver 8000
```

Доступ до API: **http://localhost:8000/api/**

---

## 2. Перевірка Django конфігурації

```bash
python manage.py check
```

Очікуваний результат: `System check identified no issues (0 silenced).`

---

## 3. REST API Endpoints — Основна інформація

### 3.1 Автентифікація

Усі endpoint'и вимагають Basic Authentication:

- **Заголовок:** `Authorization: Basic base64(username:password)`
- **Приклад cURL:**
  ```bash
  curl -u admin:password http://localhost:8000/api/product-types/
  ```

- **У Postman:**
  1. Вкладка "Authorization"
  2. Тип: "Basic Auth"
  3. Username: `admin`
  4. Password: `password` (введені під час `createsuperuser`)

---

## 4. CRUD ProductType (Розробник 1)

### 4.1 Список усіх типів продуктів

```bash
GET /api/product-types/
```

**Приклад cURL:**
```bash
curl -u admin:password http://localhost:8000/api/product-types/
```

**Відповідь (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Пиво",
    "slug": "pivo",
    "description": "Пивні напої",
    "is_active": true,
    "created_at": "2025-11-13T10:00:00Z",
    "updated_at": "2025-11-13T10:00:00Z"
  }
]
```

### 4.2 Отримати конкретний тип продукту

```bash
GET /api/product-types/{id}/
```

### 4.3 Створити новий тип продукту

```bash
POST /api/product-types/
```

**JSON-запит:**
```json
{
  "name": "Вино",
  "slug": "vino",
  "description": "Виноградні вина",
  "is_active": true
}
```

**Відповідь (201 Created):**
```json
{
  "id": 2,
  "name": "Вино",
  "slug": "vino",
  "description": "Виноградні вина",
  "is_active": true,
  "created_at": "2025-11-13T10:05:00Z",
  "updated_at": "2025-11-13T10:05:00Z"
}
```

**Обов'язкові поля:**
- `name` (string, унікальне)
- `slug` (string, унікальне)

**Опціональні поля:**
- `description` (string)
- `is_active` (boolean, за замовчуванням true)

### 4.4 Оновити тип продукту

```bash
PUT /api/product-types/{id}/         # повне оновлення
PATCH /api/product-types/{id}/       # часткове оновлення
```

**Відповідь (200 OK):** оновлений об'єкт

### 4.5 Видалити тип продукту

```bash
DELETE /api/product-types/{id}/
```

**Відповідь (204 No Content)**

### 4.6 Таблиця результатів CRUD ProductType

| Операція | HTTP Метод | Endpoint | Статус | Примітка |
|----------|-----------|----------|--------|---------|
| Список | GET | `/api/product-types/` | 200 | OK |
| Створити | POST | `/api/product-types/` | 201 | Created |
| Отримати | GET | `/api/product-types/{id}/` | 200 | OK |
| Оновити | PUT | `/api/product-types/{id}/` | 200 | OK |
| Частково оновити | PATCH | `/api/product-types/{id}/` | 200 | OK |
| Видалити | DELETE | `/api/product-types/{id}/` | 204 | No Content |

---

## 5. CRUD Store (Розробник 2)

### 5.1 Список магазинів

```bash
GET /api/stores/
```

**Відповідь (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Силпо Київ",
    "address": "вул. Хрещатик, 1",
    "city": "Київ",
    "description": "Центральний магазин",
    "is_active": true,
    "created_at": "2025-11-13T10:00:00Z",
    "updated_at": "2025-11-13T10:00:00Z"
  }
]
```

### 5.2 Отримати магазин

```bash
GET /api/stores/{id}/
```

### 5.3 Створити магазин

```bash
POST /api/stores/
```

**JSON-запит:**
```json
{
  "name": "АТБ Харків",
  "address": "вул. Сумська, 25",
  "city": "Харків",
  "description": "Дискаунтер",
  "is_active": true
}
```

**Обов'язкові поля:**
- `name` (string, унікальне)
- `address` (string)
- `city` (string)

**Опціональні поля:**
- `description` (string)
- `is_active` (boolean, за замовчуванням true)

### 5.4 Оновити магазин

```bash
PUT /api/stores/{id}/
PATCH /api/stores/{id}/
```

### 5.5 Видалити магазин

```bash
DELETE /api/stores/{id}/
```

**Примітка:** При видаленні магазину всі пов'язані продукти також видаляються (CASCADE).

### 5.6 Таблиця результатів CRUD Store

| Операція | HTTP Метод | Endpoint | Статус | Примітка |
|----------|-----------|----------|--------|---------|
| Список | GET | `/api/stores/` | 200 | OK |
| Створити | POST | `/api/stores/` | 201 | Created |
| Отримати | GET | `/api/stores/{id}/` | 200 | OK |
| Оновити | PUT | `/api/stores/{id}/` | 200 | OK |
| Частково оновити | PATCH | `/api/stores/{id}/` | 200 | OK |
| Видалити | DELETE | `/api/stores/{id}/` | 204 | No Content |

---

## 6. CRUD Product + Звіт (Розробник 3)

### 6.1 Список усіх продуктів

```bash
GET /api/products/
```

**Відповідь (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Львівське 1715",
    "sku": "BEER-001",
    "description": "Лагер 4.7%",
    "product_type": 1,
    "product_type_info": {
      "id": 1,
      "name": "Пиво",
      "slug": "pivo",
      "description": "Пивні напої",
      "is_active": true,
      "created_at": "2025-11-13T10:00:00Z",
      "updated_at": "2025-11-13T10:00:00Z"
    },
    "store": 1,
    "store_info": {
      "id": 1,
      "name": "Силпо Київ",
      "address": "вул. Хрещатик, 1",
      "city": "Київ",
      "description": "Центральний магазин",
      "is_active": true,
      "created_at": "2025-11-13T10:00:00Z",
      "updated_at": "2025-11-13T10:00:00Z"
    },
    "regular_price": "35.00",
    "promo_price": "28.50",
    "promo_ends_at": "2025-11-20",
    "is_active": true,
    "created_at": "2025-11-13T10:00:00Z",
    "updated_at": "2025-11-13T10:00:00Z"
  }
]
```

### 6.2 Отримати конкретний продукт

```bash
GET /api/products/{id}/
```

### 6.3 Створити продукт

```bash
POST /api/products/
```

**JSON-запит (з промоцією):**
```json
{
  "name": "Львівське 1715",
  "sku": "BEER-001",
  "description": "Лагер 4.7%",
  "product_type": 1,
  "store": 1,
  "regular_price": "35.00",
  "promo_price": "28.50",
  "promo_ends_at": "2025-11-20",
  "is_active": true
}
```

**JSON-запит (без промоції):**
```json
{
  "name": "Оболонь Преміум",
  "sku": "BEER-002",
  "description": "Світле 4.5%",
  "product_type": 1,
  "store": 2,
  "regular_price": "32.00",
  "is_active": true
}
```

**Відповідь (201 Created):** створений об'єкт з усіма полями

**Обов'язкові поля:**
- `name` (string, унікальне)
- `sku` (string, унікальне — артикул товару)
- `product_type` (integer — ID типу продукту)
- `store` (integer — ID магазину)
- `regular_price` (decimal — регулярна ціна)

**Опціональні поля:**
- `description` (string)
- `promo_price` (decimal — промоційна ціна)
- `promo_ends_at` (date — дата закінчення промо)
- `is_active` (boolean, за замовчуванням true)

### 6.4 Оновити продукт

```bash
PUT /api/products/{id}/         # повне оновлення
PATCH /api/products/{id}/       # часткове оновлення
```

**Приклад часткового оновлення (активація промо):**
```json
{
  "promo_price": "28.00",
  "promo_ends_at": "2025-11-25"
}
```

### 6.5 Видалити продукт

```bash
DELETE /api/products/{id}/
```

### 6.6 Отримати агрегований звіт

```bash
GET /api/products/report/
```

**Відповідь (200 OK):**
```json
[
  {
    "store_id": 1,
    "store_name": "Силпо Київ",
    "products_count": 3,
    "promo_count": 1,
    "avg_regular_price": 33.33
  },
  {
    "store_id": 2,
    "store_name": "АТБ Харків",
    "products_count": 2,
    "promo_count": 0,
    "avg_regular_price": 30.50
  }
]
```

**Пояснення полів звіту:**

| Поле | Тип | Опис |
|------|-----|------|
| `store_id` | integer | ID магазину |
| `store_name` | string | Назва магазину |
| `products_count` | integer | Загальна кількість товарів у магазині |
| `promo_count` | integer | Кількість товарів з активною промоцією (`promo_price IS NOT NULL`) |
| `avg_regular_price` | float | Середня регулярна ціна всіх товарів у магазині |

### 6.7 Таблиця результатів CRUD Product

| Операція | HTTP Метод | Endpoint | Статус | Примітка |
|----------|-----------|----------|--------|---------|
| Список | GET | `/api/products/` | 200 | OK |
| Створити | POST | `/api/products/` | 201 | Created |
| Отримати | GET | `/api/products/{id}/` | 200 | OK |
| Оновити | PUT | `/api/products/{id}/` | 200 | OK |
| Частково оновити | PATCH | `/api/products/{id}/` | 200 | OK |
| Видалити | DELETE | `/api/products/{id}/` | 204 | No Content |
| Звіт | GET | `/api/products/report/` | 200 | OK (JSON агрегація) |

---

## 7. Послідовність тестування через Postman

### 7.1 Підготовка

1. Завантажити [Postman](https://www.postman.com/)
2. Запустити Django сервер: `python manage.py runserver 8000`
3. Створити новий запит (Request)

### 7.2 Крок 1: Налаштувати автентифікацію

- Вкладка **Authorization**
- Тип: **Basic Auth**
- Username: `admin` (створений через `createsuperuser`)
- Password: ваш пароль

### 7.3 Крок 2: Створити 2 типи продуктів

**Запит 1:**
- Method: `POST`
- URL: `http://localhost:8000/api/product-types/`
- Body (JSON):
```json
{
  "name": "Пиво",
  "slug": "pivo",
  "description": "Пивні напої"
}
```

**Запит 2:**
- Method: `POST`
- URL: `http://localhost:8000/api/product-types/`
- Body (JSON):
```json
{
  "name": "Вино",
  "slug": "vino",
  "description": "Виноградні вина"
}
```

### 7.4 Крок 3: Створити 2 магазини

**Запит 1:**
- Method: `POST`
- URL: `http://localhost:8000/api/stores/`
- Body (JSON):
```json
{
  "name": "Силпо Київ",
  "address": "вул. Хрещатик, 1",
  "city": "Київ",
  "description": "Центральний магазин"
}
```

**Запит 2:**
- Method: `POST`
- URL: `http://localhost:8000/api/stores/`
- Body (JSON):
```json
{
  "name": "АТБ Харків",
  "address": "вул. Сумська, 25",
  "city": "Харків",
  "description": "Дискаунтер"
}
```

Запишіть ID магазинів з відповідей (напр. `"id": 1` та `"id": 2`).

### 7.5 Крок 4: Створити 4 продукти (різні комбінації)

**Продукт 1 (Пиво з промо у Силпо):**
- Method: `POST`
- URL: `http://localhost:8000/api/products/`
- Body (JSON):
```json
{
  "name": "Львівське 1715",
  "sku": "BEER-001",
  "description": "Лагер 4.7%",
  "product_type": 1,
  "store": 1,
  "regular_price": "35.00",
  "promo_price": "28.50",
  "promo_ends_at": "2025-11-20"
}
```

**Продукт 2 (Пиво без промо у АТБ):**
- Method: `POST`
- URL: `http://localhost:8000/api/products/`
- Body (JSON):
```json
{
  "name": "Оболонь Преміум",
  "sku": "BEER-002",
  "description": "Світле 4.5%",
  "product_type": 1,
  "store": 2,
  "regular_price": "32.00"
}
```

**Продукт 3 (Вино з промо у Силпо):**
- Method: `POST`
- URL: `http://localhost:8000/api/products/`
- Body (JSON):
```json
{
  "name": "Inkerman",
  "sku": "WINE-001",
  "description": "Червоне 13%",
  "product_type": 2,
  "store": 1,
  "regular_price": "150.00",
  "promo_price": "125.00",
  "promo_ends_at": "2025-11-22"
}
```

**Продукт 4 (Вино без промо у АТБ):**
- Method: `POST`
- URL: `http://localhost:8000/api/products/`
- Body (JSON):
```json
{
  "name": "Шато Lafite",
  "sku": "WINE-002",
  "description": "Червоне 14%",
  "product_type": 2,
  "store": 2,
  "regular_price": "200.00"
}
```

### 7.6 Крок 5: Тестувати CRUD операції

**Список продуктів:**
```bash
GET http://localhost:8000/api/products/
```
Повинні бути 4 продукти.

**Отримати один продукт:**
```bash
GET http://localhost:8000/api/products/1/
```

**Оновити продукт (знизити ціну):**
```bash
PATCH http://localhost:8000/api/products/1/
```
Body:
```json
{
  "regular_price": "33.00"
}
```

**Видалити продукт:**
```bash
DELETE http://localhost:8000/api/products/4/
```
Відповідь: 204 No Content

### 7.7 Крок 6: Отримати звіт

```bash
GET http://localhost:8000/api/products/report/
```

**Очікувана відповідь:**
```json
[
  {
    "store_id": 1,
    "store_name": "Силпо Київ",
    "products_count": 2,
    "promo_count": 2,
    "avg_regular_price": 92.50
  },
  {
    "store_id": 2,
    "store_name": "АТБ Харків",
    "products_count": 1,
    "promo_count": 0,
    "avg_regular_price": 32.00
  }
]
```

---

## 8. Перевірка реалізації репозиторію (частина 1)

Для запуску демо-скрипту з репозиторіями:

```bash
python manage.py migrate
python main.py
```

Виведе список всіх товарів, магазинів та окремо товари з промоцією.

---

## 9. Корисні команди

### 9.1 Django управління

- Перевірити конфігурацію:
  ```bash
  python manage.py check
  ```

- Переглянути статус міграцій:
  ```bash
  python manage.py showmigrations monitoring
  ```

- Запустити Django shell (для ручних тестів репозиторіїв):
  ```bash
  python manage.py shell
  ```

  Приклад в shell:
  ```python
  from monitoring.repositories import repository_registry as repo
  products = list(repo.products.get_all())
  print(f"Усього продуктів: {len(products)}")
  ```

### 9.2 База даних

- Запустити оболонку БД (для SQLite):
  ```bash
  python manage.py dbshell
  ```

- Переглянути вміст таблиці:
  ```bash
  sqlite3 db.sqlite3 "SELECT name, sku FROM monitoring_product;"
  ```

- Очистити таблиці (обережно!):
  ```bash
  python manage.py flush
  ```

### 9.3 Тестування через curl

**Список продуктів з базовою аутентифікацією:**
```bash
curl -u admin:password http://localhost:8000/api/products/
```

**Створити продукт:**
```bash
curl -u admin:password -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Пиво Нове",
    "sku": "BEER-NEW",
    "product_type": 1,
    "store": 1,
    "regular_price": "30.00"
  }'
```

**Отримати звіт:**
```bash
curl -u admin:password http://localhost:8000/api/products/report/
```

---

## 10. Запуск з MongoDB (опціонально)

1. **Запустити MongoDB Server (7.0.x):**
    ```bash
    ~/mongodb/mongodb-macos-aarch64-7.0.25/bin/mongod \
         --dbpath ~/mongodb/data/db \
         --logpath ~/mongodb/logs/mongod.log \
         --fork
    ```

2. **Встановити Python-пакети (сумісні з djongo):**
    ```bash
    pip install "django==3.1.12" "sqlparse==0.2.4" djongo==1.3.7 pymongo==3.11.4
    ```

3. **Налаштувати DATABASES для djongo у `silpo_monitor/settings.py`:**
    ```python
    DATABASES = {
         "default": {
              "ENGINE": "djongo",
              "NAME": "silpo_monitor",
              "ENFORCE_SCHEMA": False,
              "CLIENT": {
                    "host": "127.0.0.1",
                    "port": 27017,
                    "tz_aware": False,
              },
         }
    }
    ```

4. **Виконати міграції та тестування як вище:**
    ```bash
    python manage.py migrate
    python main.py
    ```

---

## 11. Технологічний стек

- **Django 5.2.7** — веб-фреймворк
- **Django REST Framework 3.14.0** — REST API
- **SQLite** — база даних
- **Python 3.11+** — мова програмування

---

## 12. Архітектура API

### 12.1 Репозиторії (частина 1)

```
monitoring/repositories/
├── base.py           # BaseRepository[T] — базовий клас
├── product.py        # ProductRepository (extends BaseRepository)
├── store.py          # StoreRepository (extends BaseRepository)
├── product_type.py   # ProductTypeRepository (extends BaseRepository)
└── registry.py       # RepositoryRegistry — singleton для доступу
```

**Методи репозиторію:**
- `get_all()` — отримати всі об'єкти
- `get_by_id(id)` — отримати об'єкт за ID
- `add(**kwargs)` — додати новий об'єкт
- `update(id, **kwargs)` — оновити об'єкт
- `delete(id)` — видалити об'єкт
- `get_queryset()` — отримати QuerySet для фільтрації

### 12.2 ViewSets та Serializers (частина 2/3)

```
monitoring/api/
├── serializers.py    # ProductTypeSerializer, StoreSerializer, ProductSerializer
└── views.py          # ProductTypeViewSet, StoreViewSet, ProductViewSet (з report action)
```

**ViewSet методи:**
- `list()` — GET /api/endpoint/
- `create()` — POST /api/endpoint/
- `retrieve()` — GET /api/endpoint/{id}/
- `update()` — PUT /api/endpoint/{id}/
- `partial_update()` — PATCH /api/endpoint/{id}/
- `destroy()` — DELETE /api/endpoint/{id}/
- `report()` — GET /api/endpoint/report/ (custom action для Products)

### 12.3 Маршрутизація

```
silpo_monitor/urls.py

DefaultRouter реєструє:
- product-types/      → ProductTypeViewSet
- stores/             → StoreViewSet
- products/           → ProductViewSet (+ products/report/)
```

---

## 13. Статус розробки

### Розробник 1 — CRUD ProductType ✅
- ✅ Методи репозиторію (create/update/delete)
- ✅ ProductTypeSerializer
- ✅ ProductTypeViewSet
- ✅ Маршрут у DefaultRouter
- ✅ Тестування через Postman
- ✅ Документація в README

### Розробник 2 — CRUD Store ✅
- ✅ Методи репозиторію StoreRepository
- ✅ StoreSerializer
- ✅ StoreViewSet
- ✅ Маршрут у DefaultRouter
- ⏳ Тестування через Postman
- ⏳ Документація в README

### Розробник 3 — CRUD Product + Report ✅
- ✅ ProductSerializer
- ✅ ProductViewSet
- ✅ CRUD через репозиторій
- ✅ Action report з агрегацією
- ⏳ Тестування через Postman
- ✅ Документація в README

---

## 14. Перед мерджем

Виконати:

```bash
# 1. Перевірка конфігурації
python manage.py check

# 2. Запуск миграцій
python manage.py migrate

# 3. Тестування з реальними даними (див. розділ 7)

# 4. Перевірка всіх endpoint'ів (list, create, retrieve, update, delete)

# 5. Перевірка звіту
curl -u admin:password http://localhost:8000/api/products/report/
```

---

## 15. Синхронізація між розробниками

Перед фіналізацією:
1. Кожен розробник оновлює свою частину README
2. Синхронізація структури документації (розділи CRUD ProductType/Store/Product)
3. Побудова спільної Postman-колекції
4. Фінальна перевірка `python manage.py check`
5. Merge PR

---

## Автори та вклади

- **Розробник 1:** CRUD ProductType
- **Розробник 2:** CRUD Store
- **Розробник 3:** CRUD Product + Звіт
