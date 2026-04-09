from app.repositories.base import BaseRepository
from app.models.battery import Battery


class BatteryRepository(BaseRepository[Battery]):
    """Репозиторий для работы с сущностью Battery."""
    pass