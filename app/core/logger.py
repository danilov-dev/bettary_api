import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional, Any, Set
from weakref import WeakSet


class AppLogger:
    """
    Класс-синглтон для управления центральным логированием приложения.
    """

    _instance: Optional['AppLogger'] = None
    _logger: Optional[logging.Logger] = None
    _handlers: Set[logging.Handler] = WeakSet()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self._initialized = False
        self.log_dir = "logs"
        self.log_file = os.path.join(self.log_dir, "app.log")
        self.max_bytes = 5 * 1024 * 1024
        self.backup_count = 3
        self.format_str = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
        self.date_format = "%H:%M:%S"

    def setup(self, level: int = logging.DEBUG, enable_console: bool = False) -> logging.Logger:
        """Настройка центрального логгера (вызывать один раз при старте)"""
        if self._initialized:
            return self._logger

        # Создаем логгер
        self._logger = logging.getLogger("app")
        self._logger.setLevel(level)

        # Предотвращаем дублирование обработчиков
        if self._logger.handlers:
            self._logger.handlers.clear()

        # Создаем директорию для логов
        os.makedirs(self.log_dir, exist_ok=True)

        # 1. Файловый обработчик
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(self.format_str, datefmt=self.date_format)
        file_handler.setFormatter(file_formatter)
        self._logger.addHandler(file_handler)
        self._handlers.add(file_handler)

        # 2. Консольный обработчик (только для DEBUG режима)
        if enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_formatter = logging.Formatter("%(levelname)s | %(message)s")
            console_handler.setFormatter(console_formatter)
            self._logger.addHandler(console_handler)
            self._handlers.add(console_handler)
            self._logger.info("Консольный вывод логов включен")

        self._initialized = True

        self._logger.info("=" * 30)
        self._logger.info("Система логирования инициализирована")
        self._logger.info(f"Файл логов: {self.log_file}")
        self._logger.info("=" * 30)

        return self._logger

    def attach_widget(self, widget: Any) -> None:
        """Подключает виджет к центральному логгеру"""
        if not self._initialized or not self._logger:
            raise RuntimeError("AppLogger не инициализирован. Вызовите setup() сначала.")

        # Создаем специальный обработчик для виджета
        class WidgetLogHandler(logging.Handler):
            def __init__(self, widget_ref: Any):
                super().__init__()
                self.widget_ref = widget_ref

            def emit(self, record: logging.LogRecord) -> None:
                msg = self.format(record)
                try:
                    if hasattr(self.widget_ref, 'write'):
                        self.widget_ref.write(msg, record.levelname)
                except Exception:
                    pass

        widget_handler = WidgetLogHandler(widget)
        widget_handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", datefmt="%H:%M:%S")
        )
        widget_handler.setLevel(self._logger.level)

        self._logger.addHandler(widget_handler)
        self._handlers.add(widget_handler)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Возвращает логгер для модуля"""
        if name is None:
            return self._logger if self._logger else logging.getLogger("app")

        if self._logger:
            return self._logger.getChild(name)
        return logging.getLogger(f"app.{name}")


# Глобальный экземпляр
app_logger = AppLogger()