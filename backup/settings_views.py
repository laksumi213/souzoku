from flet import (
    Page,
    CrossAxisAlignment,
    Container,
    NavigationRailDestination,
    NavigationRail,
    icons,
    Column,
    Row,
    Text,
    TextField,
    TextStyle,
    colors,
)
import app.utils as utils
import asyncio


class SideBer(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        # self.page.session.set('selected_index', 0)
        self.page.session.set('SideBer', self)

        self.nav_rail = NavigationRail(
            selected_index=0,
            height=self.page.window.height,
            destinations=[
                NavigationRailDestination(
                    icon=icons.MANAGE_ACCOUNTS,
                    label_content=Text("顧客一覧", color=colors.BLACK),
                    data='/home',
                ),
                NavigationRailDestination(
                    icon=icons.MANAGE_ACCOUNTS,
                    label_content=Text("手続き", color=colors.BLACK),
                    data='/home/procedure',
                ),
                NavigationRailDestination(
                    icon=icons.SETTINGS,
                    selected_icon=icons.SETTINGS,
                    label_content=Text("設定", color=colors.BLACK),
                    data='/settings'
                ),
            ],
            bgcolor=colors.AMBER_50,
            # on_change=lambda e: self.go_page(self.nav_rail)
            # on_change=lambda e: self.go_page(self.nav_rail.destinations[self.nav_rail.selected_index].data)
            # on_change=lambda e: self.go_page(self.nav_rail.destinations[self.nav_rail.selected_index].data, self.nav_rail.selected_index)
        )

        self.content = Row(
            controls=[
                self.nav_rail,
                # Container(
                #     bgcolor=colors.BLACK26,
                #     border_radius=border_radius.all(30),
                #     height=480,
                #     alignment=alignment.center_right,
                #     width=2
                # ),
            ],
            expand=True,
            vertical_alignment=CrossAxisAlignment.START,
        )


class HomeView(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 15  # 要素間の間隔を指定

        info = Text('＜顧客管理＞', size=30, color=colors.BLACK)

        self.tb_name1_huri = TextField(
            label='被相続人：姓かな',
            label_style=TextStyle(color=colors.BLACK),
            color=colors.BLACK,
            focused_border_color=colors.CYAN,
            width=200,
            autofocus=True,
            on_focus=self.ime_on,
            on_change=self.search_clicked
        )

        self.tb_name1 = TextField(
            label='被相続人：姓',
            label_style=TextStyle(color=colors.BLACK),
            color=colors.BLACK,
            focused_border_color=colors.CYAN,
            width=200,
            on_focus=self.ime_on,
            on_blur=self.search_clicked
        )

        self.content = Column(
            controls=[
                info,
                Row([self.tb_name1_huri, self.tb_name1])
            ]
        )

        # self.page.session.set('home_body', self)

    @staticmethod
    def ime_on(_):
        asyncio.new_event_loop().run_in_executor(None, utils.ime_on)

    def search_clicked(self, e):
        def close(e):
            self.page.dialog.open = False
            self.page.update()


class SettingsBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 15  # 要素間の間隔を指定

        info = Text('＜設定＞', size=30, color=colors.BLACK)

        self.controls = [
            info,
        ]

        # self.page.session.set('/settings', self)