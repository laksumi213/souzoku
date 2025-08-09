import flet as ft
from components.state import State

# 状態管理インスタンスの作成
shared_state = State("初期テキスト")
label = ft.Text(f"現在のテキスト: {shared_state.get()}")


def main(page: ft.Page):
    def update_label(value: str):
        label.value = f"現在のテキスト: {value}"
        label.update()

    # 状態変更時に呼び出される関数を登録
    shared_state.bind(update_label)

    # サイドバーの作成
    nav_rail = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME,
                selected_icon=ft.icons.HOME_FILLED,
                label="Home"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS,
                selected_icon=ft.icons.SETTINGS,
                label="Settings"
            ),
        ],
        on_change=lambda e: page.go("/settings" if e.control.selected_index == 1 else "/home")
    )

    # メインコンテンツの作成
    main_content = ft.Container(
        content=ft.Text("Main Content Area", size=30),
        expand=True,  # 残りのスペースを埋める
    )

    # レイアウトの配置
    layout = ft.Row(
        controls=[nav_rail, main_content],
        expand=True  # 利用可能なスペース全体に広がる
    )

    def text_set(e):
        shared_state.set(e)
        page.session.set('code', e)
        print('code:', page.session.get("code"))

    # ページ設定
    def route_change(e):
        if page.route == "/home":
            # main_content.content = ft.Text("Home Page!", size=30)
            text_field = ft.TextField(label="テキストを入力", on_change=lambda e: text_set(e.control.value))
            # text_field = ft.TextField(label="テキストを入力", on_change=lambda e: shared_state.set(e.control.value))
            # label = ft.Text(f"現在のテキスト: {shared_state.get()}")
            main_content.content = ft.Column([
                text_field,
                label
            ])
        elif page.route == "/settings":
            main_content.content = ft.Text("Settings Page", size=30)
        page.update()

    page.on_route_change = route_change
    page.add(layout)
    page.go("/home")  # 初期表示


if __name__ == "__main__":
    ft.app(target=main)
