from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, ContentSwitcher

from app.views.data_view import DataView
from app.views.home_view import HomeView
from app.views.settings_view import SettingsView


class MainView(Screen):
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

    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar"):
            yield Button("🏠 Home", id="nav-home", classes="menu-btn")
            yield Button("📊 Data", id="nav-data", classes="menu-btn")
            yield Button("⚙️ Settings", id="nav-settings", classes="menu-btn")

        yield ContentSwitcher(
            HomeView(id="page-home"),
            DataView(id="page-data"),
            SettingsView(id="page-settings"),
            id="content",
            initial="page-home"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        routes = {
            "nav-home": "page-home",
            "nav-data": "page-data",
            "nav-settings": "page-settings",
        }

        if target := routes.get(event.button.id):
            self.query_one("#content", ContentSwitcher).current = target
            self._update_active_button(event.button.id)

    def _update_active_button(self, active_btn_id: str) -> None:
        for btn in self.query(".menu-btn"):
            btn.remove_class("-active")
        self.query_one(f"#{active_btn_id}").add_class("-active")