import flet as ft

def main(page: ft.Page):
    # (1) ft.SnackBarのインスタンスをpage.snack_barに設定
    page.snack_bar = ft.SnackBar(
        ft.Text("これはスナックバーです！"),
        bgcolor=ft.Colors.AMBER_400
    )

    def show_snack_bar_click(e):
        print(e)
        # (2) openプロパティをTrueに設定
        page.open(page.snack_bar)
        # (3) ページを更新してスナックバーを表示
        page.update()

    page.add(
        ft.ElevatedButton("スナックバーを表示", on_click=show_snack_bar_click)
    )

if __name__ == "__main__":
    ft.app(target=main)