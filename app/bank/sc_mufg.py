### 三菱ＵＦＪモルガン・スタンレー証券
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

class ScMufg:
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
        self.building = ''
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

    # 相続に関する届出書
    def notification_form_about_inheritance(self):
        pdf = PdfCreate("A4")

        pdf.draw_string(38, 262.5, self.date[0])
        pdf.draw_string(56, 262.5, self.date[1])
        pdf.draw_string(73, 262.5, self.date[2])

        pdf.draw_string(43, 216, self.address, 12)
        if self.building:
            pdf.draw_string(43, 221, self.building, 12)

        pdf.draw_string(45, 201, jaconv.hira2kata(self.customer_name_kana), 10)
        pdf.draw_string(45, 190, self.customer_name, 14)

        pdf.draw_string(152, 199, self.birthday[0])
        pdf.draw_string(170, 199, self.birthday[1])
        pdf.draw_string(186, 199, self.birthday[2])

        pdf.draw_string(152, 187, self.passed_away_date[0])
        pdf.draw_string(170, 187, self.passed_away_date[1])
        pdf.draw_string(186, 187, self.passed_away_date[2])

        pdf.draw_string(48.8, 175.3, '103     0028', 8)
        pdf.draw_string(42, 167, '東京都中央区八重洲一丁目7-20　八重洲口会館2階', 12)
        pdf.draw_string(42, 162, f'「送付宛名：行政書士法人チェスター　森町（{self.code}）」', 12)

        pdf.draw_string(42, 151, f'ｿｳｿﾞｸﾆﾝ {mojimoji.zen_to_han(jaconv.hira2kata(self.heir_name_kana))} ﾀﾞｲﾘﾆﾝ ｷﾞｮｳｾｲｼｮｼﾎｳｼﾞﾝﾁｪｽﾀｰ ﾀﾞｲﾋｮｳｼｬｲﾝ ｼﾐｽﾞ ｾﾝｻｸ')

        pdf.draw_string(42, 141, f'相続人　{self.heir_name}　代理人　', 12)
        pdf.draw_string(42, 136, '行政書士法人チェスター　代表社員　清水　茜作', 12)

        pdf.draw_string(42, 126, '相続人代理人')

        pdf.draw_string(96, 126, '050', 12)
        pdf.draw_string(119, 126, '6864', 12)
        pdf.draw_string(143, 126, '7034', 12)


        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三菱UFJモルガン・スタンレー証券_相続に関する届出書.pdf'), page=1, open_bool=False)

        # 2ページ目
        pdf = PdfCreate("A4")

        pdf.draw_string(33, 256, '✓', 14)
        pdf.draw_string(43, 249, 1, 12)
        pdf.draw_string(57.5, 249.3, '✓', 14)
        pdf.draw_string(33, 242.7, '✓', 14)
        pdf.draw_string(33, 145.7, '✓', 14)

        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三菱UFJモルガン・スタンレー証券_相続に関する届出書.pdf'), page=2, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書_{self.date[0]}{self.date[2]}{self.date[2]}.pdf'),
            path1, path2)


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


if __name__ == '__main__':
    cl = ScMufg()
    cl.notification_form_about_inheritance()
    # cl.balance_certificate()
    # cl.inheritance_notification_create()


