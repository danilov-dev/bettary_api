from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Label


class HomeView(Horizontal):
    DEFAULT_CSS = """
    .page-home{padding: 1;}
    """
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("🏠 Главная", classes="title")
            yield Static("Здесь дашборд, графики, таблицы...")