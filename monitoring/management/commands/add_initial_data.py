from django.core.management.base import BaseCommand
from monitoring.models import ProductType, Store, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Додає початкові дані для ProductType та Store'

    def handle(self, *args, **kwargs):
        product_types = [
            {'name': 'Пиво', 'slug': 'beer', 'description': 'Алкогольний напій'},
            {'name': 'Вода', 'slug': 'water', 'description': 'Питна вода'},
            {'name': 'Сік', 'slug': 'juice', 'description': 'Фруктові соки'},
            {'name': 'Молоко', 'slug': 'milk', 'description': 'Молочні продукти'},
            {'name': 'Хліб', 'slug': 'bread', 'description': 'Хлібобулочні вироби'},
        ]

        for pt_data in product_types:
            pt, created = ProductType.objects.get_or_create(
                slug=pt_data['slug'],
                defaults={
                    'name': pt_data['name'],
                    'description': pt_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено тип продукту: {pt.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'○ Тип продукту вже існує: {pt.name}'))

        stores = [
            {'name': 'Сільпо на Хрещатику', 'city': 'Київ', 'address': 'вул. Хрещатик, 1'},
            {'name': 'Сільпо Арсенальна', 'city': 'Київ', 'address': 'вул. Арсенальна, 10'},
            {'name': 'Сільпо Позняки', 'city': 'Київ', 'address': 'просп. Григоренка, 20'},
            {'name': 'Сільпо Львів Центр', 'city': 'Львів', 'address': 'вул. Городоцька, 5'},
            {'name': 'Сільпо Одеса', 'city': 'Одеса', 'address': 'вул. Дерибасівська, 15'},
        ]

        for store_data in stores:
            store, created = Store.objects.get_or_create(
                name=store_data['name'],
                defaults={
                    'city': store_data['city'],
                    'address': store_data['address']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено магазин: {store.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'○ Магазин вже існує: {store.name}'))

        beer_type = ProductType.objects.get(slug='beer')
        water_type = ProductType.objects.get(slug='water')
        first_store = Store.objects.first()

        if first_store:
            products = [
                {
                    'name': 'Оболонь Преміум',
                    'sku': 'BEER-001',
                    'product_type': beer_type,
                    'store': first_store,
                    'regular_price': Decimal('28.50'),
                    'description': 'Світле пиво, 0.5л'
                },
                {
                    'name': 'Lvivske 1715',
                    'sku': 'BEER-002',
                    'product_type': beer_type,
                    'store': first_store,
                    'regular_price': Decimal('32.00'),
                    'promo_price': Decimal('25.00'),
                    'description': 'Світле пиво преміум класу, 0.5л'
                },
                {
                    'name': 'Моршинська',
                    'sku': 'WATER-001',
                    'product_type': water_type,
                    'store': first_store,
                    'regular_price': Decimal('18.00'),
                    'description': 'Мінеральна вода негазована, 1.5л'
                },
            ]

            for prod_data in products:
                prod, created = Product.objects.get_or_create(
                    sku=prod_data['sku'],
                    defaults=prod_data
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Створено продукт: {prod.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Продукт вже існує: {prod.name}'))

        self.stdout.write(self.style.SUCCESS('\nПочаткові дані успішно додано!'))
