from flet import (
    Page,
    UserControl,
    CrossAxisAlignment,
    MainAxisAlignment,
    Container,
    NavigationRailDestination,
    NavigationRail,
    Icon,
    icons,
    Column,
    Row,
    Text,
    TextField,
    TextStyle,
    colors,
    TextAlign,
    border,
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
                    icon=icons.ACCOUNT_BOX,
                    label_content=Text("顧客一覧", color=colors.BLACK),
                    data='/home',
                ),
                NavigationRailDestination(
                    icon=icons.EDIT_NOTE,
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


class BaseView(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 15  # 要素間の間隔を指定

    class CustomTextField(UserControl):
        def __init__(self, label, width=200, autofocus=False):
            super().__init__()
            self.text_field = TextField(
                label=label,
                label_style=TextStyle(color=colors.BLACK),
                color=colors.BLACK,
                focused_border_color=colors.CYAN,
                width=width,
                autofocus=autofocus
            )

        def build(self):
            return self.text_field

        @staticmethod
        def ime_on(_):
            asyncio.new_event_loop().run_in_executor(None, utils.ime_on)

        @staticmethod
        def ime_off(_):
            asyncio.new_event_loop().run_in_executor(None, utils.ime_off)

    class CustomContainerbutton(UserControl):
        def __init__(self, icon=None, text_value=''):
            super().__init__()
            self.Container_button = Container(
                content=Column(
                    controls=[
                        Container(
                            Icon(icon, size=45),
                            border=border.all(2, colors.BLACK),
                            padding=10,
                            on_hover=self.on_hover,
                        ),
                        Text(value=text_value, size=14, text_align=TextAlign.CENTER, color=colors.BLACK),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                border=border.all(2, colors.with_opacity(0.0, colors.CYAN)),
            )

        def build(self):
            return self.Container_button

        def on_hover(self, e):
            e.control.bgcolor = 'GREY' if e.data == "true" else 'AMBER_50'
            self.update()


class HomeView(BaseView):
    def __init__(self, page: Page):
        super().__init__(page)

        info = Text(value='＜顧客管理＞', size=30, color=colors.BLACK)

        self.tb_name1_huri = TextField(
            label='被相続人：姓かな',
            label_style=TextStyle(color=colors.BLACK),
            color=colors.BLACK,
            focused_border_color=colors.CYAN,
            width=200,
            autofocus=True
        )

        # self.tb_name1_huri = super().CustomTextField(label='被相続人：姓かな', autofocus=True)
        # self.tb_name1_huri.on_focus = super().CustomTextField.ime_on

        self.tb_name1 = super().CustomTextField(label='被相続人：姓')
        self.tb_name1.on_focus = super().CustomTextField.ime_on
        # self.tb_name1.on_change = lambda e: search_huri_change(self.page, e)

        self.controls = [
            info,
            Row([self.tb_name1_huri, self.tb_name1])
        ]

    def search_clicked(self, e):
        def close(e):
            self.page.dialog.open = False
            self.page.update()


class ProcedureView(BaseView):
    def __init__(self, page: Page):
        super().__init__(page)

        info = Text(value='＜手続き＞', size=30, color=colors.BLACK)

        self.b_heir = super().CustomContainerbutton(text_value='相続人登録', icon=icons.PERSON_ADD)
        # self.b_heir.content.controls[1].value = '相続人登録'
        # self.b_heir.content.controls[0].content = Icon(icons.PERSON_ADD, size=45)

        self.controls = [
            info,
            Container(
                content=Column(
                    controls=[
                        Text('◯ 契約後の手続き', size=20, color=colors.BLACK),
                        self.b_heir,
                    ]
                )
            )
        ]


class SettingsBody(BaseView):
    def __init__(self, page: Page):
        super().__init__(page)

        info = Text(value='＜設定＞', size=30, color=colors.BLACK)

        # self.b_name_registration = super().Container_button_large
        # self.b_name_registration.content.controls[1].value = '自分の名前登録'
        # self.b_name_registration.content.controls[0].content = Icon(icons.HOW_TO_REG, size=45)

        self.controls = [
            info,
            Container(
                content=Column(
                    controls=[
                        Text('◯ データ設定', size=20, color=colors.BLACK),
                        # self.b_name_registration,
                    ]
                )
            )
        ]
