# 栃木銀行
import jaconv
import mojimoji
import re
from app._utils.web_operation import Web
from time import sleep
from pyautogui import typewrite, hotkey, position, press, moveTo
from app.controllers.pdf_create import PdfCreate
import os
import app.utils as utils
from datetime import datetime
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

class TochigiBank:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.bank_account_number = '1099427'
        if self.bank_account_number:
            mojimoji.han_to_zen(str(self.bank_account_number).zfill(7))
        self.branch_name = ''
        self.subjects = ''
        self.birthday = '1958/9/18'
        self.address = '千葉県船橋市夏見台1-13-24'
        self.building = ''
        self.passed_away_date = '2025-06-27'
        self.heir_name = '宇野　美穂'
        self.heir_name_kana = 'うの　みほ'
        self.heir_address = '千葉県船橋市夏見台1-13-24'
        self.heir_building = ''

        self.ad_b = utils.convert_to_wareki2(self.birthday)
        self.ad_number_b = re.findall(r'\d+', self.ad_b)
        self.birthday = re.findall('[0-9]+', self.birthday)

        self.ad_d = utils.convert_to_wareki2(self.passed_away_date)
        self.ad_number_d = re.findall(r'\d+', self.ad_d)
        self.passed_away_date = re.findall('[0-9]+', self.passed_away_date)

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
        # 携帯電話番号の入力と画像認証
        self.proc = Web()
        url = 'https://reg31.smp.ne.jp/regist/is?SMPFORM=qglf-maogrb-8c5822ce307c7fc28d1bbecca1beec1b&inFlow=1'
        self.proc.web_open(url)
        self.proc.driver.implicitly_wait(10)  # 要素が見つかるまでの最大待機時間（秒）

        # ページ上のJavaScript関数 'load()' を手動で実行（オプショナル）
        # フォームの初期状態を整えるため、一部のJavaScript関数を実行
        self.proc.driver.execute_script("load()")

        ## 1. お亡くなりになられた方の情報（被相続人）の入力

        # 氏名
        self.proc.driver.find_element(By.ID, "hi_nameSei").send_keys(self.name[0])
        self.proc.driver.find_element(By.ID, "hi_nameMei").send_keys(self.name[1])

        # シメイ（自動かな入力が設定されているが、ここでは手動で入力）
        self.proc.driver.find_element(By.ID, "hi_nameSeiK").send_keys(self.name_kana[0])
        self.proc.driver.find_element(By.ID, "hi_nameMeiK").send_keys(self.name_kana[1])

        # 生年月日 (<select>タグ)
        Select(self.proc.driver.find_element(By.ID, "input_wareki")).select_by_visible_text(self.ad_b[0:2])
        Select(self.proc.driver.find_element(By.ID, "input_YY")).select_by_value(self.ad_number_b[0])
        Select(self.proc.driver.find_element(By.ID, "input_MM")).select_by_value(self.ad_number_b[1])
        Select(self.proc.driver.find_element(By.ID, "input_DD")).select_by_value(self.ad_number_b[2])

        # 死亡日 (<select>タグ)
        Select(self.proc.driver.find_element(By.ID, "input_D_YY")).select_by_value(self.ad_number_d[0])
        Select(self.proc.driver.find_element(By.ID, "input_D_MM")).select_by_value(self.ad_number_d[1])
        Select(self.proc.driver.find_element(By.ID, "input_D_DD")).select_by_value(self.ad_number_d[2])

        # 郵便番号（分割された入力フィールド）
        self.proc.driver.find_element(By.NAME, "hi_zipcode:a").send_keys(self.zipcode[:3])
        self.proc.driver.find_element(By.NAME, "hi_zipcode:t").send_keys(self.zipcode[4:])
        sleep(1)

        # 住所
        # Select(self.proc.driver.find_element(By.NAME, "hi_pref")).select_by_visible_text(HI_PREF)
        self.proc.driver.find_element(By.NAME, "hi_addr").send_keys(self.number)
        # 建物名・部屋番号 (必須ではない)
        if self.building:
            self.proc.driver.find_element(By.NAME, "hi_bldg").send_keys(self.building)

        # お取引口座支店名、口座科目、口座番号、取引有無（必須ではない）
        if self.branch_name:
            self.proc.driver.find_element(By.NAME, "hi_bsName").send_keys(self.branch_name)

        if self.subjects:
            try:
                Select(self.proc.driver.find_element(By.NAME, "hi_accType")).select_by_visible_text(self.subjects)
            except:
                pass

        if self.bank_account_number:
            self.proc.driver.find_element(By.NAME, "hi_accNo").send_keys(self.bank_account_number)

        # self.proc.driver.find_element(By.NAME, "hi_torihikiChk").click()  # その他取引ありにチェック

        ## 2. 確認事項の選択

        # 次の書類がある場合...：遺言書と遺産分割協議書にチェック
        # self.proc.driver.find_element(By.XPATH, "//input[@name='chk_01' and @value='1']").click()  # 遺言書
        self.proc.driver.find_element(By.XPATH, "//input[@name='chk_01' and @value='4']").click()  # 遺産分割協議書

        # 預金の分割について話し合いはお済ですか：いいえ
        self.proc.driver.find_element(By.XPATH, "//input[@name='chk_02' and @value='2']").click()

        # 相続人間で調停等問題が発生していませんか【必須】：いいえ
        self.proc.driver.find_element(By.XPATH, "//input[@name='chk_03' and @value='2']").click()

        ## 3. 相続手続き依頼人さまの情報の入力


        # 氏名
        self.proc.driver.find_element(By.ID, "c_nameSei").send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.ID, "c_nameMei").send_keys(f'清水茜作 担当 森町{self.code}')

        # シメイ
        self.proc.driver.find_element(By.ID, "c_nameSeiK").clear()
        self.proc.driver.find_element(By.ID, "c_nameSeiK").send_keys('ギョウセイショシホウジンチェスター')
        self.proc.driver.find_element(By.ID, "c_nameMeiK").clear()
        self.proc.driver.find_element(By.ID, "c_nameMeiK").send_keys('シミズセンサク タントウ モリマチ')

        # お亡くなりになられた方との続柄【必須】: その他
        self.proc.driver.find_element(By.XPATH, f"//input[@name='c_relShip' and @value='12']").click()
        self.proc.driver.find_element(By.ID, 'c_relShip_other').send_keys('代理人')

        # ご連絡先電話番号
        self.proc.driver.find_element(By.NAME, "c_telNo:a").send_keys('050')
        self.proc.driver.find_element(By.NAME, "c_telNo:e").send_keys('6864')
        self.proc.driver.find_element(By.NAME, "c_telNo:n").send_keys('7034')

        # ご連絡にご都合のよい時間帯【必須】：9時～12時
        self.proc.driver.find_element(By.XPATH, f"//input[@name='c_time' and @value='1']").click()

        # メールアドレス
        self.proc.driver.find_element(By.NAME, "c_mail").send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.NAME, "c_mail:cf").send_keys('t.morimachi_gy@chester-tax.com')  # 確認用

        # お亡くなりになられた方とご住所が同じ場合はチェックしてください
        # チェックしないため、依頼人住所は被相続人の情報と異なるものとして処理を続行
        self.proc.driver.find_element(By.ID, "c_zipcode_a").send_keys("103")
        self.proc.driver.find_element(By.ID, "c_zipcode_t").send_keys("0028")
        sleep(1)
        # Select(self.proc.driver.find_element(By.ID, "c_pref")).select_by_visible_text("埼玉県")
        self.proc.driver.find_element(By.ID, "c_addr").send_keys("一丁目7-20")
        self.proc.driver.find_element(By.ID, "c_bldg").send_keys("八重洲口会館2階")
        sleep(1)

        ## 4. 同意とフォーム送信

        # 個人情報の取り扱いについて のリンクをクリック (同意チェックボックスを有効化)
        # この要素はaタグでonclickイベントを持っているので、直接クリック
        self.proc.driver.find_element(By.XPATH, "//a[contains(text(), '個人情報の取り扱いについて')]").click()

        # 同意チェックボックスが有効化されるのを待つ
        WebDriverWait(self.proc.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "agreeFlg"))
        )

        # 同意条項に同意します にチェック
        agree_checkbox = self.proc.driver.find_element(By.ID, "agreeFlg")
        if not agree_checkbox.is_selected():
            agree_checkbox.click()
            print("同意条項に同意しました。")
            self.proc.driver.switch_to.window(self.proc.driver.window_handles[-1])
            self.proc.driver.close()
            self.proc.driver.switch_to.window(self.proc.driver.window_handles[-1])

        sleep(1)
        # 「確認画面へ」ボタンが表示されるのを待つ (同意チェック後にJSで表示される)
        submit_button = WebDriverWait(self.proc.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_submit"))
        )
        print("「確認画面へ」ボタンが表示されました。")

        # フォームの送信
        submit_button.click()
        print("フォームを送信しました。")
        # print("フォーム送信は行わず、5秒間待機します。")
        # time.sleep(5)

    # 残高証明書
    def balance_certificate(self):
        pdf = PdfCreate("A4")

        pdf.draw_string(111, 233, self.address)
        pdf.draw_string(111, 226.3, self.customer_name, 12)

        pdf.draw_string(111, 215, '東京都中央区八重洲1-7-20 八重洲口会館2階')
        pdf.draw_string(111, 211, f'相続人　{self.heir_name}')
        pdf.draw_string(111, 207, f'代理人　行政書士法人チェスター')
        pdf.draw_string(111, 203, f'代表社員　清水　茜作')

        pdf.draw_string(27, 185.5, self.customer_name, 14)
        pdf.draw_rect(90, 194, 107, 189)
        pdf.draw_string(135, 185.5, self.passed_away_date[0], 14)
        pdf.draw_string(155, 185.5, self.passed_away_date[1], 14)
        pdf.draw_string(169, 185.5, self.passed_away_date[2], 14)
        pdf.draw_string(77, 172.7, '1', 14)

        pdf.draw_string(72, 145, '全取引', 12)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_栃木銀行_残高証明書依頼書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '栃木銀行_残高証明書依頼書.pdf'), page=2, open_bool=True)

        pdf = PdfCreate("A4")
        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_栃木銀行_残高証明書依頼書_経理依頼用.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '栃木銀行_残高証明書依頼書.pdf'), page=1, open_bool=True)


    def trading_item(self):
        pdf = PdfCreate("A4")

        pdf.draw_string(102, 248, '東京都中央区八重洲1-7-20 八重洲口会館2階')
        pdf.draw_string(102, 244, f'相続人　{self.heir_name}　代理人　行政書士法人チェスター')
        pdf.draw_string(102, 240, f'代表社員　清水　茜作')

        pdf.draw_string(68, 172, self.customer_name, 12)
        pdf.draw_string(140, 172, self.passed_away_date[0], 12)
        pdf.draw_string(160, 172, self.passed_away_date[1], 12)
        pdf.draw_string(176, 172, self.passed_away_date[2], 12)

        pdf.draw_string(64, 162, '〇', 16)

        if self.bank_account_number:
            pdf.draw_string(130, 162, self.bank_account_number, 12)

        pdf.draw_rect(66, 153, 85, 158.5)

        pdf.draw_string(68, 136, '通帳紛失により履歴が確認できないため。', 12)
        pdf.draw_string(102.5, 126, '〇', 18)

        pdf.draw_string(116, 43, '東京都中央区八重洲1-7-20 八重洲口会館2階', 8)
        pdf.draw_string(116, 39, f'相続人　{self.heir_name}　代理人', 8)
        pdf.draw_string(116, 35, f'行政書士法人チェスター　代表社員　清水　茜作', 8)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_栃木銀行_取引明細申請書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '栃木銀行_取引明細申請書.pdf'), page=1, open_bool=True)

        ### 定期　※今回のみ
        pdf = PdfCreate("A4")

        pdf.draw_string(102, 248, '東京都中央区八重洲1-7-20 八重洲口会館2階')
        pdf.draw_string(102, 244, f'相続人　{self.heir_name}　代理人　行政書士法人チェスター')
        pdf.draw_string(102, 240, f'代表社員　清水　茜作')

        pdf.draw_string(68, 172, self.customer_name, 12)
        pdf.draw_string(140, 172, self.passed_away_date[0], 12)
        pdf.draw_string(160, 172, self.passed_away_date[1], 12)
        pdf.draw_string(176, 172, self.passed_away_date[2], 12)

        pdf.draw_rect(85, 162, 98, 167)
        pdf.draw_string(105, 163, '定期', 12)
        pdf.draw_string(130, 162, '1052464', 12)

        pdf.draw_rect(66, 153, 85, 158.5)

        pdf.draw_string(68, 136, '通帳紛失により履歴が確認できないため。', 12)
        pdf.draw_string(102.5, 126, '〇', 18)

        pdf.draw_string(116, 43, '東京都中央区八重洲1-7-20 八重洲口会館2階', 8)
        pdf.draw_string(116, 39, f'相続人　{self.heir_name}　代理人', 8)
        pdf.draw_string(116, 35, f'行政書士法人チェスター　代表社員　清水　茜作', 8)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_栃木銀行_取引明細申請書_定期.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '栃木銀行_取引明細申請書.pdf'), page=1, open_bool=True)

        # pdf = PdfCreate("A4")
        # path2 = os.path.join(self.output_path,
        #                      f'{self.code}{self.heir[0]}様_栃木銀行_取引明細申請書_経理依頼用.pdf')
        # pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
        #                                  '栃木銀行_取引明細申請書.pdf'), page=1, open_bool=True)


if __name__ == '__main__':
    cl = TochigiBank()
    # cl.account_freezing()
    # cl.balance_certificate()
    cl.trading_item()
    # cl.inheritance_notification_create()


