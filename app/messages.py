"""Сообщения для обмена данными между виджетами и приложением."""

from textual.message import Message


class CellListRequested(Message):
    """Запрос на получение списка ячеек."""
    pass

class CellListLoaded(Message):
    """Список ячеек загружен."""

    def __init__(self, cells: list) -> None:
        super().__init__()
        self.cells = cells

class MainDataRequested(Message):
    pass

class MainDataLoaded(Message):
    def __init__(self, data: list) -> None:
        super().__init__()
        self.data = data