from datetime import datetime
import logging

from textual import work
from textual.containers import Vertical, Horizontal, Container
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label, Digits

from app.core.database import async_session_maker
from app.core.logger import app_logger
from app.messages import MainDataRequested, MainDataLoaded
from app.services.cell_service import CellService
from app.tui.widgets.log_widget import LogWidget


class HomeView(Widget):
    DEFAULT_CSS = """
    HomeView{
        height: 1fr;
        layout: vertical;
        align: center top;
    }

    .header{
        height: 10;
        align: center top;
        border-bottom: solid $secondary 30%
    }

    .container {
        width: 1fr;
        align: center middle;
        border: vkey $secondary 30%
    }
    
    .wide-container{
        width: 1fr;
    }

    .digits{
        width: 1fr;
        text-align: center;
    }

    .label{
        width: 1fr;
        text-align: center;
    }

    .body {
        height: 1fr;
        margin-top: 1;
    }
    .footer {
        height: 1fr;
        margin-top: 1;
    }

    """

    def __init__(self, session_factory=None):
        super().__init__()
        self.session_factory = session_factory or async_session_maker()
        self.logger = app_logger.get_logger("tui.home_view")

    def compose(self) -> ComposeResult:
        # Верхняя панель (оставляем как есть)
        with Horizontal(classes="header"):
            with Container(classes="container"):
                yield Digits("0", id="cell_counter", classes="digits")
                yield Label("cells", classes="label")
            with Container(classes="container header-inbox"):
                yield Digits("0", id="battery_counter", classes="digits")
                yield Label("batteries", classes="label")
            with Container(classes="container header-inbox"):
                yield Digits("00-00-00", id="record", classes="digits")
                yield Label("last record", classes="label")
            with Container(classes="container header-inbox"):
                yield Digits("00.00.00", id="equipment", classes="digits")
                yield Label("last equipment", classes="label")
            with Container(classes="container"):
                yield Digits("", id="clock", classes="digits")

        # Центральная панель с тремя контейнерами
        with Horizontal(classes="body"):
            with Container(classes="container"):
                yield Digits("1", classes="digits")
                yield Label("One", classes="label")

            with Container(classes="container"):
                yield Digits("2", classes="digits")
                yield Label("Two", classes="label")

            with Container(classes="container wide-container"):
                yield Digits("3", classes="digits")
                yield Label("Three", classes="label")
        # Нижняя панель с логами
        with Vertical(classes="footer"):
            yield Label("Logs", classes="label")
            yield LogWidget(id="log_widget")

    def on_mount(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)
        self.post_message(MainDataRequested())

        # Подключаем виджет к центральному логгеру
        log_widget = self.query_one("#log_widget", LogWidget)
        app_logger.attach_widget(log_widget)

        self.logger.info("HomeView инициализирован")
        self.logger.debug("Тестовое сообщение для проверки")

    def update_clock(self) -> None:
        """Обновление часов"""
        clock = datetime.now().time()
        clock_widget = self.query_one("#clock", Digits)
        clock_widget.update(f"{clock:%T}")

    def on_main_data_requested(self, message: MainDataRequested) -> None:
        """Запрос данных"""
        self.logger.debug("Запрос данных отправлен")
        self._load_data()

    @work(exclusive=True)
    async def _load_data(self) -> None:
        """Асинхронная загрузка данных"""
        self.logger.info("Начало загрузки данных из БД")

        try:
            service = CellService(self.session_factory)

            # Логируем каждый шаг
            self.logger.debug("Получение количества ячеек...")
            cell_count = await service.get_count()
            self.logger.info(f"Загружено ячеек: {cell_count}")

            self.logger.debug("Получение последней записи...")
            last_record = await service.get_last_record()

            if last_record:
                last_record_str = last_record.strftime("%d.%m.%y")
                self.logger.info(f"Последняя запись: {last_record_str}")
            else:
                last_record_str = "Нет данных"
                self.logger.warning("Последняя запись отсутствует")

            # Отправляем данные
            data = [cell_count, last_record_str]
            self.post_message(MainDataLoaded(data))
            self.logger.info("Данные успешно загружены и отправлены")

        except Exception as e:
            self.logger.error(f"Ошибка при загрузке данных: {e}", exc_info=True)
            # Отправляем пустые данные в случае ошибки
            self.post_message(MainDataLoaded([0, "Ошибка"]))

    def on_main_data_loaded(self, message: MainDataLoaded) -> None:
        """Обновление интерфейса после загрузки данных"""
        self.logger.debug("Обновление интерфейса полученными данными")

        try:
            digit = self.query_one('#cell_counter', Digits)
            test = self.query_one('#battery_counter', Digits)
            record = self.query_one('#record', Digits)

            digit.update(str(message.data[0]))
            test.update(str(message.data[0]))
            record.update(str(message.data[1]))

            self.logger.info("Интерфейс обновлён")

        except Exception as e:
            self.logger.error(f"Ошибка обновления интерфейса: {e}")