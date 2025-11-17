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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

class Mizuhobank:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.code = 'G2087'
        self.customer_name = '関谷　雄孝'
        self.customer_name_kana = 'せきや　ゆうこう'
        self.bank_account_number = '1074942'
        if self.bank_account_number:
            self.bank_account_number = str(self.bank_account_number).zfill(7)
        self.branch_name = '本所'
        self.subjects = '普通'
        self.birthday = re.findall('[0-9]+', '1930/1/3')
        self.address = '東京都墨田区緑二丁目6番10号'
        self.building = ''
        self.passed_away_date = re.findall('[0-9]+', '2025/6/27')
        self.heir_name = '西澤　直子'
        self.heir_name_kana = 'にしざわ　なおこ'
        self.heir_address = '東京都墨田区緑二丁目1番3号'
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

        self.proc.driver.find_element(By.ID, 'address1').send_keys(jaconv.h2z(self.address.replace('-', '－').replace(' ', '').replace('　', ''), digit=True))
        # self.proc.driver.find_element(By.ID, 'searchaddr').click()
        # sleep(.5)
        self.proc.driver.find_element(By.ID, 'address2').send_keys(
            jaconv.h2z(self.building.replace('-', '－').replace(' ', '').replace('　', ''), digit=True))

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
        # self.proc.driver.find_element(By.ID, 'offerFirstkana').send_keys('モリマチ　ツバサ')
        self.proc.driver.find_element(By.ID, 'offerFirstkana').send_keys('ミヤモチ　レイナ')
        self.proc.driver.find_element(By.ID, 'offerLastkanji').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.ID, 'offerFirstkanji').send_keys(f'森町　翼（{mojimoji.han_to_zen(self.code)}）')
        # self.proc.driver.find_element(By.ID, 'offerFirstkanji').send_keys(f'宮持　玲那（{mojimoji.han_to_zen(self.code)}）')
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

        # 宮持玲那
        # self.proc.driver.find_element(By.ID, 'homePhoneNumber3').send_keys('7048')

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

        pdf.draw_string(148, 277, self.customer_name)

        # pdf.draw_string(121, 252, '〇', 14)
        pdf.draw_string(87, 267, '✓', 14)

        pdf.draw_string(112, 267, '相続人代理人')
        # pdf.draw_string(134, 252, '代理人')

        pdf.draw_string(111, 260, '103', 10)
        pdf.draw_string(127, 260, '0028', 10)
        pdf.draw_string(104, 255, '東京都中央区八重洲一丁目7-20', 8)
        pdf.draw_string(104, 251, '八重洲口会館2階', 8)
        pdf.draw_string(104, 246, f'相続人　{self.heir_name}　代理人', 8)
        # pdf.draw_string(104, 230, f'相続人　{self.heir["氏名"]}', 8)
        pdf.draw_string(104, 242, '行政書士法人チェスター　代表社員　清水　茜作', 8)
        pdf.draw_string(104, 238, f'担当：森町（{self.code}）', 8)
        # pdf.draw_string(104, 238, f'担当：宮持（{self.code}）', 8)
        pdf.draw_string(117, 234, '050', 8)
        pdf.draw_string(131, 234, '6864', 8)
        pdf.draw_string(148, 234, '7034', 8)

        # 宮持　玲那
        # pdf.draw_string(148, 234, '7048', 8)

        pdf.draw_string(18, 211.5, '✓', 12)
        # pdf.draw_string(27, 195, '✓', 8)

        pdf.draw_string(63, 211.5, '1', 12)
        # pdf.draw_string(74, 194, '1')

        # pdf.draw_string(85, 208, self.customer['支店名'], 8)

        # deathday = re.findall('[0-9]+', self.passed_away_date)
        pdf.draw_string(32, 154.5, self.passed_away_date[0])
        # pdf.draw_string(79, 123.5, deathday[0])
        pdf.draw_string(55, 154.5, self.passed_away_date[1])
        # pdf.draw_string(104, 123.5, deathday[1])
        pdf.draw_string(72, 154.5, self.passed_away_date[2])
        # pdf.draw_string(123, 123.5, deathday[2])

        # 支店名
        pdf.draw_string(85, 209.5, self.branch_name.replace('支店', ''))
        # buf = ''
        # for i, customer in enumerate(self.customer):
        #     if buf != customer['支店名']:
        #         pdf.draw_string(85 + i * 37, 209.5, customer['支店名'])
        #     buf = customer['支店名']

        # 現金払い
        pdf.draw_string(89, 115, '✓', 12)

        # pdf.draw_string(23, 193, f'相続人　{self.heir_name}　代理人', 10)
        # pdf.draw_string(23, 188, f'行政書士法人チェスター　代表社員　清水　茜作', 10)
        #
        # pdf.draw_string(63, 55, '東京都中央区八重洲1-7-20 八重洲口会館2階', 12)
        # pdf.draw_string(63, 37, f'行政書士法人チェスター　森町（{mojimoji.han_to_zen(self.code)}）', 12)

        path1 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_みずほ銀行_残高証明書_{self.date[0]}{self.date[1]}{self.date[2]}.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'みずほ銀行_残高証明書.pdf'), page=1, open_bool=True)

        # path2 = os.path.join(self.output_path,
        #                      f'{self.code}{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書2.pdf')
        # pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
        #                                  '三菱UFJモルガン・スタンレー証券_相続に関する届出書.pdf'), page=2, open_bool=False)
        #
        # pdf.pdf_marge(
        #     os.path.join(self.output_path,
        #                  f'【{self.code}】{self.heir[0]}様_三菱UFJモルガン・スタンレー証券_相続に関する届出書_{self.date[0]}{self.date[2]}{self.date[2]}.pdf'),
        #     path1, path2)

    def reservation(self):
        def click_button_by_text(driver, text):
            """ボタンの表示テキストを使って要素を探し、クリックする関数"""
            # XPath: buttonタグで、表示されているテキストが完全に一致するものを探す
            xpath_locator = f"//button[text()='{text}']"

            try:
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_locator))
                )
                button.click()
                sleep(.5)
                print(f"✅ ボタン '{text}' をクリックしました。")
            except Exception:
                raise NoSuchElementException(f"エラー: ボタン '{text}' が見つからないか、クリックできませんでした。")

        self.proc = Web()
        # 京橋支店 ※この支店は法人ではなく個人で予約
        url = 'https://www.mizuhobank.co.jp/tenpoinfo/tenpo_reservation/reservation.html?id=BA338922&_gl=1*k5k7g4*_ga*MTY5MzY1OTY1My4xNzU5ODE4NTkw*_ga_3D4K3DCJNB*czE3NjA0OTUxNDYkbzIkZzEkdDE3NjA0OTUzMzUkajYwJGwwJGgw'
        # # 八重洲口支店
        # url = 'https://www.mizuhobank.co.jp/tenpoinfo/tenpo_reservation/reservation.html?id=BA338924&_gl=1*1yjvpu4*_ga*MTY5MzY1OTY1My4xNzU5ODE4NTkw*_ga_3D4K3DCJNB*czE3NjA0OTUxNDYkbzIkZzEkdDE3NjA0OTU1MjkkajUxJGwwJGgw'
        # # 東京中央支店 ※この支店は法人ではなく個人で予約
        # url = 'https://www.mizuhobank.co.jp/tenpoinfo/tenpo_reservation/reservation.html?id=BA339731&_gl=1*1eoo2t1*_ga*MTY5MzY1OTY1My4xNzU5ODE4NTkw*_ga_3D4K3DCJNB*czE3NjA0OTUxNDYkbzIkZzEkdDE3NjA0OTU0MzgkajUyJGwwJGgw'
        self.proc.web_open(url)

        # --- ステップ 1: どちらかを選択してください。 ---
        click_button_by_text(self.proc.driver, "個人のお客さま")

        # --- ステップ 2: ご来店目的を選択してください。 ---
        # 新しい選択肢が表示されるのを待ってからクリック
        click_button_by_text(self.proc.driver, "各種手続き")

        # --- ステップ 3: 内容を選択してください。 ---
        # 新しい選択肢が表示されるのを待ってからクリック
        click_button_by_text(self.proc.driver, "相続手続")

        # --- ステップ 4: 日時・お客さま情報入力へ進む ---
        # 最後のボタンは <a> タグなので、XPathを変更して対応します。
        # reservation_link_xpath = "//a[text()='日時・お客さま情報入力へ']"
        reservation_link_xpath = '//*[@id="answer-20-3"]/div/div/a'

        reservation_link = WebDriverWait(self.proc.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, reservation_link_xpath))
        )
        # reservation_link.click()
        self.proc.driver.execute_script("arguments[0].click();", reservation_link)
        print("✅ リンク '日時・お客さま情報入力へ' をクリックしました。")

        messagebox.showinfo("待機中", "「日付選択後」にOKボタンをクリックしてください。")
        # self.proc.web_operation(self.proc.driver.current_url)
        self.proc.driver.switch_to.window(self.proc.driver.window_handles[-1])
        self.proc.driver.implicitly_wait(10)
        WebDriverWait(self.proc.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "reserveform"))
        )

        ## 1. 必須のチェックボックス（3項目）の操作
        # すべての項目をチェックして同意します。これらはすべて同じ name="attr_res4[]" を持っています。

        # # 最初の項目: 【個人のお客さま】振込・振替・税公金・両替・印鑑確認等はご予約対象外です
        self.proc.driver.find_element(By.XPATH,
                                      "//*[@id='right-column']/div[1]/form/div[1]/div[2]/div[1]/label/span").click()
        #
        # # 2番目の項目: 【法人・事業を営む個人・団体等のお客さま】事業性融資取引はご予約対象外です
        # self.proc.driver.find_element(By.XPATH,
        #                               '//*[@id="right-column"]/div[1]/form/div[1]/div[2]/div[2]/label/span').click()
        #
        # # 3番目の項目: 独立した予約メニューがあるお取引(口座開設・相続手続など)は該当のメニューでご予約ください
        # self.proc.driver.find_element(By.XPATH,
        #                               '//*[@id="right-column"]/div[1]/form/div[1]/div[2]/div[3]/label/span').click()


        if not self.branch_code or not self.bank_account_number:
            self.proc.driver.find_element(By.ID, 'bt_form_attr_res11').send_keys(
                f'相続の手続き　　残高証明書の発行依頼　　被相続人：{self.customer_name}様　　生年月日：{self.birthday[0]}年{self.birthday[1]}月{self.birthday[2]}日　　口座番号：0')
        else:
            self.proc.driver.find_element(By.ID, 'bt_form_attr_res11').send_keys(
                f'相続の手続き　　残高証明書の発行依頼　　被相続人：{self.customer_name}様　　生年月日：{self.birthday[0]}年{self.birthday[1]}月{self.birthday[2]}日　　口座番号：{mojimoji.zen_to_han(self.branch_code)}{mojimoji.zen_to_han(self.bank_account_number)}')

        # 各種証明書発行
        self.proc.driver.find_element(By.XPATH,
                                      '//*[@id="right-column"]/div[1]/form/div[1]/div[6]/div[2]/label/span').click()

        # 口座解約
        # self.proc.driver.find_element(By.XPATH,
        #                               '//*[@id="right-column"]/div[1]/form/div[1]/div[6]/div[1]/label/span').click()

        # # 2. テキストエリア（ご相談内容・ご希望など）の操作
        # textarea_field = self.proc.driver.find_element(By.ID, "bt_form_attr_res28")
        #
        # # 既存の値をクリア（あれば）
        # textarea_field.clear()
        #
        # # 新しい値を入力
        # textarea_field.send_keys(f'相続の手続き　残高証明書の発行依頼　被相続人：{self.customer_name}様　生年月日：{self.birthday[0]}年{self.birthday[1]}月{self.birthday[2]}日　口座番号：{mojimoji.zen_to_han(self.bank_account_number)}　')

        ## 3. ラジオボタン（ご予約時刻を15分過ぎてもご来店されない場合...）の操作
        # 選択肢は「確認しました」のみ (name="attr_res9", value="確認しました")
        self.proc.driver.find_element(By.XPATH, '//*[@id="right-column"]/div[1]/form/div[1]/div[8]/div/label/span').click()

        ## 4. フォームの送信
        # 「次へ進む」ボタンを特定 (type="submit", value="次へ進む")
        self.proc.driver.find_element(By.NAME, 'submit').click()

        sleep(2)
        self.proc.web_operation(self.proc.driver.current_url)
        self.proc.driver.implicitly_wait(10)
        # フォームが表示されるのを待つ
        WebDriverWait(self.proc.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "form1"))
        )

        # --- 1. 必須フィールドの操作 ---

        # お名前／法人名【漢字】 (name="cus_name")
        self.proc.driver.find_element(By.NAME, "cus_name").send_keys('行政書士法人チェスター')

        # お名前／法人名【全角カナ】 (name="cus_kana")
        self.proc.driver.find_element(By.NAME, "cus_kana").send_keys('ギョウセイショシホウジンチェスター')

        # （法人・任意団体のお客さま）ご来店者のお名前【漢字】
        self.proc.driver.find_element(By.NAME, "attr_org1").send_keys(f'森町　翼（{self.code}）')

        # （法人・任意団体のお客さま）ご来店者のお名前【全角カナ】
        self.proc.driver.find_element(By.NAME, "attr_org2").send_keys('モリマチ　ツバサ')

        # 電話番号 (name="cus_tel")
        self.proc.driver.find_element(By.NAME, "cus_tel").send_keys('05068647034')

        # 連絡がつきやすい時間帯　いつでも
        self.proc.driver.find_element(By.XPATH, "//*[@id='right-column']/div[1]/form/div[1]/div[12]/div[1]/label/span").click()

        # メールアドレス (name="cus_mail")
        self.proc.driver.find_element(By.NAME, "cus_mail").send_keys('t.morimachi_gy@chester-tax.com')

        # 生年月日 (年/月/日) ※設立年月日または今日の日付
        Select(self.proc.driver.find_element(By.ID, "bt_form_cus_birthy")).select_by_value(self.date[0])
        Select(self.proc.driver.find_element(By.ID, "bt_form_cus_birthm")).select_by_value(self.date[1])
        Select(self.proc.driver.find_element(By.ID, "bt_form_cus_birthd")).select_by_value(self.date[2])

        # 郵便番号
        self.proc.driver.find_element(By.NAME, 'cus_zip').send_keys('1030028')
        self.proc.driver.find_element(By.XPATH, '//*[@id="right-column"]/div[1]/form/div[1]/div[18]/input[2]').click()
        sleep(1)

        # 市区町村・番地
        self.proc.driver.find_element(By.NAME, 'cus_addr1').send_keys('7-20')

        # 建物名など
        self.proc.driver.find_element(By.NAME, 'cus_addr2').send_keys('八重洲口会館2階')

        # 店番号 (name="attr_org4")
        self.proc.driver.find_element(By.NAME, "attr_org4").send_keys(0)

        # 口座番号 (name="attr_org6")
        self.proc.driver.find_element(By.NAME, "attr_org6").send_keys(0)

        # ご予約時に選択いただいたメニュー... (name="attr_org8") - ラジオボタン【必須】
        # value="確認しました" のラジオボタンを選択
        self.proc.driver.find_element(By.XPATH, '//*[@id="right-column"]/div[1]/form/div[1]/div[34]/div/label/span').click()

        # 「お客さまの個人情報の利用目的」を確認し同意します。 (name="attr_org9[]") - チェックボックス【必須】
        # value="「お客さまの個人情報の利用目的」を確認し同意します。" のチェックボックスを選択
        self.proc.driver.find_element(By.XPATH,
                            '//*[@id="right-column"]/div[1]/form/div[1]/div[36]/div/label/span').click()

        # メールマガジンの配信を希望しない
        self.proc.driver.find_element(By.XPATH,
                                      '//*[@id="right-column"]/div[1]/form/div[1]/div[38]/div[2]/label/span').click()

        # --- 3. フォームの送信 ---

        # 「次へ進む」ボタンを特定 (type="submit", value="次へ進む")
        self.proc.driver.find_element(By.NAME, "submit").click()


if __name__ == '__main__':
    cl = Mizuhobank()
    # cl.account_freezing()
    # cl.balance_certificate()
    # cl.inheritance_notification_create()
    cl.reservation()    # 来店予約


