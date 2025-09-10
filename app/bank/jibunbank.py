# auじぶん銀行
# from zengin import BankSearch
# from pdf_create import PdfCreate
import jaconv
import re
from app._utils.web_operation import Web
import app.utils as utils
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import time


class JibunBank:
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
        self.proc.driver.find_element(By.NAME, 'inquiry_101').send_keys(self.deathday[0] + self.deathday[1] + self.deathday[2])
        self.proc.driver.find_element(By.NAME, 'inquiry_102_1').send_keys(name[0])
        self.proc.driver.find_element(By.NAME, 'inquiry_102_2').send_keys(name[1])
        self.proc.driver.find_element(By.NAME, 'inquiry_103_1').send_keys(name_kana[0])
        self.proc.driver.find_element(By.NAME, 'inquiry_103_2').send_keys(name_kana[1])
        self.proc.driver.find_element(By.NAME, 'inquiry_104').send_keys(self.birthday[0] + self.birthday[1] + self.birthday[2])
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
        self.proc.driver.find_element(By.NAME, 'inquiry_108').click()
        self.proc.driver.find_element(By.NAME, 'inquiry_109').click()

        # 2.相続人情報（含む代理人）
        self.proc.driver.find_element(By.NAME, 'inquiry_110_1').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.NAME, 'inquiry_110_2').send_keys('担当：森町')
        self.proc.driver.find_element(By.NAME, 'inquiry_111_1').send_keys('ギョウセイショシホウジンチェスター')
        self.proc.driver.find_element(By.NAME, 'inquiry_111_2').send_keys('タントウ：モリマチ')
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


def main():
    proc = JibunBank()
    proc.account_freezing()

if __name__ == '__main__':
    main()