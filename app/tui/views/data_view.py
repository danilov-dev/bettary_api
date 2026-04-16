from textual.containers import Vertical
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, DataTable
from textual import work

from app.core.database import async_session_maker
from app.services.cell_service import CellService
from app.messages import CellListRequested, CellListLoaded


class DataView(Widget):
    """Виджет отображения данных аккумуляторов."""

    DEFAULT_CSS = """
    DataView {
        padding: 1;
        height: 1fr;
    }

    #data-title {
        text-style: bold;
        margin-bottom: 1;
    }

    #cells-table {
        height: 1fr;
        border: solid $primary;
    }
    """

    def __init__(self, session_factory=None):
        super().__init__()
        self.session_factory = session_factory or async_session_maker

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("📊 Данные", id="data-title")
            yield DataTable(id="cells-table")

    def on_mount(self) -> None:
        """При монтировании виджета запрашиваем данные."""
        self.post_message(CellListRequested())

    def on_cell_list_requested(self, message: CellListRequested) -> None:
        """Обрабатываем запрос на получение списка ячеек."""
        self._load_cells()

    @work(exclusive=True)
    async def _load_cells(self) -> None:
        """Асинхронная загрузка данных из БД."""
        service = CellService(self.session_factory)
        cells = await service.get_all(limit=100)
        # Отправляем сообщение с загруженными данными
        self.post_message(CellListLoaded(cells))

    def on_cell_list_loaded(self, message: CellListLoaded) -> None:
        """Обрабатываем полученные данные и обновляем таблицу."""
        table = self.query_one("#cells-table", DataTable)

        # Очищаем таблицу
        table.clear()

        # Добавляем колонки
        if not table.columns:
            table.add_column("ID", width=6)
            table.add_column("Barcode", width=20)
            table.add_column("Capacity", width=10)
            table.add_column("Tested At", width=12)

        # Добавляем строки
        for cell in message.cells:
            table.add_row(
                str(cell.id),
                cell.barcode,
                str(cell.capacity),
                str(cell.tested_at)
            )