# 横浜銀行
from time import sleep

import jaconv
import mojimoji
import re
from app._utils.web_operation import Web
import app.utils as utils
from pyautogui import typewrite, hotkey, position, press, moveTo
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from app.controllers.pdf_create import PdfCreate
import os
import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class YokohamaBank:
    def __init__(self):
        super().__init__()
        self.proc = None

        self.code = 'G2014'
        self.customer_name = '菅沼　純子'
        self.customer_name_kana = 'すがぬま　すみこ'
        self.heir_name = '菅沼　富男'
        self.heir_name_kana = 'すがぬま　とみお'
        self.bank_store_number = '352'
        self.bank_branch_name = '戸塚南支店'
        self.bank_account_number = '0941366'
        self.birthday = re.findall('[0-9]+', '1937/11/3')
        self.deathday = re.findall('[0-9]+', '2025/6/12')
        self.address = '神奈川県横浜市泉区緑園4丁目3番地1サンステージ緑園都市東の街11番館603号'

        self.date = re.findall(r'\d+', datetime.now().strftime('%Y/%m/%d'))

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　','')}様（スタンダードプラン）\07.申請書類\01.残証申請書類'
        elif os.name == 'posix':
            print('posix')
            self.output_path = os.path.dirname(os.path.dirname(os.getcwd()))

        zipcode = utils.get_zipcode_from_address(self.address)
        self.zipcode = re.findall('[0-9]+', zipcode)
        print('self.zipcode:', self.zipcode)

        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]
        print('address:', re.findall(pattern, self.address)[0])
        print('utils.get_zipcode_from_address(address):', utils.get_zipcode_from_address(address))

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


    def account_freezing(self):
        # url = 'https://service.boy.co.jp/bctrl299-standard/ui/souzoku.html?_gl=1*poehqu*_gcl_au*MTMyMTczNDY1Mi4xNzU3NDgxOTQy*_ga*MTU1OTQ3OTg5MS4xNzU3NDgxOTQz*_ga_G0WHYCTTLZ*czE3NTc0ODE5NDIkbzEkZzEkdDE3NTc0ODQ0OTAkajMxJGwwJGgxMTE5OTkzNzE.*_fplc*akFWR0xkUU1aOXFxUFZHJTJGenM2SjQ0V1dCbm5pSEJXZlVTRVpnJTJCWkNnJTJGVCUyRmgydGxlVVpybUFIeEtrcEVRRk1wS2dOUzV0MjRmaDFqU25nT0lSZVU1REZLM2JOVkI0bTdteTJKRDVhdXRmQ0s0S2FYMlBPcWVuTm5GVkNOM2clM0QlM0Q.'
        url = 'https://service.boy.co.jp/bctrl299-standard/ui/souzoku.html?_gl=1*1glomly*_gcl_au*MTMyMTczNDY1Mi4xNzU3NDgxOTQy*_ga*MTU1OTQ3OTg5MS4xNzU3NDgxOTQz*_ga_G0WHYCTTLZ*czE3NTc0ODE5NDIkbzEkZzEkdDE3NTc0ODQ2MDgkajYwJGwwJGgxMTE5OTkzNzE.*_fplc*akFWR0xkUU1aOXFxUFZHJTJGenM2SjQ0V1dCbm5pSEJXZlVTRVpnJTJCWkNnJTJGVCUyRmgydGxlVVpybUFIeEtrcEVRRk1wS2dOUzV0MjRmaDFqU25nT0lSZVU1REZLM2JOVkI0bTdteTJKRDVhdXRmQ0s0S2FYMlBPcWVuTm5GVkNOM2clM0QlM0Q.'

        self.proc = Web()
        self.proc.web_open(url)
        actions = ActionChains(self.proc.driver)

        x, y = position()
        print(f"X座標: {x}, Y座標: {y}")

        self.url = self.proc.driver.current_url
        print('web url:', self.url)
        time.sleep(8)
        moveTo(950, 340)
        # time.sleep(.1)
        # press('tab')
        # time.sleep(.1)
        # press('tab')
        # time.sleep(.1)
        # press('tab')
        press('tab', presses=3)
        time.sleep(.1)
        press('space')
        time.sleep(.1)
        press('tab', presses=2)
        time.sleep(.1)
        press('space')
        time.sleep(.1)
        press('tab')
        press('space')
        time.sleep(1)

        press('tab')
        # typewrite('t.morimachi_gy@chester-tax.com')
        pyperclip.copy('t.morimachi_gy@chester-tax.com')
        hotkey('ctrl', 'v')
        time.sleep(.1)
        press('tab')
        time.sleep(.1)
        hotkey('shift', 'tab')
        # press('space')

        # Tkinterのルートウィンドウを作成（メッセージボックスの表示に必要だが、画面には表示されない）
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを非表示にする

        # メッセージボックスの表示
        # showinfo(タイトル, メッセージ)
        messagebox.showinfo("メールアドレス認証", "認証完了後にOKを押してください。")

        # ここから情報入力
        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]
        print(utils.get_zipcode_from_address(address))

        match = re.search(r'([^\d]+)(\d.*)', address[2])
        if match:
            place = match.group(1) # 最初のグループ（数字以外の文字）
            number = match.group(2)  # 2番目のグループ（数字とハイフンを含む部分）
            print(f"場所: {place}") # 出力: 場所: 夏見台
            print(f"番地: {number}")

        zipcode = utils.get_zipcode_from_address(self.address)
        zipcode = re.findall('[0-9]+', zipcode)
        print('zipcode:', zipcode)

        self.passed_away_date = re.findall('[0-9]+', '2025-06-27')

        name = re.findall(r'^(.*?)[ 　](.*)$', self.customer_name)[0]
        print('被相続人', name)

        name_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.customer_name_kana))[0]
        print('被相続人カナ', name_kana)

        heir = re.findall(r'^(.*?)[ 　](.*)$', self.heir_name)[0]
        print('相続人', heir)

        heir_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.heir_name_kana))[0]
        print('相続人カナ', heir_kana)

        print(address)
        print('self.birthday:', self.birthday)
        print('self.passed_away_date:', self.passed_away_date)

        self.proc.web_operation(self.url)

        # 1. 外側の iframe に切り替え (ID="smallchatframe"を使用)
        self.proc.driver.switch_to.frame("smallchatframe")  # IDを直接文字列で渡す

        # 2. 内側の iframe に切り替え (class="html_content_area sound_inited"を使用)
        # classをCSSセレクタで指定して WebElement を取得
        inner_iframe_selector = "iframe.html_content_area.sound_inited"
        inner_iframe_element = self.proc.driver.find_element(By.CSS_SELECTOR, inner_iframe_selector)

        # 内側の iframe にフォーカスを切り替え
        self.proc.driver.switch_to.frame(inner_iframe_element)

        self.proc.driver.find_element(By.NAME, 'family_name').send_keys(name[0])
        self.proc.driver.find_element(By.NAME, 'given_name').send_keys(name[1])
        self.proc.driver.find_element(By.NAME, 'family_name_kana').send_keys(name_kana[0])
        self.proc.driver.find_element(By.NAME, 'given_name_kana').send_keys(name_kana[1])
        self.proc.driver.find_element(By.NAME, 'postal_code').send_keys(zipcode)
        self.proc.driver.find_element(By.XPATH, '//*[@id="form1"]/div[1]/div[10]/div[2]/button').click()
        time.sleep(.1)
        # self.proc.driver.find_element(By.NAME, 'city').send_keys(mojimoji.han_to_zen(self.place))
        self.proc.driver.find_element(By.NAME, 'street').send_keys(mojimoji.han_to_zen(self.number))
        # time.sleep(1)
        # self.proc.driver.find_element(By.NAME, 'nationality').click()
        Select(self.proc.driver.find_element(By.ID, "birthday_year")).select_by_value(self.birthday[0])
        Select(self.proc.driver.find_element(By.ID, "birthday_month")).select_by_value(str(self.birthday[1]).zfill(2))
        Select(self.proc.driver.find_element(By.ID, "birthday_day")).select_by_value(str(self.birthday[2]).zfill(2))
        Select(self.proc.driver.find_element(By.ID, "dod_year")).select_by_value(self.deathday[0])
        Select(self.proc.driver.find_element(By.ID, "dod_month")).select_by_value(str(self.deathday[1]).zfill(2))
        Select(self.proc.driver.find_element(By.ID, "dod_day")).select_by_value(str(self.deathday[2]).zfill(2))
        self.proc.driver.find_element(By.NAME, 'mise1').send_keys(self.bank_store_number)
        Select(self.proc.driver.find_element(By.ID, "kamoku-id1")).select_by_value('12')
        time.sleep(.1)
        self.proc.driver.find_element(By.NAME, 'koza1').send_keys(str(self.bank_account_number).zfill(7))
        self.proc.driver.find_element(By.NAME, 'nationality').click()
        element = self.proc.driver.find_element(By.NAME, 'koza1')
        self.proc.driver.execute_script("arguments[0].scrollIntoView();", element)

        messagebox.showinfo("", "次へ押下後にOKを押してください。")

        self.proc.driver.find_element(By.ID, 'profession').click()
        time.sleep(1)
        self.proc.driver.find_element(By.ID, 'prof_company_name').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.ID, 'prof_name').send_keys(f'森町　翼（{self.code}）')
        # self.proc.driver.find_element(By.ID, 'prof_name').send_keys('清水　茜作')
        self.proc.driver.find_element(By.ID, 'prof_company_name_kana').send_keys('ギョウセイショシホウジンチェスター')
        self.proc.driver.find_element(By.ID, 'prof_name_kana').send_keys('モリマチ　ツバサ')
        # self.proc.driver.find_element(By.ID, 'prof_name_kana').send_keys('シミズ　センサク')
        self.proc.driver.find_element(By.ID, 'self_postal_code').send_keys('1030028')
        sleep(.1)
        self.proc.driver.find_element(By.XPATH, '//*[@id="address-hide"]/div[1]/div[2]/button').click()
        sleep(.1)
        self.proc.driver.find_element(By.ID, 'self_street').send_keys('１－７－２０')
        self.proc.driver.find_element(By.NAME, 'self_tel1').send_keys('050')
        self.proc.driver.find_element(By.NAME, 'self_tel2').send_keys('6864')
        self.proc.driver.find_element(By.NAME, 'self_tel3').send_keys('7034')
        Select(self.proc.driver.find_element(By.ID, 'relation_id1')).select_by_visible_text('その他')
        sleep(1)
        self.proc.driver.find_element(By.ID, 'self_relationship_others').send_keys('相続人代理人')
        element = self.proc.driver.find_element(By.NAME, 'self_koza')
        self.proc.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(1)
        self.proc.driver.find_element(By.ID, 'post_input_same').click()
        sleep(1)
        self.proc.driver.find_element(By.ID, 'legalheiron').click()

        messagebox.showinfo("", "次へ押下後にOKを押してください。")

        self.proc.driver.find_element(By.ID, 'lastwill').click()
        sleep(1)
        self.proc.driver.find_element(By.ID, 'isan').click()
        self.proc.driver.execute_script("arguments[0].scrollIntoView();",
                                        self.proc.driver.find_element(By.XPATH, '//*[@id="form1"]/div/div[5]/div[2]/div[1]/span[1]'))
        sleep(1)
        self.proc.driver.find_element(By.ID, 'foreigner1').click()
        self.proc.driver.execute_script("arguments[0].scrollIntoView();", self.proc.driver.find_element(By.ID, 'foreigner1'))
        sleep(1)
        self.proc.driver.find_element(By.ID, 'northKorea1').click()
        self.proc.driver.find_element(By.ID, 'dispute1').click()
        # self.proc.driver.execute_script("arguments[0].scrollIntoView();",
        #                                 self.proc.driver.find_element(By.XPATH,
        #                                                               '//*[@id="form1"]/div/div[5]/div[4]/div/div[1]/span[1]'))
        # sleep(1)
        element = self.proc.driver.find_element(By.NAME, 'transaction_detail')
        self.proc.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(1)
        self.proc.driver.find_element(By.ID, 'desired').click()


    def balance_certificate(self):
        # 届出書（残高証明書・取引明細表の発行依頼用）
        pdf = PdfCreate("A4")

        pdf.draw_string(28,207.5,'〇', 12)
        pdf.draw_string(169,207.5,'1', 12)
        pdf.draw_string(28,195,'〇', 12)
        pdf.draw_string(169,195,'1', 12)
        pdf.draw_string(28,188,'〇', 12)
        pdf.draw_string(169,188,'1', 12)
        pdf.draw_string(28,175,'〇', 12)
        pdf.draw_string(169,175,'1', 12)
        pdf.draw_string(28,162.5,'〇', 12)
        pdf.draw_string(38.5,162.5,'履歴事項全部証明書', 12)
        pdf.draw_string(169, 162.5, '1', 12)

        pdf.draw_string(52, 98, self.customer_name, 14)
        pdf.draw_string(52, 50, '代理人 行政書士法人チェスター 代表社員 清水 茜作', 12)

        path1 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_横浜銀行_残高証明書申請書1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '横浜銀行_残高証明書申請書.pdf'), page=1, open_bool=False)

        # 2ページ目　残高証明書等発行依頼書【相続用】
        pdf = PdfCreate("A4")

        pdf.draw_string(58, 247, self.customer_name, 14)
        pdf.draw_string(58, 234, f'相続人　{self.heir_name}　代理人', 12)
        pdf.draw_string(58, 223.5, f'行政書士法人チェスター　代表社員　清水　茜作', 12)
        pdf.draw_string(37,215, '103-0028')
        pdf.draw_string(37, 209, f'東京都中央区八重洲1-7-20 八重洲口会館2階　担当：森町({self.code})', 12)

        pdf.draw_string(67, 186.5, self.deathday[0], 12)
        pdf.draw_string(88, 186.5, self.deathday[1], 12)
        pdf.draw_string(105, 186.5, self.deathday[2], 12)

        pdf.draw_string(38.5, 167, '✓', 14)

        # pdf.draw_string(129.5, 160.3, '✓', 14)  # 定期預金の経過利息
        # pdf.draw_string(129.5, 154, '✓', 14)    # 貸金庫の有無
        # pdf.draw_string(129.5, 147.2, '✓', 14)  # 金保護預りの有無

        pdf.draw_string(27, 129, 1, 12)
        pdf.draw_string(43, 129, self.bank_branch_name)

        pdf.draw_string(15.5, 40, '✓', 14)

        path2 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_横浜銀行_残高証明書申請書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '横浜銀行_残高証明書申請書.pdf'), page=2, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_横浜銀行_残高証明書申請書_{self.date[0]}{self.date[1]}{self.date[2]}.pdf'),
            path1, path2)

    def reservation(self):
        self.proc = Web()
        url = 'https://airrsv.net/boysouzoku1/calendar?schdlId=s0000AE584&_gl=1*bycvw*_ga*MTU1OTQ3OTg5MS4xNzU3NDgxOTQz*_ga_7P4KTMZ9DQ*czE3NTk5MDA4NDkkbzQkZzEkdDE3NTk5MDA5NjQkajMyJGwwJGgw*_fplc*N1JiMlRkbTBuSEtmNEI1YWdtQ1JFeiUyRjdRelhFMkR6VCUyRiUyQklJaHZ4RFRlZXphWU5CenptdG9ObHluMGdBaGJGeUJEQXpRZEl6cTFER1lhU0UwM0ZpRlZIUkxSR1Awanp2ZEpJZEFUdUM2VmNwM2FpSUtFT0YlMkZGZDRtZ05jRUElM0QlM0Q.'
        self.proc.web_open(url)

        all_elements = self.proc.driver.find_elements(By.ID, 'resrcCategorizeTitle')
        # すべての該当要素を取得
        # all_elements = self.proc.driver.find_elements(By.CSS_SELECTOR, 'p.categorizeTitle')
        # self.proc.driver.execute_script("arguments[0].click();", all_elements[1])
        self.proc.driver.execute_script("arguments[0].click();", all_elements[0])

        active_element = self.proc.driver.switch_to.active_element
        # # body_element = self.proc.driver.find_element(By.TAG_NAME, 'body')
        tab_keys = Keys.TAB * 12
        time.sleep(1)
        active_element.send_keys(tab_keys)
        # time.sleep(1)
        press('tab')
        press('enter')

        messagebox.showinfo("クリック", "「予約するボタンを押下後」にOKボタンをクリックしてください。")

        current_url = self.proc.driver.current_url
        self.proc.web_operation(current_url)

        self.proc.driver.find_element(By.NAME, 'lastNmKn').send_keys('モリマチ')
        self.proc.driver.find_element(By.NAME, 'firstNmKn').send_keys('ツバサ')
        self.proc.driver.find_element(By.NAME, 'lastNm').send_keys('森町')
        self.proc.driver.find_element(By.NAME, 'firstNm').send_keys('翼')
        self.proc.driver.find_element(By.NAME, 'tel1').send_keys('05068647034')
        self.proc.driver.find_element(By.NAME, 'mailAddress1').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.NAME, 'mailAddress1ForCnfrm').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.XPATH, '//*[@id="frontStaffBookingEditForm"]/div[1]/button').click()

        time.sleep(1)
        current_url = self.proc.driver.current_url
        self.proc.web_operation(current_url)

        Select(self.proc.driver.find_element(By.NAME, "surveyAnswerEditForm.listSurveyQuestionEditForm[0].listAnswered[0]")).select_by_value('はい')
        self.proc.driver.find_element(By.NAME,
                                 'surveyAnswerEditForm.listSurveyQuestionEditForm[1].listAnswered[0]').send_keys(f'・')
        self.proc.driver.find_element(By.NAME,
                                 'surveyAnswerEditForm.listSurveyQuestionEditForm[2].listAnswered[0]').send_keys(f'・')
        self.proc.driver.find_element(By.XPATH, '//*[@id="js-accessibility"]/li[4]/ul/li[2]/label/span').click()  # 残高証明書の発行
        self.proc.driver.find_element(By.XPATH,
                                 '//*[@id="js-accessibility"]/li[5]/ul/li[2]/label/span[2]').click()  # 原本をお預かり 否（即日返却希望）
        self.proc.driver.find_element(By.XPATH,
                                 '//*[@id="js-accessibility"]/li[6]/ul/li[1]/label/span[2]').click()  # 手数料のお支払方法 現金
        self.proc.driver.find_element(By.XPATH, '//*[@id="js-accessibility"]/li[7]/ul/li/label/span').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="js-accessibility"]/li[8]/ul/li[1]/label/span[2]').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="js-accessibility"]/li[9]/ul/li[1]/label/span[2]').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="js-accessibility"]/li[10]/ul/li[2]/label/span[2]').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="js-accessibility"]/li[11]/ul/li/label/span').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="frontStaffBookingEditForm"]/div[1]/button[2]').click()

def main():
    proc = YokohamaBank()
    # proc.account_freezing()     # メールアドレスに認証コードのみ
    proc.balance_certificate()
    # proc.reservation()  # 来店予約

    # proc = Web()
    # proc.web_operation('https://service.boy.co.jp/bctrl299-standard/ui/souzoku.html?_gl=1*1glomly*_gcl_au*MTMyMTczNDY1Mi4xNzU3NDgxOTQy*_ga*MTU1OTQ3OTg5MS4xNzU3NDgxOTQz*_ga_G0WHYCTTLZ*czE3NTc0ODE5NDIkbzEkZzEkdDE3NTc0ODQ2MDgkajYwJGwwJGgxMTE5OTkzNzE.*_fplc*akFWR0xkUU1aOXFxUFZHJTJGenM2SjQ0V1dCbm5pSEJXZlVTRVpnJTJCWkNnJTJGVCUyRmgydGxlVVpybUFIeEtrcEVRRk1wS2dOUzV0MjRmaDFqU25nT0lSZVU1REZLM2JOVkI0bTdteTJKRDVhdXRmQ0s0S2FYMlBPcWVuTm5GVkNOM2clM0QlM0Q.')
    #
    # proc.driver.switch_to.frame("smallchatframe")  # IDを直接文字列で渡す
    #
    # # 2. 内側の iframe に切り替え (class="html_content_area sound_inited"を使用)
    # # classをCSSセレクタで指定して WebElement を取得
    # inner_iframe_selector = "iframe.html_content_area.sound_inited"
    # inner_iframe_element = proc.driver.find_element(By.CSS_SELECTOR, inner_iframe_selector)
    #
    # # 内側の iframe にフォーカスを切り替え
    # proc.driver.switch_to.frame(inner_iframe_element)

    # proc.driver.find_element(By.ID, 'profession').click()
    # proc.driver.find_element(By.ID, 'prof_company_name').send_keys('行政書士')
    # proc.driver.find_element(By.ID, 'prof_name').send_keys('森町　翼')
    # # proc.driver.find_element(By.ID, 'prof_name').send_keys('清水　茜作')
    # proc.driver.find_element(By.ID, 'prof_company_name_kana').send_keys('ギョウセイショシ')
    # proc.driver.find_element(By.ID, 'prof_name_kana').send_keys('モリマチ　ツバサ')
    # # proc.driver.find_element(By.ID, 'prof_name_kana').send_keys('シミズ　センサク')
    # proc.driver.find_element(By.ID, 'self_postal_code').send_keys('1030028')
    # sleep(.1)
    # proc.driver.find_element(By.XPATH, '//*[@id="address-hide"]/div[1]/div[2]/button').click()
    # sleep(.1)
    # proc.driver.find_element(By.ID, 'self_street').send_keys('１－７－２０')
    # proc.driver.find_element(By.NAME, 'self_tel1').send_keys('050')
    # proc.driver.find_element(By.NAME, 'self_tel2').send_keys('6864')
    # proc.driver.find_element(By.NAME, 'self_tel3').send_keys('7034')
    # Select(proc.driver.find_element(By.ID, 'relation_id1')).select_by_visible_text('その他')
    # sleep(1)
    # proc.driver.find_element(By.ID, 'self_relationship_others').send_keys('相続人代理人')
    # proc.driver.find_element(By.ID, 'post_input_same').click()
    # proc.driver.find_element(By.ID, 'legalheiron').click()
    #
    # messagebox.showinfo("", "次へ押下後にOKを押してください。")
    #
    # proc.driver.find_element(By.NAME, 'lastwill').click()
    # proc.driver.find_element(By.ID, 'foreigner1').click()
    # proc.driver.find_element(By.NAME, 'northKorea').click()
    # proc.driver.find_element(By.NAME, 'dispute').click()
    # proc.driver.find_element(By.ID, 'desired').click()
    # element = proc.driver.find_element(By.NAME, 'transaction_detail')
    # proc.driver.execute_script("arguments[0].scrollIntoView();", element)

if __name__ == '__main__':
    main()
