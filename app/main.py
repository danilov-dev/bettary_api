from textual.app import App

from app.core.database import async_session_maker
from app.views.main_view import MainView


class Application(App):
    """Главное приложение."""

    def __init__(self):
        super().__init__()
        self.session_factory = async_session_maker

    def on_mount(self):
        self.push_screen(MainView(session_factory=self.session_factory))


if __name__ == "__main__":
    app = Application()
    app.run()