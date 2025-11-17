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
from app.controllers.pdf_create import PdfCreate
import os
import app.utils as utils


class Sbishinseibank:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.bank_account_number = '1211912'
        if self.bank_account_number:
            self.bank_account_number = mojimoji.han_to_zen(str(self.bank_account_number).zfill(7))
        self.branch_name = '本店'
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

    def balance_certificate(self):
        # 残高証明書等作成依頼書
        pdf = PdfCreate("A4")

        if self.branch_code:
            pdf.draw_string(83, 238, self.branch_code[0], 12)
            pdf.draw_string(93, 238, self.branch_code[1], 12)
            pdf.draw_string(102, 238, self.branch_code[2], 12)

        if not self.bank_account_number == '０００００００':
            pdf.draw_string(119, 238, self.bank_account_number[0], 12)
            pdf.draw_string(129, 238, self.bank_account_number[1], 12)
            pdf.draw_string(137, 238, self.bank_account_number[2], 12)
            pdf.draw_string(145.5, 238, self.bank_account_number[3], 12)
            pdf.draw_string(154, 238, self.bank_account_number[4], 12)
            pdf.draw_string(163, 238, self.bank_account_number[5], 12)
            pdf.draw_string(173, 238, self.bank_account_number[6], 12)

        pdf.draw_string(56, 224, f'{self.name_kana[0]}　{self.name_kana[1]}',12)
        pdf.draw_string(56, 215, f'{self.name[0]}　{self.name[1]}',12)

        pdf.draw_string(23, 193, f'相続人　{self.heir_name}　代理人', 10)
        pdf.draw_string(23, 188, f'行政書士法人チェスター　代表社員　清水　茜作', 10)
        pdf.draw_string(108, 188, f'相続人の代理人', 12)

        pdf.draw_string(39, 154, self.passed_away_date[0][0], 14)
        pdf.draw_string(48, 154, self.passed_away_date[0][1], 14)
        pdf.draw_string(57, 154, self.passed_away_date[0][2], 14)
        pdf.draw_string(66, 154, self.passed_away_date[0][3], 14)

        pdf.draw_string(84, 154, self.passed_away_date[1][0], 14)
        pdf.draw_string(93, 154, self.passed_away_date[1][1], 14)

        pdf.draw_string(111, 154, self.passed_away_date[2][0], 14)
        pdf.draw_string(120, 154, self.passed_away_date[2][1], 14)

        pdf.draw_string(39, 133.5, 1, 14)

        pdf.draw_string(43, 90, '050', 14)
        pdf.draw_string(60.5, 90, '6864', 14)
        pdf.draw_string(81, 90, '7034', 14)

        pdf.draw_string(125, 94, 'モリマチ　ツバサ', 12)
        pdf.draw_string(125, 85, '森町　翼', 12)

        pdf.draw_string(69, 64, '1  0  3', 10)
        pdf.draw_string(87, 64, '0  0  2   8', 10)

        pdf.draw_string(63, 55, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        pdf.draw_string(63, 37, f'行政書士法人チェスター　森町（{self.code}）', 12)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_SBI新生銀行_残高証明書依頼書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'SBI新生銀行_残高証明書発行依頼書.pdf'), page=1, open_bool=True)


    def trading_item(self):
        # 取引明細
        pdf = PdfCreate("A4")

        if self.branch_code:
            pdf.draw_string(91, 236, self.branch_code[0], 14)
            pdf.draw_string(100, 236, self.branch_code[1], 14)
            pdf.draw_string(109, 236, self.branch_code[2], 14)

        if not self.bank_account_number == '０００００００':
            pdf.draw_string(126, 236, self.bank_account_number[0], 14)
            pdf.draw_string(135, 236, self.bank_account_number[1], 14)
            pdf.draw_string(144, 236, self.bank_account_number[2], 14)
            pdf.draw_string(153, 236, self.bank_account_number[3], 14)
            pdf.draw_string(162, 236, self.bank_account_number[4], 14)
            pdf.draw_string(171, 236, self.bank_account_number[5], 14)
            pdf.draw_string(180, 236, self.bank_account_number[6], 14)

        pdf.draw_string(56, 226, f'{self.name_kana[0]}　{self.name_kana[1]}',12)
        pdf.draw_string(56, 215, f'{self.name[0]}　{self.name[1]}',14)

        pdf.draw_string(23, 195, f'相続人　{self.heir_name}　代理人', 11)
        pdf.draw_string(23, 190, f'行政書士法人チェスター　代表社員　清水　茜作', 11)
        pdf.draw_string(121, 190, f'相続人代理人', 11)

        pdf.draw_string(34, 128, '050', 12)
        pdf.draw_string(51, 128, '6864', 12)
        pdf.draw_string(72, 128, '7034', 12)

        pdf.draw_string(114, 132, 'モリマチ　ツバサ', 12)
        pdf.draw_string(114, 124, '森町　翼', 12)

        pdf.draw_string(50, 97, '103', 10)
        pdf.draw_string(68, 97, '0028', 10)

        pdf.draw_string(50, 87, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        pdf.draw_string(50, 69, f'行政書士法人チェスター　森町（{self.code}）', 12)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_SBI新生銀行_取引明細申請書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'SBI新生銀行_取引明細申請書.pdf'), page=3, open_bool=True)

def main():
    proc = Sbishinseibank()
    # proc.account_freezing()
    # proc.balance_certificate()
    proc.trading_item()     #取引明細
    # proc.reservation()  # 来店予約


if __name__ == '__main__':
    main()