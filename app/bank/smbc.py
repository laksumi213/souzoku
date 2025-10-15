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
        self.account_number = '6559066'
        self.branch_name = '緑園都市支店'
        self.subjects = '普通預金'
        # self.trading_shop_code = '241'
        self.birthday = '1937/11/3'
        # self.birthday = re.findall('[0-9]+', self.birthday)
        self.deathday = '2025-06-12'
        self.deathday = re.findall('[0-9]+', self.deathday)
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
        self.address_pattern = re.findall(pattern, self.address)[0]
        print('address:', re.findall(pattern, self.address)[0])
        print('utils.get_zipcode_from_address(address):', utils.get_zipcode_from_address(self.address_pattern))

        match = re.search(r'([^\d]+)(\d.*)', self.address_pattern[2])
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

        banks = utils.bank_search(name='三井住友銀行')
        for bank in banks:
            if utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name):
                self.branch_code = utils.branch_code_search(bank_code=bank[1], branch_name=self.branch_name)

    def balance_certificate(self):
        # 残高証明書等作成依頼書
        pdf = PdfCreate("A4")

        # 住所
        pdf.draw_string(52, 259, '103-0028')
        pdf.draw_string(52, 249, '東京', 12)
        pdf.draw_string(73, 251.5, '〇', 14)
        pdf.draw_string(84, 249, '東京都中央区八重洲一丁目7-20 八重洲口会館2階', 12)

        # 以下は被相続人の住所のため不要
        # pdf.draw_string(52, 259, f'{self.zipcode[0]}-{self.zipcode[1]}')
        # pdf.draw_string(52, 249, self.address_pattern[0][:len(self.address_pattern[0]) - 1], 12)
        #
        # if self.address_pattern[0][-1] == '都':
        #     pdf.draw_string(73, 251.5, '〇', 14)
        # elif self.address_pattern[0][-1] == '道':
        #     pdf.draw_string(76.5, 251.5, '〇', 14)
        # elif self.address_pattern[0][-1] == '府':
        #     pdf.draw_string(73, 247.5, '〇', 14)
        # elif self.address_pattern[0][-1] == '県':
        #     pdf.draw_string(76.5, 247.5, '〇', 14)

        # address_len = len(f'{self.address_pattern[1]}{self.address_pattern[2]} {self.heir_building_name}')
        # print('address_len:', address_len)
        # if 40 > address_len > 32:
        #     size = 8
        # elif address_len < 32:
        #     size = 10
        # pdf.draw_string(84, 249, f'{self.address_pattern[1]}{self.address_pattern[2]} {self.heir_building_name}', size)

        # 氏名
        pdf.draw_string(57, 240, f'ｿｳｿﾞｸﾆﾝ　{mojimoji.zen_to_han(jaconv.hira2kata(self.heir_name_kana))}')
        pdf.draw_string(57, 236.5, 'ﾀﾞｲﾘﾆﾝ　ｷﾞｮｳｾｲｼｮｼﾎｳｼﾞﾝﾁｪｽﾀｰ　ﾀﾞｲﾋｮｳｼｬｲﾝ　ｼﾐｽﾞ ｾﾝｻｸ')
        pdf.draw_string(57, 232, f'相続人　{self.heir_name}')
        pdf.draw_string(57, 228, '代理人　行政書士法人チェスター　代表社員　清水　茜作')

        # 電話番号
        pdf.draw_string(54, 221, '050　　　6864　　　7034', 12)

        # 被相続人
        pdf.draw_string(57, 187, mojimoji.zen_to_han(jaconv.hira2kata(self.customer_name_kana)))
        pdf.draw_string(57, 174, self.customer_name, 14)
        pdf.draw_string(173,180.5, '〇', 18)
        pdf.draw_string(138,173.5, f'{self.deathday[0][0]}  {self.deathday[0][1]}   {self.deathday[0][2]}   {self.deathday[0][3]}')
        pdf.draw_string(161,173.5, f'{str(self.deathday[1]).zfill(2)[0]}  {str(self.deathday[1]).zfill(2)[1]}')
        pdf.draw_string(175,173.5, f'{str(self.deathday[2]).zfill(2)[0]}   {str(self.deathday[2]).zfill(2)[1]}')

        # 口座
        if "支店" in self.branch_name:
            pdf.draw_string(87, 142, '〇', 14)
            pdf.draw_string(53, 139, self.branch_name.replace('支店',''), 12)
        elif "出張所" in self.branch_name:
            pdf.draw_string(87, 138, '〇', 14)
            pdf.draw_string(53, 139, self.branch_name.replace('出張所', ''), 12)
        pdf.draw_string(69,131,1,14)

        # 引き落とし口座
        # pdf.draw_string(53,109,'ギョ）チェスター',12)
        pdf.draw_string(53,109,'行政書士法人チェスター　代表社員　古庄　夏耶',12)
        pdf.draw_string(53,95,'日本橋',12)
        pdf.draw_string(87, 98, '〇', 14)
        pdf.draw_rect(114, 100.5, 127, 105 )
        pdf.draw_string(133, 94, '8   6   0  0   2  1  1')

        path1 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_三井住友銀行_残高証明書依頼書_郵送専用1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三井住友銀行_残高証明書依頼書_郵送専用.pdf'), page=1, open_bool=False)

        path2 = os.path.join(self.output_path,
                             f'{self.code}{self.heir[0]}様_三井住友銀行_残高証明書依頼書_郵送専用2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '三井住友銀行_残高証明書依頼書_郵送専用.pdf'), page=2, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path, f'【{self.code}】{self.heir[0]}様_三井住友銀行_残高証明書依頼書_郵送専用.pdf'),
            path1, path2)

def main():
    proc = Smbc()
    proc.balance_certificate()


if __name__ == '__main__':
    main()