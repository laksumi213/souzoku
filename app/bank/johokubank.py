# 城北信用金庫
import jaconv
import mojimoji
import re
from app._utils.web_operation import Web
import app.utils as utils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from app.controllers.pdf_create import PdfCreate
import os

class JohokuBank:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.bank_account_number = mojimoji.han_to_zen(str('').zfill(7))
        self.branch_name = ''
        self.subjects = ''
        self.birthday = '1958/9/18'
        # self.birthday = re.findall('[0-9]+', '1958/9/18')
        self.address = '千葉県船橋市夏見台1-13-24'
        self.passed_away_date = '2025-06-27'
        # self.passed_away_date = re.findall('[0-9]+', '2025-06-27')
        self.heir_name = '宇野　美穂'
        self.heir_name_kana = 'うの　みほ'
        self.heir_address = '千葉県船橋市夏見台1-13-24'
        self.heir_building = ''

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　','')}様（フルサポートプラン）\07.申請書類\01.残証申請書類'
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

        banks = utils.bank_search(name='SBI新生銀行')
        self.branch_code = ''
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                self.branch_code = mojimoji.han_to_zen(utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))
                print('self.branch_code:', self.branch_code)

    def balance_certificate(self):
        # 残高証明書等作成依頼書
        pdf = PdfCreate("A4")

        pdf.draw_string(73, 231.5, self.customer_name, 14)

        era = utils.convert_to_wareki2(self.birthday)
        if era[:2] == '昭和':
            pdf.draw_string(55, 221, '◯')
        elif era[:2] == '平成':
            pdf.draw_string(55, 215, '◯')
        elif era[:2] == '令和':
            pdf.draw_string(55, 209, '◯')
        pdf.draw_string(64, 215, re.findall(r'\d+', era)[0], 12)
        pdf.draw_string(78, 215, re.findall(r'\d+', era)[1], 12)
        pdf.draw_string(89, 215, re.findall(r'\d+', era)[2], 12)

        era = utils.convert_to_wareki2(self.passed_away_date)
        if era[:2] == '平成':
            pdf.draw_string(135.5, 218.5, '◯')
        elif era[:2] == '令和':
            pdf.draw_string(135.5, 210.5, '◯')
        pdf.draw_string(145, 215, re.findall(r'\d+', era)[0], 12)
        pdf.draw_string(158, 215, re.findall(r'\d+', era)[1], 12)
        pdf.draw_string(170, 215, re.findall(r'\d+', era)[2], 12)

        pdf.draw_string(60, 188, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        pdf.draw_string(60, 180, f'相続人　{self.heir_name}　代理人', 12)
        pdf.draw_string(60, 174, f'行政書士法人チェスター　代表社員　清水　茜作', 12)

        pdf.draw_string(81.5, 163.5, '✓', 14)
        pdf.draw_string(57.7, 141, '✓', 14)
        pdf.draw_string(172, 137.5, '1', 14)
        # pdf.draw_string(185, 37, f'行政書士法人チェスター　森町（{self.code}）', 12)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_城北信用金庫_残高証明書発行依頼書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '城北信用金庫_残高証明書発行依頼書.pdf'), page=1, open_bool=True)


def main():
    proc = JohokuBank()
    proc.balance_certificate()


if __name__ == '__main__':
    main()