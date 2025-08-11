from flet import Page, app

from app.controllers.controllers import MainController
from config.config import DB_FILE  # config.py から DB_FILE をインポート


def main(page: Page):
    MainController(page)
    # page.title = '遺言・相続手続きシステム'
    # page.scrollTo = "always"
    # page.scroll = 'always'
    # page.bgcolor = colors.AMBER_50
    # page.window_top = 0
    # page.window_left = 0
    # page.window_height = pyautogui.size().height
    # page.window_width = pyautogui.size().width
    # page.add(MyLayout(page))
    # page.go("/home")


if __name__ == "__main__":
    app(target=main)
