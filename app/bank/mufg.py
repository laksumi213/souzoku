# 三菱UFJ銀行
from app._utils.web_operation import Web
import app.utils as utils
import jaconv
import mojimoji
import re
from time import sleep
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Mufg:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.url = None
        self.code = 'G2069'
        self.customer_name = '鈴木　幡雄'
        self.customer_name_kana = 'すずき　はたお'
        self.heir_name = '臼杵　優子'
        self.heir_name_kana = 'うすき　ゆうこ'
        # self.bank_store_number = '352'
        self.branch_name = '渋谷明治通支店'
        self.bank_account_number = '3159175'
        self.birthday = re.findall('[0-9]+', '1927/12/1')
        self.deathday = re.findall('[0-9]+', '2025-05-26')
        self.address = '東京都目黒区中町2丁目38番21号'

        zipcode = utils.get_zipcode_from_address(self.address)
        self.zipcode = re.findall('[0-9]+', zipcode)
        print('self.zipcode:', self.zipcode)

        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]
        print('address:', re.findall(pattern, self.address)[0])
        print('utils.get_zipcode_from_address(address):', utils.get_zipcode_from_address(address))

        match = re.search(r'([^\d]+)(\d.*)', address[2])
        if match:
            self.place = match.group(1) # 最初のグループ（数字以外の文字）
            self.number = match.group(2)  # 2番目のグループ（数字とハイフンを含む部分）
            print(f"場所: {self.place}") # 出力: 場所: 夏見台
            print(f"番地: {self.number}")

        self.name = re.findall(r'^(.*?)[ 　](.*)$', self.customer_name)[0]
        print('被相続人', self.name)

        self.name_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.customer_name_kana))[0]
        print('被相続人カナ', self.name_kana)

        self.heir = re.findall(r'^(.*?)[ 　](.*)$', self.heir_name)[0]
        print('相続人', self.heir)

        self.heir_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.heir_name_kana))[0]
        print('相続人カナ', self.heir_kana)


    def account_freezing(self):
        url = 'https://sozoku.bk.mufg.jp/uketsuke/A010'
        self.proc = Web()
        self.proc.web_open(url)
        # 確認しました
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[2]/ul/li/label/span").click()
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/div[4]/ul/li/label/span").click()
        sleep(0.5)

        # 次へ
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/a[2]/span").click()

        sleep(.5)

        # Eメールアドレス
        self.proc.driver.find_element(By.ID, 'MailAddress').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.ID, 'MailAddressConfirmation').send_keys('t.morimachi_gy@chester-tax.com')

        # 次へ
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/nav/ul/li[2]/a/p").click()
        sleep(0.5)

        # 登録する
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/form/nav/ul/li[2]/a/p").click()

        # 認証番号の入力はこちらのボタンを押す
        self.proc.driver.find_element(By.XPATH, '//*[@id="form0"]/a/span').click()

        messagebox.showinfo("認証番号入力", "「認証番号入力後」にOKボタンをクリックしてください。")

        # 氏名
        self.proc.driver.find_element(By.ID, 'InheriteeLastName').send_keys(self.name[0])
        self.proc.driver.find_element(By.ID, 'InheriteeFirstName').send_keys(self.name[1])
        self.proc.driver.find_element(By.ID, 'InheriteeLastNameKana').send_keys(self.name_kana[0])
        self.proc.driver.find_element(By.ID, 'InheriteeFirstNameKana').send_keys(self.name_kana[1])

        # 国籍
        self.proc.driver.find_element(By.ID, 'InheriteeNationality').send_keys('日本')

        # 住所
        self.proc.driver.find_element(By.ID, 'InheriteeZipCode1').send_keys(self.zipcode[0])
        self.proc.driver.find_element(By.ID, 'InheriteeZipCode2').send_keys(self.zipcode[1])
        # 郵便番号から調べる
        self.proc.driver.find_element(By.XPATH, "/html/body/article/section/div/div/form/div[4]/div/ul/li/dl/dd/input[3]").click()
        sleep(0.5)

        self.proc.driver.find_element(By.ID, 'InheriteeAddress').send_keys(self.number)

        # 生年月日
        Select(self.proc.driver.find_element(By.ID, "InheriteeBirthdayYear")).select_by_visible_text(self.birthday[0] + '年')
        Select(self.proc.driver.find_element(By.ID, "InheriteeBirthdayMonth")).select_by_visible_text(f"{int(self.birthday[1])}月")
        Select(self.proc.driver.find_element(By.ID, "InheriteeBirthdayDay")).select_by_visible_text(f"{int(self.birthday[2])}日")

        # 死亡日
        Select(self.proc.driver.find_element(By.ID, "InheriteeDateOfDeathYear")).select_by_visible_text(self.deathday[0] + '年')
        Select(self.proc.driver.find_element(By.ID, "InheriteeDateOfDeathMonth")).select_by_visible_text(f"{int(self.deathday[1])}月")
        Select(self.proc.driver.find_element(By.ID, "InheriteeDateOfDeathDay")).select_by_visible_text(f"{int(self.deathday[2])}日")

        # 金融機関
        Select(self.proc.driver.find_element(By.ID, 'InheriteeFinancialInstitution1')).select_by_visible_text(
            "三菱UFJ銀行（金融機関コード：0005）")
        sleep(0.5)

        banks = utils.bank_search(name=self.branch_name)
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                print(self.branch_name, bank[1])
                print(self.branch_name, utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))

                # 店番
                self.proc.driver.find_element(By.ID, 'InheriteeOfficeNumber1').send_keys(utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name))

                # 店名
                self.proc.driver.find_element(By.ID, 'InheriteeOfficeName1').send_keys(self.branch_name)

def main():
    proc = Mufg()
    proc.account_freezing()
    # proc.personal_information_bill()

if __name__ == '__main__':
    # name = '三菱UFJ銀行'
    # branch_name = '渋谷明治通支店'
    #
    # banks = utils.bank_search(name=name)
    # for bank in banks:
    #     if utils.branch_code_search(bank_code=bank[1], branch_name=branch_name):
    #         print(name, bank[1])
    #         print(branch_name, utils.branch_code_search(bank_code=bank[1], branch_name=branch_name))
    main()