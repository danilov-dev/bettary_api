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
        background: $surface;
    }
    """

    def __init__(self, *, id: Optional[str] = None, classes: Optional[str] = None, **kwargs):
        super().__init__(id=id, classes=classes, **kwargs)
        self._rich_log: Optional[RichLog] = None
        self._pending_logs: deque = deque()

    def compose(self) -> ComposeResult:
        yield RichLog(
            id="log_content",
            highlight=True,
            markup=True,
            wrap=True,
            auto_scroll=True
        )

    def on_mount(self) -> None:
        self._rich_log = self.query_one("#log_content", RichLog)
        self._rich_log.auto_scroll = True
        # Сбрасываем накопленные логи после монтирования
        while self._pending_logs:
            msg, level = self._pending_logs.popleft()
            self._write_message(msg, level)

    def _write_message(self, message: str, level: str) -> None:
        """Внутренний метод записи в RichLog."""
        color_map = {
            "WARNING": "yellow",
            "ERROR": "bold red",
            "CRITICAL": "bold white on red"
        }
        color = color_map.get(level.upper())
        # Исправлена Rich-разметка: [цвет]текст[/]
        if color:
            formatted = f"[{color}][{level:<8}][/]{message}"
        else:
            formatted = f"[{level:<8}]{message}"
        self._rich_log.write(formatted)

    def write(self, message: str, level: str = "INFO") -> None:
        """Публичный метод для добавления лога. Безопасен до и после on_mount."""
        if self._rich_log is None:
            self._pending_logs.append((message, level))
        else:
            self._write_message(message, level)

    def attach_std_logger(self, logger_name: str = "app", level: int = logging.DEBUG) -> logging.Handler:
        """Подключает стандартный logging к этому виджету."""
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        class _TextualLogHandler(logging.Handler):
            def __init__(self, widget: "LogWidget"):
                super().__init__(level)
                self.widget = widget

            def emit(self, record: logging.LogRecord) -> None:
                msg = self.format(record)
                self.widget.call_later(self.widget.write, msg, record.levelname)

        handler = _TextualLogHandler(self)
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", datefmt="%H:%M:%S")
        )
        logger.addHandler(handler)
        return handler