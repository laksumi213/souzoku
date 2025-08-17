import flet as ft
from models import Bank, Customer

from database import DatabaseManager


class CustomerTabContent(ft.Column):
    """
    顧客情報管理タブのUIとロジックをカプセル化したFletコンポーネント。
    """

    def __init__(self, db_manager: DatabaseManager, show_message_callback):
        super().__init__()
        self.db = db_manager
        self.show_message = show_message_callback  # スナックバー表示用のコールバック
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

        # 顧客情報入力フィールド
        self.customer_id_input = ft.TextField(
            label="顧客ID", width=200, keyboard_type=ft.KeyboardType.TEXT
        )
        self.customer_name_input = ft.TextField(
            label="氏名", width=200, keyboard_type=ft.KeyboardType.TEXT
        )
        self.customer_address_input = ft.TextField(
            label="住所", width=200, keyboard_type=ft.KeyboardType.TEXT
        )
        self.customer_phone_input = ft.TextField(
            label="電話番号", width=200, keyboard_type=ft.KeyboardType.PHONE
        )

        # 顧客情報データテーブル
        self.customer_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("顧客ID")),
                ft.DataColumn(ft.Text("氏名")),
                ft.DataColumn(ft.Text("住所")),
                ft.DataColumn(ft.Text("電話番号")),
            ],
            rows=[],
            heading_row_color=ft.colors.BLUE_GREY_100,
            horizontal_lines=ft.BorderSide(1, ft.colors.BLACK12),
            vertical_lines=ft.BorderSide(1, ft.colors.BLACK12),
            show_checkbox_column=False,
            data_row_min_height=40,
            data_row_max_height=40,
            width=600,
            border=ft.border.all(1, ft.colors.BLUE_GREY_200),
            border_radius=ft.border_radius.all(10),
        )

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([self.customer_id_input, self.customer_name_input]),
                        ft.Row(
                            [self.customer_address_input, self.customer_phone_input]
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "追加",
                                    icon=ft.icons.ADD,
                                    on_click=self.add_customer,
                                ),
                                ft.ElevatedButton(
                                    "更新",
                                    icon=ft.icons.UPDATE,
                                    on_click=self.update_customer_data,
                                ),
                                ft.ElevatedButton(
                                    "削除",
                                    icon=ft.icons.DELETE,
                                    on_click=self.delete_customer_data,
                                ),
                                ft.OutlinedButton(
                                    "クリア",
                                    icon=ft.icons.CLEAR,
                                    on_click=self.clear_customer_data_fields,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=20,
                margin=20,
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                width=650,
            ),
            ft.Text("顧客リスト", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([self.customer_data_table], scroll="auto"),
                alignment=ft.alignment.center,
                padding=10,
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                height=300,
                width=650,
            ),
        ]

    def clear_customer_inputs(self):
        """顧客情報入力フィールドをクリアします。"""
        self.customer_id_input.value = ""
        self.customer_name_input.value = ""
        self.customer_address_input.value = ""
        self.customer_phone_input.value = ""
        self.customer_id_input.read_only = False  # IDフィールドを編集可能に戻す
        self.update()  # このコンポーネント内を更新

    def load_customer_data(self):
        """データベースから顧客情報をロードし、データテーブルを更新します。"""
        customers = self.db.get_all_customers()
        self.customer_data_table.rows.clear()
        for customer in customers:
            self.customer_data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(customer.customer_id)),
                        ft.DataCell(ft.Text(customer.name)),
                        ft.DataCell(ft.Text(customer.address)),
                        ft.DataCell(ft.Text(customer.phone)),
                    ],
                    on_select_changed=lambda e, c=customer: self.select_customer_row(c),
                )
            )
        self.update()

    def select_customer_row(self, customer: Customer):
        """顧客情報テーブルの行が選択されたときに、入力フィールドにデータを設定します。"""
        self.customer_id_input.value = customer.customer_id
        self.customer_name_input.value = customer.name
        self.customer_address_input.value = customer.address
        self.customer_phone_input.value = customer.phone
        self.customer_id_input.read_only = True  # IDは更新時に変更不可にする
        self.update()  # このコンポーネント内を更新

    def add_customer(self, e):
        """顧客情報を追加します。"""
        customer_id = self.customer_id_input.value
        name = self.customer_name_input.value
        address = self.customer_address_input.value
        phone = self.customer_phone_input.value

        if not customer_id or not name:
            self.show_message("顧客IDと氏名は必須です。", ft.colors.RED_500)
            return

        new_customer = Customer(customer_id, name, address, phone)
        if self.db.insert_customer(new_customer):
            self.show_message("顧客情報を追加しました。")
            self.clear_customer_inputs()
            self.load_customer_data()
        else:
            self.show_message("顧客IDが既に存在します。", ft.colors.RED_500)

    def update_customer_data(self, e):
        """顧客情報を更新します。"""
        customer_id = self.customer_id_input.value
        name = self.customer_name_input.value
        address = self.customer_address_input.value
        phone = self.customer_phone_input.value

        if not customer_id:
            self.show_message("更新する顧客を選択してください。", ft.colors.RED_500)
            return
        if not name:
            self.show_message("氏名は必須です。", ft.colors.RED_500)
            return

        updated_customer = Customer(customer_id, name, address, phone)
        if self.db.update_customer(updated_customer):
            self.show_message("顧客情報を更新しました。")
            self.clear_customer_inputs()
            self.load_customer_data()
        else:
            self.show_message(
                "顧客情報が見つからないか、更新に失敗しました。", ft.colors.RED_500
            )

    def delete_customer_data(self, e):
        """顧客情報を削除します。"""
        customer_id = self.customer_id_input.value
        if not customer_id:
            self.show_message("削除する顧客を選択してください。", ft.colors.RED_500)
            return

        if self.db.delete_customer(customer_id):
            self.show_message("顧客情報を削除しました。")
            self.clear_customer_inputs()
            self.load_customer_data()
        else:
            self.show_message(
                "顧客情報が見つからないか、削除に失敗しました。", ft.colors.RED_500
            )

    def clear_customer_data_fields(self, e):
        """顧客情報入力フィールドをクリアボタンでクリアします。"""
        self.clear_customer_inputs()


class BankTabContent(ft.Column):
    """
    銀行情報管理タブのUIとロジックをカプセル化したFletコンポーネント。
    """

    def __init__(self, db_manager: DatabaseManager, show_message_callback):
        super().__init__()
        self.db = db_manager
        self.show_message = show_message_callback  # スナックバー表示用のコールバック
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

        # 銀行情報入力フィールド
        self.bank_id_input = ft.TextField(
            label="銀行ID", width=200, keyboard_type=ft.KeyboardType.TEXT
        )
        self.bank_name_input = ft.TextField(
            label="銀行名", width=200, keyboard_type=ft.KeyboardType.TEXT
        )
        self.bank_account_input = ft.TextField(
            label="口座番号", width=200, keyboard_type=ft.KeyboardType.NUMBER
        )
        self.bank_branch_input = ft.TextField(
            label="支店名", width=200, keyboard_type=ft.KeyboardType.TEXT
        )

        # 銀行情報データテーブル
        self.bank_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("銀行ID")),
                ft.DataColumn(ft.Text("銀行名")),
                ft.DataColumn(ft.Text("口座番号")),
                ft.DataColumn(ft.Text("支店名")),
            ],
            rows=[],
            heading_row_color=ft.colors.BLUE_GREY_100,
            horizontal_lines=ft.BorderSide(1, ft.colors.BLACK12),
            vertical_lines=ft.BorderSide(1, ft.colors.BLACK12),
            show_checkbox_column=False,
            data_row_min_height=40,
            data_row_max_height=40,
            width=600,
            border=ft.border.all(1, ft.colors.BLUE_GREY_200),
            border_radius=ft.border_radius.all(10),
        )

        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([self.bank_id_input, self.bank_name_input]),
                        ft.Row([self.bank_account_input, self.bank_branch_input]),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "追加", icon=ft.icons.ADD, on_click=self.add_bank
                                ),
                                ft.ElevatedButton(
                                    "更新",
                                    icon=ft.icons.UPDATE,
                                    on_click=self.update_bank_data,
                                ),
                                ft.ElevatedButton(
                                    "削除",
                                    icon=ft.icons.DELETE,
                                    on_click=self.delete_bank_data,
                                ),
                                ft.OutlinedButton(
                                    "クリア",
                                    icon=ft.icons.CLEAR,
                                    on_click=self.clear_bank_data_fields,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=20,
                margin=20,
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                width=650,
            ),
            ft.Text("銀行リスト", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([self.bank_data_table], scroll="auto"),
                alignment=ft.alignment.center,
                padding=10,
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                height=300,
                width=650,
            ),
        ]
        self.load_bank_data()

    def clear_bank_inputs(self):
        """銀行情報入力フィールドをクリアします。"""
        self.bank_id_input.value = ""
        self.bank_name_input.value = ""
        self.bank_account_input.value = ""
        self.bank_branch_input.value = ""
        self.bank_id_input.read_only = False  # IDフィールドを編集可能に戻す
        self.update()  # このコンポーネント内を更新

    def load_bank_data(self):
        """データベースから銀行情報をロードし、データテーブルを更新します。"""
        banks = self.db.get_all_banks()
        self.bank_data_table.rows.clear()
        for bank in banks:
            self.bank_data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(bank.bank_id)),
                        ft.DataCell(ft.Text(bank.bank_name)),
                        ft.DataCell(ft.Text(bank.account_number)),
                        ft.DataCell(ft.Text(bank.branch)),
                    ],
                    on_select_changed=lambda e, b=bank: self.select_bank_row(b),
                )
            )
        # self.update()  # このコンポーネント内を更新

    def select_bank_row(self, bank: Bank):
        """銀行情報テーブルの行が選択されたときに、入力フィールドにデータを設定します。"""
        self.bank_id_input.value = bank.bank_id
        self.bank_name_input.value = bank.bank_name
        self.bank_account_input.value = bank.account_number
        self.bank_branch_input.value = bank.branch
        self.bank_id_input.read_only = True  # IDは更新時に変更不可にする
        self.update()  # このコンポーネント内を更新

    def add_bank(self, e):
        """銀行情報を追加します。"""
        bank_id = self.bank_id_input.value
        bank_name = self.bank_name_input.value
        account_number = self.bank_account_input.value
        branch = self.bank_branch_input.value

        if not bank_id or not bank_name:
            self.show_message("銀行IDと銀行名は必須です。", ft.colors.RED_500)
            return

        new_bank = Bank(bank_id, bank_name, account_number, branch)
        if self.db.insert_bank(new_bank):
            self.show_message("銀行情報を追加しました。")
            self.clear_bank_inputs()
            self.load_bank_data()
        else:
            self.show_message("銀行IDが既に存在します。", ft.colors.RED_500)

    def update_bank_data(self, e):
        """銀行情報を更新します。"""
        bank_id = self.bank_id_input.value
        bank_name = self.bank_name_input.value
        account_number = self.bank_account_input.value
        branch = self.bank_branch_input.value

        if not bank_id:
            self.show_message("更新する銀行を選択してください。", ft.colors.RED_500)
            return
        if not bank_name:
            self.show_message("銀行名は必須です。", ft.colors.RED_500)
            return

        updated_bank = Bank(bank_id, bank_name, account_number, branch)
        if self.db.update_bank(updated_bank):
            self.show_message("銀行情報を更新しました。")
            self.clear_bank_inputs()
            self.load_bank_data()
        else:
            self.show_message(
                "銀行情報が見つからないか、更新に失敗しました。", ft.colors.RED_500
            )

    def delete_bank_data(self, e):
        """銀行情報を削除します。"""
        bank_id = self.bank_id_input.value
        if not bank_id:
            self.show_message("削除する銀行を選択してください。", ft.colors.RED_500)
            return

        if self.db.delete_bank(bank_id):
            self.show_message("銀行情報を削除しました。")
            self.clear_bank_inputs()
            self.load_bank_data()
        else:
            self.show_message(
                "銀行情報が見つからないか、削除に失敗しました。", ft.colors.RED_500
            )

    def clear_bank_data_fields(self, e):
        """銀行情報入力フィールドをクリアボタンでクリアします。"""
        self.clear_bank_inputs()
