# 三井住友銀行
import app.utils as utils
import jaconv
import mojimoji
import re
from app.controllers.pdf_create import PdfCreate
import os


class Smbc:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.url = None
        self.code = 'G2014'
        self.customer_name = '菅沼　純子'
        self.customer_name_kana = 'すがぬま　すみこ'
        self.heir_name = '菅沼　富男'
        self.heir_name_kana = 'すがぬま　とみお'
        self.heir_tel = '080-5546-7144'
        self.account_number = '173339'
        self.trading_store_name = '戸塚支店'
        self.trading_shop_code = '241'
        self.birthday = '1937/11/3'
        # self.birthday = re.findall('[0-9]+', self.birthday)
        self.deathday = '2025-06-12'
        # self.deathday = re.findall('[0-9]+', self.deathday)
        self.address = '神奈川県横浜市泉区緑園4丁目3番地1'
        self.building_name = 'サンステージ緑園都市東の街11番館603号'
        self.heir_address = '神奈川県横浜市泉区緑園4丁目3番地1'
        self.heir_building_name = 'サンステージ緑園都市東の街11番館603号'

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　','')}様（スタンダードプラン）\07.申請書類\01.残証申請書類'
        elif os.name == 'posix':
            print('posix')
            self.output_path = os.path.dirname(os.path.dirname(os.getcwd()))

        zipcode = utils.get_zipcode_from_address(self.address)
        self.zipcode = re.findall('[0-9]+', zipcode)
        print('self.zipcode:', self.zipcode)

        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        address = re.findall(pattern, self.address)[0]
        print('address:', re.findall(pattern, self.address)[0])
        print('utils.get_zipcode_from_address(address):', utils.get_zipcode_from_address(address))

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

    def balance_certificate(self):
        # 残高証明書等作成依頼書
        pdf = PdfCreate("A4")

        path1 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_三井住友銀行_残高証明書依頼書_郵送専用.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三井住友銀行_残高証明書依頼書_郵送専用.pdf'), page=1, open_bool=True)


def main():
    proc = Smbc()
    proc.balance_certificate()

if __name__ == '__main__':
    main()