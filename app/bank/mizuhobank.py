# みずほ銀行
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

class Mizuhobank:
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
        self.zipcode = utils.get_zipcode_from_address(address)
        print('address:', re.findall(pattern, self.address)[0])
        print('self.zipcode:', self.zipcode)

        heir_address = re.findall(pattern, self.heir_address)[0]
        self.heir_zipcode = re.findall('[0-9]+', utils.get_zipcode_from_address(heir_address))
        print('heir_address:', re.findall(pattern, self.heir_address)[0])
        print('self.heir_zipcode:', self.heir_zipcode)

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

        banks = utils.bank_search(name='みずほ銀行')
        self.branch_code = ''
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                self.branch_code = mojimoji.han_to_zen(
                    utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))
                print('self.branch_code:', self.branch_code)

    # 口座凍結
    def account_freezing(self):
        # 携帯電話番号の入力と画像認証
        self.proc = Web()
        url = 'https://inherit.m041.mizuhobank.co.jp/apply/applyConsent.php'
        self.proc.web_open(url)
        self.proc.driver.find_element(By.NAME, 'agree').click()
        self.proc.driver.find_element(By.ID, 'telNum1').send_keys('080')
        self.proc.driver.find_element(By.ID, 'telNum2').send_keys('8897')
        self.proc.driver.find_element(By.ID, 'telNum3').send_keys('4708')
        messagebox.showinfo("認証番号入力", "「認証番号入力後」にOKボタンをクリックしてください。")

        self.proc.driver.find_element(By.ID, 'hisozokujinSeikana').send_keys(self.name_kana[0])
        self.proc.driver.find_element(By.ID, 'hisozokujinmeikana').send_keys(self.name_kana[1])
        self.proc.driver.find_element(By.ID, 'hisozokujinSeikaji').send_keys(self.name[0])
        self.proc.driver.find_element(By.ID, 'hisozokujinmeikaji').send_keys(self.name[1])
        self.proc.driver.find_element(By.ID, 'zipCode1').send_keys(re.findall(r'\d+', self.zipcode)[0])
        self.proc.driver.find_element(By.ID, 'zipCode2').send_keys(re.findall(r'\d+', self.zipcode)[1])

        self.proc.driver.find_element(By.ID, 'address1').send_keys(jaconv.h2z(self.address, digit=True))
        # self.proc.driver.find_element(By.ID, 'searchaddr').click()
        # sleep(.5)
        self.proc.driver.find_element(By.ID, 'address2').send_keys(
            jaconv.h2z(self.building.replace('-', '－'), digit=True))

        self.proc.driver.find_element(By.XPATH, '//*[@id="birthday_swRadioset"]/label[1]').click()
        sleep(.5)
        self.proc.driver.find_element(By.ID, 'adLivingDate_y').send_keys(self.birthday[0])
        self.proc.driver.find_element(By.ID, 'adLivingDate_m').send_keys(self.birthday[1])
        self.proc.driver.find_element(By.ID, 'adLivingDate_d').send_keys(self.birthday[2])
        self.proc.driver.find_element(By.XPATH, '//*[@id="deathday_swRadioset"]/label[1]').click()
        sleep(.5)
        self.proc.driver.find_element(By.ID, 'adDeathDate_y').send_keys(self.passed_away_date[0])
        self.proc.driver.find_element(By.ID, 'adDeathDate_m').send_keys(self.passed_away_date[1])
        self.proc.driver.find_element(By.ID, 'adDeathDate_d').send_keys(self.passed_away_date[2])
        if self.branch_code:
            self.proc.driver.find_element(By.ID, 'tenbanNo').send_keys(mojimoji.zen_to_han(str(self.branch_code).zfill(3)))
        else:
            self.proc.driver.find_element(By.ID, 'tenbanNo').send_keys('000')

        self.proc.driver.find_element(By.XPATH, '//*[@id="kamoku-button"]/span[2]').click()
        sleep(.5)
        if '普通' in self.subjects:
            self.proc.driver.find_element(By.ID, 'ui-id-20').click()
        elif '定期' in self.subjects:
            self.proc.driver.find_element(By.ID, 'ui-id-23').click()
        elif '当座' in self.subjects:
            self.proc.driver.find_element(By.ID, 'ui-id-21').click()
        elif '貯蓄' in self.subjects:
            self.proc.driver.find_element(By.ID, 'ui-id-22').click()
        else:
            # 普通預金で仮に入力
            self.proc.driver.find_element(By.ID, 'ui-id-20').click()
        sleep(.5)

        # if self.bank_account_number:
        self.proc.driver.find_element(By.ID, 'acntNumIn').send_keys(mojimoji.zen_to_han(self.bank_account_number))

        self.proc.driver.find_element(By.ID, 'offerLastkana').send_keys('ギョウセイショシホウジンチェスター')
        self.proc.driver.find_element(By.ID, 'offerFirstkana').send_keys('モリマチ　ツバサ')
        self.proc.driver.find_element(By.ID, 'offerLastkanji').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.ID, 'offerFirstkanji').send_keys(f'森町　翼（{mojimoji.han_to_zen(self.code)}）')
        self.proc.driver.find_element(By.XPATH, '//*[@id="decedentRelationship-button"]/span[2]').click()
        sleep(.5)
        self.proc.driver.find_element(By.ID, 'ui-id-26').click()
        self.proc.driver.find_element(By.ID, 'heirsOther').send_keys('代理人')
        self.proc.driver.find_element(By.ID, 'offerorZipCode1').send_keys('103')
        self.proc.driver.find_element(By.ID, 'offerorZipCode2').send_keys('0028')
        self.proc.driver.find_element(By.ID, 'offerorSearchaddr').click()
        sleep(.5)
        self.proc.driver.find_element(By.ID, 'offerorAddress1').send_keys(
            jaconv.h2z('一丁目７番２０号', digit=True))
        self.proc.driver.find_element(By.ID, 'offerorAddress2').send_keys(
            jaconv.h2z('八重洲口会館２階', digit=True))
        self.proc.driver.find_element(By.ID, 'homePhoneNumber1').send_keys('050')
        self.proc.driver.find_element(By.ID, 'homePhoneNumber2').send_keys('6864')
        self.proc.driver.find_element(By.ID, 'homePhoneNumber3').send_keys('7034')
        self.proc.driver.find_element(By.ID, 'representLastkana').send_keys(self.heir_kana[0])
        self.proc.driver.find_element(By.ID, 'representFirstkana').send_keys(self.heir_kana[1])
        self.proc.driver.find_element(By.ID, 'representLastkanji').send_keys(self.heir[0])
        self.proc.driver.find_element(By.ID, 'representFirstkanji').send_keys(self.heir[1])
        # self.proc.driver.find_element(By.XPATH, '//*[@id="representativeRelationship-button"]').click()
        # if self.customer['続柄'] == '夫':
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="ui-id-33"]').click()
        # elif self.customer['続柄'] == '妻':
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="ui-id-34"]').click()
        # elif '男' in self.customer['続柄'] or '女' in self.customer['続柄']:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="ui-id-35"]').click()
        # else:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="ui-id-36"]').click()
        #     self.proc.driver.find_element(By.ID, 'representativeRelationshipOther').send_keys(self.customer['続柄'])
        #

        if self.address == self.heir_address:
        # if self.customer['被相続人_住所'] == self.customer['依頼者_住所']:
            self.proc.driver.find_element(By.XPATH, '//*[@id="sameAsDecedentArea"]/div[1]/label').click()
        else:
            self.proc.driver.find_element(By.ID, 'representativeZipCode1').send_keys(self.heir_zipcode[0])
            self.proc.driver.find_element(By.ID, 'representativeZipCode2').send_keys(self.heir_zipcode[1])
            self.proc.driver.find_element(By.ID, 'representativeAddress1').send_keys(
                jaconv.h2z(self.heir_address.replace('-', '－'), digit=True))
            if self.heir_building:
                self.proc.driver.find_element(By.ID, 'representativeAddress2').send_keys(
                jaconv.h2z(self.heir_address.replace('-', '－'), digit=True))
        #     self.proc.driver.find_element(By.ID, 'representativeSearchaddr').click()
        #     sleep(.5)
        #     self.proc.driver.find_element(By.ID, 'representativeAddress2').send_keys(
        #         jaconv.h2z(self.customer['依頼者_住所'].replace('-', '－'), digit=True))

        # if not self.customer['連絡先_携帯'] == "":
        #     self.proc.driver.find_element(By.ID, 'representativePhoneNumber1').send_keys(
        #         re.findall(r'\d+', self.customer['連絡先_携帯'])[0])
        #     self.proc.driver.find_element(By.ID, 'representativePhoneNumber2').send_keys(
        #         re.findall(r'\d+', self.customer['連絡先_携帯'])[1])
        #     self.proc.driver.find_element(By.ID, 'representativePhoneNumber3').send_keys(
        #         re.findall(r'\d+', self.customer['連絡先_携帯'])[2])
        # if not self.customer['連絡先_自宅'] == "":
        #     self.proc.driver.find_element(By.ID, 'repHomePhoneNumber1').send_keys(
        #         re.findall(r'\d+', self.customer['連絡先_自宅'])[0])
        #     self.proc.driver.find_element(By.ID, 'repHomePhoneNumber2').send_keys(
        #         re.findall(r'\d+', self.customer['連絡先_自宅'])[1])
        #     self.proc.driver.find_element(By.ID, 'repHomePhoneNumber3').send_keys(
        #         re.findall(r'\d+', self.customer['連絡先_自宅'])[2])

        # spouse = 0
        # children = 0
        # parents = 0
        # grandparent = 0  # 利用していない
        # brother_sister = 0
        # for heir in self.heirs:
        #     if heir[0] == '妻' or heir[0] == '夫':
        #         self.proc.driver.find_element(By.XPATH, '//*[@id="haigushaChoshuRadioset"]/label[1]').click()
        #         spouse += 1
        #     elif '男' in heir[0] or '女' in heir[0]:
        #         self.proc.driver.find_element(By.XPATH, '//*[@id="childrenChoshuRadioset"]/label[1]/span[1]').click()
        #         children += 1
        #     elif heir[0] == '父' or heir[0] == '夫':
        #         self.proc.driver.find_element(By.XPATH, '//*[@id="grandparentsChoshuRadioset"]/label[1]').click()
        #         parents += 1
        #     elif '兄弟' in heir[0] or '姉妹' in heir[0]:
        #         self.proc.driver.find_element(By.XPATH, '//*[@id="brotherAndSisterChoshuRadioset"]/label[1]/span[1]').click()
        #         brother_sister += 1
        #
        # # 両親：
        # if spouse == 0:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="haigushaChoshuRadioset"]/label[2]').click()
        #
        # # 祖父母：
        # if children == 0:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="childrenChoshuRadioset"]/label[2]').click()
        # else:
        #     self.proc.driver.find_element(By.ID, 'childrensChoshu').send_keys(children)
        #
        # # 兄弟姉妹：
        # if parents == 0:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="parentsChoshuRadioset"]/label[2]').click()
        # if grandparent == 0:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="grandparentsChoshuRadioset"]/label[2]/span[1]').click()
        # if brother_sister == 0:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="brotherAndSisterChoshuRadioset"]/label[2]').click()
        #
        # # 遺言書：
        # if self.t_will.value == '有':
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="testamentChoshuRadioset"]/label[1]').click()
        # else:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="testamentChoshuRadioset"]/label[2]').click()

        # 遺言書：無し
        self.proc.driver.find_element(By.XPATH, '//*[@id="testamentChoshuRadioset"]/label[2]').click()

        # # 遺産分割協議書：
        # if self.rg_discussed_document.value == '有':
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="heritageChoshuRadioset"]/label[1]').click()
        # else:
        #     self.proc.driver.find_element(By.XPATH, '//*[@id="heritageChoshuRadioset"]/label[2]').click()

        # 遺産分割協議書：有
        self.proc.driver.find_element(By.XPATH, '//*[@id="heritageChoshuRadioset"]/label[1]').click()

        # 相続人さま間の意見の相違：
        self.proc.driver.find_element(By.XPATH, '//*[@id="troubleChoshuRadioset"]/label[2]').click()

        # 相続預金の残高証明書の発行希望：
        self.proc.driver.find_element(By.XPATH, '//*[@id="balanceCertificateChoshuRadioset"]/label[1]').click()

        # 相続人さまへの連絡：
        self.proc.driver.find_element(By.XPATH, '//*[@id="contactChoshuRadioset"]/label[1]').click()

        # ⑥郵便物送付先情報について
        self.proc.driver.find_element(By.XPATH, '//*[@id="mailingAddress-button"]/span[2]').click()
        sleep(.5)
        # 申出人住所を選択
        self.proc.driver.find_element(By.ID, 'ui-id-33').click()

    # 残高証明書
    def balance_certificate(self):
        pdf = PdfCreate("A4")

        pdf.draw_string(23, 193, f'相続人　{self.heir_name}　代理人', 10)
        pdf.draw_string(23, 188, f'行政書士法人チェスター　代表社員　清水　茜作', 10)

        pdf.draw_string(63, 55, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        pdf.draw_string(63, 37, f'行政書士法人チェスター　森町（{mojimoji.han_to_zen(self.code)}）', 12)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_SBI申請銀行_残高証明書依頼書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'SBI新生銀行_残高証明書発行依頼書.pdf'), page=1, open_bool=True)

        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三菱UFJモルガン・スタンレー証券_相続に関する届出書.pdf'), page=2, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path,
                         f'【{self.code}】{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書_{self.date[0]}{self.date[2]}{self.date[2]}.pdf'),
            path1, path2)

if __name__ == '__main__':
    cl = Mizuhobank()
    cl.account_freezing()
    # cl.balance_certificate()
    # cl.inheritance_notification_create()


