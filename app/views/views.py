import asyncio

# from typing import Dict, Any
from time import sleep
import pyautogui
import pyperclip
import subprocess
from flet import (
    AlertDialog,
    ButtonStyle,
    Checkbox,
    Column,
    Container,
    CrossAxisAlignment,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    DropdownM2,
    ElevatedButton,
    Icon,
    IconButton,
    MainAxisAlignment,
    NavigationRail,
    NavigationRailDestination,
    OutlinedButton,
    Page,
    Row,
    SnackBar,
    Tab,
    Tabs,
    Text,
    TextAlign,
    TextField,
    TextStyle,
    alignment,
    border,
    Colors,
    dropdown,
    Icons,
)

import app.utils as utils


# class BaseView(Row):
class BaseView(Column):
    def __init__(self):
        super().__init__()
        self._controller = None
        self._page = None
        self.spacing = 15  # 要素間の間隔を指定
        self.alignment = MainAxisAlignment.START
        self.vertical_alignment = CrossAxisAlignment.START
        self.expand = True
        self.scrollTo = "always"
        self.scroll = "always"
        # self.page.scrollTo = "always"
        # self.page.scroll = 'always'

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, page):
        self._page = page

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def dialog_close(self, _):
        self._page.dialog.open = False
        # self.page.overlay.clear()
        self._page.update()

    def dialog_registration(self, _):
        def dialog_close(_):
            self._page.dialog.open = False
            self._page.update()

        self._page.dialog = AlertDialog(
            open=True,
            modal=True,
            title=Text("登録完了"),
            content=Text("登録が完了しました。"),
            actions=[ElevatedButton(text="OK", on_click=dialog_close)],
            actions_alignment=MainAxisAlignment.END,
        )
        self._page.update()


class CustomText(Text):
    def __init__(self, value: str = "", size=30, *args, **kwargs):
        super().__init__(value=value, size=size, *args, **kwargs)
        self.color = Colors.BLACK

    @classmethod
    def create_self(cls, config=None):
        return CustomText(**config)
        # if config is not None:
        #     return CustomText(**config)
        # else:
        #     return CustomText()


class CustomTextField(TextField):
    def __init__(
        self,
        label: str = "",
        label_style=TextStyle(color=Colors.BLACK),
        # hint_text: str = "",
        color=Colors.BLACK,
        focused_border_color=Colors.CYAN,
        password: bool = False,
        width=200,
        on_change=None,
        on_focus=None,
        _blur=None,
        format=None,
        hinttext=None,
        *args,
        **kwargs,
    ):
        super().__init__(
            label=label,
            label_style=label_style,
            color=color,
            width=width,
            focused_border_color=focused_border_color,
            password=password,
            on_change=self._on_change,
            on_focus=self._on_focus,
            _blur=self._blur,
            *args,
            **kwargs,
        )
        self._on_change_callback = on_change
        self._blur_callback = _blur
        self._on_focus = on_focus
        self._blur = _blur
        self.hint_text = hinttext
        self.format = format
        # self.label_style = TextStyle(color=Colors.BLACK)
        # self.color = Colors.BLACK
        # self.focused_border_color = Colors.CYAN

    def _blur(self, e):
        print('_blur:')
        if self._blur_callback:
            self._blur_callback(e)

    def _on_change(self, e):
        if self._on_change_callback:
            self._on_change_callback(e)

    def _on_focus(self, e):
        if self.format == "ime_on":
            self.ime_on()

        if self.format == "ime_off":
            self.ime_off()

        if self.format == "number":
            self.ime_off()
            self.re_number_format(e)

    # def _on_blur(self, e):
    #     if self.format == "number":
    #         self.number_format(e)

    def number_format(self, e):
        e.control.value = (
            format(int(e.control.value), ",") if e.control.value != "" else 0
        )
        self.page.update()

    def re_number_format(self, e):
        e.control.value = str(e.control.value).replace(",", "")
        self.page.update()

    @classmethod
    def ime_on(cls):
        asyncio.new_event_loop().run_in_executor(None, utils.ime_on)

    @classmethod
    def ime_off(cls):
        asyncio.new_event_loop().run_in_executor(None, utils.ime_off)

    @classmethod
    def create_self(cls, config=None):
        return CustomTextField(**config)
        # if config is not None:
        #     return CustomText(**config)
        # else:
        #     return CustomText()


class CustomTextFieldDialog(CustomTextField):
    def __init__(
        self,
        label_style=TextStyle(color=Colors.WHITE),
        width=150,
        color=Colors.WHITE,
        border_color=Colors.WHITE,
        focused_border_color=Colors.CYAN,
        *args,
        **kwargs,
    ):
        super().__init__(
            label_style=label_style,
            width=width,
            color=color,
            border_color=border_color,
            focused_border_color=focused_border_color,
            *args,
            **kwargs,
        )


class CustomContainerButton(Container):
    def __init__(
        self,
        icon: str = "",
        text_value: str = "",
        border=border.all(2, Colors.with_opacity(0.0, Colors.CYAN)),
        on_hover=None,
        *args,
        **kwargs,
    ):
        super().__init__(border=border, on_hover=self._on_hover, *args, **kwargs)
        self.icon = icon
        self.text_value = text_value
        self._on_hover = on_hover
        self.build()

    def build(self):
        self.content = Column(
            controls=[
                Container(
                    Icon(self.icon, size=45),
                    border=border.all(2, Colors.BLACK),
                    padding=10,
                    on_hover=self._on_hover,
                ),
                Text(
                    value=self.text_value,
                    size=14,
                    text_align=TextAlign.CENTER,
                    color=Colors.BLACK,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

    def _on_hover(self, e):
        e.control.bgcolor = "GREY" if e.data == "true" else "AMBER_50"
        self.update()


class CustomDropdown(DropdownM2):
    def __init__(
        self,
        color=Colors.BLACK,
        bgcolor=Colors.AMBER_50,
        width=200,
        text_style=TextStyle(color=Colors.BLACK),
        label_style=TextStyle(color=Colors.BLACK),
        focused_color=Colors.BLACK,
        # focused_border_color=Colors.BLACK,
        focused_border_color=Colors.CYAN,
        *args,
        **kwargs,
    ):
        super().__init__(
            color=color,
            bgcolor=bgcolor,
            width=width,
            text_style=text_style,
            label_style=label_style,
            focused_color=focused_color,
            focused_border_color=focused_border_color,
            *args,
            **kwargs,
        )

    def add_options(self, data):
        # self.options = None
        for item in data:
            self.options.append(dropdown.Option(*item.values()))


class CustomElevatedButton(ElevatedButton):
    def __init__(
            self,
            icon: str = "",
            text_value: str = '',
            text_size=20,
            height=40,
            data='',
            on_click=None,
            # on_hover=None,
            *args,
            **kwargs
    ):
        super().__init__(
            height=height,
            data=data,
            on_click=self._on_click,
            on_hover=self._on_hover,
            *args,
            **kwargs
        )

        self._on_click_callback = on_click

        self.content = Container(
            content=Row(
                controls=[
                    Icon(icon),
                    Text(value=text_value, size=text_size),
                ]
            ),
            height=height,
            data=data
        )

    def _on_click(self, e):
        print('_on_click:')
        print('self.data:', self.data)
        if self._on_click_callback:
            self._on_click_callback(e, self.data)

    def _on_hover(self, e):
        e.control.bgcolor = "GREY" if e.data == "true" else "AMBER_50"
        self.update()


class InputField(BaseView):
    def __init__(self, items):
        super().__init__()
        self.delete_items = []
        self.items = items
        # self.add_items = []
        self.containers = Column()
        # self.containers = Container()

        # 行削除ボタン
        self.ib_delete = IconButton(
            icons.DELETE_OUTLINE,
            icon_color=Colors.BLACK,
        )

        # 行追加ボタン
        self.eb_add = ElevatedButton(
            content=Container(Row([Icon(Icons.ADD), Text(value="行追加")])),
            on_click=lambda e: self.row_add_clicked(),
        )

        self.controls.append(
            Column(
                [
                    self.containers,
                    self.eb_add,
                ]
            )
        )

        self.container = []
        for row_items in self.items:
            self.row_items = Row()
            self.add_items = Row()
            for item in row_items:
                if item.__class__.__name__ == "Text":
                    print(eval(item.__str__().replace("text ", "")))
                    self.row_items.controls.append(
                        CustomText.create_self(
                            eval(item.__str__().replace("text ", ""))
                        )
                    )
                    self.add_items.controls.append(
                        CustomText.create_self(
                            eval(item.__str__().replace("text ", ""))
                        )
                    )
                    # self.add_items.controls.append(CustomText.create_self({'value': ''}))

                elif item.__class__.__name__ == "TextField":
                    print("len:", len(self.row_items.controls), self.row_items.controls)
                    print("item:", eval(item.__str__().replace("textfield ", "")))
                    self.row_items.controls.append(
                        CustomTextField.create_self(
                            eval(item.__str__().replace("textfield ", ""))
                        )
                    )
                    self.add_items.controls.append(
                        CustomTextField.create_self(
                            eval(item.__str__().replace("textfield ", ""))
                        )
                    )

            #         # elif item.__class__.__name__ == 'CustomTextField':
            #         #     # print('item:', item)
            #         #     self.row_items.controls.append(
            #         #         CustomTextField.create_self(eval(item.__str__().replace('textfield ', ''))))
            #
            self.row_items.controls.append(self.ib_delete)
            self.add_items.controls.append(self.ib_delete)
            #     # self.row_items.controls.append(self.id)
            #
            self.container.append(Container(content=self.row_items))
            self.ib_delete.on_click = lambda e: self.row_delete_clicked(
                self.container[len(self.container) - 1]
            )
        #     self.row_add_clicked()

        # self.containers.controls.append(self.container)
        self.containers.controls.append(self.row_items)
        # self.containers.controls.append(Row([TextField(label='氏', width=150, hint_text='name1'), TextField(label='名', data='name2', width=150)]))

        # self.row_add_clicked(self.containers)
        self.page.update()

    def row_add_clicked(self):
        # self.containers.content = self.container
        # self.controls[0].controls.insert(-1, self.container)
        # self.containers.controls.append(self.container)
        self.containers.controls.append(self.add_items)
        for container in self.containers.controls[-1].controls:
            try:
                print("container:", container.value)
                container.value = ""
            except:
                pass
        self.page.update()

    def row_delete_clicked(self, e):
        self.delete_items.append(e)
        self.containers.controls.remove(e)
        self.page.update()


class InputField2(BaseView):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.containers = []
        self.max_count = 0
        self.delete_items = []

        # 行追加ボタン
        self.b_row_add = ElevatedButton(
            content=Container(Row([Icon(Icons.ADD), Text(value="行追加")])),
            on_click=lambda e: self.InnerClass(self),
        )

        # # 行削除ボタン
        # self.ib_delete = IconButton(
        #     icons.DELETE_OUTLINE,
        #     icon_color=Colors.BLACK,
        #     on_click=lambda e: self.row_delete_clicked
        # )

        self.controls.append(Column())
        self.controls[0].controls.append(self.b_row_add)
        self.InnerClass(self)

    class InnerClass:
        # def __init__(self, outer_instance, b_row_add):
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            # if len(self.outer_instance.containers) != 0:
            #     self.outer_instance.max_count = self.outer_instance.max_count + 1
            self.id = Text(data=self.outer_instance.max_count)
            # self.row_items = Row()

            # 行削除ボタン
            self.ib_delete = IconButton(
                icons.DELETE_OUTLINE,
                icon_color=Colors.BLACK,
            )

            for items in self.outer_instance.items:
                self.row_items = Row()
                for item in items:
                    if item.__class__.__name__ == "Text":
                        print(item)
                        self.row_items.controls.append(
                            CustomText.create_self(
                                eval(item.__str__().replace("text ", ""))
                            )
                        )

                    elif item.__class__.__name__ == "TextField":
                        self.row_items.controls.append(
                            CustomTextField.create_self(
                                eval(item.__str__().replace("textfield ", ""))
                            )
                        )

                    # elif item.__class__.__name__ == 'CustomTextField':
                    #     # print('item:', item)
                    #     self.row_items.controls.append(
                    #         CustomTextField.create_self(eval(item.__str__().replace('textfield ', ''))))

                self.row_items.controls.append(self.ib_delete)
                self.row_items.controls.append(self.id)

                self.container = Container(content=self.row_items)
                self.ib_delete.on_click = lambda e: self.row_delete_clicked(
                    self.container
                )

                self.outer_instance.containers.append(self.container)
                self.outer_instance.controls[0].controls.insert(-1, self.container)

            self.outer_instance.page.update()

        def row_delete_clicked(self, e):
            self.outer_instance.delete_items.append(e)
            self.outer_instance.controls[0].controls.remove(e)
            self.outer_instance.page.update()


class SideBer(BaseView):
    def __init__(self):
        super().__init__()
        super().page.session.set("sideber", self)

        self.nav_rail = NavigationRail(
            selected_index=0,
            height=super().page.window.height,
            destinations=[
                NavigationRailDestination(
                    icon=Icons.ACCOUNT_BOX,
                    label_content=Text("顧客一覧", color=Colors.BLACK),
                    data="/home",
                ),
                NavigationRailDestination(
                    icon=Icons.EDIT_NOTE,
                    label_content=Text("手続き", color=Colors.BLACK),
                    data="/home/procedure",
                ),
                NavigationRailDestination(
                    icon=Icons.LABEL,
                    label_content=Text("ラベル印刷", color=Colors.BLACK),
                    data="/labelprint",
                ),
                NavigationRailDestination(
                    icon=Icons.SETTINGS,
                    label_content=Text("設定", color=Colors.BLACK),
                    data="/settings",
                ),
            ],
            bgcolor=Colors.AMBER_50,
            on_change=lambda e: super().controller.go_page(
                self.nav_rail.destinations[self.nav_rail.selected_index].data
            ),
        )

        self.controls = [Column(controls=[self.nav_rail])]
        # self.controls = Column([self.nav_rail])
        # self.content = Row(
        #     controls=[
        #         self.nav_rail,
        #     ],
        #     expand=True,
        #     vertical_alignment=CrossAxisAlignment.START,
        # )


class MyLayout(BaseView):
    def __init__(self, page: Page = None, controller=None):
        super().__init__()
        BaseView.page = page
        BaseView.controller = controller
        page.title = "遺言・相続手続きシステム"
        page.bgcolor = Colors.AMBER_50
        page.window.top = 0
        page.window.left = 0
        page.window.height = pyautogui.size().height
        page.window.width = pyautogui.size().width
        page.scrollTo = "always"
        page.scroll = "always"

        # スナックバー (メッセージ表示用)
        super().page.snack_bar = SnackBar(content=Text(""), open=False)

        self.past_route = []
        page.session.set("past_route", self.past_route)

        page.session.set('/customer_registration', CustomerRegistration())

        self.eb_home = Container(
            content=ElevatedButton(
                "ホームへ",
                icon=Icons.HOME,
                visible=False,
                on_click=controller.home_clicked,
            ),
            margin=5,
        )
        page.session.set("eb_home", self.eb_home)

        self.eb_return = Container(
            content=ElevatedButton(
                "戻る",
                icon=Icons.ARROW_BACK,
                visible=False,
                on_click=controller.return_clicked,
            ),
            margin=5,
        )
        page.session.set("eb_return", self.eb_return)

        # self.main_body = Container(content=HomeBody())
        self.page.session.set('/home', HomeBody())
        self.main_body = Container(
            content=self.page.session.get('home'),
            expand=True,  # 残りのスペースを埋める
        )
        page.session.set("main_body", self.main_body)

        self.controls = [
            Column([
                Row([self.page.session.get('eb_home'),self.page.session.get('eb_return'),]),
                self.main_body
            ])
        ]

    # def show_message(self, message: str, color=Colors.GREEN_500):
    #     """スナックバーにメッセージを表示します。"""
    #     self._page.snack_bar.content = Text(message)
    #     self._page.snack_bar.bgcolor = color
    #     self._page.snack_bar.open = True
    #     self._page.update()


class HomeBody(BaseView):
    def __init__(self):
        super().__init__()
        # self.home_tab = TabSearch(super().page.snack_bar)
        self.home_tab = TabSearch()

        self.controls = [
            Tabs(
                selected_index=0,
                animation_duration=300,
                label_color=Colors.BLACK,
                divider_color=Colors.BLACK,
                unselected_label_color=Colors.BLACK,
                indicator_color=Colors.RED,
                tabs=[
                    Tab(
                        text="顧客情報",
                        icon=Icons.PEOPLE,
                        content=self.home_tab,
                    ),
                    Tab(
                        text="設定",
                        icon=Icons.SETTINGS,
                        # content=self.settings_tab,
                    ),
                ],
            )
        ]


class HeirsTab(BaseView):
    def __init__(self):
        super().__init__()
        super().page.session.set("/heirs_tab", self)

        self.tb_name1 = CustomTextField(label='姓', autofocus=True)
        self.tb_name2 = CustomTextField(label='名')
        self.tb_name1_huri = CustomTextField(label='姓ふりがな')
        self.tb_name2_huri = CustomTextField(label='名ふりがな')

        self.controls = [
            Container(
                content=Column(
                    controls=[
                        Row([self.tb_name1, self.tb_name2,]),
                        Row([self.tb_name1_huri, self.tb_name2_huri,]),
                    ]
                ),
                padding=10,
                margin=10,
                # border_radius=10,
                # border=border.all(1, Colors.BLACK),
            )
        ]


class Registration(BaseView):
    def __init__(self,
                 # show_message_callback,
                 tb_name1=None,
                 tb_name2=None,
                 tb_name1_huri=None,
                 tb_name2_huri=None,
                 tb_zipcode=None,
                 tb_address1=None,
                 tb_address2=None,
                 tb_address3=None,
                 tb_address4=None,
                 tb_building=None,
                 birthday=None,
                 deathday=None,
                 tb_code=None,
                 dd_code=None,
                 card1=None,
                 card2=None,
                 b_delete=None
                 ):
        super().__init__()
        # self.show_message_callback = show_message_callback
        # super().page.snack_bar = SnackBar(content=Text(""), open=False)

        self.tb_name1 = CustomTextField(label='姓', autofocus=True)
        self.tb_name2 = CustomTextField(label='名')
        self.tb_name1_huri = CustomTextField(label='姓ふりがな')
        self.tb_name2_huri = CustomTextField(label='名ふりがな')
        self.birthday = CustomTextField(label='生年月日', hint_text='1900/1/1', width=120,
                                        on_blur=lambda e: utils.convert_seireki(self.birthday.value, e))
        self.deathday = CustomTextField(label='死亡日', hint_text='1900/1/1', width=120,
                                        on_blur=lambda e: utils.convert_seireki(self.deathday.value, e))
        self.tb_zipcode = CustomTextField(label='郵便番号', hint_text='194-0022', width=120,)
                                          # on_blur=self.zipcode_change)
        self.tb_address1 = CustomTextField(label='都道府県', hint_text='東京都', width=150)
        self.tb_address2 = CustomTextField(label='市区町村', hint_text='中央区', width=150)
        self.tb_address3 = CustomTextField(label='町域名', hint_text='八重洲', width=150)
        self.tb_address4 = CustomTextField(label='番地', hint_text='1-7-20', width=280)
        self.tb_building = CustomTextField(label='建物名', hint_text='八重洲口会館2階', width=889)
        self.note = CustomTextField(label='備考', width=500, multiline=True)
        self.tb_code = CustomTextField(label='コード', hint_text='G0000')
        # self.dd_code = DropdownM2(label='コード・氏名選択', on_change=self.change_dd_code)
        self.dd_code = DropdownM2(label='コード・氏名選択',)
        # self.set_dd_code()
        # self.b_delete = ElevatedButton(
        #     content=Container(
        #         content=Row(
        #             controls=[
        #                 Icon(Icons.DELETE),
        #                 Text(value="顧客削除", size=20),
        #             ]
        #         )
        #     ),
        #     height=50,
        #     # on_click=self.delete_clicked
        # )
        self.b_delete = CustomElevatedButton(icon=Icons.DELETE, text_value='顧客削除')
        self.b_Registration = CustomElevatedButton(text_value="登録", icon=Icons.SAVE,
                                                   on_click=self.controller.customer_registration)

    def change_date(self, e):
        if e.control.data == 'birthday':
            self.birthday.value = str(e.control.value)[:10].replace('-', '/')
        elif e.control.data == 'deathday':
            self.deathday.value = str(e.control.value)[:10].replace('-', '/')
        self.body.update()


class CustomerRegistration(Registration):
    def __init__(self,
                 tb_name1=None,
                 tb_name2=None,
                 tb_name1_huri=None,
                 tb_name2_huri=None,
                 tb_zipcode=None,
                 tb_address1=None,
                 tb_address2=None,
                 tb_address3=None,
                 tb_address4=None,
                 tb_building=None,
                 birthday=None,
                 deathday=None,
                 tb_code=None,
                 dd_code=None,
                 card1=None,
                 card2=None,
                 b_delete=None
                 ):
        super().__init__()
        super().page.session.set("/customer_registration", self)

        self.tb_domicile = CustomTextField(label='本籍', width=700)
        self.b_address_copy = CustomElevatedButton(icon=Icons.COPY, text_value='住所をコピー')
        self.old_address1 = CustomTextField(label='旧住所1', width=889)
        self.old_address2 = CustomTextField(label='旧住所2', width=889)
        self.old_address3 = CustomTextField(label='旧住所3', width=889)
        self.folder = CustomTextField(label='フォルダーパス', width=889)

        self.dd_will = CustomDropdown(label='遺言書有無', width=130, options=[dropdown.Option('有'), dropdown.Option('無')])

        # 手続きステータス
        self.dd_progress = CustomDropdown(
            label="状況",
            options=[
                dropdown.Option("見積中"),
                dropdown.Option("契約待ち"),
                dropdown.Option("戸籍収集"),
                dropdown.Option("法定相続情報作成"),
                dropdown.Option("残高証明書"),
                dropdown.Option("金融機関手続き"),
                dropdown.Option("財産評価"),
                dropdown.Option("分割協議書"),
                dropdown.Option("登記"),
                dropdown.Option("完了書類作成"),
                dropdown.Option("入金待ち"),
                dropdown.Option("手続終了"),
                dropdown.Option("キャンセル"),
            ],
            data="decedent",
            # on_change=self.controller.contractor_change,
        )

        # print('self.b_Registration1:', self.b_Registration.data)
        # self.b_Registration.data = "decedent"
        self.b_Registration.data = "/customer_registration"
        # print('self.b_Registration2:', self.b_Registration.data)

        # self.tb_code = CustomTextField(label='コード', hint_text='E00200', width=200)
        # self.dd_code = DropdownM2(label='コード・氏名選択', width=200)
        # # self.dd_code = DropdownM2(label='コード・氏名選択', width=200, on_change=self.change_dd_code)
        # # self.set_dd_code()

        self.customer = Column(
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Row([self.tb_code, self.dd_code, self.b_delete,]),
                            Row([self.tb_name1, self.tb_name2,]),
                            Row([self.tb_name1_huri, self.tb_name2_huri,]),
                            Row([self.birthday, self.deathday,]),
                            Row([self.tb_zipcode, self.tb_address1, self.tb_address2, self.tb_address3, self.tb_address4]),
                            Row([self.tb_building]),
                            Row([self.tb_domicile, self.b_address_copy]),
                            self.old_address1,
                            self.old_address2,
                            self.old_address3,
                            self.folder,
                            # self.folder_a_path,
                            # self.folder_s_path,
                            Row([self.dd_will, self.dd_progress]),
                            self.note,
                            Row([self.b_Registration]),
                            # ElevatedButton("登録", icon=Icons.SAVE),
                            # ElevatedButton("登録", icon=Icons.SAVE, on_click=self.registration),
                        ],
                    ),
                    padding=10,
                    margin=10,
                    # border_radius=10,
                    # border=border.all(1, Colors.BLACK),
                )
            ]
        )

        self.deceased_tab = Tab(
            text="被相続人",
            content=self.customer,
            # content=Column(
            #     [
            #         Text("被相続人の情報", size=18),
            #         TextField(label="氏名"),
            #         TextField(label="死亡年月日"),
            #     ]
            # ),
        )

        # 動的に追加される相続人タブを格納するリスト
        self.heirs_tabs = []

        self.add_tab_button = Tab(text="相続人を追加",)
            # on_change=self.add_heir_tab,
            # content=ElevatedButton(text="相続人を追加", on_click=self.add_heir_tab),
        # )

        self.my_tab = Tabs(
            tabs=[],
            expand=1,
            animation_duration=300,
            label_color=Colors.BLACK,
            divider_color=Colors.BLACK,
            unselected_label_color=Colors.BLACK,
            indicator_color=Colors.RED,
            on_change=self.add_heir_tab,
            # on_change=self.tabs_changed,
        )

        self.controls = [
            self.my_tab
        ]

        # 初期表示時にタブを構築
        self.rebuild_tabs()

    def rebuild_tabs(self):
        print('rebuild_tabs')
        # 固定タブと動的タブを結合して、新しいリストを作成
        fixed_tabs = [
            self.deceased_tab,
            Tab(
                text="代表相続人",
                content=RegistrationHeir(),
                # content=Column([TextField(label="氏名"), TextField(label="続柄")]),
            ),
        ]

        # 新しいタブリストを作成し、Tabsに設定
        self.my_tab.tabs = fixed_tabs + self.heirs_tabs + [self.add_tab_button]
        super().page.update()

    def add_heir_tab(self, e):
        current_tab_index = e.control.selected_index
        print(f"タブが切り替わりました。現在のインデックス: {current_tab_index}")
        print(f"選択されたタブのテキスト: {e.control.tabs[current_tab_index].text}")
        if e.control.tabs[current_tab_index].text == '相続人を追加':
            # self.new_heir_tab_content = HeirsTab()
            # self.new_heir_tab_content = RegistrationHeir(),
            new_tab = Tab(
                text=f"相続人 {current_tab_index - 1}",
                # content=HeirsTab(),
                content=RegistrationHeir()
            )
            self.heirs_tabs.append(new_tab)
            self.rebuild_tabs()

            self.my_tab.selected_index = len(self.my_tab.tabs) - 1
            super().page.update()

            sleep(.1)
            self.my_tab.selected_index = len(self.my_tab.tabs) - 2  # 追加タブは除く
            super().page.update()

    def tabs_changed(self, e):
        current_tab_index = e.control.selected_index
        print(f"タブが切り替わりました。現在のインデックス: {current_tab_index}")
        print(f"選択されたタブのテキスト: {e.control.tabs[current_tab_index].text}")
        if e.control.tabs[current_tab_index].text == '相続人を追加':
            # HeirsTabクラスのインスタンスを生成
            # new_heir_tab_content = HeirsTab()

            # ft.Tabコンポーネントを作成し、contentにクラスインスタンスを渡す
            new_tab = Tab(
                text=f"相続人 {current_tab_index}",
                content=HeirsTab(),
                # content=new_heir_tab_content,
            )

            # タブのリストに追加
            self.my_tab.tabs.append(new_tab)

            # self.my_tab.tabs.append(Tab(text=f"相続人を追加"))
            # super().page.update()

            # self.my_tab.tabs[current_tab_index].text = f'相続人{current_tab_index - 2}'
            # self.my_tab.tabs[current_tab_index].icon = Icons.PEOPLE
            # # self.my_tab.tabs.append(Tab(text=f"相続人を追加", icon=Icons.CREATE))
            # print('e.control.selected_index:', e.control.selected_index)
            # self.my_tab.tabs.append(HeirInformation())
            # print('e.control.selected_index:', e.control.selected_index)
            # # self.my_tab.tabs.append(self.new_tab)
            # self.my_tab.selected_index = len(self.my_tab.tabs) - 1
            # e.control.selected_index = len(self.my_tab.tabs) - 2
            super().page.update()


        # self.controls = [
        #     Row([
        #         self.tb_code, self.dd_code, self.b_delete,
        #     ]),
        #     Row([
        #         self.tb_name1, self.tb_name2,
        #     ]),
        #     Row([
        #         self.tb_name1_huri, self.tb_name2_huri,
        #     ]),
        #     Row([
        #         self.birthday, self.deathday,
        #     ]),
        #     Row([
        #         self.tb_zipcode, self.tb_address1, self.tb_address2, self.tb_address3, self.tb_address4
        #     ]),
        #     Row([
        #         self.tb_building
        #     ]),
        #     # Row([self.tb_domicile, self.b_address_copy]),
        #     # self.old_address1,
        #     # self.old_address2,
        #     # self.old_address3,
        #     # self.folder_a_path,
        #     # self.folder_s_path,
        #     # Row([self.dd_will, self.dd_responsible_person, self.dd_progress]),
        #     self.note,
        #     ElevatedButton("登録", icon=Icons.SAVE),
        #     # ElevatedButton("登録", icon=Icons.SAVE, on_click=self.registration),
        # ]

    # def change_date(self, e):
    #     if e.control.data == 'birthday':
    #         self.birthday.value = str(e.control.value)[:10].replace('-', '/')
    #     elif e.control.data == 'deathday':
    #         self.deathday.value = str(e.control.value)[:10].replace('-', '/')
    #     self.body.update()
    #
    # def date_picker_dismissed(self, e):
    #     print('date_picker_dismissed', e)
    #     # print(f"Date picker dismissed, value is {self.date_picker_birthday.value}")
    #
    # def clicked(self, e):
    #     pass
    #
    def set_dd_code(self):
        pass
    #     sql = 'SELECT code, username1 || " " || username2 FROM customer ORDER BY code DESC'
    #     record = GlobalValues.get_db(sql)
    #     # print('record: ', record)
    #     self.dd_code.options.append(dropdown.Option("-"))
    #     [self.dd_code.options.append(dropdown.Option(f'{i[0]} {i[1]}')) for i in record]
    #
    def change_dd_code(self, e):
        pass

    def zipcode_change(self, e):
        self.tb_address4.focus()
        self.update()
        zipcode_address = utils.zipcode_to_address(e.control.value)
        if zipcode_address:
            self.tb_address1.value = zipcode_address[0]
            self.tb_address2.value = zipcode_address[1]
            self.tb_address3.value = zipcode_address[2]
        else:
            self.tb_address1.value = ''
            self.tb_address2.value = ''
            self.tb_address3.value = ''
        self.update()

        # ret = MessageForefront('顧客削除', f'{self.tb_name1.value}　{self.tb_name2.value}の情報をデータベースから削除しますが良いでしょうか？', 'okcancel')
        # if ret:
        #     sql = 'delete from customer where code = ?'
        #     GlobalValues.set_db(sql, tuple([self.tb_code.value]))
        #     messagebox.showinfo('顧客削除', '削除が完了しました。')
        #     [self.body.controls.pop() for _ in range(len(self.body.controls))]
        #     self.body.controls.append(RegistrationCustomer())
        #     self.body.update()


class RegistrationHeir(Registration):
    def __init__(self,
                 heir_id=None,
                 # tb_name1=None,
                 # tb_name2=None,
                 # tb_name1_huri=None,
                 # tb_name2_huri=None,
                 # tb_zipcode=None,
                 # tb_address1=None,
                 # tb_address2=None,
                 # tb_address3=None,
                 # tb_address4=None,
                 # tb_building=None,
                 # birthday=None,
                 # deathday=None,
                 # tb_code=None,
                 # dd_code=None
                 ):
        super().__init__(
            # tb_name1,
            # tb_name2,
            # tb_name1_huri,
            # tb_name2_huri,
            # tb_zipcode,
            # tb_address1,
            # tb_address2,
            # tb_address3,
            # tb_address4,
            # tb_building,
            # birthday,
            # deathday,
            # tb_code,
            # dd_code
        ),
        self.info = CustomText('＜相続人　登録・修正＞', size=24)
        self.tb_code.label = '被相続人コード'
        self.dd_code.label = '被相続人選択'
        self.tf_heir_id = CustomTextField(label='相続人コード', hint_text='新規登録は空欄',)
                                          # on_blur=self.change_tf_heir_id)
        self.tf_heir_id.value = heir_id
        # print('self.tf_heir_id.value:', self.tf_heir_id.value)
        self.dd_heir_id = DropdownM2(label='相続人氏名選択')
        # self.dd_heir_id = DropdownM2(label='相続人氏名選択', on_change=self.change_dd_heir_id)
        # self.ch_offer = Checkbox(label='依頼人')
        # self.ch_transfer = Checkbox(label='振込者')
        self.legal_heir = CustomText('相続人チェック', visible=False)
        # self.inheritance_form = CustomText(visible=False)
        self.contact_home = CustomTextField(label='連絡先(自宅) ※ハイフンあり')
        self.contact_phone = CustomTextField(label='連絡先(携帯) ※ハイフンあり')
        self.mail = CustomTextField(label='連絡先(メール)', width=899)
        self.relationship = CustomDropdown(
            label='続柄',
            width=130,
            options=[
                dropdown.Option('妻'),
                dropdown.Option('夫'),
                dropdown.Option('父'),
                dropdown.Option('母'),
                dropdown.Option('長男'),
                dropdown.Option('長女'),
                dropdown.Option('二男'),
                dropdown.Option('二女'),
                dropdown.Option('三男'),
                dropdown.Option('三女'),
                dropdown.Option('四男'),
                dropdown.Option('四女'),
                dropdown.Option('五男'),
                dropdown.Option('五女'),
                dropdown.Option('兄弟1'),
                dropdown.Option('姉妹1'),
                dropdown.Option('兄弟2'),
                dropdown.Option('姉妹2'),
                dropdown.Option('兄弟3'),
                dropdown.Option('姉妹3'),
                dropdown.Option('兄弟4'),
                dropdown.Option('姉妹4'),
                dropdown.Option('兄弟5'),
                dropdown.Option('姉妹5'),
                dropdown.Option('孫'),
                dropdown.Option('甥'),
                dropdown.Option('姪'),
                dropdown.Option('養子'),
                dropdown.Option('義兄'),
                dropdown.Option('義弟'),
                dropdown.Option('義姉'),
                dropdown.Option('義妹'),
                dropdown.Option('祖父_父'),
                dropdown.Option('祖父_母'),
                dropdown.Option('祖母_父'),
                dropdown.Option('祖母_母'),
                dropdown.Option('元夫'),
                dropdown.Option('元妻'),
                dropdown.Option('元妻の子'),
                dropdown.Option('父の元妻'),
                dropdown.Option('母の元夫'),
                dropdown.Option('子の夫'),
                dropdown.Option('子の妻'),
            ],
            # on_change=self.change_relationship
        )

        self.relationship2 = CustomDropdown(
            label='親の続柄',
            width=130,
            options=[
                dropdown.Option('父'),
                dropdown.Option('母'),
                dropdown.Option('長男'),
                dropdown.Option('長女'),
                dropdown.Option('二男'),
                dropdown.Option('二女'),
                dropdown.Option('三男'),
                dropdown.Option('三女'),
                dropdown.Option('四男'),
                dropdown.Option('四女'),
                dropdown.Option('五男'),
                dropdown.Option('五女'),
                dropdown.Option('兄弟1'),
                dropdown.Option('姉妹1'),
                dropdown.Option('兄弟2'),
                dropdown.Option('姉妹2'),
                dropdown.Option('兄弟3'),
                dropdown.Option('姉妹3'),
                dropdown.Option('兄弟4'),
                dropdown.Option('姉妹4'),
                dropdown.Option('兄弟5'),
                dropdown.Option('姉妹5'),
            ],
            visible=False
        )

        self.situation = CustomDropdown(
            label='状態',
            width=130,
            options=[
                dropdown.Option(' '),
                dropdown.Option('死亡'),
                dropdown.Option('海外居住'),
                dropdown.Option('相続放棄'),
                dropdown.Option('成年被後見人'),
                dropdown.Option('相続人外')
            ],
            value=' ',
        )
        self.note = CustomTextField(label='内容', width=769, multiline=True)
        self.updated_date = CustomTextField(label='更新日', hint_text='1900/1/1', width=120,
                                            on_blur=lambda e: utils.convert_seireki(self.updated_date.value, e))

        self.controls =[
            Row([self.info,]),
            Row([self.tb_code, self.dd_code, self.b_delete, self.legal_heir,]),
            # Row([self.tb_code, self.dd_code, self.b_delete, self.legal_heir, self.inheritance_form]),
            # Row([self.tf_heir_id, self.dd_heir_id]),
            Row([self.tb_name1, self.tb_name2]),
            # Row([self.tb_name1, self.tb_name2, self.ch_offer, self.ch_transfer]),
            Row([self.tb_name1_huri, self.tb_name2_huri,]),
            Row([self.relationship, self.relationship2, self.situation,]),
            Row([self.contact_home, self.contact_phone,]),
            Row([self.mail,]),
            Row([self.birthday, self.deathday,]),
            Row([self.tb_zipcode, self.tb_address1, self.tb_address2, self.tb_address3, self.tb_address4]),
            Row([self.tb_building]),
            Row([self.updated_date, self.note]),
            Row([CustomElevatedButton(text_value="登録", icon=Icons.SAVE, on_click=self.controller.customer_registration)]),
        ]

        
class ProcedureView(BaseView):
    def __init__(self):
        super().__init__()

        self.b_heir = CustomContainerButton(
            text_value="相続人登録", icon=Icons.PERSON_ADD
        )
        # self.b_heir.content.controls[1].value = '相続人登録'
        # self.b_heir.content.controls[0].content = Icon(Icons.PERSON_ADD, size=45)

        self.controls = [
            Text(value="＜手続き＞"),
            Container(
                content=Column(
                    controls=[
                        Text("◯ 契約後の手続き", size=20, color=Colors.BLACK),
                        self.b_heir,
                    ]
                )
            ),
        ]


class TabSearch(BaseView):
    # def __init__(self, show_message_callback):
    def __init__(self):
        super().__init__()
        # self.show_message_callback = show_message_callback
        self.spacing = 20
        super().page.session.set("/home", self)

        # self.info = Text('＜顧客情報＞', size=24)

        # 検索した結果の数
        self.result_count = Text(value="", color=Colors.BLACK)

        # 被相続人　かなフィールド
        self.customer_name_kana_input = CustomTextField(
            label="被相続人：姓かな",
            # width=200,
            autofocus=True,
            data="decedent",
            on_change=self.controller.search_change,
        )

        # 被相続人　姓フィールド
        self.customer_name_input = CustomTextField(
            label="被相続人：姓",
            data="decedent",
            on_change=self.controller.search_change,
        )

        # 手続きステータス
        self.dd_progress = CustomDropdown(
            label="状況",
            options=[
                dropdown.Option("見積中"),
                dropdown.Option("契約待ち"),
                dropdown.Option("戸籍収集"),
                dropdown.Option("法定相続情報作成"),
                dropdown.Option("残高証明書"),
                dropdown.Option("金融機関手続き"),
                dropdown.Option("財産評価"),
                dropdown.Option("分割協議書"),
                dropdown.Option("登記"),
                dropdown.Option("完了書類作成"),
                dropdown.Option("入金待ち"),
                dropdown.Option("手続終了"),
                dropdown.Option("キャンセル"),
            ],
            # width=200,
            data="decedent",
            on_change=self.controller.contractor_change,
        )

        # 備考
        self.note = CustomTextField(
            label="備考",
            data="decedent",
            on_change=self.controller.search_change,
        )

        # 相続人　かなフィールド
        self.heir_name_kana_input = CustomTextField(
            label="依頼人：姓かな",
            data="heir",
            on_change=self.controller.search_change,
        )

        # 相続人　性フィールド
        self.heir_name_input = CustomTextField(
            label="依頼人：姓",
            data="heir",
            on_change=self.controller.search_change,
        )

        # 相続人　電話番号フィールド
        self.heir_tel_input = CustomTextField(
            label="電話番号",
            data="heir",
            on_change=self.controller.search_change,
        )

        # クリアボタン
        self.clear_bt = OutlinedButton(
            icon=Icons.CLEAR,
            text="クリア(C)",
            style=ButtonStyle(color=Colors.BLACK),
            # style=ButtonStyle(text_style=(TextStyle(size=20))),
            # color=Colors.BLACK,
            # height=40,
            # bgcolor=Colors.BLUE_200,
            on_click=self.controller.clear_click,
        )

        # 手続き中のチェックボックス
        self.ch_contractor = Checkbox(
            label="手続き中",
            value=True,
            label_style=TextStyle(color=Colors.BLACK, size=18),
            data="decedent",
            on_change=self.controller.search_change,
        )

        self.search_fields = Container(
            content=Column(
                [
                    Row(
                        [
                            self.customer_name_kana_input,
                            self.customer_name_input,
                            self.dd_progress,
                            self.note
                        ]
                    ),
                    Row(
                        [
                            self.heir_name_kana_input,
                            self.heir_name_input,
                            self.heir_tel_input,
                        ]
                    ),
                    Row(
                        [
                            self.clear_bt,
                            self.ch_contractor
                        ]
                    )
                ]
            ),
            padding=10,
            margin=10,
            border_radius=10,
            border=border.all(1, Colors.BLACK),
        )

        self.dt_decedent = DataTable(
            [
                DataColumn(
                    Text("選択"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("Code"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("状況"), heading_row_alignment=MainAxisAlignment.START
                ),
                DataColumn(
                    Text("フォルダ"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("被相続人"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("依頼人"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("更新日"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("内容"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("自宅電話番号"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("携帯電話番号"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("備考"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
            ],
            data_text_style=TextStyle(color=Colors.BLACK),
            heading_text_style=TextStyle(color=Colors.WHITE),
            heading_row_color=Colors.BLUE_GREY_300,
        )

        results = self.controller.get_result_view_all(page=super().page)
        self.customer_data_table(results)

        self.controls = [
            # self.info,
            self.search_fields,
            Row(
                [
                    ElevatedButton(
                        icon=Icons.CREATE,
                        text="新規顧客登録",
                        color=Colors.BLACK,
                        bgcolor=Colors.BLUE_200,
                        on_click=lambda e: self.page.go('/customer_registration')
                    ),
                    # ElevatedButton(
                    #     icon=Icons.CREATE,
                    #     text="相続人 新規登録",
                    #     color=Colors.BLACK,
                    #     bgcolor=Colors.BLUE_200,
                    # ),
                    self.result_count,
                ]
            ),
            self.dt_decedent,
        ]

    def customer_data_table(self, results):
        # print()
        # print('customer_data_table:', results)
        self.dt_decedent.rows = []
        if results:
            for result in results:
                self.dt_decedent.rows.append(
                    DataRow(
                        [
                            DataCell(Icon(Icons.TOUCH_APP)),
                            # DataCell(Icon(Icons.TOUCH_APP, color=Colors.BLACK)),
                            DataCell(
                                Container(
                                    Text(result["code"], size=11), alignment=alignment.center
                                ),
                                data=result["code"],
                                on_tap=lambda e: pyperclip.copy(e.control.data),
                            ),
                            DataCell(
                                Container(
                                    Text(result["状況"], size=11),
                                    alignment=alignment.center_left,
                                    width=60,
                                )
                            ),
                            # DataCell(
                            #     Container(
                            #         Icon(Icons.PERSON_SEARCH_SHARP),
                            #         alignment=alignment.center,
                            #     )
                            # ),
                            DataCell(
                                Container(
                                    Icon(Icons.FOLDER), alignment=alignment.center
                                ),
                                data=result["フォルダ"],
                                on_tap=self.folder_open
                            ),
                            DataCell(
                                Container(
                                    Text(result["被相続人"]),
                                    alignment=alignment.center_left,
                                    width=80
                                ),
                                data=result["被相続人"],
                                on_tap=lambda e: pyperclip.copy(e.control.data),
                            ),
                            DataCell(
                                Container(
                                    Text(result["依頼人"]),
                                    alignment=alignment.center_left,
                                    width=80
                                ),
                                data=result["依頼人"],
                                on_tap=lambda e: pyperclip.copy(e.control.data),
                            ),
                            DataCell(
                                Container(
                                    Text(result["更新日"], size=11), alignment=alignment.center
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["内容"], size=11, tooltip=result['内容']),
                                    alignment=alignment.center_left,
                                )
                            ),
                            # DataCell(Container(Text(result['内容']), alignment=alignment.center_left, width=300)),
                            DataCell(
                                Container(
                                    Text(result["自宅電話番号"], size=11),
                                    alignment=alignment.center,
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["携帯電話番号"], size=11),
                                    alignment=alignment.center,
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["備考"], size=11, tooltip=result["備考"]),
                                    alignment=alignment.center_left,
                                    # width=200
                                )
                            ),
                        ]
                    )
                )
        self.result_count.value = "検索数：" + str(len(results)) + "件"
        super().page.update()

    def folder_open(self, e):
        folder = e.control.data.replace('/', '\\')
        print('folder:', folder)
        subprocess.Popen(["explorer", "/root,", folder], shell=True)
        # if os.name == 'nt':
        #     print('nt folder_open')
        #     subprocess.Popen(["explorer", "/root,", folder], shell=True)
        # else:
        #     print('posix folder_open')
        #     folder = '/Users/laksumi/Library/CloudStorage/OneDrive-株式会社プロフィット・ワン/' + folder[folder.find('General'):]
        #     folder = folder.replace('\\', '/')
        #     subprocess.call(['open', folder])


class TabBank(BaseView):
    def __init__(self, show_message_callback):
        super().__init__()
        self.show_message_callback = show_message_callback
        self.spacing = 20