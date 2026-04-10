from textual.app import App

from app.views.main_view import MainView

class Application(App):
    def on_mount(self):
        self.push_screen(MainView())


if __name__ == "__main__":
    app = Application()
    app.run()

