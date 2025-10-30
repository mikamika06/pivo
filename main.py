from __future__ import annotations

import os
import sys
from decimal import Decimal
from pathlib import Path

import django
from django.conf import settings
from django.core.exceptions import ValidationError

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def bootstrap_django() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silpo_monitor.settings")
    if not settings.configured:
        module = os.environ["DJANGO_SETTINGS_MODULE"]
        if not module:
            raise RuntimeError(
                "DJANGO_SETTINGS_MODULE is not configured. "
                "Set it before running this script."
            )
    django.setup()


def _get_by_name(repo, name: str):
    for entity in repo.get_all():
        if getattr(entity, "name", None) == name:
            return repo.get_by_id(entity.id)
    return None


def ensure_product_type(registry):
    repo = registry.product_types
    existing = _get_by_name(repo, "Beer")
    if existing:
        return existing
    return repo.add(
        name="Beer",
        slug="beer",
        description="Alcohol beverages monitored for promotions.",
    )


def ensure_store(registry):
    repo = registry.stores
    existing = _get_by_name(repo, "Silpo Kyiv Center")
    if existing:
        return existing
    return repo.add(
        name="Silpo Kyiv Center",
        description="Flagship store for promo scraping.",
        address="Khreshchatyk St. 1",
        city="Kyiv",
    )


def ensure_product(registry, store, product_type):
    repo = registry.products
    for entity in repo.get_all():
        if getattr(entity, "sku", None) == "BEER-0001":
            return repo.get_by_id(entity.id)
    return repo.add(
        name="Lvivske 1715",
        description="Filtered lager 4.7%",
        sku="BEER-0001",
        product_type=product_type,
        store=store,
        regular_price=Decimal("32.50"),
        promo_price=Decimal("27.90"),
        promo_ends_at=None,
    )


def get_repository_registry():
    from monitoring.repositories import repository_registry

    return repository_registry


def demo() -> None:
    registry = get_repository_registry()
    product_type = ensure_product_type(registry)
    store = ensure_store(registry)
    product = ensure_product(registry, store, product_type)

    product_type_by_id = registry.product_types.get_by_id(product_type.id)
    store_by_id = registry.stores.get_by_id(store.id)
    product_by_id = registry.products.get_by_id(product.id)

    all_types = list(registry.product_types.get_all())
    all_stores = list(registry.stores.get_all())
    all_products = list(registry.products.get_all())

    print("Product type:", product_type_by_id)
    print("Store:", store_by_id)
    discount = 0
    if product_by_id and product_by_id.regular_price and product_by_id.promo_price:
        discount = round(
            (1 - (product_by_id.promo_price / product_by_id.regular_price)) * 100, 2
        )

    print("Product:", product_by_id, "discount =", discount, "%")
    print("All product types:", [obj.name for obj in all_types])
    print("All stores:", [obj.name for obj in all_stores])
    print("All products:", [obj.name for obj in all_products])


if __name__ == "__main__":
    try:
        bootstrap_django()
        demo()
    except ValidationError as exc:
        print("Validation error:", exc, file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print("Error:", exc, file=sys.stderr)
        sys.exit(1)
