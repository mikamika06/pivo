from django.core.management.base import BaseCommand
from monitoring.models import ProductType, Store, Product
from decimal import Decimal
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Генерує велику кількість тестових даних для дашбордів'

    def handle(self, *args, **options):
        self.stdout.write('Початок генерації даних...')
        
        Product.objects.all().delete()
        Store.objects.all().delete()
        ProductType.objects.all().delete()
        
        self.stdout.write('Створюю типи продуктів...')
        product_types = self.create_product_types()
        
        self.stdout.write('Створюю міста та магазини...')
        stores = self.create_stores()
        
        self.stdout.write('Створюю продукти...')
        self.create_products(product_types, stores)
        
        self.stdout.write(self.style.SUCCESS('Дані успішно згенеровано!'))
        self.stdout.write(f'Типів продуктів: {ProductType.objects.count()}')
        self.stdout.write(f'Магазинів: {Store.objects.count()}')
        self.stdout.write(f'Продуктів: {Product.objects.count()}')

    def create_product_types(self):
        types_data = [
            {'name': 'Beer', 'slug': 'beer', 'description': 'Пиво'},
            {'name': 'Wine', 'slug': 'wine', 'description': 'Вино'},
            {'name': 'Whiskey', 'slug': 'whiskey', 'description': 'Віскі'},
            {'name': 'Vodka', 'slug': 'vodka', 'description': 'Горілка'},
            {'name': 'Cognac', 'slug': 'cognac', 'description': 'Коньяк'},
            {'name': 'Champagne', 'slug': 'champagne', 'description': 'Шампанське'},
            {'name': 'Liqueur', 'slug': 'liqueur', 'description': 'Лікер'},
            {'name': 'Rum', 'slug': 'rum', 'description': 'Ром'},
        ]
        
        product_types = []
        for data in types_data:
            pt = ProductType.objects.create(**data)
            product_types.append(pt)
        
        return product_types

    def create_stores(self):
        cities = [
            'Київ', 'Харків', 'Одеса', 'Дніпро', 'Львів',
            'Запоріжжя', 'Вінниця', 'Полтава', 'Чернівці', 'Івано-Франківськ'
        ]
        
        store_chains = ['Сільпо', 'АТБ', 'Новус', 'Фора', 'Таврія В']
        
        stores = []
        store_counter = 1
        
        for city in cities:
            stores_in_city = random.randint(4, 6)
            
            for i in range(stores_in_city):
                chain = random.choice(store_chains)
                store = Store.objects.create(
                    name=f'{chain} {city} №{store_counter}',
                    address=f'вул. Тестова, {random.randint(1, 200)}',
                    city=city,
                    description=f'Магазин {chain} у місті {city}'
                )
                stores.append(store)
                store_counter += 1
        
        return stores

    def create_products(self, product_types, stores):
        beer_brands = [
            'Lvivske', 'Оболонь', 'Chernigivske', 'Carlsberg', 'Tuborg',
            'Corona', 'Heineken', 'Stella Artois', 'Budweiser', 'Guinness',
            'Hoegaarden', 'Leffe', 'Franziskaner', 'Paulaner', 'Warsteiner',
            'Pilsner Urquell', 'Staropramen', 'Amstel', 'Kronenbourg', 'Peroni'
        ]
        
        wine_brands = [
            'Inkerman', 'Shabo', 'Коблево', 'Colonist', 'Bolgrad',
            'Château Chizay', 'French Kiss', 'Esse', 'Cotnar', 'Cricova',
            'Barton & Guestier', 'Barefoot', 'Yellow Tail', 'Casillero del Diablo', 'Frontera',
            'Gato Negro', 'Santa Rita', 'Concha y Toro', 'Trivento', 'Norton'
        ]
        
        whiskey_brands = [
            'Jameson', 'Jack Daniels', 'Johnnie Walker', 'Chivas Regal', 'Ballantines',
            'Grants', 'Jim Beam', 'Wild Turkey', 'Makers Mark', 'Bulleit'
        ]
        
        vodka_brands = [
            'Nemiroff', 'Khortytsia', 'Finlandia', 'Absolut', 'Smirnoff',
            'Grey Goose', 'Belvedere', 'Ciroc', 'Ketel One', 'Titos'
        ]
        
        cognac_brands = [
            'Hennessy', 'Rémy Martin', 'Courvoisier', 'Martell', 'Camus',
            'Ararat', 'Shustov', 'Praskoveya', 'Tavria', 'Odessa'
        ]
        
        champagne_brands = [
            'Moët & Chandon', 'Veuve Clicquot', 'Dom Pérignon', 'Prosecco', 'Asti',
            'Odessa', 'Artemivske', 'Krymskoye', 'Soviet', 'Krimart'
        ]
        
        liqueur_brands = [
            'Baileys', 'Jägermeister', 'Kahlúa', 'Amaretto', 'Cointreau',
            'Sambuca', 'Limoncello', 'Frangelico', 'Becherovka', 'Chartreuse'
        ]
        
        rum_brands = [
            'Bacardi', 'Captain Morgan', 'Havana Club', 'Malibu', 'Sailor Jerry',
            'Kraken', 'Don Papa', 'Diplomatico', 'Mount Gay', 'Appleton Estate'
        ]
        
        brands_map = {
            'Beer': beer_brands,
            'Wine': wine_brands,
            'Whiskey': whiskey_brands,
            'Vodka': vodka_brands,
            'Cognac': cognac_brands,
            'Champagne': champagne_brands,
            'Liqueur': liqueur_brands,
            'Rum': rum_brands,
        }
        
        price_ranges = {
            'Beer': (25, 80),
            'Wine': (80, 500),
            'Whiskey': (400, 3000),
            'Vodka': (150, 800),
            'Cognac': (500, 5000),
            'Champagne': (200, 2000),
            'Liqueur': (200, 1500),
            'Rum': (300, 1200),
        }
        
        products_per_type = {
            'Beer': 200,
            'Wine': 200,
            'Whiskey': 80,
            'Vodka': 100,
            'Cognac': 60,
            'Champagne': 70,
            'Liqueur': 50,
            'Rum': 40,
        }
        
        sku_counter = 1
        
        for product_type in product_types:
            type_name = product_type.name
            brands = brands_map.get(type_name, ['Generic'])
            price_min, price_max = price_ranges.get(type_name, (50, 500))
            count = products_per_type.get(type_name, 50)
            
            for i in range(count):
                brand = random.choice(brands)
                store = random.choice(stores)
                
                regular_price = Decimal(random.uniform(price_min, price_max)).quantize(Decimal('0.01'))
                
                has_promo = random.random() < 0.3
                promo_price = None
                promo_ends_at = None
                
                if has_promo:
                    discount = random.uniform(0.1, 0.3)
                    promo_price = (regular_price * Decimal(1 - discount)).quantize(Decimal('0.01'))
                    days_until_end = random.randint(1, 30)
                    promo_ends_at = datetime.now().date() + timedelta(days=days_until_end)
                
                variant = f"{random.choice(['0.33л', '0.5л', '0.7л', '1л', '1.5л'])}"
                year = random.choice(['', '2020', '2021', '2022', '2023', '2024'])
                
                Product.objects.create(
                    name=f'{brand} {variant} #{sku_counter} {year}'.strip(),
                    description=f'{type_name} {brand}',
                    sku=f'{type_name[:3].upper()}-{sku_counter:05d}',
                    product_type=product_type,
                    store=store,
                    regular_price=regular_price,
                    promo_price=promo_price,
                    promo_ends_at=promo_ends_at,
                    created_at=datetime.now() - timedelta(days=random.randint(0, 365))
                )
                
                sku_counter += 1
