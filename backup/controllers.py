from app.views.views import SideBer, HomeView, SettingsBody, ProcedureView
from app.models.models import *
from flet import (
    Row,
    Page,
    MainAxisAlignment,
    CrossAxisAlignment,
    VerticalDivider,
    colors,
    Column,
    Container,
    ElevatedButton,
    icons,
)


def search_huri_change(page: Page, e):
    print()
    print('search_huri_change:', e.control.value)
    print(get_customer_huri(e.control.value))


def route_change(page: Page, e):
    print()
    print('route_change', e.route)

    # 戻るボタンが非表示の場合は表示する
    # print('eb_return:', page.session.get('eb_return').content.visible)
    if not page.session.get('eb_return').content.visible and len(page.session.get('past_route')) > 0:
        page.session.get('eb_return').content.visible = True

    # routeを保存
    past_route = page.session.get('past_route')
    past_route.append(e.route)
    page.session.set('past_route', past_route)
    print('past_route:', page.session.get('past_route'))

    # サイドバーのインデックスを保存（戻るボタンを押したときに使用）
    page.session.get('past_selected_index')[e.route] = page.session.get('sideBer').nav_rail.selected_index

    page.session.get('main_body').content = page.session.get(e.route)
    page.update()


class BaseControllers(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.on_route_change = lambda e: route_change(self.page, e)
        self.alignment = MainAxisAlignment.START
        self.vertical_alignment = CrossAxisAlignment.START
        self.expand = True


class MyLayout(BaseControllers):
    def __init__(self, page: Page):
        super().__init__(page)
        # self.page = page
        # self.page.on_route_change = lambda e: route_change(self.page, e)
        # self.alignment = MainAxisAlignment.START
        # self.vertical_alignment = CrossAxisAlignment.START
        # self.expand = True
        self.past_route = []
        page.session.set('past_route', self.past_route)

        # AppHeader(page, 'WEB LAYOUT')

        self.page.session.set('sideBer', SideBer(self.page))
        self.page.session.set('/settings', SettingsBody(self.page))
        self.page.session.set('/home', HomeView(self.page))
        self.page.session.set('/home/procedure', ProcedureView(self.page))

        main_body = Container(
            content=page.session.get('home'),
            expand=True,  # 残りのスペースを埋める
        )
        self.page.session.set('main_body', main_body)

        self.eb_return = Container(
            content=ElevatedButton(
                "戻る",
                # style=ButtonStyle(
                #     padding=20,
                #     color=colors.BLUE,
                #     bgcolor=colors.WHITE,
                # ),
                icon=icons.ARROW_BACK,
                # visible=True,
                visible=False,
                on_click=self.return_clicked
            ),
            margin=5,
        )
        self.page.session.set('eb_return', self.eb_return)

        self.controls = [
            self.page.session.get('sideBer'),
            Container(height=self.page.window_height, content=VerticalDivider(thickness=1, color=colors.BLACK)),
            Column([
                self.page.session.get('eb_return'),
                main_body
            ])
        ]

        # サイドバーのselected_indexを保存
        self.past_selected_index = {
            self.page.session.get('sideBer').nav_rail.destinations[
                self.page.session.get('sideBer').nav_rail.selected_index
            ].data: self.page.session.get('sideBer').nav_rail.selected_index
        }
        self.page.session.set('past_selected_index', self.past_selected_index)

        # サイドバーのボタンを押したときの動きを登録
        self.page.session.get('sideBer').nav_rail.on_change = lambda e: self.page.go(
            self.page.session.get('sideBer').nav_rail.destinations[
                self.page.session.get('sideBer').nav_rail.selected_index].data
        )

        # home_viewのカナを入力した場合の動きを登録
        print(self.page.session.get('/home').tb_name1_huri)
        self.page.session.get('/home').tb_name1_huri.on_change = lambda e: search_huri_change(self.page, e)

        # self.page.session.get('/home').tb_name1.label = '被相続人：姓'
        # print(self.page.session.get('/home').tb_name1.label)
        # home_controllers = HomeControllers(self.page)

    def return_clicked(self, _):
        print('')
        print('return_clicked:')

        # 戻るrouteを取得して削除
        self.page.session.get('past_route').pop()
        key = self.page.session.get('past_route').pop()
        # print('past_route:', self.page.session.get('past_route'))

        # サイドバーのインデックスを設定
        # print('past_selected_index:', self.page.session.get('past_selected_index')[key])
        self.page.session.get('sideBer').nav_rail.selected_index = self.page.session.get('past_selected_index')[key]

        # 前のページに戻る
        self.page.go(key)

        # 過去ルートがホームだけの場合、戻るボタンを非表示
        if len(self.page.session.get('past_route')) == 0:
            # self.eb_return.visible = False
            self.page.session.get('eb_return').content.visible = False
            self.page.update()


class HomeControllers(BaseControllers):
    def __init__(self, page: Page):
        super().__init__(page)

        # home_viewのカナを入力した場合の動きを登録
        self.page.session.get('/home').tb_name1_huri.on_change = lambda e: search_huri_change(self.page, e)