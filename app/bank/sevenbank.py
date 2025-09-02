# セブン銀行
import flet as ft
# from zengin import BankSearch
# from pdf_create import PdfCreate
from datetime import datetime
import jaconv
import mojimoji
import re
import os.path
from app._utils.web_operation import Web
import app.utils as utils
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


class Sevenbank:
    def __init__(self):
        super().__init__()
        self.deathday = None
        self.proc = None
        self.code = None
        self.customer_name = None
        self.customer_name_kana = None
        self.bank_account_number = None
        self.birthday = None
        self.address = None
        self.passed_away_date = None


    def account_freezing(self):
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.bank_account_number = ''
        self.birthday = re.findall('[0-9]+', '1958/9/18')
        self.deathday = re.findall('[0-9]+', '2025/6/27')
        self.address = '千葉県船橋市夏見台1-13-24'
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
        self.proc.driver.find_element(By.NAME, 'LastName_Kanji_Attorney').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.NAME, 'LastName_Kana_Attorney').send_keys('ギョウセイショシホウジンチェスター')

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


def main():
    proc = Sevenbank()
    proc.account_freezing()

if __name__ == '__main__':
    main()