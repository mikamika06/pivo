from __future__ import annotations

from typing import Any, Generic, Iterable, Optional, Type, TypeVar

from django.db import models

ModelType = TypeVar("ModelType", bound=models.Model)


class BaseRepository(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    def get_queryset(self) -> models.QuerySet[ModelType]:
        return self.model._default_manager.all()

    def get_all(self) -> Iterable[ModelType]:
        return self.get_queryset().all()

    def get_by_id(self, object_id: Any) -> Optional[ModelType]:
        return self.get_queryset().filter(pk=object_id).first()

    def add(self, **payload: Any) -> ModelType:
        instance = self.model(**payload)
        instance.full_clean()
        instance.save()
        return instance
