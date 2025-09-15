import flet as ft


def main(page: ft.Page):
    page.title = "Add Tabs Dynamically"
    page.vertical_alignment = ft.CrossAxisAlignment.START

    # タブのリストを定義
    my_tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[],  # 初期状態は空のタブリスト
        expand=1,
    )

    tab_counter = 0

    def add_tab_btn_clicked(e):
        nonlocal tab_counter
        tab_counter += 1

        # 新しいタブを作成
        new_tab = ft.Tab(
            text=f"新しいタブ {tab_counter}",
            content=ft.Text(f"これは新しいタブ {tab_counter} のコンテンツです。"),
        )

        # 既存のタブリストに新しいタブを追加
        my_tabs.tabs.append(new_tab)

        # 新しく追加されたタブをアクティブにする
        my_tabs.selected_index = len(my_tabs.tabs) - 1

        # UIを更新
        page.update()

    page.add(
        my_tabs,
        ft.ElevatedButton("新しいタブを追加", on_click=add_tab_btn_clicked),
    )


ft.app(target=main)