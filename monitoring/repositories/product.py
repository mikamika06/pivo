from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional

from django.db.models import Avg, Count, Q

from monitoring.models import Product

from .base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self) -> None:
        super().__init__(Product)

    def get_products_by_store(self, store_id: int):
        return self.get_queryset().filter(store_id=store_id)

    def get_products_with_promo(self):
        return self.get_queryset().filter(promo_price__isnull=False)

    def get_report_by_stores(self):
        from django.db.models import F
        
        stores = self.get_queryset().values('store_id', 'store__name').annotate(
            products_count=Count('id'),
            promo_count=Count('id', filter=Q(promo_price__isnull=False)),
            avg_regular_price=Avg('regular_price')
        ).order_by('store_id')
        
        result = []
        for store_data in stores:
            result.append({
                'store_id': store_data['store_id'],
                'store_name': store_data['store__name'],
                'products_count': store_data['products_count'],
                'promo_count': store_data['promo_count'],
                'avg_regular_price': float(store_data['avg_regular_price']) if store_data['avg_regular_price'] else 0.0
            })
        return result

