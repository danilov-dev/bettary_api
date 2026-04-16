from typing import Generic, TypeVar, Optional, List, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, func

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий для работы с сущностями."""

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Получить сущность по ID."""
        result = await self.db_session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """Получить все сущности с пагинацией."""
        result = await self.db_session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def get_count(self) -> int:
        """Получить общее кол-во записей"""
        result = await self.db_session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar() or 0


    async def create(self, obj_in: dict) -> ModelType:
        """Создать новую сущность."""
        obj = self.model(**obj_in)
        self.db_session.add(obj)
        await self.db_session.flush()
        await self.db_session.refresh(obj)
        return obj

    async def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        """Обновить сущность по ID."""
        obj = await self.get_by_id(id)
        if not obj:
            return None

        for field, value in obj_in.items():
            setattr(obj, field, value)

        await self.db_session.flush()
        await self.db_session.refresh(obj)
        return obj

    async def delete(self, id: int) -> bool:
        """Удалить сущность по ID."""
        obj = await self.get_by_id(id)
        if not obj:
            return False

        await self.db_session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.db_session.flush()
        return True