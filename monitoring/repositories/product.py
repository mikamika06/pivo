from __future__ import annotations

from monitoring.models import Product

from .base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self) -> None:
        super().__init__(Product)

