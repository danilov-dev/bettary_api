from datetime import datetime

from textual import work
from textual.containers import Vertical, Horizontal, Container
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label, Digits

from app.core.database import async_session_maker
from app.messages import MainDataRequested, MainDataLoaded
from app.services.cell_service import CellService


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

    .digits{
        width: 1fr;
        text-align: center;
    }
    .label{
        width: 1fr;
        text-align: center;
    }
    """

    def __init__(self, session_factory=None):
        super().__init__()
        self.session_factory = session_factory or async_session_maker()

    def compose(self) -> ComposeResult:
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
        with Horizontal(classes="body"):
            with Container(classes="container"):
                yield Digits("1", classes="digits")
                yield Label("One", classes="label")
            with Container(classes="container"):
                yield Digits("2", classes="digits")
                yield Label("Two", classes="label")
            with Container(classes="container"):
                yield Digits("3", classes="digits")
                yield Label("Three", classes="label")

    def on_mount(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)
        self.post_message(MainDataRequested())

    def update_clock(self) -> None:
        clock = datetime.now().time()
        clock_widget = self.query_one("#clock", Digits)
        clock_widget.update(f"{clock:%T}")

    def on_main_data_requested(self, message: MainDataRequested) -> None:
        self._load_data()

    @work(exclusive=True)
    async def _load_data(self) -> None:
        data = []
        service = CellService(self.session_factory)
        cell_count = await service.get_count()
        last_record = await service.get_last_record()
        data.append(cell_count)
        data.append(last_record.strftime("%d.%m.%y"))
        self.post_message(MainDataLoaded(data))

    def on_main_data_loaded(self, message: MainDataLoaded) -> None:
        digit = self.query_one('#cell_counter', Digits)
        test = self.query_one('#battery_counter', Digits)
        record = self.query_one('#record', Digits)
        digit.update(str(message.data[0]))
        test.update(str(message.data[0]))
        record.update(str(message.data[1]))