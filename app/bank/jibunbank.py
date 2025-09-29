# auじぶん銀行
# from zengin import BankSearch
from app.controllers.pdf_create import PdfCreate
import jaconv
import re
import os
from app._utils.web_operation import Web
import app.utils as utils
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import time


class JibunBank:
    def __init__(self):
        super().__init__()
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.heir_name = '宇野　美穂'
        self.heir_name_kana = 'うの　みほ'
        self.bank_account_number = '1111'
        self.branch_name = '緑園都市支店'
        self.subjects = '普通預金'
        self.birthday = re.findall('[0-9]+', '1958/9/18')
        self.deathday = re.findall('[0-9]+', '2025/6/27')
        self.address = '千葉県船橋市夏見台1-13-24'
        self.building = ''
        self.heir_address = '神奈川県横浜市泉区緑園4丁目3番地1'
        self.heir_building = 'サンステージ緑園都市東の街11番館603号'
        self.proc = None
        self.passed_away_date = None
        zipcode = utils.get_zipcode_from_address(self.address)
        self.zipcode = re.findall('[0-9]+', zipcode)
        print('self.zipcode:', self.zipcode)

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　','')}様（スタンダードプラン）\07.申請書類\01.残証申請書類'
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

        banks = utils.bank_search(name='auじぶん銀行')
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                self.branch_code = utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name)
                print('self.branch_code:', self.branch_code)

    def account_freezing(self):
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

        self.passed_away_date = re.findall('[0-9]+', '2025-06-27')

        name = re.findall(r'^(.*?)[ 　](.*)$', self.customer_name)[0]
        print('氏名', name)

        name_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.customer_name_kana))[0]
        print('氏名カナ', name_kana)

        print(address)
        print('birthday:', self.birthday)

        self.proc = Web()
        url = 'https://help.jibunbank.co.jp/form/inheritance.html'
        self.proc.web_open(url)

        # 1.被相続人情報（亡くなられたお客さま）
        self.proc.driver.find_element(By.NAME, 'inquiry_101').send_keys(self.deathday[0].zfill(4) + self.deathday[1].zfill(2) + self.deathday[2].zfill(2))
        self.proc.driver.find_element(By.NAME, 'inquiry_102_1').send_keys(name[0])
        self.proc.driver.find_element(By.NAME, 'inquiry_102_2').send_keys(name[1])
        self.proc.driver.find_element(By.NAME, 'inquiry_103_1').send_keys(name_kana[0])
        self.proc.driver.find_element(By.NAME, 'inquiry_103_2').send_keys(name_kana[1])
        self.proc.driver.find_element(By.NAME, 'inquiry_104').send_keys(self.birthday[0].zfill(4) + self.birthday[1].zfill(2) + self.birthday[2].zfill(2))
        self.proc.driver.find_element(By.NAME, 'inquiry_4_1').send_keys('090')
        self.proc.driver.find_element(By.NAME, 'inquiry_4_2').send_keys('9999')
        self.proc.driver.find_element(By.NAME, 'inquiry_4_3').send_keys('9999')
        self.proc.driver.find_element(By.NAME, 'inquiry_2_1').send_keys(zipcode[0])
        self.proc.driver.find_element(By.NAME, 'inquiry_2_2').send_keys(zipcode[1])
        self.proc.driver.find_element(By.NAME, 'search-address-from-zipcode').click()
        time.sleep(1)
        self.proc.driver.find_element(By.XPATH, '//*[@id="final_search_result"]/table/tbody/tr/td/a').click()
        time.sleep(1)
        if match:
            self.proc.driver.find_element(By.NAME, 'inquiry_105').send_keys(number)
        # self.proc.driver.find_element(By.NAME, 'inquiry_108').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="inquiry_item108"]/label[3]').click()
        # self.proc.driver.find_element(By.NAME, 'inquiry_109').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="inquiry_item109"]/label[3]').click()

        # 2.相続人情報（含む代理人）
        self.proc.driver.find_element(By.NAME, 'inquiry_110_1').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.NAME, 'inquiry_110_2').send_keys(f'森町({self.code})')
        self.proc.driver.find_element(By.NAME, 'inquiry_111_1').send_keys('ギョウセイショシホウジンチェスター')
        self.proc.driver.find_element(By.NAME, 'inquiry_111_2').send_keys('モリマチ')
        self.proc.driver.find_element(By.NAME, 'inquiry_112').send_keys('相続人代理人')
        self.proc.driver.find_element(By.NAME, 'inquiry_113_1').send_keys('050')
        self.proc.driver.find_element(By.NAME, 'inquiry_113_2').send_keys('6864')
        self.proc.driver.find_element(By.NAME, 'inquiry_113_3').send_keys('7034')
        self.proc.driver.find_element(By.NAME, 'inquiry_5_1').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.NAME, 'inquiry_5_2').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.NAME, 'inquiry_114_1').send_keys('103')
        self.proc.driver.find_element(By.NAME, 'inquiry_114_2').send_keys('0028')
        # self.proc.driver.find_element(By.NAME, 'search-address-from-zipcode2').click()
        # time.sleep(1)
        self.proc.driver.find_element(By.NAME, 'inquiry_115').send_keys('東京都中央区八重洲')
        self.proc.driver.find_element(By.NAME, 'inquiry_116').send_keys('1-7-20-八重洲口会館2階')

        self.proc.driver.find_element(By.NAME, 'inquiry_124_1').send_keys('エーユージブン')
        self.proc.driver.find_element(By.NAME, 'inquiry_124_2').send_keys('アカ')
        self.proc.driver.find_element(By.NAME, 'inquiry_124_4').send_keys('1234567')
        self.proc.driver.find_element(By.NAME, 'inquiry_124_5').send_keys('ジブン　タロウ')


        # 3.相続方法など
        self.proc.driver.find_element(By.NAME, 'inquiry_117_1').click()
        self.proc.driver.find_element(By.NAME, 'inquiry_117_2').click()
        self.proc.driver.find_element(By.NAME, 'inquiry_117_3').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="inquiry_item118"]/label[2]/input').click()
        self.proc.driver.find_element(By.XPATH, '//*[@id="inquiry_item118"]/span[3]/div[2]/label[2]/input').click()

    def balance_certificate(self):
        # 残高証明書等作成依頼書
        pdf = PdfCreate("A4")

        pdf.draw_string(68, 243.5, self.zipcode[0])
        pdf.draw_string(81, 243.5, self.zipcode[1])

        if self.building:
            pdf.draw_string(68, 238, self.address)
            pdf.draw_string(68, 233, self.building)
        else:
            pdf.draw_string(68, 236, self.address, 12)

        pdf.draw_string(68, 223, self.customer_name, 12)

        pdf.draw_string(68, 216, '103')
        pdf.draw_string(81, 216, '0028')
        pdf.draw_string(68, 208, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        pdf.draw_string(66, 200, f'被相続人　{self.customer_name}', 10)
        pdf.draw_string(66, 195, f'相続人　{self.heir_name}　代理人', 10)
        pdf.draw_string(66, 190, '行政書士法人チェスター 代表社員 清水 茜作', 10)
        pdf.draw_string(68, 184, '050', 12)
        pdf.draw_string(89, 184, '6864', 12)
        pdf.draw_string(108, 184, '7034', 12)

        pdf.draw_string(60, 161.5, self.deathday[0], 12)
        pdf.draw_string(79, 161.5, self.deathday[1], 12)
        pdf.draw_string(92, 161.5, self.deathday[2], 12)

        pdf.draw_string(72, 152, 1, 12)

        pdf.draw_string(21.5, 127, '✓', 14)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_auじぶん銀行_残高証明書依頼書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'auじぶん銀行_残高証明書申請書・取引明細申請書.pdf'), page=2, open_bool=True)

        # 取引明細表発行依頼書
        pdf = PdfCreate("A4")

        pdf.draw_string(80, 217, self.zipcode[0])
        pdf.draw_string(93, 217, self.zipcode[1])

        if self.building:
            pdf.draw_string(80, 213, self.address)
            pdf.draw_string(80, 208, self.building)
        else:
            pdf.draw_string(80, 210, self.address, 12)

        pdf.draw_string(80, 197, self.customer_name, 12)
        pdf.draw_string(76, 187.5, self.branch_name.replace('支店', ''), 10)
        pdf.draw_string(141, 187.5, self.bank_account_number.zfill(7), 12)

        pdf.draw_string(80, 181, '103')
        pdf.draw_string(93, 181, '0028')
        pdf.draw_string(80, 175, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        pdf.draw_string(78, 164, f'被相続人　{self.customer_name}', 10)
        pdf.draw_string(78, 159, f'相続人　{self.heir_name}　代理人', 10)
        pdf.draw_string(78, 154, '行政書士法人チェスター 代表社員 清水 茜作', 10)
        pdf.draw_string(80, 145, '050', 12)
        pdf.draw_string(103, 145, '6864', 12)
        pdf.draw_string(128, 145, '7034', 12)
        pdf.draw_string(89, 113.5, 1, 12)

        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_auじぶん銀行_取引明細表発行依頼書.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'auじぶん銀行_残高証明書申請書・取引明細申請書.pdf'), page=3, open_bool=True)


def main():
    proc = JibunBank()
    # proc.account_freezing()
    proc.balance_certificate()


if __name__ == '__main__':
    main()