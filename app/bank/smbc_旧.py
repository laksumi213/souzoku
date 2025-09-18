### 三井住友銀行
import flet as ft
from pdf_create import PdfCreate
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import jaconv
import os
import re


class Smbc(ft.UserControl):
    def __init__(self):
        super().__init__()

    def close_dlg(self, e):
        self.page.dialog.open = False
        self.page.update()

    def b_account_freezing_click(self):
        self.t_balance_certificate = ft.Text('相続用残高証明書発行希望')
        self.rg_balance_certificate = ft.RadioGroup(
            value='相続用残高証明書発行希望',
            content=ft.Row([ft.Radio(value='有', label='有'), ft.Radio(value='無', label='無'), ]),
        )

        # 遺言の有無を変更
        def will_change(e):
            if e.control.value == '有':
                self.t_will_inheritance.visible = True
                self.t_will_inheritance.update()
                self.rg_will_inheritance.visible = True
                self.rg_will_inheritance.update()
            else:
                self.t_will_inheritance.visible = False
                self.t_will_inheritance.update()
                self.rg_will_inheritance.visible = False
                self.rg_will_inheritance.update()

        # 遺言の有無
        self.t_will_existence = ft.Text('遺言の有無')
        self.rg_will_existence = ft.RadioGroup(
            value='遺言の有無',
            content=ft.Row([ft.Radio(value='有', label='有'), ft.Radio(value='無', label='無'),
                            ft.Radio(value='不明', label='不明'), ]),
            on_change=will_change
        )

        # 遺言どおり相続する
        self.t_will_inheritance = ft.Text('遺言どおり相続する', visible=False)
        self.rg_will_inheritance = ft.RadioGroup(
            value='遺言どおり相続する',
            content=ft.Row([ft.Radio(value='はい', label='はい'), ft.Radio(value='いいえ', label='いいえ'),
                            ft.Radio(value='未定', label='未定'), ]),
            visible=False
        )

        # 遺産分割協議書の有無
        self.t_discussed_document = ft.Text('遺産分割協議書の有無')
        self.rg_discussed_document = ft.RadioGroup(
            value='遺産分割協議書の有無',
            content=ft.Row([ft.Radio(value='有', label='有'), ft.Radio(value='無', label='無'),
                            ft.Radio(value='不明', label='不明'), ]),
        )

        # お預け入れの預金等の金融資産を受け取られる方
        self.t_transfer_person = ft.Text('お預け入れの預金等の金融資産を受け取られる方')
        self.rg_transfer_person = ft.RadioGroup(
            value='お預け入れの預金等の金融資産を受け取られる方',
            content=ft.Row([ft.Radio(value='1名', label='1名'),
                            ft.Radio(value='2名以上', label='2名以上'),
                            ft.Radio(value='決まっていない', label='決まっていない'), ]),
        )

        self.page.dialog = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text('三井住友銀行の手続き'),
            content=ft.Column(
                [
                    self.t_balance_certificate,
                    self.rg_balance_certificate,
                    ft.VerticalDivider(),
                    self.t_will_existence,
                    self.rg_will_existence,
                    ft.VerticalDivider(),
                    self.t_will_inheritance,
                    self.rg_will_inheritance,
                    ft.VerticalDivider(),
                    self.t_discussed_document,
                    self.rg_discussed_document,
                    ft.VerticalDivider(),
                    self.t_transfer_person,
                    self.rg_transfer_person,
                ],
                height=400,
            ),
            actions=[ft.ElevatedButton(text="OK", on_click=self.smbc_2),
                     ft.ElevatedButton(text="キャンセル", on_click=self.close_dlg)],
            actions_alignment="end",
        )
        self.page.update()

    def smbc_2(self, e):
        # try:
        self.bw = webdriver.Chrome()
        self.bw.maximize_window()
        self.bw.implicitly_wait(3)
        self.page.dialog = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text('三井住友銀行の手続き'),
            content=ft.Text('手動でスクロールが必要なため、スクロール終了後、OKボタンを押してください。'),
            actions=[ft.ElevatedButton(text="OK", on_click=self.smbc_3)],
            actions_alignment="end",
        )
        self.page.update()

        self.bw.get("https://inherit.smbc.co.jp/INR/#/SINR10101")
        # sleep(5)

        # 「確認しました」のチェックボックスON
        self.bw.find_element(By.XPATH, "/html/body/div[1]/main-app/sinr10101/div[4]/div[2]/div/label/label").click()

        # ページをスクロール
        target_element = self.bw.find_element(By.ID, "agree-window")
        # target_element = self.bw.find_element(By.XPATH, '//*[@id="mainAPP_1"]/sinr10101/div[4]/h2[2]')
        self.bw.execute_script("arguments[0].scrollIntoView();", target_element)

        # finally:
        #     os.kill(self.bw.service.process.pid, signal.SIGTERM)

    def smbc_3(self, e):
        self.close_dlg(self)
        self.page.update()
        self.bw.minimize_window()
        sleep(.1)
        self.bw.maximize_window()

        # 「上記内容に同意します。」のチェックボックスON
        # if not self.bw.find_element(By.ID, "agree-text").is_selected():
        #     self.bw.find_element(By.ID, "agree-text").click()

        sql = ('''
            SELECT
                t1.username1 AS 姓,
                t1.username2 AS 名,
                t1.username1_hurigana AS セイ,
                t1.username2_hurigana AS メイ,
                t1.zipcode AS 郵便番号,
                t1.prefectures AS 都道府県,
                t1.municipalities AS 市区町村,
                t1.townarea AS 丁目,
                t1.house_number AS 番地,
                t1.building AS 建物名,
                t1.birthday AS 生年月日,
                t1.deathday AS 死亡日,
                t2.branch_code AS 店番号,
                t2.deposit_type AS 科目,
                t2.bank_number AS 口座番号
            FROM customer AS t1
            INNER JOIN bank_customer AS t2
                ON t1.code = t2.code
                AND t2.jba_code = "0009"
            WHERE
                t1.code = ?      
        ''')
        record = GlobalValues.get_db(sql, tuple([GlobalValues.code]), True)[0]
        print(GlobalValues.get_db(sql, tuple([GlobalValues.code])))

        # 姓
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1003").send_keys(record["姓"])

        # 名
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1004").send_keys(record["名"])

        # セイ
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1005").send_keys(jaconv.hira2kata(record["セイ"]))

        # メイ
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1006").send_keys(jaconv.hira2kata(record["メイ"]))

        # 郵便番号
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1007").send_keys(record["郵便番号"].replace('-', ''))

        # 都道府県
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1009").send_keys(record["都道府県"])

        # 市区町村
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1010").send_keys(record["市区町村"] + record["丁目"])

        address = re.findall('[0-9]+', str(record["番地"]))

        # 丁目
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1011").send_keys(address[0])

        # 番地
        try:
            self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1012").send_keys(address[1])
        except Exception as e:
            print(e)

        # 号
        try:
            self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1013").send_keys(address[2])
        except Exception as e:
            print(e)

        # 建物
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1014").send_keys(record["建物名"])

        # 生年月日
        tdatetime = datetime.strptime(record["生年月日"], '%Y/%m/%d')
        dropdown = self.bw.find_element(By.ID, "UNQ_formcontrolselectExt_1015")
        Select(dropdown).select_by_index(datetime.now().year - tdatetime.year + 3)

        dropdown = self.bw.find_element(By.ID, "UNQ_formcontrolselectExt_1016")
        Select(dropdown).select_by_index(tdatetime.month)

        dropdown = self.bw.find_element(By.ID, "UNQ_formcontrolselectExt_1017")
        Select(dropdown).select_by_index(tdatetime.day)

        # 死亡日
        tdatetime = datetime.strptime(record["死亡日"], '%Y/%m/%d')
        dropdown = self.bw.find_element(By.ID, "UNQ_formcontrolselectExt_1018")
        Select(dropdown).select_by_index(datetime.now().year - tdatetime.year + 1)

        dropdown = self.bw.find_element(By.ID, "UNQ_formcontrolselectExt_1019")
        Select(dropdown).select_by_index(tdatetime.month)

        dropdown = self.bw.find_element(By.ID, "UNQ_formcontrolselectExt_1020")
        Select(dropdown).select_by_index(tdatetime.day)

        # 店番号
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1021").send_keys(str(record["店番号"]).zfill(3))

        # 科目
        dropdown = self.bw.find_element(By.ID, "UNQ_formcontrolselectExt_1022")
        buf = record["科目"].replace("預金", "")
        if buf == '普通':
            buf = '普通・貯蓄'
        Select(dropdown).select_by_visible_text(buf)

        # 口座番号
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1024").send_keys(str(record["口座番号"]).zfill(7))

        # 会社名
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1025").send_keys('森町')

        # 氏名
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1026").send_keys('翼')

        # カタガキ又はカイシャメイ
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1027").send_keys('モリマチ')

        # シメイ
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1028").send_keys('ツバサ')

        # 相続人さま等とのご関係
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1029").send_keys('相続人等代理人')

        # 会社住所
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1031").send_keys('1940022')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1033").send_keys('東京都')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1034").send_keys('町田市森野')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1035").send_keys('1')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1036").send_keys('22')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1037").send_keys('5')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_1038").send_keys('町田310五十子ビル3F')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_10391").send_keys('042')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_10392").send_keys('710')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_10393").send_keys('6178')

        ### お手続者さまについて
        # 「手続者が弁護士、司法書士、行政書士、税理士のいずれかの資格を有する場合、チェックをお願いします」にチェック
        self.bw.find_element(By.ID, "UNQ_checkboxExt_1084").click()
        # sleep(.1)

        # 「士業(※)の方はこちら」にチェック
        self.bw.find_element(By.XPATH,
                             "/html/body/div[1]/main-app/sinr10101/div[5]/div/div[8]/div[3]/div[1]/h2[1]/div/div[1]/label/label").click()

        # お手続者さまのお名前
        self.bw.find_element(By.NAME, "ProceduralKatagaki").send_keys(
            '相続手続支援センター町田有限責任事業組合 組合員　株式会社　プロフィット・ワン　クミアイイン　カブシキカイシャ　プロフィット・ワン')
        self.bw.find_element(By.NAME, "ProceduralSimei").send_keys('職務執行者　大貫利一')
        self.bw.find_element(By.NAME, "ProceduralKatagakiKana").send_keys(
            'ソウゾクテツヅキシエンセンターマチダユウゲンセキニンジギョウクミアイクミアイイン')
        # self.bw.find_element(By.ID,"UNQ_formcontrolinputtextExt_1070").send_keys('シヨクムシツコウシヤオオヌキトシカズ')
        self.bw.find_element(By.NAME, "ProceduralSimeiKana").send_keys('ショクムシッコウシャオオヌキトシカズ')

        # 続柄（お亡くなりになられた方からみたご関係）
        # self.bw.find_element(By.ID,"UNQ_formcontrolinputtextExt_1090").send_keys('委任を受けている士業')
        self.bw.find_element(By.NAME, "proceduralGokankei").send_keys('相続人等代理人')

        self.bw.find_element(By.NAME, "proceduralZipcode").send_keys('1940022')
        self.bw.find_element(By.NAME, "proceduralTodohuken").send_keys('東京都')
        self.bw.find_element(By.NAME, "proceduralSikuchoson").send_keys('町田市森野')
        self.bw.find_element(By.NAME, "proceduralBanchiChou").send_keys('1')
        self.bw.find_element(By.NAME, "proceduralBanchiBan").send_keys('22')
        self.bw.find_element(By.NAME, "proceduralBanchiGou").send_keys('5')
        self.bw.find_element(By.NAME, "proceduralOther").send_keys('町田310五十子ビル3F')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_10581").send_keys('042')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_10582").send_keys('710')
        self.bw.find_element(By.ID, "UNQ_formcontrolinputtextExt_10583").send_keys('6178')
        # sleep(.1)

        # 残高証明書有無
        if self.rg_balance_certificate.value == '有':
            self.bw.find_element(By.XPATH, '//*[@id="bs115"]/div/div[1]/div[2]/li[1]/label/label').click()
        elif self.rg_balance_certificate.value == '無':
            self.bw.find_element(By.XPATH, '//*[@id="bs115"]/div/div[1]/div[2]/li[2]/label/label').click()

        # 遺言の有無
        if self.rg_will_existence.value == '有':
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10101/div[5]/div/div[8]/div[4]/div[1]/div/div[1]/div[2]/li[2]/label/label").click()
            # sleep(.1)
            if self.rg_will_inheritance.value == 'はい':
                self.bw.find_element(By.XPATH, '//*[@id="isanumu-area"]/div[1]/div[2]/li[1]/label').click()
            elif self.rg_will_inheritance.value == 'いいえ':
                self.bw.find_element(By.XPATH, '//*[@id="isanumu-area"]/div[1]/div[2]/li[2]/label/label').click()
            elif self.rg_will_inheritance.value == '未定':
                self.bw.find_element(By.XPATH, '//*[@id="isanumu-area"]/div[1]/div[2]/li[3]/label/label').click()

            # 手続は遺言執行者が行う　→　いいえ
            self.bw.find_element(By.XPATH, '//*[@id="isanumu-area"]/div[2]/div[2]/li[2]/label/label').click()

        elif self.rg_will_existence.value == '無':
            self.bw.find_element(By.XPATH, '//*[@id="bs115"]/div/div[2]/div[2]/li[2]/label/label').click()
        elif self.rg_will_existence.value == '不明':
            self.bw.find_element(By.XPATH, '//*[@id="bs115"]/div/div[2]/div[2]/li[3]/label/label').click()

        # 遺産分割協議書の有無
        if self.rg_discussed_document.value == '有':
            self.bw.find_element(By.XPATH, '//*[@id="bs115"]/div/div[4]/div[2]/li[1]/label/label').click()
        elif self.rg_discussed_document.value == '無':
            self.bw.find_element(By.XPATH, '//*[@id="bs115"]/div/div[4]/div[2]/li[2]/label/label').click()
        elif self.rg_discussed_document.value == '不明':
            self.bw.find_element(By.XPATH, '//*[@id="bs115"]/div/div[4]/div[2]/li[3]/label/label').click()

        # 相続人間の意見の相違　→　なし
        self.bw.find_element(By.XPATH,
                             "/html/body/div[1]/main-app/sinr10101/div[5]/div/div[8]/div[4]/div[1]/div/div[5]/div[2]/li[2]/label/label").click()

        # 次へ
        self.bw.find_element(By.XPATH, '//*[@id="UNQ_oranchor_1086"]').click()
        sleep(0.5)

        # 配偶者
        sql = "SELECT COUNT(*) FROM heir WHERE code = ? AND situation != '死亡' AND(relationship = '妻' OR relationship = '夫')"
        spouse_count = GlobalValues.get_db(sql, tuple([GlobalValues.code]))[0][0]

        # 子ども
        sql = "SELECT COUNT(*) FROM Heir WHERE code = ? AND situation != '死亡' AND(relationship LIKE '%男' OR relationship LIKE '%女') AND relationship NOT LIKE '%孫%'"
        children_count = GlobalValues.get_db(sql, tuple([GlobalValues.code]))[0][0]

        # 孫
        sql = "SELECT COUNT(*) FROM heir WHERE code = ? AND situation != '死亡' AND relationship LIKE '%孫%'"
        grandchild_count = GlobalValues.get_db(sql, tuple([GlobalValues.code]))[0][0]

        # 父母
        sql = "SELECT COUNT(*) FROM heir WHERE code = ? AND situation != '死亡' AND(relationship LIKE '%父%' OR relationship LIKE '%母%')"
        parents_count = GlobalValues.get_db(sql, tuple([GlobalValues.code]))[0][0]

        # 祖父母
        sql = "SELECT COUNT(*) FROM heir WHERE code = ? AND situation != '死亡' AND(relationship LIKE '%祖父%' OR relationship LIKE '%祖母%')"
        old_parents_spouse_count = GlobalValues.get_db(sql, tuple([GlobalValues.code]))[0][0]

        # 兄弟姉妹
        sql = "SELECT COUNT(*) FROM Heir WHERE code = ? AND situation != '死亡' AND(relationship LIKE '%兄弟' OR relationship LIKE '%姉妹') AND relationship NOT LIKE '%孫%'"
        brother_sister_count = GlobalValues.get_db(sql, tuple([GlobalValues.code]))[0][0]

        # 甥姪
        sql = "SELECT COUNT(*) FROM Heir WHERE code = ? AND situation != '死亡' AND(relationship LIKE '%甥' OR relationship LIKE '%姪') AND relationship NOT LIKE '%孫%'"
        nephew_niece_count = GlobalValues.get_db(sql, tuple([GlobalValues.code]))[0][0]

        # 配偶者のみ
        if spouse_count >= 1 and children_count == 0 and grandchild_count == 0 and parents_count == 0 and old_parents_spouse_count == 0 and brother_sister_count == 0 and nephew_niece_count == 0:
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[2]/main-app/sinr10102/div[5]/div/ul/li[1]/label/label").click()
        # 配偶者と子
        elif spouse_count >= 1 and children_count >= 1 and grandchild_count == 0 and parents_count == 0 and old_parents_spouse_count == 0 and brother_sister_count == 0 and nephew_niece_count == 0:
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10102/div[4]/div/ul/li[2]/label/label").click()
        # 子のみ
        elif spouse_count == 0 and children_count >= 1 and grandchild_count == 0 and parents_count == 0 and old_parents_spouse_count == 0 and brother_sister_count == 0 and nephew_niece_count == 0:
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10102/div[4]/div/ul/li[3]/label/label").click()
        # 配偶者と親
        elif spouse_count >= 1 and children_count == 0 and grandchild_count == 0 and parents_count >= 1 and old_parents_spouse_count == 0 and brother_sister_count == 0 and nephew_niece_count == 0:
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10102/div[4]/div/ul/li[4]/label/label").click()
        # 配偶者と兄弟姉妹（または甥姪）
        elif spouse_count >= 1 and children_count == 0 and grandchild_count == 0 and parents_count == 0 and old_parents_spouse_count == 0 and (
                brother_sister_count >= 1 or nephew_niece_count >= 1):
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10102/div[4]/div/ul/li[5]/label/label").click()
        # 親のみ
        elif spouse_count == 0 and children_count == 0 and grandchild_count == 0 and parents_count >= 1 and old_parents_spouse_count == 0 and brother_sister_count == 0 and nephew_niece_count == 0:
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10102/div[4]/div/ul/li[6]/label/label").click()
        # 兄弟姉妹（または甥姪）のみ
        elif spouse_count == 0 and children_count == 0 and grandchild_count == 0 and parents_count == 0 and old_parents_spouse_count == 0 and (
                brother_sister_count >= 1 or nephew_niece_count >= 1):
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10102/div[4]/div/ul/li[7]/label/label").click()
        # 子と孫(または孫のみ)
        elif spouse_count == 0 and (
                children_count >= 1 or grandchild_count >= 1) and parents_count == 0 and old_parents_spouse_count == 0 and brother_sister_count == 0 and nephew_niece_count == 0:
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10102/div[4]/div/ul/li[8]/label/label").click()
        # 上記以外
        else:
            self.bw.find_element(By.XPATH,
                                 "/html/body/div[1]/main-app/sinr10102/div[4]/div/ul/li[9]/label/label").click()

        # 三井住友銀行にお預け入れの預金等の金融資産を受け取られる方
        if self.rg_transfer_person.value == '1名':
            self.bw.find_element(By.XPATH, "/html/body/div[1]/main-app/sinr10102/div[5]/div/ul/li[1]/label").click()
        elif self.rg_transfer_person.value == '2名以上':
            self.bw.find_element(By.XPATH, '//*[@id="bs202"]/div/ul/li[3]/label/label').click()
        elif self.rg_transfer_person.value == '決まっていない':
            self.bw.find_element(By.XPATH, '//*[@id="bs202"]/div/ul/li[4]/label/label').click()

        ## ご相続人さまの状況
        sql = 'SELECT * FROM heir WHERE code = ?'
        heir_records = GlobalValues.get_db(sql, tuple([GlobalValues.code]))

        if not isinstance(heir_records, list):
            heir_records = tuple([heir_records])

        # print(heir_records)

        bool1 = 0
        bool2 = 0
        for heir_record in heir_records:
            # print(heir_record)
            if heir_record[11] == '相続放棄':
                bool1 = 1

            if heir_record[11] == '海外在住':
                bool2 = 1

        if bool1 == 1:
            self.bw.find_element(By.ID, 'joukyouhouki-text').click()

        if bool2 == 1:
            self.bw.find_element(By.ID, 'joukyoukaigai-text').click()

        if bool1 == 0 and bool2 == 0:
            self.bw.find_element(By.ID, 'joukyouother-text').click()

        # 入力内容の確認
        self.bw.find_element(By.ID, 'UNQ_oranchor_2039').click()

    # 残高証明書
    def balance_certificate(self):
        self.create_date = ft.TextField(label='作成日', value=datetime.now().strftime('%Y/%m/%d'))
        self.dd_rep = ft.Dropdown(
            label='担当者',
            options=[
                ft.dropdown.Option('堀井'),
                ft.dropdown.Option('森町'),
                ft.dropdown.Option('浅野'),
                ft.dropdown.Option('堀池'),
                ft.dropdown.Option('大田'),
                ft.dropdown.Option('鎌田'),
            ],
            value='堀池',
            width=100,
        )
        self.page = GlobalValues.my_page
        self.page.dialog = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text('三井住友銀行の手続き'),
            content=ft.Column(
                [
                    self.create_date,
                    ft.VerticalDivider(),
                    self.dd_rep,
                ],
                height=150,
            ),
            actions=[ft.ElevatedButton(text="OK", autofocus=True,
                                       on_click=self.balance_certificate_create),
                     ft.ElevatedButton(text="キャンセル", on_click=self.close_dlg)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.update()

    def balance_certificate_create(self, _):
        self.close_dlg(self)

        pdf = PdfCreate("A4")
        sql = (f'''
            SELECT
                t1.folder_s_path AS フォルダパス,
                t1.username1_hurigana || "  " || t1.username2_hurigana AS 被相続人_かな,
                t1.username1 || "  " || t1.username2 AS 被相続人,
                t1.deathday AS 死亡日,
                t2.branch_code AS 店番号,
                t2.bank_number AS 口座番号,
                t2.deposit_type AS 種類,
                t3.bank_branch_name AS 支店名,
                t4.username1 || "  " || t4.username2 AS 相続人,
                t4.username1_hurigana || "  " || t4.username2_hurigana AS 相続人かな
            FROM customer AS t1
                INNER JOIN bank_customer AS t2
                ON t1.code = t2.code
                AND t2.jba_code = "0009"
                    INNER JOIN bank_branch AS t3
                    ON t3.bank_branch_code = t2.branch_code
                        INNER JOIN heir AS t4
                        ON t4.code = t1.code
                        AND t4.offer = 1
            WHERE t1.code = "{GlobalValues.code}"
        ''')
        self.customer = GlobalValues.get_db(sql, row_factory=True)
        print(GlobalValues.get_db(sql, row_factory=False))

        # pdf.draw_string(146, 271, self.create_date.value[2])
        # pdf.draw_string(151, 271, self.create_date.value[3])
        # pdf.draw_string(161, 271, self.create_date.value[5])
        # pdf.draw_string(166, 271, self.create_date.value[6])
        # pdf.draw_string(176, 271, self.create_date.value[8])
        # pdf.draw_string(181, 271, self.create_date.value[9])

        pdf.draw_string(40, 268, f'{self.customer[0]["被相続人"]}　相続人　{self.customer[0]["相続人"]}　代理人')
        pdf.draw_string(40, 263, '相続手続支援センター町田有限責任事業組合')
        pdf.draw_string(40, 258, '組合員　株式会社プロフィット・ワン')
        pdf.draw_string(40, 253, '職務執行者　大貫　利一')
        if self.dd_rep.value == '森町':
            pdf.draw_string(130, 258, '042-710-6178')
        elif self.dd_rep.value == '堀池':
            pdf.draw_string(130, 258, '080-4800-3208')
        elif self.dd_rep.value == '大田':
            pdf.draw_string(130, 258, '080-7007-1684')
        elif self.dd_rep.value == '鎌田':
            pdf.draw_string(130, 258, '080-7007-1781')
        pdf.draw_string(145, 248, self.dd_rep.value)

        pdf.draw_string(46, 235, self.customer[0]['支店名'], 12)
        pdf.draw_string(86, 232, str(self.customer[0]['店番号']).zfill(3)[0])
        pdf.draw_string(91, 232, str(self.customer[0]['店番号']).zfill(3)[1])
        pdf.draw_string(96, 232, str(self.customer[0]['店番号']).zfill(3)[2])
        if '普通' in self.customer[0]['種類']:
            pdf.draw_string(101, 233.5, '〇', 12)
        elif '当座' in self.customer[0]['種類']:
            pdf.draw_string(109, 233.5, '〇', 12)
        else:
            pass
        pdf.draw_string(131, 232, str(self.customer[0]['口座番号']).zfill(7)[0], 12)
        pdf.draw_string(136, 232, str(self.customer[0]['口座番号']).zfill(7)[1], 12)
        pdf.draw_string(141, 232, str(self.customer[0]['口座番号']).zfill(7)[2], 12)
        pdf.draw_string(146, 232, str(self.customer[0]['口座番号']).zfill(7)[3], 12)
        pdf.draw_string(151, 232, str(self.customer[0]['口座番号']).zfill(7)[4], 12)
        pdf.draw_string(156.5, 232, str(self.customer[0]['口座番号']).zfill(7)[5], 12)
        pdf.draw_string(161, 232, str(self.customer[0]['口座番号']).zfill(7)[6], 12)

        pdf.draw_string(27, 195, '✓')
        pdf.draw_string(47, 195, 'ﾄｳｷｮｳﾄﾏﾁﾀﾞｼﾓﾘﾉ1ﾁｮｳﾒ22ﾊﾞﾝ5ｺﾞｳ ﾏﾁﾀﾞ310ｲﾗｺﾞﾋﾞﾙ3ｶｲ')
        pdf.draw_string(42, 188, '194-0022')
        pdf.draw_string(75, 188, '東京都町田市森野一丁目22番5号')
        pdf.draw_string(75, 183, '町田310五十子ビル3階')

        pdf.draw_string(27.5, 158, '✓')

        deathday = re.findall(r'\d+', self.customer[0]['死亡日'])
        pdf.draw_string(60, 132, str(deathday[0]).zfill(4)[2], 14)
        pdf.draw_string(69, 132, str(deathday[0]).zfill(4)[3], 14)
        pdf.draw_string(84, 132, str(deathday[1]).zfill(2)[0], 14)
        pdf.draw_string(93, 132, str(deathday[1]).zfill(2)[1], 14)
        pdf.draw_string(108.5, 132, str(deathday[2]).zfill(2)[0], 14)
        pdf.draw_string(119, 132, str(deathday[2]).zfill(2)[1], 14)
        pdf.draw_string(172, 132.5, 1, 14)

        # 手数料引落口座
        # pdf.draw_string(27.5, 117, '✓')

        pdf.pdf_save(os.path.join(self.customer[0]['フォルダパス'], '三井住友銀行_残高証明書依頼書1'),
                     os.path.dirname(__file__) + "/pdf/三井住友銀行_残高証明書依頼書.pdf", page=1, open_bool=False)

        pdf = PdfCreate("A4")
        pdf.pdf_save(os.path.join(self.customer[0]['フォルダパス'], '三井住友銀行_残高証明書依頼書2'),
                     os.path.dirname(__file__) + "/pdf/三井住友銀行_残高証明書依頼書.pdf", page=2, open_bool=False)

        os.makedirs(os.path.join(self.customer[0]['フォルダパス'], '金融機関手続', '残高証明書', '申請書'), exist_ok=True)

        pdf.pdf_marge(
            os.path.join(self.customer[0]['フォルダパス'], '金融機関手続', '残高証明書', '申請書', '三井住友銀行_残高証明書依頼書'),
            os.path.join(self.customer[0]['フォルダパス'], '三井住友銀行_残高証明書依頼書1'),
            os.path.join(self.customer[0]['フォルダパス'], '三井住友銀行_残高証明書依頼書2')
        )


def main(page: ft.Page):
    GlobalValues.code = "2501029"
    page.scrollTo = "always"
    page.scroll = 'AUTO'
    page.window_width = 1930
    page.window_height = 1080 - 50
    page.window_center()
    page.window_minimizable = True
    page.window_maximizable = True
    page.window_resizable = True
    GlobalValues.my_page = page
    cl = Smbc()
    page.add(cl)
    # cl.b_account_freezing_click()
    # cl.balance_certificate()
    # cl.inheritance_notification()


if __name__ == '__main__':
    ft.app(target=main)
    # GlobalValues.code = "E00246"
    # cl = Smbc()
    # cl.balance_certificate()
    # cl.inheritance_notification()

    # pdf = PdfCreate("A4")
    # pdf.pdf_marge(
    #     os.path.join(r'C:\Users\prof162\OneDrive - 株式会社プロフィット・ワン\General\py\pdf', '三井住友銀行_残高証明書依頼書'),
    #     os.path.join(r'C:\Users\prof162\OneDrive - 株式会社プロフィット・ワン\General\py\pdf', '三井住友銀行_残高証明書1'),
    #     os.path.join(r'C:\Users\prof162\OneDrive - 株式会社プロフィット・ワン\General\py\pdf', '三井住友銀行_残高証明書2')
    # )