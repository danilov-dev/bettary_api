from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, TabbedContent, TabPane

from app.core.database import async_session_maker
from app.tui.views.data_view import DataView
from app.tui.views.home_view import HomeView
from app.tui.views.settings_view import SettingsView


class MainView(Screen):
    """Главный экран приложения с табами."""

    DEFAULT_CSS = """
    MainView{
        min-width: 100%;
    }
    TabbedContent {
        margin: 0;
        padding: 0;
    }

    TabPane {
        padding: 1;
    }

    /* Стилизация табов */
    TabbedContent > .tab--active {
        background: $primary 20%;
        color: $text;
        border-bottom: solid $primary;
    }

    TabbedContent > .tab:hover {
        background: $primary 10%;
    }
    """

    def __init__(self, session_factory=None):
        super().__init__()
        self.session_factory = session_factory or async_session_maker

    def compose(self) -> ComposeResult:
        yield Header()

        # Указываем initial по имени вкладки (без суффиксов)
        with TabbedContent(initial="home"):
            with TabPane("🏠 HOME", id="home"):
                # yield HomeView(session_factory=self.session_factory)
                yield HomeView(session_factory=self.session_factory)

            with TabPane("📊 DATA", id="data"):
                yield DataView(session_factory=self.session_factory)

            with TabPane("⚙️ SETTINGS", id="settings"):
                yield SettingsView()

        yield Footer()

    def on_mount(self) -> None:
        self.title = "Battery System"