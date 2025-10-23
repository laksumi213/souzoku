# マネックス証券
import jaconv
import mojimoji
import re
from app._utils.web_operation import Web
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
from pyautogui import typewrite, hotkey, position, press, moveTo
from app.controllers.pdf_create import PdfCreate
import os
import app.utils as utils
from datetime import datetime
from tkinter import messagebox

class Monex:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.bank_account_number = mojimoji.han_to_zen(str('').zfill(7))
        self.branch_name = ''
        self.subjects = ''
        self.birthday = re.findall('[0-9]+', '1958/9/18')
        self.address = '千葉県船橋市夏見台1-13-24'
        self.building = ''
        self.passed_away_date = re.findall('[0-9]+', '2025/6/27')
        self.heir_name = '宇野　美穂'
        self.heir_name_kana = 'うの　みほ'
        self.heir_address = '千葉県船橋市夏見台1-13-24'
        self.heir_building = ''

        self.date = re.findall(r'\d+', datetime.now().strftime('%Y/%m/%d'))

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　', '')}様（フルサポートプラン）\07.申請書類\01.残証申請書類'
        elif os.name == 'posix':
            print('posix')
            self.output_path = os.path.dirname(os.path.dirname(os.getcwd()))

        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]
        self.zipcode = utils.get_zipcode_from_address(self.address)
        print('address:', re.findall(pattern, self.address)[0])
        print('self.zipcode:', self.zipcode)

        heir_address = re.findall(pattern, self.heir_address)[0]
        self.heir_zipcode = re.findall('[0-9]+', utils.get_zipcode_from_address(heir_address))
        print('heir_address:', re.findall(pattern, self.heir_address)[0])
        print('utils.get_zipcode_from_address(address):', self.heir_zipcode)

        match = re.search(r'([^\d]+)(\d.*)', address[2])
        if match:
            self.place = match.group(1)  # 最初のグループ（数字以外の文字）
            self.number = match.group(2)  # 2番目のグループ（数字とハイフンを含む部分）
            print(f"場所: {self.place}")  # 出力: 場所: 夏見台
            print(f"番地: {self.number}")

        self.name = re.findall(r'^(.*?)[ 　](.*)$', self.customer_name)[0]
        print('被相続人', self.name)

        self.name_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.customer_name_kana))[0]
        print('被相続人カナ', self.name_kana)

        self.heir = re.findall(r'^(.*?)[ 　](.*)$', self.heir_name)[0]
        print('相続人', self.heir)

        self.heir_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.heir_name_kana))[0]
        print('相続人カナ', self.heir_kana)

        banks = utils.bank_search(name='SBI新生銀行')
        self.branch_code = ''
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                self.branch_code = mojimoji.han_to_zen(
                    utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))
                print('self.branch_code:', self.branch_code)

    # 口座凍結
    def account_freezing(self):
        self.proc = Web()
        url = 'https://seminar2.monex.co.jp/public/application/add/48758'
        self.proc.web_open(url)
        self.proc.driver.implicitly_wait(10)
        WebDriverWait(self.proc.driver, 10).until(
            EC.presence_of_element_located((By.ID, "input_form"))
        )

        # ----------------------------------------------------
        # I. 被相続人情報 (すべて必須)
        # ----------------------------------------------------

        # 被相続人名（漢字）
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_name1").send_keys(self.name[0])
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_name2").send_keys(self.name[1])

        # 被相続人名（カナ）
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_name1_ka").send_keys(self.name_kana[0])
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_name2_ka").send_keys(self.name_kana[1])

        # 被相続人の生年月日
        Select(self.proc.driver.find_element(By.NAME,
                                   "Public::Application::Userenquete_D__P__D_VisitorData.attribute15")).select_by_visible_text(
            f'{self.birthday[0]}年')
        Select(self.proc.driver.find_element(By.NAME,
                                   "Public::Application::Userenquete_D__P__D_VisitorData.attribute10")).select_by_visible_text(
            f'{self.birthday[1]}月')
        Select(self.proc.driver.find_element(By.NAME,
                                   "Public::Application::Userenquete_D__P__D_VisitorData.attribute16")).select_by_visible_text(
            f'{self.birthday[2]}日')

        # 死亡年月日
        Select(self.proc.driver.find_element(By.NAME,
                                   "Public::Application::Userenquete_D__P__D_VisitorData.attribute21")).select_by_visible_text(
            f'{self.passed_away_date[0]}年')
        Select(self.proc.driver.find_element(By.NAME,
                                   "Public::Application::Userenquete_D__P__D_VisitorData.attribute20")).select_by_visible_text(
            f'{self.passed_away_date[1]}月')
        Select(self.proc.driver.find_element(By.NAME,
                                   "Public::Application::Userenquete_D__P__D_VisitorData.attribute22")).select_by_visible_text(
            f'{self.passed_away_date[2]}日')

        print("被相続人情報を入力しました。")

        # ----------------------------------------------------
        # II. 手続受任者情報 (すべて必須)
        # ----------------------------------------------------

        # 法人名称
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7876").send_keys(
            '行政書士法人チェスター')
        # 本支店もしくは部署名
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7877").send_keys(
            '東京本店')
        # 手続名義人
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7878").send_keys(
            f'故{self.customer_name}様　相続人{self.heir_name}様　代理人　行政書士法人チェスター　代表社員　清水　茜作')
        # 担当者名
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7880").send_keys(
            f'事務担当　森町　翼')
        # 担当者名（カナ）
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7881").send_keys(
            'モリマチ　ツバサ')
        # 連絡先メールアドレス
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7886").send_keys('t.morimachi_gy@chester-tax.com')
        # 連絡先電話番号
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7887").send_keys('050-6864-7034')

        # ----------------------------------------------------
        # III. 郵送先情報 (すべて必須)
        # ----------------------------------------------------

        # 郵送先［宛名］
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute8093").send_keys(
            f'行政書士法人チェスター　森町　翼（{self.code}）')
        # 郵送先［郵便番号］
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7870").send_keys('1030028')
        # 郵送先［都道府県］
        Select(self.proc.driver.find_element(By.NAME,
                                   "Public::Application::Userenquete_D__P__D_Enquete.attribute7304")).select_by_value(
            '13')
        # 郵送先［市区郡］
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7871").send_keys(
            '中央区')
        # 郵送先［町村番地］
        self.proc.driver.find_element(By.NAME, "Public::Application::Userenquete_D__P__D_Enquete.attribute7872").send_keys(
            '八重洲一丁目7-20')

        self.proc.driver.find_element(By.NAME, 'Public::Application::Userenquete_D__P__D_Enquete.attribute7873').send_keys('八重洲口会館2階')

        # ----------------------------------------------------
        # IV. 受任業務と相続方法 (必須)
        # ----------------------------------------------------

        # 受任業務: 遺産整理 (value="1") を選択
        self.proc.driver.find_element(By.XPATH,
                            "//input[@name='Public::Application::Userenquete_D__P__D_Enquete.attribute7580' and @value='1']").click()

        # 当社資産の相続方法: 分割相続（相続人複数名で相続する）(value="3") を選択
        self.proc.driver.find_element(By.XPATH,
                            "//input[@name='Public::Application::Userenquete_D__P__D_Enquete.attribute7931' and @value='3']").click()

        print("受任者情報を入力しました。")
        print("すべての必須項目にデータが入力されました。")

        # ----------------------------------------------------
        # V. フォームの送信
        # ----------------------------------------------------

        # フォームの「次へ（入力内容確認）」ボタンはJavaScriptで挿入される（class="js_submit_btn"）ため、
        # フォームIDを取得し、JavaScriptでサブミットするのが安全です。

        # マネックス証券のフォームでは、SubmitボタンのHTMLがJavaScriptで置き換えられる仕様のため、
        # フォーム内の隠し要素を操作し、JavaScriptでフォームを送信します。

        # フォーム要素を特定
        form_element = self.proc.driver.find_element(By.ID, "input_form")

        # JavaScriptでフォームを直接サブミット
        self.proc.driver.execute_script("arguments[0].submit();", form_element)

    # 残高証明書
    def balance_certificate(self):
        pdf = PdfCreate("A4")

        pdf.draw_string(23, 193, f'相続人　{self.heir_name}　代理人', 10)
        pdf.draw_string(23, 188, f'行政書士法人チェスター　代表社員　清水　茜作', 10)

        pdf.draw_string(63, 55, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        pdf.draw_string(63, 37, f'行政書士法人チェスター　森町（{self.code}）', 12)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_SBI申請銀行_残高証明書依頼書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'SBI新生銀行_残高証明書発行依頼書.pdf'), page=1, open_bool=True)

        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三菱UFJモルガン・スタンレー証券_相続に関する届出書.pdf'), page=2, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path,
                         f'{self.code}{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書_{self.date[0]}{self.date[1]}{self.date[2]}.pdf'),
            path1, path2)

    def reservation(self):
        self.proc = Web()
        url = ''
        self.proc.web_open(url)
        self.proc.self.proc.driver.implicitly_wait(10)
        Webself.proc.driverWait(self.proc.self.proc.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "reserveform"))
        )

if __name__ == '__main__':
    cl = Monex()
    cl.account_freezing()
    # cl.balance_certificate()
    # cl.inheritance_notification_create()
    # cl.reservation()  # 来店予約


