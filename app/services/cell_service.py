from typing import List, Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.models.cell import Cell
from app.repositories.cell_repo import CellRepository


class CellService:
    """Сервис для бизнес-логики работы с Cell."""

    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Cell]:
        """Получить все ячейки с пагинацией."""
        async with self.session_factory() as session:
            repo = CellRepository(model=Cell, db_session=session)
            return await repo.get_all(limit=limit, offset=offset)

    async def get_by_id(self, cell_id: int) -> Optional[Cell]:
        """Получить ячейку по ID."""
        async with self.session_factory() as session:
            repo = CellRepository(model=Cell, db_session=session)
            return await repo.get_by_id(cell_id)

    async def create_cell(self, data: dict) -> Cell:
        """Создать новую ячейку."""
        async with self.session_factory() as session:
            repo = CellRepository(model=Cell, db_session=session)
            result = await repo.create(data)
            await session.commit()
            await session.refresh(result)
            return result

    async def update_cell(self, cell_id: int, data: dict) -> Optional[Cell]:
        """Обновить ячейку."""
        async with self.session_factory() as session:
            repo = CellRepository(model=Cell, db_session=session)
            result = await repo.update(id=cell_id, obj_in=data)
            if result:
                await session.commit()
                await session.refresh(result)
            return result

    async def delete_cell(self, cell_id: int) -> bool:
        """Удалить ячейку."""
        async with self.session_factory() as session:
            repo = CellRepository(model=Cell, db_session=session)
            result = await repo.delete(id=cell_id)
            if result:
                await session.commit()
            return result