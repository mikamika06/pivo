import os
import django
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silpo_monitor.settings")
django.setup()

from monitoring.repositories import repository_registry as repo
from monitoring.models import Product, Store, ProductType


def main():
    repo.stores.delete_all()
    repo.product_types.delete_all()
    repo.products.delete_all()
    print("Database cleared\n")

    beer = repo.product_types.add(name="Beer", slug="beer", description="Пиво")
    wine = repo.product_types.add(name="Wine", slug="wine", description="Вино")
    silpo_kyiv = repo.stores.add(name="Silpo Київ", city="Київ", address="Хрещатик 1", description="Центр")
    atb = repo.stores.add(name="АТБ Харків", city="Харків", address="Сумська 25", description="Дискаунтер")
    print("Product types and stores added")

    repo.products.add(name="Lvivske 1715", sku="BEER-001", description="Лагер 4.7%",
                      product_type=beer, store=silpo_kyiv, regular_price=Decimal("32.50"), 
                      promo_price=Decimal("27.90"), promo_ends_at=None)
    
    repo.products.add(name="Оболонь Преміум", sku="BEER-002", description="Світле 4.5%",
                      product_type=beer, store=atb, regular_price=Decimal("35.00"), 
                      promo_price=None, promo_ends_at=None)
    
    repo.products.add(name="Inkerman", sku="WINE-001", description="Червоне 13%",
                      product_type=wine, store=silpo_kyiv, regular_price=Decimal("125.00"), 
                      promo_price=Decimal("99.00"), promo_ends_at=None)
    print("Products added\n")


def demo_queries():

    print("\nAll products:")
    for p in repo.products.get_all():
        print(f"{p.name} - {p.regular_price} грн")

    print("\nProducts with discount:")
    for p in repo.products.get_all():
        if p.promo_price:
            discount = round((1 - p.promo_price/p.regular_price) * 100, 1)
            print(f"{p.name}: {p.regular_price} -> {p.promo_price} грн (-{discount}%)")

    products = list(repo.products.get_all())
    avg_price = sum(p.regular_price for p in products) / len(products)
    print(f"\nStats:")
    print(f"All products: {len(products)}")
    print(f"All stores: {len(list(repo.stores.get_all()))}")


if __name__ == "__main__":
    main()
    demo_queries()
