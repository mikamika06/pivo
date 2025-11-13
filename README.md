# Django REST API для моніторингу цін

## Встановлення

```bash
pip install Django==5.2.7 djangorestframework==3.14.0
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

API: **http://localhost:8000/api/**

---

## Автентифікація

Всі endpoint'и вимагають Basic Auth:
```bash
curl -u admin:password http://localhost:8000/api/products/
```

У Postman: Authorization → Basic Auth → username/password

---

## API Endpoints

### ProductType

| Метод | Endpoint | Опис |
|-------|----------|------|
| GET | `/api/product-types/` | Список типів |
| POST | `/api/product-types/` | Створити тип |
| GET | `/api/product-types/{id}/` | Отримати тип |
| PUT/PATCH | `/api/product-types/{id}/` | Оновити тип |
| DELETE | `/api/product-types/{id}/` | Видалити тип |

**Приклад POST:**
```json
{
  "name": "Пиво",
  "slug": "pivo",
  "description": "Пивні напої"
}
```

---

### Store
| Метод | Endpoint | Опис |
|-------|----------|------|
| GET | `/api/stores/` | Список магазинів |
| POST | `/api/stores/` | Створити магазин |
| GET | `/api/stores/{id}/` | Отримати магазин |
| PUT/PATCH | `/api/stores/{id}/` | Оновити магазин |
| DELETE | `/api/stores/{id}/` | Видалити магазин |

**Приклад POST:**
```json
{
  "name": "Сільпо Київ",
  "address": "вул. Хрещатик, 1",
  "city": "Київ",
  "description": "Центральний магазин"
}
```

---

### Product 

| Метод | Endpoint | Опис |
|-------|----------|------|
| GET | `/api/products/` | Список продуктів |
| POST | `/api/products/` | Створити продукт |
| GET | `/api/products/{id}/` | Отримати продукт |
| PUT/PATCH | `/api/products/{id}/` | Оновити продукт |
| DELETE | `/api/products/{id}/` | Видалити продукт |
| GET | `/api/products/report/` | Звіт по магазинах |

**Приклад POST продукту:**
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

**Звіт (GET /api/products/report/):**
```json
[
  {
    "store_id": 1,
    "store_name": "Силпо Київ",
    "products_count": 3,
    "promo_count": 1,
    "avg_regular_price": 33.33
  }
]
```

**Поля звіту:**
- `store_id` — ID магазину
- `store_name` — Назва магазину
- `products_count` — Кількість товарів
- `promo_count` — Товарів з промо
- `avg_regular_price` — Середня ціна

---

## ProductSerializer 

```python
class ProductSerializer(serializers.ModelSerializer):
    product_type_info = ProductTypeSerializer(source="product_type", read_only=True)
    store_info = StoreSerializer(source="store", read_only=True)
    
    product_type = serializers.PrimaryKeyRelatedField(
        queryset=ProductType.objects.all()
    )
    store = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all()
    )
```

Вкладені дані типу та магазину в GET запитах, ID в POST/PATCH.

---

## ProductViewSet 

```python
class ProductViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["get"])
    def report(self, request):
        report_data = self.get_repository().get_report_by_stores()
        return Response(report_data)
```

---

## ProductRepository 

```python
class ProductRepository(BaseRepository[Product]):
    def get_products_by_store(self, store_id: int):
        return self.get_queryset().filter(store_id=store_id)
    
    def get_products_with_promo(self):
        return self.get_queryset().filter(promo_price__isnull=False)
    
    def get_report_by_stores(self):
        # Агрегація: count, promo_count, avg_price по магазинах
        stores = self.get_queryset().values('store_id', 'store__name').annotate(
            products_count=Count('id'),
            promo_count=Count('id', filter=Q(promo_price__isnull=False)),
            avg_regular_price=Avg('regular_price')
        )
        return [...]
```

---

## Тестування

### Django check
```bash
python manage.py check
```

### Curl примери
```bash
# Список продуктів
curl -u admin:pass http://localhost:8000/api/products/

# Створити продукт
curl -u admin:pass -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Пиво","sku":"BEER-001","product_type":1,"store":1,"regular_price":"30.00"}'

# Звіт
curl -u admin:pass http://localhost:8000/api/products/report/
```

### Postman
1. Authorization → Basic Auth
2. POST http://localhost:8000/api/product-types/ (створити тип)
3. POST http://localhost:8000/api/stores/ (створити магазин)
4. POST http://localhost:8000/api/products/ (створити продукт)
5. GET http://localhost:8000/api/products/report/ (отримати звіт)

---


