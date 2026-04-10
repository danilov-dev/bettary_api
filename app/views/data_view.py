from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Label


class DataView(Vertical):
    DEFAULT_CSS = """
    .page-home{padding: 1;}
    """
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("📊 Данные", classes="title")
            yield Static("Здесь данные по аккумуляторам")