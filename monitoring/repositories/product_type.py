from __future__ import annotations

from monitoring.models import ProductType

from .base import BaseRepository


class ProductTypeRepository(BaseRepository[ProductType]):

    def __init__(self) -> None:
        super().__init__(ProductType)
