from flet import (
    Page,
    Column,
    Row,
    Text,
    TextField,
    TextStyle,
    colors,
)
import app.utils as utils
import asyncio


class HomeBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 15  # 要素間の間隔を指定

        info = Text('＜顧客管理＞', size=30, color=colors.BLACK)

        self.tb_name1 = TextField(
            label='被相続人：姓',
            label_style=TextStyle(color=colors.BLACK),
            color=colors.BLACK,
            focused_border_color=colors.CYAN,
            width=200,
            on_focus=self.ime_on,
            on_blur=self.search_clicked
        )

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

        self.controls = [
            info,
            Row([self.tb_name1_huri, self.tb_name1])
        ]

        # self.page.session.set('home_body', self)

    def ime_on(self, _):
        asyncio.new_event_loop().run_in_executor(None, utils.ime_on)

    def search_clicked(self, e):
        def close(e):
            self.page.dialog.open = False
            self.page.update()

        # if self.dd_progress.value == '手続終了':
        #     self.ch_contractor.value = False
        #     GlobalValues.body.update()
        #
        # v = []
        # z = []
        #
        # if self.tb_name_heir_huri.value != "" or self.tb_name_heir.value != "":
        #     sql = ('''
        #         SELECT
        #             code,
        #             (SELECT responsible_person FROM customer WHERE customer.code = heir.code),
        #             (SELECT situation FROM customer WHERE customer.code = heir.code),
        #             (SELECT folder_a_path FROM customer WHERE customer.code = heir.code),
        #             (SELECT folder_s_path FROM customer WHERE customer.code = heir.code),
        #             (SELECT username1 || "　" || username2 FROM customer WHERE customer.code = heir.code),
        #             (SELECT username1_hurigana || "　" || username2_hurigana FROM customer WHERE customer.code = heir.code),
        #             username1 || "　" || username2 ,
        #             username1_hurigana || "　" || username2_hurigana,
        #             (SELECT note FROM customer WHERE customer.code = heir.code),
        #             note,
        #             updated_date
        #         FROM heir
        #         WHERE offer = 1
        #     ''')
        #     if not self.tb_name_heir.value == '':
        #         v.append('%' + self.tb_name_heir.value + '%')
        #         z.append('username1')
        #         sql += ' AND ' if not sql.strip()[-5:] == 'WHERE' else ' '
        #         sql += ' username1 LIKE (:username1)'
        #     if not self.tb_name_heir_huri.value == '':
        #         v.append('%' + self.tb_name_heir_huri.value + '%')
        #         z.append('username1_hurigana')
        #         sql += ' AND ' if not sql.strip()[-5:] == 'WHERE' else ' '
        #         sql += 'username1_hurigana LIKE (:username1_hurigana)'
        #
        # else:
        #     sql = ('''
        #         SELECT
        #             code,
        #             responsible_person as "担当者",
        #             situation as "進捗状況",
        #             folder_a_path as "あずさフォルダ",
        #             folder_s_path as "センターフォルダ",
        #             username1 || "　" || username2 as "被相続人氏名",
        #             username1_hurigana || "　" || username2_hurigana as "被相続人かな",
        #             (
        #                 SELECT
        #                     heir.username1 || "　" || heir.username2
        #                 FROM heir
        #                 WHERE customer.code = heir.code
        #                 AND offer = 1
        #             ) as "依頼人氏名",
        #             (
        #                 SELECT
        #                     heir.username1_hurigana || "　" ||  heir.username2_hurigana
        #                 FROM heir
        #                 WHERE customer.code = heir.code
        #                 AND offer = 1
        #             ) as "依頼人かな",
        #             note as "備考",
        #         (
        #             SELECT
        #                 note
        #             FROM heir
        #             WHERE customer.code = heir.code
        #             AND offer = 1
        #         ) as "更新日",
        #         (
        #             SELECT
        #                 updated_date
        #             FROM heir
        #             WHERE customer.code = heir.code
        #             AND offer = 1
        #         ) as "内容"
        #         FROM customer
        #         WHERE
        #     ''')
        #
        #     if not self.tb_name1.value == '':
        #         v.append('%' + self.tb_name1.value + '%')
        #         z.append('username1')
        #         sql += ' username1 LIKE (:username1)'
        #
        #     if not self.tb_name1_huri.value == '':
        #         v.append('%' + self.tb_name1_huri.value + '%')
        #         z.append('username1_hurigana')
        #         sql += ' AND ' if not sql.strip()[-5:] == 'WHERE' else ' '
        #         sql += 'username1_hurigana LIKE (:username1_hurigana)'
        #
        #     if self.dd_responsible_person.value is not None and not self.dd_responsible_person.value == "":
        #         v.append('%' + self.dd_responsible_person.value + '%')
        #         z.append('responsible_person')
        #         sql += ' AND ' if not sql.strip()[-5:] == 'WHERE' else ' '
        #         sql += 'responsible_person LIKE (:responsible_person)'
        #
        #     if self.dd_progress.value is not None and not self.dd_progress.value == "":
        #         v.append('%' + self.dd_progress.value + '%')
        #         z.append('situation')
        #         sql += ' AND ' if not sql.strip()[-5:] == 'WHERE' else ' '
        #         sql += 'situation LIKE (:situation)'
        #
        #     if not self.tb_note.value == '':
        #         v.append('%' + self.tb_note.value + '%')
        #         z.append('note')
        #         sql += ' AND ' if not sql.strip()[-5:] == 'WHERE' else ' '
        #         sql += 'note LIKE (:note)'
        #
        #     if self.ch_contractor.value:
        #         sql += ' AND ' if not sql.strip()[-5:] == 'WHERE' else ' '
        #         sql += ' situation != "手続終了" AND situation != "キャンセル" '
        #
        #     if self.ch_me_rep_person.value:
        #         config = configparser.ConfigParser()
        #         if os.path.isfile(os.path.dirname(__file__) + r'/config/config.ini'):
        #             config.read(os.path.dirname(__file__) + r'/config/config.ini', encoding='CP932')
        #
        #         if not config.has_section(os.getlogin()):
        #             page = GlobalValues.my_page
        #             page.dialog = AlertDialog(
        #                 open=True,
        #                 modal=True,
        #                 title=Text("自分の名前登録が未登録"),
        #                 content=Text('自分の名前が登録されておりません。なお、登録は設定から行えます。'),
        #                 actions=[ElevatedButton(text="OK", on_click=close)],
        #                 actions_alignment="center",
        #             )
        #             page.update()
        #         else:
        #             v.append(config.get(os.getlogin(), 'family_name'))
        #             z.append('responsible_person')
        #             sql += ' AND ' if not sql.strip()[-5:] == 'WHERE' else ' '
        #             sql += 'responsible_person == (:responsible_person)'
        #
        # s = dict(zip(z, v))
        # if not s:
        #     sql = ('''
        #         SELECT
        #             code,
        #             responsible_person,
        #             situation,
        #             folder_a_path,
        #             folder_s_path,
        #             username1 || "　" || username2,
        #             username1_hurigana || "　" || username2_hurigana,
        #             (
        #                 SELECT
        #                     heir.username1 || "　" || heir.username2
        #                 FROM heir
        #                 WHERE customer.code = heir.code
        #                 AND offer = 1
        #             ),
        #             (
        #                 SELECT
        #                     heir.username1_hurigana || "　" ||  heir.username2_hurigana
        #                 FROM heir
        #                 WHERE customer.code = heir.code
        #                 AND offer = 1
        #             ),
        #             note,
        #         (
        #             SELECT
        #                 note
        #             FROM heir
        #             WHERE customer.code = heir.code
        #             AND offer = 1
        #         ) as "更新日",
        #         (
        #             SELECT
        #                 updated_date
        #             FROM heir
        #             WHERE customer.code = heir.code
        #             AND offer = 1
        #         ) as "内容"
        #         FROM customer
        #         ORDER BY code DESC
        #     ''')
        #     record = GlobalValues.get_db(sql)
        # else:
        #     sql += ' ORDER BY code DESC'
        #     record = GlobalValues.get_db(sql, s)
        #
        # my_rows = []
        # # c = 0
        # for i, rec in enumerate(record):
        #     # c += 1
        #     row = DataRow(
        #         cells=[
        #             DataCell(Icon(icons.TOUCH_APP), data=rec[0],
        #                         on_tap=lambda e: self.customer_selection(e.control.data)),
        #             DataCell(Text(rec[0]), data=rec[0], on_tap=lambda e: pyperclip.copy(e.control.data)),
        #             DataCell(Text(rec[1]), data=rec[1], on_tap=lambda e: pyperclip.copy(e.control.data)),
        #             DataCell(Text(rec[2]), data=rec[2], on_tap=lambda e: pyperclip.copy(e.control.data)),
        #             DataCell(Icon(icons.TOUCH_APP), data=rec[0],
        #                         on_tap=lambda e: OneNote(e.control.data)),
        #             DataCell(Icon(icons.FOLDER), data=rec[4], on_tap=self.folder_open),
        #             DataCell(Text(rec[5]), data=rec[5], on_tap=lambda e: pyperclip.copy(e.control.data)),
        #             DataCell(Text(rec[7]), data=rec[7], on_tap=lambda e: pyperclip.copy(e.control.data)),
        #             DataCell(Text(rec[11]), data=rec[11], on_tap=lambda e: pyperclip.copy(e.control.data)),
        #             DataCell(Text(rec[10]), data=rec[10], on_tap=lambda e: pyperclip.copy(e.control.data)),
        #             DataCell(Text(rec[9]), data=rec[9], on_tap=lambda e: pyperclip.copy(e.control.data)),
        #         ],
        #         selected=True,
        #     )
        #     my_rows.append(row)
        # self.db_customer.rows = my_rows
        #
        # self.search_count.value = '検索数：' + str(len(my_rows)) + '件'
        # GlobalValues.sql = sql
        # self.db_customer.update()
        # GlobalValues.body.update()
        # self.search_count.update()
        # self.update()


class SettingsBody(Column):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.spacing = 15  # 要素間の間隔を指定

        info = Text('＜設定＞', size=30, color=colors.BLACK)

        self.controls = [
            info,
        ]

        self.page.session.set('settings_body', self)
