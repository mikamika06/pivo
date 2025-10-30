from __future__ import annotations

from dataclasses import dataclass, field

from .product import ProductRepository
from .product_type import ProductTypeRepository
from .store import StoreRepository


@dataclass(frozen=True)
class RepositoryRegistry:
    product_types: ProductTypeRepository = field(
        default_factory=ProductTypeRepository
    )
    stores: StoreRepository = field(default_factory=StoreRepository)
    products: ProductRepository = field(default_factory=ProductRepository)


repository_registry = RepositoryRegistry()
