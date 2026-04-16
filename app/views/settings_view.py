from textual.containers import Vertical
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Static, Label


class SettingsView(Widget):
    """Виджет настроек."""

    DEFAULT_CSS = """
    SettingsView {
        padding: 1;
        height: 1fr;
    }

    .title {
        text-style: bold;
        margin-bottom: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("⚙️ Настройки", classes="title")
            yield Static("Здесь настройки приложения")