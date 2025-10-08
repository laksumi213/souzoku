# みずほ証券
import jaconv
import mojimoji
import re
from app._utils.web_operation import Web
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
from pyautogui import typewrite, hotkey, position, press, moveTo
from app.controllers.pdf_create import PdfCreate
import os
import app.utils as utils
from datetime import datetime

class MizuhoSc:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.code = 'G2069'
        self.customer_name = '鈴木　幡雄'
        self.customer_name_kana = 'すずき　はたお'
        self.bank_account_number = mojimoji.han_to_zen(str('').zfill(7))
        self.branch_name = ''
        self.subjects = ''
        self.birthday = re.findall('[0-9]+', '1927/12/1')
        self.address = '東京都目黒区中町二丁目38番21号'
        self.passed_away_date = re.findall('[0-9]+', '2025/5/26')
        self.heir_name = '臼杵　優子'
        self.heir_name_kana = 'うすき　ゆうこ'
        self.heir_address = '東京都世田谷区若林一丁目2番20号'
        self.heir_building = ''

        self.date = re.findall(r'\d+', datetime.now().strftime('%Y/%m/%d'))

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　', '')}様（スタンダードプラン）\09.申請書類\01.残証申請書類'
        elif os.name == 'posix':
            print('posix')
            self.output_path = os.path.dirname(os.path.dirname(os.getcwd()))

        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]
        print('address:', re.findall(pattern, self.address)[0])
        print('utils.get_zipcode_from_address(address):', utils.get_zipcode_from_address(address))

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


    # 残高証明書
    def balance_certificate(self):
        pdf = PdfCreate("A4")

        # 日付
        pdf.draw_string(147, 252.5, self.date[0][2])
        pdf.draw_string(151.5, 252.5, self.date[0][3])
        pdf.draw_string(160, 252.5, str(self.date[1]).zfill(2)[0])
        pdf.draw_string(164.5, 252.5, str(self.date[1]).zfill(2)[1])
        pdf.draw_string(173.5, 252.5, str(self.date[2]).zfill(2)[0])
        pdf.draw_string(178, 252.5, str(self.date[2]).zfill(2)[1])

        pdf.draw_string(56, 228, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        pdf.draw_string(56, 223, f'「送付宛名：行政書士法人チェスター　森町（{self.code}）」', 10)
        pdf.draw_string(56, 217, f'相続人　{self.heir_name}　代理人')
        pdf.draw_string(56, 212, '行政書士法人チェスター　代表社員　清水　茜作')
        pdf.draw_string(56, 205, '050-6864-7034', 12)
        pdf.draw_string(56, 179.5, self.customer_name, 14)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_みずほ証券_残高証明書作成依頼書1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'みずほ証券_残高証明書作成依頼書（相続用）20250515.pdf'), page=1, open_bool=False)

        pdf = PdfCreate("A4")
        pdf.draw_line(86, 122, 86, 130)
        pdf.draw_line(88, 122, 88, 130)
        pdf.draw_string(84, 117, '御', 16)
        pdf.draw_string(84, 111, '中', 16)

        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_みずほ証券_残高証明書作成依頼書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'みずほ証券_残高証明書作成依頼書（相続用）20250515.pdf'), page=3, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_みずほ証券_残高証明書作成依頼書_{self.date[0]}{self.date[1]}{self.date[2]}.pdf'),
            path1, path2)

if __name__ == '__main__':
    cl = MizuhoSc()
    cl.balance_certificate()
    # cl.inheritance_notification_create()


