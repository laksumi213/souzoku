# 楽天証券
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
import asyncio
from webdriver_manager.chrome import ChromeDriverManager


class RakutenSec:
    def __init__(self):
        super().__init__()
        self.deathday = None
        self.heir_name_kana = None
        self.heir_name = None
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
        self.heir_name = '宇野　美穂'
        self.heir_name_kana = 'うの　みほ'
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
        print('被相続人', name)

        name_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.customer_name_kana))[0]
        print('被相続人カナ', name_kana)

        heir = re.findall(r'^(.*?)[ 　](.*)$', self.heir_name)[0]
        print('相続人', heir)

        heir_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.heir_name_kana))[0]
        print('相続人カナ', heir_kana)

        print(address)
        print('birthday:', self.birthday)

        self.proc = Web()
        url = 'https://member.rakuten-sec.co.jp/service/setup/inheritanceInputInit.do?inheritance=agent'
        self.proc.web_open(url)

        self.proc.driver.find_element(By.NAME, 'inheritanceAccountBean.giverLastName').send_keys(name[0])
        self.proc.driver.find_element(By.NAME, 'inheritanceAccountBean.giverFirstName').send_keys(name[1])
        self.proc.driver.find_element(By.NAME, 'inheritanceAccountBean.giverLastNameKana').send_keys(jaconv.hira2kata(name_kana[0]))
        self.proc.driver.find_element(By.NAME, 'inheritanceAccountBean.giverFirstNameKana').send_keys(jaconv.hira2kata(name_kana[1]))
        self.proc.driver.find_element(By.ID, 'giverPostCode1').send_keys(jaconv.hira2kata(zipcode[0]))
        self.proc.driver.find_element(By.ID, 'giverPostCode2').send_keys(jaconv.hira2kata(zipcode[1]))
        time.sleep(1)
        Select(self.proc.driver.find_element(By.ID, "giverBirthCeYear")).select_by_value(self.birthday[0])
        Select(self.proc.driver.find_element(By.ID, "giverBirthMonth")).select_by_value(self.birthday[1])
        Select(self.proc.driver.find_element(By.ID, "giverBirthDay")).select_by_value(self.birthday[2])
        if match:
            self.proc.driver.find_element(By.ID, 'giverAddressTown').send_keys(number)
            self.proc.driver.find_element(By.ID, 'giverAddressTownKana').send_keys(number)
        Select(self.proc.driver.find_element(By.ID, "giverDeathCeYear")).select_by_value(self.deathday[0])
        Select(self.proc.driver.find_element(By.ID, "giverDeathMonth")).select_by_value(self.deathday[1])
        Select(self.proc.driver.find_element(By.ID, "giverDeathDay")).select_by_value(self.deathday[2])

        # 手続受任者
        self.proc.driver.find_element(By.ID, 'agentCorpName').send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.ID, 'agentBranchName').send_keys('東京本店')
        self.proc.driver.find_element(By.ID, 'agentName').send_keys(f'故　{name[0]}{name[1]}様　相続人　{heir[0]}{heir[1]}様　相続人代理人　行政書士法人チェスター')
        # self.proc.driver.find_element(By.ID, 'agentName').send_keys(f'故　{name[0]}{name[1]}様　相続人　{name_kana[0]}{name_kana[1]}様　相続人代理人　行政書士法人チェスター　代表社員　清水　茜作')
        self.proc.driver.find_element(By.ID, 'agentNameKana').send_keys(f'コ　{name_kana[0]}{name_kana[1]}サマ　ソウゾクニン　{heir_kana[0]}{heir_kana[1]}サマ　ソウゾクニンダイリニン　ギョウセイショシホウジンチェスター')
        # self.proc.driver.find_element(By.ID, 'agentNameKana').send_keys(f'コ　{name_kana[0]}{name_kana[1]}サマ　ソウゾクニン　{heir_kana[0]}{heir_kana[1]}サマ　ソウゾクニンダイリニン　ギョウセイショシホウジンチェスター　ダイヒョウシャイン　シミズ　センサク')
        self.proc.driver.find_element(By.ID, 'agentChargeName').send_keys('事務担当　森町翼')
        self.proc.driver.find_element(By.ID, 'agentChargeNameKana').send_keys('ジムタントウモリマチツバサ')
        self.proc.driver.find_element(By.ID, 'agentPostCode1').send_keys('103')
        self.proc.driver.find_element(By.ID, 'agentPostCode2').send_keys('0028')
        time.sleep(1)
        self.proc.driver.find_element(By.XPATH, '//*[@id="agentAcceptedWork"]/div/div[1]/label/span').click()
        time.sleep(1)
        self.proc.driver.find_element(By.ID, 'agentAddressTown').send_keys('１－７－２０')
        self.proc.driver.find_element(By.ID, 'agentAddressBldg').send_keys('八重洲口会館２階')

        self.proc.driver.find_element(By.ID, 'agentMail').send_keys('t.morimachi_gy@chester-tax.com')
        self.proc.driver.find_element(By.ID, 'agentMailRe').send_keys('t.morimachi_gy@chester-tax.com')

        self.proc.driver.find_element(By.ID, 'agentAddressTownKana').send_keys('１－７－２０')
        self.proc.driver.find_element(By.ID, 'agentAddressBldgKana').send_keys('ヤエスグチカイカン２カイ')

        self.proc.driver.find_element(By.NAME, 'inheritanceAccountBean.agentTel1No1').send_keys('050')
        self.proc.driver.find_element(By.NAME, 'inheritanceAccountBean.agentTel1No2').send_keys('6864')
        self.proc.driver.find_element(By.NAME, 'inheritanceAccountBean.agentTel1No3').send_keys('7034')

        self.proc.driver.find_element(By.XPATH, '//*[@id="js-form-validate_inheritanceAgent"]/div[11]/div[13]/div[10]/div/div/label/span').click()
        self.proc.driver.find_element(By.NAME, 'inheritanceAccountBean.agentInheritanceMethodDetail').send_keys('決まっていない')

        # 残高証明書発行依頼
        self.proc.driver.find_element(By.XPATH, '//*[@id="agentBalanceCertificate"]/div[3]/label/span').click()

        # 入力内容の確認
        self.proc.driver.find_element(By.ID, 'nextButton').click()

        # self.proc.driver.find_element(By.ID, '00N0K00000LYk1u').send_keys('森町　翼')
        # self.proc.driver.find_element(By.ID, '00N2y0000010J8s').send_keys('モリマチ　ツバサ')
        # self.proc.driver.find_element(By.NAME, 'email').send_keys('t.morimachi_gy@chester-tax.com')
        # self.proc.driver.find_element(By.NAME, '00N0K00000LYk1y').send_keys('代理人')
        # self.proc.driver.find_element(By.NAME, 'phone').send_keys('050-6864-7034')
        # self.proc.driver.find_element(By.ID, '00N0K00000JEq7R').send_keys('1030028')
        # self.proc.driver.find_element(By.ID, 'zipbutton').click()
        # time.sleep(0.5)
        # self.proc.driver.find_element(By.ID, '00N0K00000JEq7M').send_keys(mojimoji.han_to_zen('一丁目7-20 八重洲口会館2階'))
        # self.proc.driver.find_element(By.ID, '00N0K00000JEq7Q').send_keys('森町　翼（' + mojimoji.han_to_zen(self.code) +'）')
        # self.proc.driver.find_element(By.ID, '00N0K00000LYk1t').click()


def main():
    proc = RakutenSec()
    proc.account_freezing()

if __name__ == '__main__':
    main()