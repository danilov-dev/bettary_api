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
    HomeView {
        height: 100%;
        width: 100%;
        padding: 0 2;
        height: 1fr;
        layout: vertical;
        overflow-y:auto;
        overflow-x:auto;
    }

    
    .header {
        padding: 0 2;
        width: 100%;
        height: 1fr;
        layout: horizontal;
        border-bottom: solid $secondary
    }
    
    .container {
        layout: vertical;
        content-align: center middle;
        box-sizing: border-box;
        padding: 0 0 0 4
    }
    .header-inbox{
        border: vkey $secondary;
        width: 1fr;
        height: auto;
    }
    
    .container > Digits{
        content-align: center middle;
    }
    
    Digits, Label{
        width: 100%;
        height: 1fr;
    }
    
    .test{
        layout: horizontal;
        content-align: center middle;
    }
    .box {
        height: 100%;
        width: 1fr;
        border: solid $secondary;
    }
    .body{
        height: 3fr;
    }    
    
    """

    def __init__(self, session_factory=None):
        super().__init__()
        self.session_factory = session_factory or async_session_maker()

    def compose(self) -> ComposeResult:
        with Horizontal(classes="header"):
            with Vertical(classes="container header-inbox"):
                yield Digits("0", id="cell_counter")
                yield Label("cells", classes="")
            with Vertical(classes="container header-inbox"):
                yield Digits("0", id="battery_counter")
                yield Label("batteries", classes="")
            with Vertical(classes="container header-inbox"):
                yield Digits("00-00-00", id="record")
                yield Label("last record", classes="")
            with Vertical(classes="container header-inbox"):
                yield Digits("00.00.00", id="equipment")
                yield Label("last equipment", classes="")
            with Vertical(classes="container clock-box header-inbox"):
                yield Digits("", id="clock")
        with Vertical(classes="body container"):
            with Horizontal(classes="test"):
                yield Container(Label("One"), classes="box")
                yield Static("Two", classes="box")
                yield Static("Three", classes="box")

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