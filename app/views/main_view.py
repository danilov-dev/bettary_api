from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button

from app.core.database import async_session_maker
from app.views.data_view import DataView
from app.views.home_view import HomeView
from app.views.settings_view import SettingsView


class MainView(Screen):
    """Главный экран приложения с навигацией."""

    DEFAULT_CSS = """
    Screen { layout: horizontal; }

    /* Боковое меню припарковано слева */
    #sidebar {
        dock: left;
        width: 30;
        background: $panel;
        padding: 1;
        border-right: solid $primary;
    }

    .menu-btn {
        width: 100%;
        margin: 1 0;
    }

    .menu-btn.-active {
        background: $primary 30%;
        color: $text;
        border-bottom: solid $primary;
    }

    /* Контент растягивается на всё оставшееся место */
    #content {
        width: 1fr;
        height: 100%;
        background: $surface;
        overflow-y: auto;
    }
    """

    def __init__(self, session_factory=None):
        super().__init__()
        self.session_factory = session_factory or async_session_maker
        self.current_screen_id = "home"

    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar"):
            yield Button("🏠 Home", id="nav-home", classes="menu-btn")
            yield Button("📊 Data", id="nav-data", classes="menu-btn")
            yield Button("⚙️ Settings", id="nav-settings", classes="menu-btn")

        # Контейнер для динамической подмены экранов
        with Vertical(id="content"):
            pass

    def on_mount(self) -> None:
        """При монтировании показываем домашний экран."""
        self._show_screen("home")
        self._update_active_button("nav-home")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Обработка нажатий кнопок меню."""
        routes = {
            "nav-home": "home",
            "nav-data": "data",
            "nav-settings": "settings",
        }

        if target := routes.get(event.button.id):
            self._show_screen(target)
            self._update_active_button(event.button.id)

    def _show_screen(self, screen_name: str) -> None:
        """Показывает нужный экран, удаляя предыдущий."""
        content_container = self.query_one("#content", Vertical)

        # Очищаем контейнер от предыдущего экрана
        content_container.remove_children()

        # Создаем и добавляем новый экран
        if screen_name == "home":
            screen = HomeView()
        elif screen_name == "data":
            screen = DataView(session_factory=self.session_factory)
        elif screen_name == "settings":
            screen = SettingsView()
        else:
            return

        self.current_screen_id = screen_name
        content_container.mount(screen)

    def _update_active_button(self, active_btn_id: str) -> None:
        """Обновляет активную кнопку в меню."""
        for btn in self.query(".menu-btn"):
            btn.remove_class("-active")
        self.query_one(f"#{active_btn_id}").add_class("-active")