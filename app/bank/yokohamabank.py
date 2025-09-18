# 横浜銀行
import jaconv
import mojimoji
import re
from app._utils.web_operation import Web
import app.utils as utils
from pyautogui import typewrite, hotkey, position, press, moveTo
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from app.controllers.pdf_create import PdfCreate
import os
import time
import tkinter as tk
from tkinter import messagebox


class YokohamaBank:
    def __init__(self):
        super().__init__()
        self.url = None
        self.deathday = None
        self.heir_name_kana = None
        self.heir_name = None
        self.proc = None
        self.code = None
        self.customer_name = None
        self.customer_name_kana = None
        self.bank_account_number = None
        self.birthday = None
        self.address = None
        self.passed_away_date = None

        self.code = 'G2014'
        self.customer_name = '菅沼　純子'
        self.customer_name_kana = 'すがぬま　すみこ'
        self.heir_name = '菅沼　富男'
        self.heir_name_kana = 'すがぬま　とみお'
        self.bank_store_number = '352'
        self.bank_account_number = '0941366'
        self.birthday = re.findall('[0-9]+', '1937/11/3')
        self.deathday = re.findall('[0-9]+', '2025/6/12')
        self.address = '神奈川県横浜市泉区緑園四丁目3番地1サンステージ緑園都市東の街11番館603号'

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
        time.sleep(1)
        moveTo(950, 340)
        time.sleep(.1)

        press('tab')
        pyperclip.copy(name[0])
        hotkey('ctrl', 'v')
        time.sleep(.1)

        press('tab')
        pyperclip.copy(name[1])
        hotkey('ctrl', 'v')
        time.sleep(.1)

        press('tab')
        pyperclip.copy(name_kana[0])
        hotkey('ctrl', 'v')
        time.sleep(.1)

        press('tab')
        pyperclip.copy(name_kana[1])
        hotkey('ctrl', 'v')
        time.sleep(.1)

        press('tab')
        pyperclip.copy(zipcode)
        hotkey('ctrl', 'v')
        time.sleep(.1)

        press('tab')
        press('space')
        time.sleep(.1)

        press('tab', presses=3)
        pyperclip.copy(mojimoji.han_to_zen(number))
        hotkey('ctrl', 'v')
        time.sleep(.1)

        press('tab')
        press('space')
        time.sleep(.1)

        press('tab')
        typewrite(self.birthday[0])
        time.sleep(1)

        press('tab')
        press('down', presses=self.birthday[1])
        time.sleep(1)

        press('tab')
        press('down', presses=self.birthday[2])
        time.sleep(1)

        press('tab')
        typewrite(self.passed_away_date[0])
        time.sleep(1)

        press('tab')
        press('down', presses=self.passed_away_date[1])
        time.sleep(1)

        press('tab')
        press('down', presses=self.passed_away_date[2])
        time.sleep(1)


    def balance_certificate(self):
        # 届出書（残高証明書・取引明細表の発行依頼用）
        pdf = PdfCreate("A4")

        path1 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_三井住友銀行_残高証明書依頼書_郵送専用1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三井住友銀行_残高証明書依頼書_郵送専用.pdf'), page=1, open_bool=False)

        # 2ページ目　残高証明書等発行依頼書【相続用】
        pdf = PdfCreate("A4")

        path2 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_野村證券_残高証明書申請書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '野村證券_残高証明書申請書.pdf'), page=2, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_野村證券_残高証明書申請書.pdf'),
            path1, path2)

def main():
    proc = YokohamaBank()
    # proc.account_freezing()     # メールアドレスに認証コードのみ
    proc.balance_certificate()

if __name__ == '__main__':
    main()
