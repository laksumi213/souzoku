import os
import app.utils as utils
from app.views.views import BaseView, CustomContainerButton, CustomText, CustomTextFieldDialog, InputField, CustomTextField
from flet import (
    Divider,
    VerticalDivider,
    ElevatedButton,
    CrossAxisAlignment,
    MainAxisAlignment,
    alignment,
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
    Checkbox,
    ButtonStyle,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    Dropdown,
    dropdown,
    AlertDialog,
    IconButton,
)


class SettingsBody(BaseView):
    def __init__(self):
        super().__init__()
        super().page.session.set('/settings', self)

        self.b_name_registration = CustomContainerButton(
            text_value='自分の名前登録',
            icon=icons.HOW_TO_REG,
            on_click=self.clicked_name_registration
        )

        self.b_staff_registration = CustomContainerButton(
            text_value='職員登録',
            icon=icons.PERSON_ADD,
            on_click=self.clicked_staff_registration
        )

        self.controls = [
            Container(
                content=Column(
                    controls=[
                        CustomText(value='＜設定＞'),
                        CustomText('◯ データ設定', size=20, color=colors.BLACK),
                        Row([self.b_name_registration, self.b_staff_registration, ])
                    ]
                )
            )
        ]

    def clicked_name_registration(self, e):
        def registration(_):
            config.set(os.getlogin(), 'family_name', tf_family_name.value)
            config.set(os.getlogin(), 'name', tf_name.value)
            config.set(os.getlogin(), 'family_name_huri', tf_family_name_huri.value)
            config.set(os.getlogin(), 'name_huri', tf_name_huri.value)
            config.set(os.getlogin(), 'mail', tf_mail.value + t_mail.value)
            with open(utils.get_config_path(), 'w', encoding='CP932', errors='ignore') as f:
                config.write(f)
            self.dialog_registration(self)

        print('clicked_name_registration:', e)
        tf_family_name = CustomTextFieldDialog(label="姓", autofocus=True)
        tf_name = CustomTextFieldDialog(label="名")
        tf_family_name_huri = CustomTextFieldDialog(label="氏のフリガナ")
        tf_name_huri = CustomTextFieldDialog(label="名のフリガナ")
        tf_mail = CustomTextFieldDialog(label="メールアドレス", hint_text='@前を入力')
        t_mail = CustomTextFieldDialog(value="@tax-info.jp", label="メルアド@以降")

        config = utils.read_config()
        try:
            tf_family_name.value = config.get(os.getlogin(), 'family_name')
            tf_name.value = config.get(os.getlogin(), 'name')
            tf_family_name_huri.value = config.get(os.getlogin(), 'family_name_huri')
            tf_name_huri.value = config.get(os.getlogin(), 'name_huri')
            tf_mail.value = config.get(os.getlogin(), 'mail').replace('@tax-info.jp', '')
        except Exception as e:
            print('read_config error:', e)

        eb_registration = ElevatedButton(text="登録", on_click=registration)
        eb_cancel = ElevatedButton(text="キャンセル", on_click=self.dialog_close)
        # super().page.overlay.append(
        #     AlertDialog(
        super().page.dialog = AlertDialog(
            open=True,
            modal=True,
            title=Text("自分の名前を登録"),
            content=Column(
                [
                    Row([tf_family_name, tf_name]),
                    Row([tf_family_name_huri, tf_name_huri]),
                    Row([tf_mail, t_mail]),
                ],
                width=300,
                height=200,
                tight=True
            ),
            actions=[
                eb_registration,
                eb_cancel
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        # )
        super().page.update()

    def clicked_staff_registration(self, e):
        super().page.session.get('main_body').content = StaffRegistration()
        super().page.update()


class StaffRegistration(BaseView):
    def __init__(self):
        super().__init__()
        super().page.session.set('/StaffRegistration', self)
        self.input_field = Column()

        self.controls = [
            Column([
                CustomText('職員登録'),
                self.input_field,
                VerticalDivider(),
                VerticalDivider(),
                ElevatedButton(
                    "登録",
                    icon=icons.HOW_TO_REG,
                    on_click=lambda e: self.controller.staff_registration_clicked(self.input_field.controls)
                ),
            ])
        ]

        self.staff = self.controller.get_all_staff()
        print('self.staff:', self.staff)

        if len(self.staff) == 0:
            row_items = [TextField(label='氏', width=150, hint_text='name1'), TextField(label='名', data='name2', width=150),
                         TextField(label='ふりがな(姓)', data='name1_huri', width=150),
                         TextField(label='ふりがな(名)', data='name2_huri', width=150),
                         TextField(label='メール', data='mail'), TextField(label='電話番号', data='tel', width=150)]
            self.input_field.controls.append(InputField(row_items))

        else:
            row_items = []
            for item in self.staff:
                row_items.append(
                    [
                        Text(value=item['staff_id']), TextField(label='氏', value=item['name1']),
                        TextField(label='名', value=item['name2']),
                        TextField(label='ふりがな(姓)', value=item['name1_huri']),
                        TextField(label='ふりがな(名)', value=item['name2_huri']),
                        TextField(label='メール', value=item['mail']),
                        TextField(label='電話番号', value=item['tel'])
                    ]
                )
            self.input_field.controls.append(InputField(row_items))

