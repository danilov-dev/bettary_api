from datetime import date

from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.cell import Cell


class CellRepository(BaseRepository[Cell]):
        """Репозиторий для работы с сущностью Cell."""

        async def get_last_record(self) -> date:
                """Получить дату последней записи."""
                result = await self.db_session.execute(
                        select(self.model.tested_at).order_by(self.model.id.desc()).limit(1)
                )
                last_record = result.scalar_one_or_none()
                return last_record or date.today()


