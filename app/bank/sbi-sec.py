# SBI証券
from app.controllers.pdf_create import PdfCreate
import jaconv
import re
from app._utils.web_operation import Web
import app.utils as utils
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os


class SbiSec:
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
        self.bank_number = None
        self.code = 'G1967'
        self.customer_name = '宇野　正名'
        self.customer_name_kana = 'うの　まさな'
        self.heir_name = '宇野　美穂'
        self.heir_name_kana = 'うの　みほ'
        self.bank_account_number = ''
        self.birthday = re.findall('[0-9]+', '1958/9/18')
        self.deathday = re.findall('[0-9]+', '2025/6/27')
        self.address = '千葉県船橋市夏見台1-13-24'
        self.passed_away_date = re.findall('[0-9]+', '2025-06-27')
        self.bank_number = re.findall('[0-9]+','322-0252565')
        self._heir_name = re.findall(r'^(.*?)[ 　](.*)$', self.heir_name)[0]


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
        self.proc.driver.find_element(By.ID, 'agentChargeName').send_keys(f'森町翼({self.code})')
        self.proc.driver.find_element(By.ID, 'agentChargeNameKana').send_keys('モリマチツバサ')
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

    # SBI証券_個人情報に関する開示等請求書
    def personal_information_bill(self):
        pdf = PdfCreate(pagesize='A4')
        pdf.draw_string(58, 253.5, '103-0028')
        pdf.draw_string(117, 253.5, '050      6864      7034')
        pdf.draw_string(58, 246.5, '東京都中央区八重洲一丁目7-20 八重洲口会館2階', 12)
        pdf.draw_string(58, 239, f'被相続人　{self.customer_name}　相続人　{self.heir_name}',)
        pdf.draw_string(58, 234, '代理人　行政書士法人チェスター　代表社員　清水　茜作',)
        pdf.draw_string(58, 207, jaconv.hira2kata(self.customer_name_kana))
        pdf.draw_string(58, 202, self.customer_name, 12)
        pdf.draw_string(85, 197, f'{self.birthday[0]}　　{self.birthday[1].zfill(2)}　{self.birthday[2].zfill(2)}')
        pdf.draw_string(130.0, 202.5, self.bank_number[0][0], 12)
        pdf.draw_string(135.5, 202.5, self.bank_number[0][1], 12)
        pdf.draw_string(140.9, 202.5, self.bank_number[0][2], 12)
        pdf.draw_string(158.0, 202.5, self.bank_number[1].zfill(7)[1], 12)
        pdf.draw_string(163.3, 202.5, self.bank_number[1].zfill(7)[2], 12)
        pdf.draw_string(168.4, 202.5, self.bank_number[1].zfill(7)[3], 12)
        pdf.draw_string(173.6, 202.5, self.bank_number[1].zfill(7)[4], 12)
        pdf.draw_string(178.7, 202.5, self.bank_number[1].zfill(7)[5], 12)
        pdf.draw_string(183.5, 202.5, self.bank_number[1].zfill(7)[6], 12)
        pdf.draw_string(54.5, 170.5 , '〇',16)   # 個人情報の開示
        pdf.draw_string(84, 170.5, '〇',16)  # 書面
        pdf.draw_string(32.3, 120.5, '〇',16)    # 残高証明書
        pdf.draw_string(57.5, 121.5, f'{self.deathday[0]}    　{self.deathday[1].zfill(2)}　 　{self.deathday[2].zfill(2)}', 9)
        pdf.draw_string(117.5, 120.5, '〇',16)
        # pdf.draw_string(119, 120, '〇',16)   # 顧客勘定元帳

        output_path = r'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\G1967宇野美穂様（フルサポートプラン）\07.申請書類\01.残証申請書類'
        path1 = os.path.join(output_path, f'【{self.code}】{self._heir_name[0]}様_SBI証券_個人情報に関する開示等請求書.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.getcwd()), './assets/pdf', 'SBI証券_個人情報に関する開示等請求書.pdf'), page=2, open_bool=True)

        # 4ページ目
        pdf = PdfCreate(pagesize='A4')
        pdf.draw_rect(21, 66.9, 199.2, 74.5, linewidth=3, colors='RED')
        path2 = os.path.join(output_path, f'【{self.code}】{self._heir_name[0]}様_SBI証券_個人情報に関する開示等請求書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.getcwd()), './assets/pdf', 'SBI証券_個人情報に関する開示等請求書.pdf'), page=4, open_bool=False)

        # 6ページ目
        pdf = PdfCreate(pagesize='A4')
        pdf.draw_string(117, 210, '←', size=40, colors='#FF0000')
        pdf.draw_string(132, 213, f'{self.bank_number[0]}-{self.bank_number[1]}ｷﾞｮｳｾｲｼｮｼﾎｳｼﾞﾝﾁｪｽﾀｰ', size=13, colors='#FF0000')
        # pdf.draw_string(132, 213, f'口座番号：{self.bank_number[0]}-{self.bank_number[1]}', size=13, colors='#FF0000')
        path3 = os.path.join(output_path, f'【{self.code}】{self._heir_name[0]}様_SBI証券_個人情報に関する開示等請求書3.pdf')
        pdf.pdf_save(path3, os.path.join(os.path.dirname(os.getcwd()), './assets/pdf', 'SBI証券_個人情報に関する開示等請求書.pdf'), page=6, open_bool=False)

        # pdf.pdf_marge(os.path.join(output_path, f'【{self.code}】{self._heir_name[0]}様_SBI証券_個人情報に関する開示等請求書.pdf'), path1, path2, path3)
        pdf.pdf_marge(os.path.join(output_path, f'【{self.code}】{self._heir_name[0]}様_SBI証券_【行チェ】証明書費用振込申請アプリ用.pdf'), path2, path3)


def main():
    proc = SbiSec()
    # proc.account_freezing()
    proc.personal_information_bill()

if __name__ == '__main__':
    main()