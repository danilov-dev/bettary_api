from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static, Label


class SettingsView(Vertical):
    DEFAULT_CSS = """
    .page-home{padding: 1;}
    """
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("⚙️ Настройки", classes="title")
            yield Static("Здесь настройки приложения")