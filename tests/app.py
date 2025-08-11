import flet as ft
from ui_tabs import BankTabContent, CustomerTabContent

from database import DatabaseManager


class MainApp(ft.Column):
    """
    Fletアプリケーションのメインクラス。
    UIの構築とデータベース操作の連携を行います。
    """

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "顧客・銀行情報管理システム"
        self.page.vertical_alignment = ft.CrossAxisAlignment.START
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.window_width = 800
        self.page.window_height = 700
        self.page.scroll = "auto"

        self.db = DatabaseManager()

        # スナックバー (メッセージ表示用)
        self.page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

        # 各タブコンテンツのインスタンス化
        # show_message_callback を渡して、タブ内でスナックバーを表示できるようにする
        self.customer_tab_content = CustomerTabContent(self.db, self.show_message)
        self.bank_tab_content = BankTabContent(self.db, self.show_message)

        self.controls = [
            ft.AppBar(
                title=ft.Text("顧客・銀行情報管理システム", color=ft.colors.WHITE),
                bgcolor=ft.colors.BLUE_ACCENT_700,
                center_title=True,
            ),
            ft.Tabs(
                selected_index=0,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text="顧客情報",
                        icon=ft.icons.PEOPLE,
                        content=self.customer_tab_content,
                    ),
                    ft.Tab(
                        text="銀行情報",
                        icon=ft.icons.ACCOUNT_BALANCE,
                        content=self.bank_tab_content,
                    ),
                ],
                expand=1,
            ),
        ]

    def show_message(self, message: str, color=ft.colors.GREEN_500):
        """スナックバーにメッセージを表示します。"""
        self.page.snack_bar.content = ft.Text(message)
        self.page.snack_bar.bgcolor = color
        self.page.snack_bar.open = True
        self.page.update()
