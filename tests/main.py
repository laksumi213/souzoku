import flet as ft

from app import MainApp


def main(page: ft.Page):
    """
    Fletアプリケーションのエントリポイント。
    """
    app = MainApp(page)
    page.add(app)
    # page.update() は MainApp の __init__ 内で行われるか、
    # 各コンポーネントの update() で自動的に行われます。
    # ここでは明示的に呼ぶ必要はありません。


if __name__ == "__main__":
    # 既存のデータベースファイルを削除（テスト用、本番では注意）
    # if os.path.exists(DB_FILE):
    #     os.remove(DB_FILE)
    #     print(f"既存のデータベースファイル '{DB_FILE}' を削除しました。")

    ft.app(target=main)
