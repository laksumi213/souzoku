# 三菱UFJ銀行
from app._utils.web_operation import Web
import app.utils as utils
import jaconv
import mojimoji
import re
from time import sleep
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.controllers.pdf_create import PdfCreate
import os
from pyautogui import press
from datetime import datetime

class Mufg:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.url = None
        self.code = 'G2069'
        self.customer_name = '鈴木　幡雄'
        self.customer_name_kana = 'すずき　はたお'
        self.bank_account_number = '3159175'
        if self.bank_account_number:
            self.bank_account_number = str(self.bank_account_number).zfill(7)
        self.branch_name = '渋谷明治通支店'
        self.subjects = '普通'
        self.birthday = re.findall('[0-9]+', '1927/12/1')
        self.address = '東京都目黒区中町2丁目38番21号'
        self.building = ''
        self.passed_away_date = re.findall('[0-9]+', '2025/5/26')
        self.deathday = re.findall('[0-9]+' ,utils.convert_to_wareki2('2025/5/26'))
        self.heir_name = '臼杵　優子'
        self.heir_name_kana = 'うすき　ゆうこ'
        self.heir_address = '東京都世田谷区若林1丁目2番20号'
        self.heir_building = ''

        self.date = re.findall(r'\d+', datetime.now().strftime('%Y/%m/%d'))

        zipcode = utils.get_zipcode_from_address(self.address)
        self.zipcode = re.findall('[0-9]+', zipcode)
        print('self.zipcode:', self.zipcode)

        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]
        print('address:', re.findall(pattern, self.address)[0])
        print('utils.get_zipcode_from_address(address):', utils.get_zipcode_from_address(address))

        match = re.search(r'([^\d]+)(\d.*)', address[2])
        if match:
            self.place = match.group(1) # 最初のグループ（数字以外の文字）
            self.number = match.group(2)  # 2番目のグループ（数字とハイフンを含む部分）
            print(f"場所: {self.place}") # 出力: 場所: 夏見台
            print(f"番地: {self.number}")

        self.name = re.findall(r'^(.*?)[ 　](.*)$', self.customer_name)[0]
        print('被相続人', self.name)

        self.name_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.customer_name_kana))[0]
        print('被相続人カナ', self.name_kana)

        self.heir = re.findall(r'^(.*?)[ 　](.*)$', self.heir_name)[0]
        print('相続人', self.heir)

        self.heir_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.heir_name_kana))[0]
        print('相続人カナ', self.heir_kana)


    def account_freezing(self):
        url = 'https://sozoku.bk.mufg.jp/uketsuke/A010'
        self.proc = Web()
        self.proc.web_open(url)
        # 確認しました
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[2]/ul/li/label/span").click()
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[4]/ul/li/label/span").click()
        sleep(0.5)

        # 次へ
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/a[2]/span").click()

        sleep(.5)

        # Eメールアドレス
        self.proc.driver.find_element(By.ID, 'MailAddress').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.ID, 'MailAddressConfirmation').send_keys('t.morimachi_gy@chester-tax.com')

        # 次へ
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/nav/ul/li[2]/a/p").click()
        sleep(0.5)

        # 登録する
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/nav/ul/li[2]/a/p").click()
        sleep(0.5)

        # 認証番号の入力はこちらのボタンを押す
        self.proc.driver.find_element(By.XPATH, '//*[@id="form0"]/a/span').click()

        messagebox.showinfo("認証番号入力", "「認証番号入力後」にOKボタンをクリックしてください。")

        # 氏名
        self.proc.driver.find_element(By.ID, 'InheriteeLastName').send_keys(self.name[0])
        self.proc.driver.find_element(By.ID, 'InheriteeFirstName').send_keys(self.name[1])
        self.proc.driver.find_element(By.ID, 'InheriteeLastNameKana').send_keys(self.name_kana[0])
        self.proc.driver.find_element(By.ID, 'InheriteeFirstNameKana').send_keys(self.name_kana[1])

        # 国籍
        self.proc.driver.find_element(By.ID, 'InheriteeNationality').send_keys('日本')

        # 住所
        self.proc.driver.find_element(By.ID, 'InheriteeZipCode1').send_keys(self.zipcode[0])
        self.proc.driver.find_element(By.ID, 'InheriteeZipCode2').send_keys(self.zipcode[1])
        # 郵便番号から調べる
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/div/form/div[4]/div/ul/li/dl/dd/input[3]").click()
        sleep(0.5)

        self.proc.driver.find_element(By.ID, 'InheriteeAddress').send_keys(self.number)

        # 生年月日
        Select(self.proc.driver.find_element(By.ID, "InheriteeBirthdayYear")).select_by_visible_text(self.birthday[0] + '年')
        sleep(0.1)
        Select(self.proc.driver.find_element(By.ID, "InheriteeBirthdayMonth")).select_by_visible_text(f"{int(self.birthday[1])}月")
        sleep(0.1)
        Select(self.proc.driver.find_element(By.ID, "InheriteeBirthdayDay")).select_by_visible_text(f"{int(self.birthday[2])}日")
        sleep(0.1)

        # 死亡日
        Select(self.proc.driver.find_element(By.ID, "InheriteeDateOfDeathYear")).select_by_visible_text(self.passed_away_date[0] + '年')
        sleep(0.1)
        Select(self.proc.driver.find_element(By.ID, "InheriteeDateOfDeathMonth")).select_by_visible_text(f"{int(self.passed_away_date[1])}月")
        sleep(0.1)
        Select(self.proc.driver.find_element(By.ID, "InheriteeDateOfDeathDay")).select_by_visible_text(f"{int(self.passed_away_date[2])}日")
        sleep(0.1)

        # 金融機関
        Select(self.proc.driver.find_element(By.ID, 'InheriteeFinancialInstitution1')).select_by_visible_text(
            "三菱UFJ銀行（金融機関コード：0005）")
        sleep(0.5)

        banks = utils.bank_search(name='三菱UFJ銀行')
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                print(self.branch_name, bank[1])
                print(self.branch_name, utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))

                # 店番
                self.proc.driver.find_element(By.ID, f'InheriteeOfficeNumber1').send_keys(utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))

                # 店名
                self.proc.driver.find_element(By.ID, f'InheriteeOfficeName1').send_keys(self.branch_name)

        # 科目
        if '普通' in self.subjects:
            Select(self.proc.driver.find_element(By.ID, f'InheriteeAccountType1')).select_by_visible_text("普通預金（総合口座）")
        elif '定期' in self.subjects:
            Select(self.proc.driver.find_element(By.ID, f'InheriteeAccountType1')).select_by_visible_text("定期預金")
        elif '貯蓄' in self.subjects:
            Select(self.proc.driver.find_element(By.ID, f'InheriteeAccountType1')).select_by_visible_text("貯蓄預金")
        elif '当座' in self.subjects:
            Select(self.proc.driver.find_element(By.ID, f'InheriteeAccountType1')).select_by_visible_text("当座預金")
        elif '外貨' in self.subjects:
            Select(self.proc.driver.find_element(By.ID, f'InheriteeAccountType1')).select_by_visible_text("外貨預金")

        # 口座番号
        self.proc.driver.find_element(By.ID, f'InheriteeAccountType1').send_keys(str(self.bank_account_number).zfill(7))

        # 次へ
        self.proc.driver.find_element(By.XPATH, '//*[@id="form0"]/nav/ul/li[2]/a').click()
        sleep(0.5)

        # 姓名
        self.proc.driver.find_element(By.ID, 'NotifierLastName').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.ID, 'NotifierFirstName').send_keys(f'森町翼({self.code})')
        self.proc.driver.find_element(By.ID, 'NotifierLastNameKana').send_keys('モリマチ')
        self.proc.driver.find_element(By.ID, 'NotifierFirstNameKana').send_keys('ツバサ')

        # 住所
        # 上記以外をクリック
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[3]/ul/li/div/label[2]").click()
        sleep(0.5)
        self.proc.driver.find_element(By.ID, 'NotifierZipCode1').send_keys('103')
        self.proc.driver.find_element(By.ID, 'NotifierZipCode2').send_keys('0028')
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[4]/div/ul/li/dl/dd/input[3]").click()
        sleep(0.5)
        self.proc.driver.find_element(By.ID, 'NotifierAddress').send_keys('1-7-20 八重洲口会館2階')

        # 電話番号
        self.proc.driver.find_element(By.ID, 'NotifierPhoneNumber11').send_keys('050')
        self.proc.driver.find_element(By.ID, 'NotifierPhoneNumber12').send_keys('6864')
        self.proc.driver.find_element(By.ID, 'NotifierPhoneNumber13').send_keys('7034')

        # 電話番号種類
        Select(self.proc.driver.find_element(By.ID, "NotifierPhoneType1")).select_by_visible_text("勤務先")

        # お亡くなりになられた方からみたご関係
        Select(self.proc.driver.find_element(By.ID, "NotifierRelationship")).select_by_visible_text("その他")
        sleep(0.5)
        self.proc.driver.find_element(By.ID, 'NotifierRelationshipOther').send_keys('代理人')

        # 次へ
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/nav/ul/li[2]/a/p").click()
        sleep(0.5)

        # 遺言書有無
        # なし
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[1]/ul/li/div/label[2]").click()
        # if self.rg_will.value == '有':
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="form0"]/div[1]/ul/li/div/label[1]').click()
        # else:
        #     self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[1]/ul/li/div/label[2]").click()
        sleep(0.5)

        # 遺産分割協議書
        # わからない
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[3]/ul[2]/li/div/label[4]").click()
        # if self.rg_discussed_document.value == '有':
        #     # 作成予定
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="form0"]/div[3]/ul[2]/li/div/label[3]').click()
        # else:
        #     # わからない
        #     self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[3]/ul[2]/li/div/label[4]").click()
        sleep(0.5)

        # 相続手続書類の郵送を希望する
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[6]/ul[2]/li/div/label[1]").click()
        sleep(0.5)

        # 郵送先
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[8]/ul[1]/li/div/label[2]").click()
        sleep(0.5)

        # 残高証明書
        self.proc.driver.find_element(By.XPATH, '//*[@id="form0"]/div[7]/ul[2]/li/div/label[1]').click()
        # if self.rg_balance_certificate.value == '有':
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="form0"]/div[7]/ul[2]/li/div/label[1]').click()
        # else:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="form0"]/div[7]/ul[2]/li/div/label[2]').click()

        # 次へ
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/nav/ul/li[2]/a/p").click()
        sleep(0.5)

    def balance_certificate_create(self):
        pdf = PdfCreate("A4")

        pdf.draw_string(30, 265.5, '103', 8)
        pdf.draw_string(46, 265.5, '0028', 8)
        pdf.draw_string(47, 260.2, '〇', 15)
        pdf.draw_string(31, 257, '東京', 12)
        pdf.draw_string(65, 257, '中央区', 12)
        pdf.draw_string(31, 248, '八重洲1-7-20  八重洲口会館2階', 12)
        pdf.draw_string(135, 249, '050', 10)
        pdf.draw_string(135, 240, '6864', 10)
        pdf.draw_string(154, 240, '7034', 10)
        pdf.draw_string(26, 240, f'被相続人　{self.customer_name}　相続人　{self.heir_name}')
        pdf.draw_string(26, 235, '代理人　行政書士法人チェスター　代表社員　清水　茜作')

        pdf.draw_string(53, 220, self.customer_name, 12)

        # 証明日
        deathday = self.deathday
        pdf.draw_string(37.5, 193.5, str(deathday[0]).zfill(2)[0], 12)
        pdf.draw_string(43.5, 193.5, str(deathday[0]).zfill(2)[1], 12)
        pdf.draw_string(37+18.5, 193.5, str(deathday[1]).zfill(2)[0], 12)
        pdf.draw_string(37+25, 193.5, str(deathday[1]).zfill(2)[1], 12)
        pdf.draw_string(37+37, 193.5, str(deathday[2]).zfill(2)[0], 12)
        pdf.draw_string(37+43.5, 193.5, str(deathday[2]).zfill(2)[1], 12)

        ### 残高証明書 ###
        rec_row = []
        banks = utils.bank_search(name='三菱UFJ銀行')
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                print(self.branch_name, bank[1])
                print(self.branch_name, utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))
                branch_code = utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name)

        i = 0
        bool = 0
        pdf.draw_string(9, (181 - i * 7), str(branch_code).zfill(3)[0], 11)
        pdf.draw_string(16, (181 - i * 7), str(branch_code).zfill(3)[1], 11)
        pdf.draw_string(24, (181 - i * 7), str(branch_code).zfill(3)[2], 11)

        pdf.draw_string(30, (181 - i * 7), self.branch_name.replace('支店', ''), 11)

        if '普通' in self.subjects:
            pdf.draw_string(73.3, (183.2 - i * 7), '✓', 10)
        else:
            pdf.draw_string(71, (178 - i * 7), '✓', 10)
            pdf.draw_string(85, (178.5 - i * 7), self.subjects.replace('預金', ''), 8)

        if '定期' in self.subjects:
            bool = 1
            rec_row.append(i)

        pdf.draw_string(122, (182 - i * 7), str(self.bank_account_number).zfill(7)[0], 11)
        pdf.draw_string(130, (182 - i * 7), str(self.bank_account_number).zfill(7)[1], 11)
        pdf.draw_string(138, (182 - i * 7), str(self.bank_account_number).zfill(7)[2], 11)
        pdf.draw_string(145.5, (182 - i * 7), str(self.bank_account_number).zfill(7)[3], 11)
        pdf.draw_string(153, (182 - i * 7), str(self.bank_account_number).zfill(7)[4], 11)
        pdf.draw_string(161, (182 - i * 7), str(self.bank_account_number).zfill(7)[5], 11)
        pdf.draw_string(169, (182 - i * 7), str(self.bank_account_number).zfill(7)[6], 11)

        pdf.draw_string(192, (182 - i * 7), '1', 11)

        # bool = 0
        # rec_row = []
        # for i, bank_apdfount_record in enumerate(self.customer):
        #     print(bank_apdfount_record["支店名"], bank_apdfount_record["口座番号"], bank_apdfount_record["種類"])
        #     pdf.draw_string(9, (215 - i * 7), str(bank_apdfount_record["店番号"]).zfill(3)[0], 11)
        #     pdf.draw_string(16, (215 - i * 7), str(bank_apdfount_record["店番号"]).zfill(3)[1], 11)
        #     pdf.draw_string(24, (215 - i * 7), str(bank_apdfount_record["店番号"]).zfill(3)[2], 11)
        #
        #     pdf.draw_string(35, (215 - i * 7), bank_apdfount_record["支店名"], 11)
        #
        #     if '普通' in bank_apdfount_record["種類"]:
        #         pdf.draw_string(72, (217 - i * 7), '✓', 8)
        #     else:
        #         pdf.draw_string(72, (214 - i * 7), '✓', 8)
        #         pdf.draw_string(85, (214.5 - i * 7), bank_apdfount_record["種類"].replace('預金', ''), 8)
        #
        #     if '定期' in bank_apdfount_record["種類"]:
        #         bool = 1
        #         rec_row.append(i)
        #
        #     pdf.draw_string(114, (215 - i * 7), str(bank_apdfount_record["口座番号"]).zfill(7)[0], 11)
        #     pdf.draw_string(122, (215 - i * 7), str(bank_apdfount_record["口座番号"]).zfill(7)[1], 11)
        #     pdf.draw_string(130, (215 - i * 7), str(bank_apdfount_record["口座番号"]).zfill(7)[2], 11)
        #     pdf.draw_string(138, (215 - i * 7), str(bank_apdfount_record["口座番号"]).zfill(7)[3], 11)
        #     pdf.draw_string(145.5, (215 - i * 7), str(bank_apdfount_record["口座番号"]).zfill(7)[4], 11)
        #     pdf.draw_string(153, (215 - i * 7), str(bank_apdfount_record["口座番号"]).zfill(7)[5], 11)
        #     pdf.draw_string(161, (215 - i * 7), str(bank_apdfount_record["口座番号"]).zfill(7)[6], 11)
        #
        #     pdf.draw_string(192, (215 - i * 7), '1', 11)

        ### 経過利息 ###
        if bool == 1:
            deathday = re.findall('[0-9]+', utils.convert_to_wareki2(self.deathday))
            pdf.draw_string(40, 137, str(deathday[0]).zfill(2)[0], 12)
            pdf.draw_string(46, 137, str(deathday[0]).zfill(2)[1], 12)
            pdf.draw_string(58, 137, str(deathday[1]).zfill(2)[0], 12)
            pdf.draw_string(65, 137, str(deathday[1]).zfill(2)[1], 12)
            pdf.draw_string(77, 137, str(deathday[2]).zfill(2)[0], 12)
            pdf.draw_string(82, 137, str(deathday[2]).zfill(2)[1], 12)

        for i, rec in enumerate(rec_row):
            pdf.draw_string(9, (123 - i * 7), str(branch_code).zfill(3)[0], 11)
            pdf.draw_string(16, (123 - i * 7), str(branch_code).zfill(3)[1], 11)
            pdf.draw_string(24, (123 - i * 7), str(branch_code).zfill(3)[2], 11)

            pdf.draw_string(35, (123 - i * 7), self.branch_name, 11)
            pdf.draw_string(80, (123 - i * 7), self.subjects.replace('預金', ''), 11)

            pdf.draw_string(114, (123 - i * 7), str(self.bank_account_number).zfill(7)[0], 11)
            pdf.draw_string(122, (123 - i * 7), str(self.bank_account_number).zfill(7)[1], 11)
            pdf.draw_string(130, (123 - i * 7), str(self.bank_account_number).zfill(7)[2], 11)
            pdf.draw_string(138, (123 - i * 7), str(self.bank_account_number).zfill(7)[3], 11)
            pdf.draw_string(145.5, (123 - i * 7), str(self.bank_account_number).zfill(7)[4], 11)
            pdf.draw_string(153, (123 - i * 7), str(self.bank_account_number).zfill(7)[5], 11)
            pdf.draw_string(161, (123 - i * 7), str(self.bank_account_number).zfill(7)[6], 11)

            pdf.draw_string(166, (125 - i * 7), '✓', 10)
            pdf.draw_string(194, (125 - i * 7), '1', 8)
            # bool = 0



        ### 受取方法 ###
        # pdf.draw_string(22, 53, '✓', 8)

        if os.name == 'nt':
            print('nt')
            output_path = r'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\G2069臼杵優子様（スタンダードプラン）\09.申請書類\01.残証申請書類'

        elif os.name == 'posix':
            print('posix')
            output_path = os.path.dirname(os.path.dirname(os.getcwd()))

        print('output_path:', output_path)
        path1 = os.path.join(output_path, f'【{self.code}】{self.heir[0]}様_三菱UFJ銀行_残高証明書・取引明細書依頼書1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf', '三菱UFJ銀行_残高証明書・取引明細書依頼書.pdf'), page=5, open_bool=False)


        # 書類2
        pdf = PdfCreate("A4")
        pdf.draw_string(30, 265.5, '103', 8)
        pdf.draw_string(46, 265.5, '0028', 8)
        pdf.draw_string(47.3, 259.8, '〇', 15)
        pdf.draw_string(31, 257, '東京', 12)
        pdf.draw_string(65, 257, '中央区', 12)
        pdf.draw_string(31, 248, '八重洲1-7-20  八重洲口会館2階', 12)
        pdf.draw_string(26, 241, f'被相続人　{self.customer_name}　相続人　{self.heir_name}')
        pdf.draw_string(26, 236, '代理人　行政書士法人チェスター　代表社員　清水　茜作')
        pdf.draw_string(26, 231.5, f'担当：森町（{self.code}）')
        path2 = os.path.join(output_path, f'【{self.code}】{self.heir[0]}様_三菱UFJ銀行_残高証明書・取引明細書依頼書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf', '三菱UFJ銀行_残高証明書・取引明細書依頼書.pdf'), page=6, open_bool=False)

        # # 書類3
        # pdf = PdfCreate("A4")
        # pdf.draw_string(30, 265.5, '103', 8)
        # pdf.draw_string(46, 265.5, '0028', 8)
        # pdf.draw_string(47.5, 260, '〇', 16)
        # pdf.draw_string(31, 257, '東京', 12)
        # pdf.draw_string(65, 257, '中央区', 12)
        # pdf.draw_string(31, 248, '八重洲1-7-20  八重洲口会館2階', 12)
        # pdf.draw_string(31, 240, '行政書士法人チェスター　代表社員　清水　茜作', 10)
        # pdf.draw_string(31, 235, f'担当：森町（{self.code}）', 10)
        # path3 = os.path.join(output_path, f'【{self.code}】{self.heir[0]}様_三菱UFJ銀行_残高証明書・取引明細書依頼書3.pdf')
        # pdf.pdf_save(path3, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
        #                                  '三菱UFJ銀行_残高証明書・取引明細書依頼書.pdf'), page=3, open_bool=False)

        pdf.pdf_marge(
            os.path.join(output_path, f'{self.code}{self.heir[0]}様_三菱UFJ銀行_残高証明書・取引明細書依頼書_{self.date[0]}{self.date[1]}{self.date[2]}.pdf'),
            path1, path2)

    def reservation(self):
        self.proc = Web()
        # 新丸の内支店（徒歩１０分）
        url = 'https://airrsv.net/AKR2137240529/calendar'
        self.proc.web_open(url)
        messagebox.showinfo("待機中", "「予約するボタンを押下後」にOKボタンをクリックしてください。")
        self.proc.web_operation(self.proc.driver.current_url)
        self.proc.driver.implicitly_wait(10)
        # フォームの存在を確認
        WebDriverWait(self.proc.driver, 10).until(
            EC.presence_of_element_located((By.ID, "frontStaffBookingEditForm"))
        )

        # --- 1. ご予約者様情報の入力 (必須) ---

        # フリガナ（セイ）(name="lastNmKn")
        self.proc.driver.find_element(By.NAME, "lastNmKn").send_keys('ギョウセイショシホウジンチェスター　モリマチ')

        # フリガナ（メイ）(name="firstNmKn")
        self.proc.driver.find_element(By.NAME, "firstNmKn").send_keys(KANA_MEI)

        # 名前（姓）(name="lastNm")
        self.proc.driver.find_element(By.NAME, "lastNm").send_keys(KANJI_SEI)

        # 名前（名）(name="firstNm")
        self.proc.driver.find_element(By.NAME, "firstNm").send_keys(KANJI_MEI)

        # 電話番号 (name="tel1")
        self.proc.driver.find_element(By.NAME, "tel1").send_keys(TEL_NUMBER)

        # メールアドレス (name="mailAddress1")
        self.proc.driver.find_element(By.NAME, "mailAddress1").send_keys(EMAIL_ADDRESS)

        # メールアドレス（確認用）(name="mailAddress1ForCnfrm")
        self.proc.driver.find_element(By.NAME, "mailAddress1ForCnfrm").send_keys(EMAIL_ADDRESS)

        # --- 2. お亡くなりになった方の情報（生年月日とお客様番号）の入力 (必須) ---

        # 生年月日（年）(name="birthdayYyyy")
        Select(self.proc.driver.find_element(By.NAME, "birthdayYyyy")).select_by_value(BIRTH_YEAR)

        # 生年月日（月）(name="birthdayMm")
        Select(self.proc.driver.find_element(By.NAME, "birthdayMm")).select_by_value(BIRTH_MONTH)

        # 生年月日（日）(name="birthdayDd")
        Select(self.proc.driver.find_element(By.NAME, "birthdayDd")).select_by_value(BIRTH_DAY)

        # お客様番号 (name="cstmrNo")
        self.proc.driver.find_element(By.NAME, "cstmrNo").send_keys(CSTMR_NO)

        # --- 3. 備考欄の入力 (必須) ---

        # 備考欄 (name="exItem01", id="rmFreeEntry")
        textarea_field = self.proc.driver.find_element(By.ID, "rmFreeEntry")
        textarea_field.clear()  # 既存のテキストがあればクリア
        textarea_field.send_keys(MEMO_DETAILS)

        print("必須項目にデータを入力しました。")
        print(f"備考欄の入力内容: {MEMO_DETAILS[:20]}...")

        # --- 4. フォームの送信 ---

        # 「次へ」ボタンを特定 (type="submit", class="btn is-primary")
        # フォームの送信機能はJavaScriptに依存しているため、クリックが確実です。
        submit_button = self.proc.driver.find_element(By.XPATH, "//button[@type='submit' and text()='次へ']")

        # 実際にフォームを送信したい場合は、以下のコメントを外してください
        # submit_button.click()

    # 相続届
    def inheritance_notification(self):
        pdf = PdfCreate("A3")
        pdf.draw_string(30, 150, '194', 20)

        if os.name == 'nt':
            print('nt')
            output_path = r'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\G2069臼杵優子様（スタンダードプラン）\09.申請書類\02.解約・名変申請書類'

        elif os.name == 'posix':
            print('posix')
            output_path = os.path.dirname(os.path.dirname(os.getcwd()))

        print('output_path:', output_path)
        path1 = os.path.join(output_path, f'【{self.code}】{self.heir[0]}様_三菱UFJ銀行_相続届1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf', '三菱UFJ銀行_相続届.pdf'), page=1, open_bool=False)


        # 書類2
        pdf = PdfCreate("A3")
        path2 = os.path.join(output_path, f'【{self.code}】{self.heir[0]}様_三菱UFJ銀行_相続届2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf', '三菱UFJ銀行_相続届.pdf'), page=2, open_bool=False)


        pdf.pdf_marge(
            os.path.join(output_path, f'{self.code}{self.heir[0]}様_三菱UFJ銀行_相続届.pdf'),
            path1, path2)

def main():
    proc = Mufg()
    # proc.account_freezing()
    # proc.balance_certificate_create()
    proc.reservation()
    # proc.inheritance_notification()

if __name__ == '__main__':
    main()