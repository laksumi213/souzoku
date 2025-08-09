from flet import (
    app,
    Page,
)
from app.controllers.controllers import MainController
import shutil


def db_copy():
    src = '/Users/laksumi/Library/CloudStorage/OneDrive-株式会社プロフィット・ワン/General/py/inheritance/inheritance.db'  # "コピー元のファイルパス"
    dst = '/Users/laksumi/souzoku/database/'  # "コピー先のファイルパス"
    try:
        shutil.copy2(src, dst)
        print(f"データベースをコピーしました（メタデータ保持）。")
    except FileNotFoundError:
        print(f"エラー: {src} が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


def main(page: Page):
    # db_copy()
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
