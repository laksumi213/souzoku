from flet import Page, app

from app.controllers.controllers import MainController


def main(page: Page):
    MainController(page)


if __name__ == "__main__":
    app(target=main)
