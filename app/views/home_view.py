from datetime import datetime

from textual.containers import Vertical, Horizontal, Grid
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label, Digits

from app.core.database import async_session_maker


class HomeView(Widget):
    DEFAULT_CSS = """
    HomeView {
        height: 100%;
        width: 100%;
        layout: vertical;
    }
    .header{
        height: 10;
        width: 100%;
        content-align: center middle;
    }
    #clock {
        dock: right;
        width: auto;
        margin: 3;
    }
    .main-grid{
        layout: grid;
        grid-size: 3;        
    }

    .page-home {
        padding: 1;
        height: 100%;
        width: 100%;
    }

    .long {
        column-span: 2;
        background: magenta 40%;
    }

    .outer-box {
        height: 100%;
        border: solid grey;
        layout: vertical;
    }

    .inner-box {
        height: 1fr;
        border: solid blue;
        margin: 1;
    }

    .line-box {
        height: auto;
        layout: horizontal;
        align: center middle;  /* Это выравнивает содержимое внутри line-box */
        border: solid blue;
        padding: 1;
    }

    /* Исправлено: .lable → .label */
    .label {
        height: auto;
        width: 1fr;  /* Даем метке гибкую ширину */
        content-align: center middle;
    }

    /* Стили для счетчика */
    .counter {
        height: auto;
        width: auto;
        content-align: center middle;
        background: $surface;
        padding: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(classes="header"):
            yield Static("Label", classes="inner-box")
            yield Digits("", id="clock")
        with Grid(classes="main-grid"):
            with Vertical(classes="outer-box"):
                with Horizontal(classes="line-box"):
                    yield Label("Cell's count", classes="label")  # Исправлено: "label" вместо "lable"
                    yield Digits("0", classes="counter")
                with Horizontal(classes="line-box"):
                    yield Label("Cell's count", classes="label")  # Исправлено: "label" вместо "lable"
                    yield Digits("0", classes="counter")
            yield Static("Two (column-span: 2)", classes="outer-box", id="two")
            yield Static("Three", classes="outer-box")
            yield Static("Four", classes="outer-box")
            yield Static("Five", classes="outer-box")
            yield Static("Six", classes="outer-box")
            yield Static("Seven", classes="outer-box")

    def on_mount(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        clock_widget = self.query_one("#clock", Digits)
        clock_widget.update(f"{clock:%T}")