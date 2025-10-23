# 三菱UFJ信託銀行
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
from tkinter import messagebox

class TrMufg:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.code = 'G2103'
        self.customer_name = '水谷　弘'
        self.customer_name_kana = 'みずたに　ひろし'
        self.bank_account_number = mojimoji.han_to_zen(str('1178860').zfill(7))
        self.branch_name = '銀座中央'
        self.subjects = '普通'
        self.birthday = re.findall('[0-9]+', '1935/1/12')
        self.address = '東京都中央区晴海'
        self.building = '二丁目5番16-1101号'
        self.passed_away_date = re.findall('[0-9]+', '2025/5/16')
        self.heir_name = '水谷　昌代'
        self.heir_name_kana = 'みずたに　まさよ'
        self.heir_address = '東京都中央区晴海'
        self.heir_building = '二丁目5番16-1101号'

        self.date = re.findall(r'\d+', datetime.now().strftime('%Y/%m/%d'))

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　', '')}様（スタンダードプラン）\09.申請書類\01.残証申請書類'
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

        banks = utils.bank_search(name='三菱UFJ信託銀行')
        self.branch_code = ''
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                self.branch_code = mojimoji.han_to_zen(
                    utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))
                print('self.branch_code:', self.branch_code)

    # 口座凍結
    def account_freezing(self):
        self.proc = Web()
        url = 'https://safe.tr.mufg.jp/cgi-bin/shisan/souzoku/moushikomi_01.cgi'
        self.proc.web_open(url)
        self.proc.driver.find_element(By.ID, 'Z001_TE_JC_040_MT').send_keys(self.customer_name)
        self.proc.driver.find_element(By.ID, 'Z002_TE_KA_040_MT').send_keys(jaconv.hira2kata(self.customer_name_kana))
        self.proc.driver.find_element(By.ID, 'Z003_TE_FI_004_MT').send_keys(self.birthday[0])
        Select(self.proc.driver.find_element(By.ID, "Z004_SE_JC_999_MT")).select_by_visible_text(self.birthday[1] + '月')
        Select(self.proc.driver.find_element(By.ID, "Z005_SE_JC_999_MT")).select_by_visible_text(self.birthday[2] + '日')
        self.proc.driver.find_element(By.ID, 'Z006_TE_FI_003_MT').send_keys(re.findall('[0-9]+', self.zipcode)[0])
        self.proc.driver.find_element(By.ID, 'Z007_TE_FI_004_MT').send_keys(re.findall('[0-9]+', self.zipcode)[1])
        # Select(self.proc.driver.find_element(By.ID, "TD_Z008_SE_JC_999_MT")).select_by_value(self.customer_record['都道府県'])
        # self.proc.driver.find_element(By.ID, 'Z009_TE_JC_040_MT').send_keys(self.customer_record['市区町村'])
        self.proc.driver.find_element(By.ID, 'Z010_TE_JC_060_MT').send_keys(self.number)
        self.proc.driver.find_element(By.ID, 'Z011_TE_FI_004_OP').send_keys(self.passed_away_date[0])
        Select(self.proc.driver.find_element(By.ID, "Z012_SE_JC_999_OP")).select_by_visible_text(self.passed_away_date[1] + '月')
        Select(self.proc.driver.find_element(By.ID, "Z013_SE_JC_999_OP")).select_by_visible_text(self.passed_away_date[2] + '日')

        if self.branch_code:
            self.proc.driver.find_element(By.ID, 'Z015_TE_JC_040_MT').send_keys(self.branch_name)
            self.proc.driver.find_element(By.ID, 'Z016_TE_FI_009_MT').send_keys(self.bank_account_number)
        # try:
        #     banks = [(bank_name, bank_code) for bank_name, bank_code in
        #              BankSearch.bank_search(code=str(self.customer_record['銀行コード']).zfill(4))][0]
        #     print('banks:', banks)
        #
        #     branches = [(branch_code, branch_name) for branch_code, branch_name in
        #                 BankSearch.branch_search(bank_code=str(self.customer_record['銀行コード']).zfill(4),
        #                                          code=str(self.customer_record['支店コード']).zfill(3))][0]
        #     print('branches:', branches)
        #     self.proc.driver.find_element(By.ID, 'Z015_TE_JC_040_MT').send_keys(branches[1])
        #     self.proc.driver.find_element(By.ID, 'Z016_TE_FI_009_MT').send_keys(self.customer_record['口座番号'])
        # except:
        #     pass

        # 遺言書：無
        self.proc.driver.find_element(By.ID, 'Z023_RA_JC_999_MT2').click()
        # if self.rg_will.value == '無':
        #     self.proc.driver.find_element(By.ID, 'Z023_RA_JC_999_MT2').click()
        # else:
        #     self.proc.driver.find_element(By.ID, 'Z023_RA_JC_999_MT1').click()

        # 遺産分割協議書：有
        self.proc.driver.find_element(By.ID, 'Z026_RA_JC_999_MT1').click()
        # if self.rg_discussed_document.value == '無':
        #     self.proc.driver.find_element(By.ID, 'Z026_RA_JC_999_MT2').click()
        # else:
        #     self.proc.driver.find_element(By.ID, 'Z026_RA_JC_999_MT1').click()

        # 相続人数:不明
        self.proc.driver.find_element(By.ID, 'Z028_CH_JC_999_OP').click()
        # self.proc.driver.find_element(By.ID, 'Z027_TE_FI_004_OP').send_keys(self.heir[0]['相続人数'])
        # for heir in self.heir:
        #     print(heir['続柄'])
        #     if '夫' in heir['続柄'] or '妻' in heir['続柄']:
        #         self.proc.driver.find_element(By.ID, 'Z029_CH_JC_999_OP1').click()
        #     elif '男' in heir['続柄'][1:2] or '女' in heir['続柄'][1:2]:
        #         self.proc.driver.find_element(By.ID, 'Z029_CH_JC_999_OP2').click()
        #     elif '孫' in heir['続柄']:
        #         self.proc.driver.find_element(By.ID, 'Z029_CH_JC_999_OP3').click()
        #     elif '父' in heir['続柄'] or '母' in heir['続柄']:
        #         self.proc.driver.find_element(By.ID, 'Z029_CH_JC_999_OP4').click()
        #     elif '兄弟' in heir['続柄'] or '姉妹' in heir['続柄']:
        #         self.proc.driver.find_element(By.ID, 'Z029_CH_JC_999_OP5').click()
        #     elif '甥' in heir['続柄'] or '姪' in heir['続柄']:
        #         self.proc.driver.find_element(By.ID, 'Z029_CH_JC_999_OP6').click()
        #     else:
        #         self.proc.driver.find_element(By.ID, 'Z029_CH_JC_999_OP7').click()

        self.proc.driver.find_element(By.ID, 'Z030_RA_JC_999_OP2').click()  # 相続人間の意見の相違「無」
        self.proc.driver.find_element(By.ID, 'Z031_TE_JC_040_MT').send_keys(f'行政書士法人チェスター　代表社員　清水　茜作　担当：森町翼（{self.code}）')
        self.proc.driver.find_element(By.ID, 'Z032_TE_KA_040_MT').send_keys(f'{"ギョウセイショシホウジンチェスター　ダイヒョウシャイン　シミズ　センサク"}')
        self.proc.driver.find_element(By.ID, 'Z033_RA_JC_999_OP1').click()  # 男にチェック
        self.proc.driver.find_element(By.ID, 'Z034_TE_FI_003_MT').send_keys('103')
        self.proc.driver.find_element(By.ID, 'Z035_TE_FI_004_MT').send_keys('0028')
        self.proc.driver.find_element(By.ID, 'Z038_TE_JC_060_MT').send_keys('一丁目7-20 八重洲口会館2階')
        self.proc.driver.find_element(By.ID, 'Z039_TE_FI_010_OP').send_keys('050')
        self.proc.driver.find_element(By.ID, 'Z040_TE_FI_010_OP').send_keys('6864')
        self.proc.driver.find_element(By.ID, 'Z041_TE_FI_010_OP').send_keys('7034')
        self.proc.driver.find_element(By.ID, 'Z042_TE_FI_010_OP').send_keys('03')
        self.proc.driver.find_element(By.ID, 'Z043_TE_FI_010_OP').send_keys('6868')
        self.proc.driver.find_element(By.ID, 'Z044_TE_FI_010_OP').send_keys('8328')
        self.proc.driver.find_element(By.ID, 'Z045_TE_MA_100_MT').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.ID, 'Z046_TE_MA_100_MT').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.ID, 'Z047_RA_JC_999_MT6').click()  # その他にチェック
        self.proc.driver.find_element(By.ID, 'Z048_TE_JC_999_OP').send_keys('相続人代理人')
        self.proc.driver.find_element(By.ID, 'Z049_RA_JC_999_MT2').click()  # 当社との取引の無にチェック
        self.proc.driver.find_element(By.ID, 'Z052_RA_JC_999_MT1').click()  # 手続に関する連絡先:お届人さまと同一にチェック
        self.proc.driver.find_element(By.ID, 'Z069_CH_JC_999_MT').click()
        self.proc.driver.find_element(By.ID, 'Z070_CH_JC_999_MT').click()
        self.proc.driver.find_element(By.ID, 'Z071_RA_JC_999_MT1').click()
        # self.proc.driver.find_element(By.ID, 'Z072_RA_JC_999_OP1').click()  # 受取1名（代表者）
        self.proc.driver.find_element(By.ID, 'Z072_RA_JC_999_OP2').click()  # 受取2名以上
        self.proc.driver.find_element(By.ID, 'Z073_RA_JC_999_OP1').click()
        self.proc.driver.find_element(By.ID, 'Z074_RA_JC_999_MT1').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="TD_Z090_CH_JC_999_MT"]/p[2]/label').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[6]/div/p/button').click()

    # 残高証明書
    def balance_certificate(self):
        pdf = PdfCreate("A4")

        pdf.draw_string(30, 210, self.customer_name, 16)

        pdf.draw_string(120, 215, f'相続人　{self.heir_name}', 10)
        pdf.draw_string(120, 211, f'行政書士法人チェスター', 10)
        pdf.draw_string(120, 207, f'代表社員　清水　茜作', 10)

        pdf.draw_string(60, 202, f'103', 9)
        pdf.draw_string(76, 202, f'0028', 9)
        pdf.draw_string(131, 202, f'050', 10)
        pdf.draw_string(153, 202, f'6864', 10)
        pdf.draw_string(176, 202, f'7034', 10)

        # pdf.draw_string(26, 196, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        # pdf.draw_string(26, 191, f'行政書士法人チェスター　担当：森町（{self.code}）', 12)
        pdf.draw_string(26, 193, f'東京都中央区八重洲1-7-20 八重洲口会館2階　担当：森町（{self.code}）', 12)

        pdf.draw_string(63, 152, self.passed_away_date[0], 14)
        pdf.draw_string(87, 152, self.passed_away_date[1], 14)
        pdf.draw_string(106, 152, self.passed_away_date[2], 14)

        # 評価証明書
        # pdf.draw_string(178, 148.5, 1, 14)
        # pdf.draw_string(85, 90.5, '✓', 14)

        # 残高証明書
        pdf.draw_string(178, 141, 1, 14)
        pdf.draw_string(111, 90.5, '✓', 14)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_三菱UFJ信託_証明書等発行依頼書_預金1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三菱UFJ信託_証明書等発行依頼書_預金.pdf'), page=1, open_bool=False)

        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_三菱UFJ信託_証明書等発行依頼書_預金2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三菱UFJ信託_証明書等発行依頼書_預金.pdf'), page=2, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path,
                         f'{self.code}{self.heir[0]}様_三菱UFJ信託_証明書等発行依頼書_預金_{self.date[0]}{self.date[2]}{self.date[2]}.pdf'),
            path1, path2)

        # 経理提出書類
        pdf = PdfCreate("A4")
        pdf.draw_line(100, 187, 100, 171)
        pdf.draw_line(100, 187, 98, 184)
        pdf.draw_line(100, 187, 102, 184)

        pdf.draw_string(75,168, f'C25009668　行政書士法人チェスター　代表社員　清水　茜作', 12)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_三菱UFJ信託_証明書等発行依頼書_経理提出書類.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三菱UFJ信託_証明書等発行依頼書_預金.pdf'), page=5, open_bool=True)


if __name__ == '__main__':
    cl = TrMufg()
    # cl.account_freezing()
    cl.balance_certificate()
    # cl.inheritance_notification_create()


