from textual.widget import Widget
from textual.widgets import RichLog
from textual.app import ComposeResult
import logging
from typing import Optional
from collections import deque


class LogWidget(Widget):
    """Виджет для отображения логов в реальном времени."""

    DEFAULT_CSS = """
    LogWidget {
        height: 1fr;
        width: 1fr;
        border: solid $secondary 30%;
        padding: 1;
    }

    #log_content{
        background: $background
    }
    """

    def __init__(self, *, id: Optional[str] = None, classes: Optional[str] = None, **kwargs):
        super().__init__(id=id, classes=classes, **kwargs)
        self._rich_log: Optional[RichLog] = None
        self._pending_logs: deque = deque()
        self._is_mounted = False

    def compose(self) -> ComposeResult:
        yield RichLog(
            id="log_content",
            highlight=True,
            markup=True,
            wrap=True,
            auto_scroll=True
        )

    def on_mount(self) -> None:
        self._is_mounted = True
        self._rich_log = self.query_one("#log_content", RichLog)
        self._rich_log.auto_scroll = True

        # Сбрасываем накопленные логи
        while self._pending_logs:
            msg, level = self._pending_logs.popleft()
            self._write_message(msg, level)

    def _write_message(self, message: str, level: str) -> None:
        """Внутренний метод записи в RichLog."""
        color_map = {
            "DEBUG": "dim cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "bold red",
            "CRITICAL": "bold white on red"
        }
        color = color_map.get(level.upper())

        if color:
            formatted = f"[{color}]{message}[/]"
        else:
            formatted = message

        self._rich_log.write(formatted)

    def write(self, message: str, level: str = "INFO") -> None:
        """Публичный метод для добавления лога."""
        if not self._is_mounted or self._rich_log is None:
            self._pending_logs.append((message, level))
        else:
            self._write_message(message, level)