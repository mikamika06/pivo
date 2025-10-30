from __future__ import annotations

from monitoring.models import Store

from .base import BaseRepository


class StoreRepository(BaseRepository[Store]):
    def __init__(self) -> None:
        super().__init__(Store)
