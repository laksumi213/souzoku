# セブン銀行
# from zengin import BankSearch
import jaconv
import re
from app._utils.web_operation import Web
import app.utils as utils
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from app.controllers.pdf_create import PdfCreate
import os
import mojimoji
from datetime import datetime


class Sevenbank:
    def __init__(self):
        super().__init__()
        self.deathday = None
        self.proc = None
        self.date = re.findall(r'\d+', datetime.now().strftime('%Y/%m/%d'))
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.bank_account_number = mojimoji.han_to_zen(str('').zfill(7))
        self.branch_name = ''
        self.subjects = ''
        self.birthday = re.findall('[0-9]+', '1958/9/18')
        self.address = '千葉県船橋市夏見台1-13-24'
        self.passed_away_date = re.findall('[0-9]+', '2025-06-27')
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



    def account_freezing(self):
        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]
        print(utils.get_zipcode_from_address(address))

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
        url = 'https://kyoudou.bbf-souzoku.com/UAP/MoushideninTouroku'
        self.proc.web_open(url)

        self.proc.driver.find_element(By.NAME, 'Inheritance_Represents_Attorney').click()
        self.proc.driver.find_element(By.NAME, 'LastName_Kanji_Attorney').send_keys('行政書士法人チェスター　担当：森町')
        self.proc.driver.find_element(By.NAME, 'LastName_Kana_Attorney').send_keys('ギョウセイショシホウジンチェスタータントウモリマチ')

        self.proc.driver.find_element(By.NAME, 'Postal_Code1').send_keys('103')
        self.proc.driver.find_element(By.NAME, 'Postal_Code2').send_keys('0028')
        Select(self.proc.driver.find_element(By.NAME, "Address_Pref")).select_by_visible_text('東京都')
        self.proc.driver.find_element(By.NAME, 'Address_City_Kanji').send_keys('中央区八重洲')
        self.proc.driver.find_element(By.NAME, 'Address_City_Kana').send_keys('チュウオウクヤエス')
        self.proc.driver.find_element(By.NAME, 'Address_Street').send_keys('1-7-20')
        self.proc.driver.find_element(By.NAME, 'Building_Kanji').send_keys('八重洲口会館2階')
        self.proc.driver.find_element(By.NAME, 'Building_Kana').send_keys('ヤエスグチカイカン2カイ')
        # self.proc.driver.find_element(By.NAME, 'Phone_Number1').send_keys('050')
        # self.proc.driver.find_element(By.NAME, 'Phone_Number2').send_keys('6864')
        # self.proc.driver.find_element(By.NAME, 'Phone_Number3').send_keys('7034')
        self.proc.driver.find_element(By.NAME, 'Mobile_Number1').send_keys('050')
        self.proc.driver.find_element(By.NAME, 'Mobile_Number2').send_keys('6864')
        self.proc.driver.find_element(By.NAME, 'Mobile_Number3').send_keys('7034')
        self.proc.driver.find_element(By.NAME, 'Mail_Address').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.NAME, 'Inheritance_Relationship').send_keys('相続人代理人')
        self.proc.driver.find_element(By.XPATH, '//*[@id="form1"]/div[3]/div/input').click()
        time.sleep(1)
        self.proc.driver.find_element(By.XPATH, '//*[@id="divStep3"]/div[3]/div/div/div[4]/div[1]/div[4]/div/button').click()
        time.sleep(1)

        # 相続人の登録
        self.proc.driver.find_element(By.NAME, 'LastName_Kanji').send_keys(name[0])
        self.proc.driver.find_element(By.NAME, 'FirstName_Kanji').send_keys(name[1])
        self.proc.driver.find_element(By.NAME, 'LastName_Kana').send_keys(name_kana[0])
        self.proc.driver.find_element(By.NAME, 'FirstName_Kana').send_keys(name_kana[1])

        Select(self.proc.driver.find_element(By.NAME, "Year_Of_Death")).select_by_value(self.deathday[0].zfill(4))
        Select(self.proc.driver.find_element(By.NAME, "Month_Of_Death")).select_by_value(self.deathday[1].zfill(2))
        Select(self.proc.driver.find_element(By.NAME, "Date_Of_Death")).select_by_value(self.deathday[2].zfill(2))

        self.proc.driver.find_element(By.NAME, 'Postal_Code1').send_keys(zipcode[0])
        self.proc.driver.find_element(By.NAME, 'Postal_Code2').send_keys(zipcode[1])
        self.proc.driver.find_element(By.NAME, 'btn_addr_search').click()
        time.sleep(0.5)
        self.proc.driver.find_element(By.NAME, 'Address_Street').send_keys(address[2])

        Select(self.proc.driver.find_element(By.NAME, "Year_Of_Birth")).select_by_value(self.birthday[0].zfill(4))
        Select(self.proc.driver.find_element(By.NAME, "Month_Of_Birth")).select_by_value(self.birthday[1].zfill(2))
        Select(self.proc.driver.find_element(By.NAME, "Date_Of_Birth")).select_by_value(self.birthday[2].zfill(2))

        self.proc.driver.find_element(By.ID, 'Cash_Card_Status_mu').click()

        self.proc.driver.find_element(By.NAME, 'Address_Street').click()

    def balance_certificate(self):
        # 残高証明書等作成依頼書
        pdf = PdfCreate("A4")

        pdf.draw_string(45, 177, jaconv.hira2kata(self.customer_name_kana), 8)
        pdf.draw_string(45, 169, self.customer_name, 12)

        pdf.draw_string(45, 160.5, f'ｿｳｿﾞｸﾆﾝ　{mojimoji.zen_to_han(jaconv.hira2kata(self.heir_name_kana))} ﾀﾞｲﾘﾆﾝ ｷﾞｮｳｾｲｼｮｼﾎｳｼﾞﾝﾁｪｽﾀｰ ﾀﾞｲﾋｮｳｼｬｲﾝ ｼﾐｽﾞ ｾﾝｻｸ', 8)
        pdf.draw_string(45, 155, f'相続人　{self.heir_name}　代理人', 12)
        pdf.draw_string(45, 150, f'行政書士法人チェスター　代表社員　清水　茜作', 12)

        pdf.draw_string(40, 146, '相続人', 6)
        pdf.draw_string(40, 144, '代理人', 6)

        pdf.draw_string(45, 140.5, 'ﾄｳｷｮｳﾄﾁｭｳｵｳｸﾔｴｽ1-7-20 ﾔｴｽｸﾞﾁｶｲｶﾝ2ｶｲ ﾀﾝﾄｳ:ﾓﾘﾏﾁ', 8)

        pdf.draw_string(35, 136, '1 0  3    0  0  2  8', 8)
        pdf.draw_string(37, 127, '東京', 12)
        pdf.draw_string(49.6, 130.4, '〇', 12)
        pdf.draw_string(64, 133, '中央区八重洲一丁目7-20 八重洲口会館2階')
        pdf.draw_string(64, 127, f'宛先　担当：森町（{self.code}）')

        pdf.draw_string(44, 117, '050', 12)
        pdf.draw_string(59, 117, '6864', 12)
        pdf.draw_string(77, 117, '7034', 12)

        pdf.draw_string(26, 81, self.passed_away_date[0][2:4])
        pdf.draw_string(38, 81, self.passed_away_date[1])
        pdf.draw_string(51, 81, self.passed_away_date[2])

        pdf.draw_string(102, 82, 1, 14)

        path1 = os.path.join(self.output_path,
             f'{self.code}{self.heir_name[0]}様_セブン銀行_残高証明書依頼書_{self.date[0]}{self.date[1]}{self.date[2]}.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'セブン銀行_残高証明書依頼書.pdf'), page=3, open_bool=True)

        # 経理への振込依頼時の添付ファイル
        pdf = PdfCreate("A4")
        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir_name[0]}様_セブン銀行_残高証明書依頼書1_{self.date[0]}{self.date[2]}{self.date[2]}.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'セブン銀行_残高証明書依頼書.pdf'), page=1, open_bool=False)

        pdf = PdfCreate("A4")
        pdf.draw_string(70, 143, f'「故　{self.customer_name}さま　代理人　行政書士法人チェスター　代表社員　清水　茜作」')
        path3 = os.path.join(self.output_path,
                             f'{self.code}{self.heir_name[0]}様_セブン銀行_残高証明書依頼書2_{self.date[0]}{self.date[2]}{self.date[2]}.pdf')
        pdf.pdf_save(path3, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'セブン銀行_残高証明書依頼書.pdf'), page=2, open_bool=False)
        pdf.pdf_marge(
            os.path.join(self.output_path,
                         f'{self.code}{self.heir_name[0]}様_セブン銀行_残高証明書の振込情報（経理用）.pdf'),
            path2, path3)

def main():
    proc = Sevenbank()
    # proc.account_freezing()
    proc.balance_certificate()


if __name__ == '__main__':
    main()