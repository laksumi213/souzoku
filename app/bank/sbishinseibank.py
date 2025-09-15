# SBI新生銀行
import jaconv
import mojimoji
import re
from app._utils.web_operation import Web
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
from pyautogui import typewrite, hotkey, position, press, moveTo


class Sbishinseibank:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.code = None
        self.customer_name = None
        self.customer_name_kana = None
        self.bank_account_number = None
        self.birthday = None
        self.address = None
        self.passed_away_date = None
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.bank_account_number = ''
        self.birthday = re.findall('[0-9]+', '1958/9/18')
        self.address = '千葉県船橋市夏見台1-13-24'
        self.passed_away_date = re.findall('[0-9]+', '2025-06-27')

    def account_freezing(self):
        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]

        # name = re.findall(r'^(.*?)[ 　](.*)$', self.customer_name)[0]
        # print('氏名', name)
        # print('氏名', re.search(r'^(.*?)[ 　](.*)$', self.customer_name))
        print(address)
        print('birthday:', self.birthday)

        self.proc = Web()
        url = 'https://www.sbishinseibank.co.jp/crm/form/n02/'
        self.proc.web_open(url)
        self.proc.driver.find_element(By.ID, 'name').send_keys(self.customer_name)
        self.proc.driver.find_element(By.ID, '00N0K00000Jtc9H').send_keys(jaconv.hira2kata(self.customer_name_kana))
        if self.bank_account_number:
            self.proc.driver.find_element(By.ID, '00N0K00000Jo2gq').send_keys(self.bank_account_number.zfill(7))
        self.proc.driver.find_element(By.ID, '00N0K00000Jtc9I').send_keys(self.birthday[0].zfill(4))
        self.proc.driver.find_element(By.ID, '00N0K00000Jtc9F').send_keys(self.birthday[1].zfill(2))
        self.proc.driver.find_element(By.ID, '00N0K00000Jtc9D').send_keys(self.birthday[2].zfill(2))
        self.proc.driver.find_element(By.ID, '00N0K00000LYk1s').send_keys(address[0])
        self.proc.driver.find_element(By.ID, '00N0K00000LYk1q').send_keys(address[1])
        self.proc.driver.find_element(By.ID, '00N0K00000LYk1t').send_keys(mojimoji.han_to_zen(address[2]))
        Select(self.proc.driver.find_element(By.ID, "00N0K00000JEq7T")).select_by_visible_text('なし')
        self.proc.driver.find_element(By.ID, '00N2y000000uZnj').send_keys(self.passed_away_date[0].zfill(4))
        self.proc.driver.find_element(By.ID, '00N2y000000uZni').send_keys(self.passed_away_date[1].zfill(2))
        self.proc.driver.find_element(By.ID, '00N2y000000uZng').send_keys(self.passed_away_date[2].zfill(2))
        self.proc.driver.find_element(By.ID, '00N0K00000LYk1u').send_keys('森町　翼')
        self.proc.driver.find_element(By.ID, '00N2y0000010J8s').send_keys('モリマチ　ツバサ')
        self.proc.driver.find_element(By.NAME, 'email').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.NAME, '00N0K00000LYk1y').send_keys('代理人')
        self.proc.driver.find_element(By.NAME, 'phone').send_keys('050-6864-7034')
        self.proc.driver.find_element(By.ID, '00N0K00000JEq7R').send_keys('1030028')
        self.proc.driver.find_element(By.ID, 'zipbutton').click()
        sleep(0.5)
        self.proc.driver.find_element(By.ID, '00N0K00000JEq7M').send_keys(mojimoji.han_to_zen('一丁目7-20 八重洲口会館2階'))
        self.proc.driver.find_element(By.ID, '00N0K00000JEq7Q').send_keys('森町　翼（' + mojimoji.han_to_zen(self.code) +'）')
        self.proc.driver.find_element(By.ID, '00N0K00000LYk1t').click()


    def reservation(self):
        self.proc = Web()
        url = 'https://webforms.sbishinseibank.co.jp/reserve/input?type=inv_sfc&lid=temp_bran_btn_03&h=form&intcid=temp_bran_btn_03'
        self.proc.web_open(url)
        self.proc.driver.find_element(By.XPATH, '//*[@id="counselingReservation"]/div[2]/div/div[2]/div[1]/label').click()
        sleep(.1)
        self.proc.driver.find_element(By.XPATH, '//*[@id="counselingReservation"]/div[4]/div[2]/div[2]/div/p[1]/label').click()

        sleep(1)
        element = self.proc.driver.find_element(By.XPATH, '//*[@id="counselingReservation"]/div[6]/h3')
        self.proc.driver.execute_script("arguments[0].scrollIntoView();", element)

        self.proc.driver.find_element(By.ID, 'lastNameKanji').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.ID, 'firstNameKanji').send_keys(f'森町翼（{mojimoji.han_to_zen(self.code)}）')
        self.proc.driver.find_element(By.ID, 'lastNameKatakana').send_keys('ギョウセイショシホウジンチェスター')
        self.proc.driver.find_element(By.ID, 'firstNameKatakana').send_keys('モリマチツバサ')
        self.proc.driver.find_element(By.ID, 'phoneNumber').send_keys('05068647034')
        self.proc.driver.find_element(By.ID, 'bankAccountNumber').send_keys('0000000000')
        self.proc.driver.find_element(By.ID, 'email').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.XPATH, '//*[@id="consultation"]/label[5]').click()
        self.proc.driver.find_element(By.NAME, 'consultDetail').send_keys(f'残高証明書の発行　被相続人：{self.customer_name}({self.customer_name_kana})　生年月日：{self.birthday[0]}/{self.birthday[1].zfill(2)}/{self.birthday[2].zfill(2)}')
        # self.proc.driver.find_element(By.XPATH, '//*[@id="counselingReservation"]/div[13]/div/div/div/div/label/span').click()

        sleep(1)
        element = self.proc.driver.find_element(By.XPATH, '//*[@id="counselingReservation"]/div[6]/h3')
        self.proc.driver.execute_script("arguments[0].scrollIntoView();", element)


def main():
    proc = Sbishinseibank()
    # proc.account_freezing()
    proc.reservation()  # 来店予約

if __name__ == '__main__':
    main()