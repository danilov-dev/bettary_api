

from textual.app import App

from app.core import async_session_maker
from app.tui.views.main_view import MainView
from app.core.logger import app_logger


class Application(App):
    """Главное приложение."""

    def __init__(self):
        super().__init__()
        self.session_factory = async_session_maker
        app_logger.setup(level=logging.DEBUG)
        self.logger = app_logger.get_logger("app")

    def on_mount(self):
        self.logger.info("Application started.")
        self.push_screen(MainView(session_factory=self.session_factory))


if __name__ == "__main__":
    import logging
    app = Application()
    app.run()