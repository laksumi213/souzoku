import asyncio

# from typing import Dict, Any
import pyautogui
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
    Divider,
    Dropdown,
    ElevatedButton,
    Icon,
    IconButton,
    MainAxisAlignment,
    NavigationRail,
    NavigationRailDestination,
    Page,
    Row,
    Text,
    TextAlign,
    TextField,
    TextStyle,
    VerticalDivider,
    alignment,
    border,
    colors,
    dropdown,
    icons,
)

import app.utils as utils


class BaseView(Row):
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
        self.color = colors.BLACK

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
        label_style=TextStyle(color=colors.BLACK),
        # hint_text: str = "",
        color=colors.BLACK,
        focused_border_color=colors.CYAN,
        password: bool = False,
        on_change=None,
        on_focus=None,
        on_blur=None,
        format=None,
        hinttext=None,
        *args,
        **kwargs,
    ):
        super().__init__(
            label=label,
            label_style=label_style,
            color=color,
            focused_border_color=focused_border_color,
            password=password,
            on_change=self._on_change,
            on_focus=self._on_focus,
            on_blur=self._on_blur,
            *args,
            **kwargs,
        )
        self._on_change_callback = on_change
        self._on_focus = on_focus
        self._on_blur = on_blur
        self.hint_text = hinttext
        self.format = format
        # self.label_style = TextStyle(color=colors.BLACK)
        # self.color = colors.BLACK
        # self.focused_border_color = colors.CYAN

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

    def _on_blur(self, e):
        if self.format == "number":
            self.number_format(e)

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
        label_style=TextStyle(color=colors.WHITE),
        width=150,
        color=colors.WHITE,
        border_color=colors.WHITE,
        focused_border_color=colors.CYAN,
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
        border=border.all(2, colors.with_opacity(0.0, colors.CYAN)),
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
                    border=border.all(2, colors.BLACK),
                    padding=10,
                    on_hover=self._on_hover,
                ),
                Text(
                    value=self.text_value,
                    size=14,
                    text_align=TextAlign.CENTER,
                    color=colors.BLACK,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

    def _on_hover(self, e):
        e.control.bgcolor = "GREY" if e.data == "true" else "AMBER_50"
        self.update()


class CustomDropdown(Dropdown):
    def __init__(
        self,
        color=colors.BLACK,
        bgcolor=colors.AMBER_50,
        text_style=TextStyle(color=colors.BLACK),
        label_style=TextStyle(color=colors.BLACK),
        focused_color=colors.BLACK,
        focused_border_color=colors.CYAN,
        *args,
        **kwargs,
    ):
        super().__init__(
            color=color,
            bgcolor=bgcolor,
            text_style=text_style,
            label_style=label_style,
            focused_color=focused_color,
            focused_border_color=focused_border_color,
            *args,
            **kwargs,
        )

    def add_options(self, data):
        self.options = None
        for item in data:
            self.options.append(dropdown.Option(*item.values()))


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
            icon_color=colors.BLACK,
        )

        # 行追加ボタン
        self.eb_add = ElevatedButton(
            content=Container(Row([Icon(icons.ADD), Text(value="行追加")])),
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
            content=Container(Row([Icon(icons.ADD), Text(value="行追加")])),
            on_click=lambda e: self.InnerClass(self),
        )

        # # 行削除ボタン
        # self.ib_delete = IconButton(
        #     icons.DELETE_OUTLINE,
        #     icon_color=colors.BLACK,
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
                icon_color=colors.BLACK,
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
                    icon=icons.ACCOUNT_BOX,
                    label_content=Text("顧客一覧", color=colors.BLACK),
                    data="/home",
                ),
                NavigationRailDestination(
                    icon=icons.EDIT_NOTE,
                    label_content=Text("手続き", color=colors.BLACK),
                    data="/home/procedure",
                ),
                NavigationRailDestination(
                    icon=icons.LABEL,
                    label_content=Text("ラベル印刷", color=colors.BLACK),
                    data="/labelprint",
                ),
                NavigationRailDestination(
                    icon=icons.SETTINGS,
                    label_content=Text("設定", color=colors.BLACK),
                    data="/settings",
                ),
            ],
            bgcolor=colors.AMBER_50,
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
        page.bgcolor = colors.AMBER_50
        page.window.top = 0
        page.window.left = 0
        page.window.height = pyautogui.size().height
        page.window.width = pyautogui.size().width
        page.scrollTo = "always"
        page.scroll = "always"

        self.past_route = []
        page.session.set("past_route", self.past_route)

        self.eb_return = Container(
            content=ElevatedButton(
                "戻る",
                icon=icons.ARROW_BACK,
                visible=False,
                on_click=controller.return_clicked,
            ),
            margin=5,
        )
        page.session.set("eb_return", self.eb_return)

        main_body = Container(content=HomeView())
        page.session.set("main_body", main_body)

        self.controls = [
            # Container(SideBer()),
            # Container(height=800, content=VerticalDivider(thickness=1, color=colors.BLACK)),
            # Container(
            #     height=page.window.height,
            #     content=VerticalDivider(thickness=1, color=colors.BLACK),
            # ),
            Container(
                Column(
                    [
                        self.eb_return,
                        main_body,
                    ]
                )
            ),
        ]

        # サイドバーのselected_indexを保存
        # self.past_selected_index = {
        #     page.session.get("sideber")
        #     .nav_rail.destinations[page.session.get("sideber").nav_rail.selected_index]
        #     .data: page.session.get("sideber")
        #     .nav_rail.selected_index
        # }
        # page.session.set("past_selected_index", self.past_selected_index)
        #
        # # サイドバーのボタンを押したときの動きを登録
        # page.session.get("sideber").nav_rail.on_change = lambda e: page.go(
        #     page.session.get("sideber")
        #     .nav_rail.destinations[page.session.get("sideber").nav_rail.selected_index]
        #     .data
        # )


class HomeView(BaseView):
    def __init__(self):
        super().__init__()
        super().page.session.set("/home", self)

        self.ch_contractor = Checkbox(
            label="手続き中",
            value=True,
            label_style=TextStyle(color=colors.BLACK, size=18),
            data="decedent",
            on_change=self.controller.search_change,
        )

        # self.ch_me_rep_person = Checkbox(label='自分の担当者', value=True,
        #                                  label_style=TextStyle(color=colors.BLACK, size=18),
        #                                  data='decedent', on_change=self.controller.search_change)

        self.result_count = Text(value="", color=colors.BLACK)

        # self.dd_responsible_person = CustomDropdown(
        #     label="担当者",
        #     width=150,
        #     data="decedent",
        #     on_change=self.controller.responsible_person_change,
        # )
        # self.dd_responsible_person.add_options(
        #     self.controller.get_responsible_person_dropdown()
        # )

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
            width=150,
            data="decedent",
            on_change=self.controller.contractor_change,
        )

        self.tf_kana = CustomTextField(
            label="被相続人：姓かな",
            width=200,
            autofocus=True,
            data="decedent",
            on_change=self.controller.search_change,
        )
        self.search_fields = Column(
            controls=[
                Row(
                    [
                        self.tf_kana,
                        CustomTextField(
                            label="被相続人：姓",
                            width=200,
                            data="decedent",
                            on_change=self.controller.search_change,
                        ),
                        # self.dd_responsible_person,
                        self.dd_progress,
                        CustomTextField(
                            label="備考",
                            width=200,
                            data="decedent",
                            on_change=self.controller.search_change,
                        ),
                    ]
                ),
                Row(
                    [
                        CustomTextField(
                            label="依頼人：姓かな",
                            width=200,
                            data="heir",
                            on_change=self.controller.search_change,
                        ),
                        CustomTextField(
                            label="依頼人：姓",
                            width=200,
                            data="heir",
                            on_change=self.controller.search_change,
                        ),
                        CustomTextField(
                            label="電話番号",
                            width=200,
                            data="heir",
                            on_change=self.controller.search_change,
                        ),
                    ]
                ),
            ]
        )
        super().page.session.set("search_fields", self.search_fields.controls)

        self.dt_decedent = DataTable(
            [
                DataColumn(
                    Text("選択"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("Code"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                DataColumn(
                    Text("状況"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
                # DataColumn(
                #     Container(Text("OneNote"), width=35),
                #     heading_row_alignment=MainAxisAlignment.CENTER,
                # ),
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
                # DataColumn(
                #     Text("担当者"), heading_row_alignment=MainAxisAlignment.CENTER
                # ),
                # DataColumn(
                #     Text("税担当"), heading_row_alignment=MainAxisAlignment.CENTER
                # ),
                DataColumn(
                    Text("備考"), heading_row_alignment=MainAxisAlignment.CENTER
                ),
            ],
            data_text_style=TextStyle(color=colors.BLACK),
            heading_text_style=TextStyle(color=colors.WHITE),
            heading_row_color=colors.BLUE_GREY_300,
        )

        # results = self.controller.get_result_view_all()
        # results = self.controller.get_result_view_all(me_rep_person='森町')
        results = self.controller.get_result_view_all(page=super().page)
        self.customer_data_table(results)

        self.controls = [
            Column(
                controls=[
                    # CustomText(value='＜顧客管理＞'),
                    self.search_fields,
                    Row(
                        [
                            ElevatedButton(
                                icon=icons.CLEAR,
                                text="クリア(C)",
                                style=ButtonStyle(text_style=(TextStyle(size=20))),
                                color=colors.BLACK,
                                height=40,
                                bgcolor=colors.BLUE_200,
                                on_click=self.controller.clear_click,
                            ),
                            self.ch_contractor,
                            # self.ch_me_rep_person,
                        ]
                    ),
                    Divider(),
                    Row(
                        [
                            ElevatedButton(
                                icon=icons.CREATE,
                                text="被相続人 新規登録",
                                color=colors.BLACK,
                                bgcolor=colors.BLUE_200,
                            ),
                            ElevatedButton(
                                icon=icons.CREATE,
                                text="相続人 新規登録",
                                color=colors.BLACK,
                                bgcolor=colors.BLUE_200,
                            ),
                            self.result_count,
                        ]
                    ),
                    self.dt_decedent,
                ]
            )
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
                            DataCell(Icon(icons.TOUCH_APP)),
                            # DataCell(Icon(icons.TOUCH_APP, color=colors.BLACK)),
                            DataCell(
                                Container(
                                    Text(result["code"]), alignment=alignment.center
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["状況"]),
                                    alignment=alignment.center_left,
                                )
                            ),
                            # DataCell(
                            #     Container(
                            #         Icon(icons.PERSON_SEARCH_SHARP),
                            #         alignment=alignment.center,
                            #     )
                            # ),
                            DataCell(
                                Container(
                                    Icon(icons.FOLDER), alignment=alignment.center
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["被相続人"]),
                                    alignment=alignment.center_left,
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["依頼人"]),
                                    alignment=alignment.center_left,
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["更新日"]), alignment=alignment.center
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["内容"]),
                                    alignment=alignment.center_left,
                                )
                            ),
                            # DataCell(Container(Text(result['内容']), alignment=alignment.center_left, width=300)),
                            DataCell(
                                Container(
                                    Text(result["自宅電話番号"]),
                                    alignment=alignment.center,
                                )
                            ),
                            DataCell(
                                Container(
                                    Text(result["携帯電話番号"]),
                                    alignment=alignment.center,
                                )
                            ),
                            # DataCell(
                            #     Container(
                            #         Text(result["担当者"]), alignment=alignment.center
                            #     )
                            # ),
                            # DataCell(Container(Text(""), alignment=alignment.center)),
                            # DataCell(Container(Text(result['税当者']), alignment=alignment.center)),
                            DataCell(
                                Container(
                                    Text(result["備考"]),
                                    alignment=alignment.center_left,
                                )
                            ),
                        ]
                    )
                )
        self.result_count.value = "検索数：" + str(len(results)) + "件"
        super().page.update()


class ProcedureView(BaseView):
    def __init__(self):
        super().__init__()

        self.b_heir = CustomContainerButton(
            text_value="相続人登録", icon=icons.PERSON_ADD
        )
        # self.b_heir.content.controls[1].value = '相続人登録'
        # self.b_heir.content.controls[0].content = Icon(icons.PERSON_ADD, size=45)

        self.controls = [
            Text(value="＜手続き＞"),
            Container(
                content=Column(
                    controls=[
                        Text("◯ 契約後の手続き", size=20, color=colors.BLACK),
                        self.b_heir,
                    ]
                )
            ),
        ]
