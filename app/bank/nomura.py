# 野村證券
import app.utils as utils
import jaconv
import mojimoji
import re
from app.controllers.pdf_create import PdfCreate
import os


class Nomura:
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

        # dt_now = datetime.now().strftime('%Y/%m/%d')
        # pdf.draw_string(147, 220, dt_now[0:4])
        # pdf.draw_string(170, 220, dt_now[5:7])
        # pdf.draw_string(183, 220, dt_now[8:])

        pdf.draw_string(62, 204, self.customer_name, 12)
        pdf.draw_string(62, 214, jaconv.hira2hkata(self.customer_name_kana), 12)

        birthday = re.findall('[0-9]+', self.birthday)
        ad = utils.convert_to_wareki2(self.birthday)[0:2]
        if ad == '大正':
            pdf.draw_string(46, 195, '✓', 10)
        elif ad == '昭和':
            pdf.draw_string(46, 189.5, '✓', 10)
        elif ad == '平成':
            pdf.draw_string(59.5, 195, '✓', 10)
        elif ad == '令和':
            pdf.draw_string(59.5, 189.5, '✓', 10)

        pdf.draw_string(74, 192, re.findall('[0-9]+', utils.convert_to_wareki2(self.birthday))[0], 10)
        pdf.draw_string(85, 192, birthday[1], 10)
        pdf.draw_string(97, 192, birthday[2], 10)

        deathday = re.findall('[0-9]+', self.deathday)
        pdf.draw_string(150, 192, deathday[0], 10)
        pdf.draw_string(168, 192, deathday[1], 10)
        pdf.draw_string(182, 192, deathday[2], 10)

        # if '支店' in self.customer['支店名']:
        #     pdf.draw_string(62, 172, self.customer['支店名'].replace('支店', ''), 12)
        #     pdf.draw_string(101.5, 169.5, '〇', 12)

        if self.trading_store_name:
            pdf.draw_string(62, 172, self.trading_store_name.replace('支店', ''), 12)
            pdf.draw_string(113, 172, str(self.trading_shop_code)[0], 12)
            pdf.draw_string(120, 172, str(self.trading_shop_code)[1], 12)
            pdf.draw_string(129, 172, str(self.trading_shop_code)[2], 12)

        if self.account_number:
            pdf.draw_string(137, 172, str(self.account_number).zfill(7)[0], 12)
            pdf.draw_string(146, 172, str(self.account_number).zfill(7)[1], 12)
            pdf.draw_string(155, 172, str(self.account_number).zfill(7)[2], 12)
            pdf.draw_string(163, 172, str(self.account_number).zfill(7)[3], 12)
            pdf.draw_string(171, 172, str(self.account_number).zfill(7)[4], 12)
            pdf.draw_string(179, 172, str(self.account_number).zfill(7)[5], 12)
            pdf.draw_string(188, 172, str(self.account_number).zfill(7)[6], 12)


        # pdf.draw_string(62, 84.5, self.zipcode[0], 8)
        # pdf.draw_string(76, 84.5, self.zipcode[1], 8)
        pdf.draw_string(62, 84.5, '103', 8)
        pdf.draw_string(76, 84.5, '0028', 8)
        # pdf.draw_string(60, 80, f'{self.heir_address} {self.heir_building_name}',9)
        pdf.draw_string(60, 80, f'東京都中央区八重洲一丁目7-20 八重洲口会館2階',9)
        # pdf.draw_string(57, 67, f'被相続人　{self.customer_name}　相続人　{self.heir_name}', 6)
        pdf.draw_string(57, 67, f'故　{self.customer_name}　相続手続代理人　{self.heir_name}', 6)
        pdf.draw_string(57, 64, '行政書士法人チェスター　代表社員　清水　茜作', 6)
        pdf.draw_string(67, 74, f'ｺ {mojimoji.zen_to_han(jaconv.hira2kata(self.customer_name_kana))} ｿｳｿﾞｸﾃﾂﾂﾞｷﾀﾞｲﾘﾆﾝ {mojimoji.zen_to_han(jaconv.hira2kata(self.heir_name_kana))}', 5)
        pdf.draw_string(67, 71.5, 'ｷﾞｮｳｾｲｼｮｼﾎｳｼﾞﾝﾁｪｽﾀｰ ﾀﾞｲﾋｮｳｼｬｲﾝ ｼﾐｽﾞｾﾝｻｸ', 5)
        # pdf.draw_string(149, 68.5, re.findall('[0-9]+', self.heir_tel)[0])
        # pdf.draw_string(166.5, 68.5, re.findall('[0-9]+', self.heir_tel)[1])
        # pdf.draw_string(183, 68.5, re.findall('[0-9]+', self.heir_tel)[2])
        pdf.draw_string(149, 68.5, '050')
        pdf.draw_string(166.5, 68.5, '6864')
        pdf.draw_string(183, 68.5, '7034')

        path1 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_野村證券_残高証明書申請書1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '野村證券_残高証明書申請書.pdf'), page=1, open_bool=False)

        # 2ページ目　原本返却依頼書
        pdf = PdfCreate("A4")

        # pdf.draw_string(121, 206, dt_now[0:4])
        # pdf.draw_string(140, 206, dt_now[5:7])
        # pdf.draw_string(155, 206, dt_now[8:])
        pdf.draw_string(131, 196, self.customer_name, 12)
        pdf.draw_string(74, 183, '103', 12)
        pdf.draw_string(95, 183, '0028', 12)
        pdf.draw_string(81, 167, '東京都中央区八重洲1-7-20', 12)
        pdf.draw_string(81, 154, '八重洲口会館2階', 12)

        pdf.draw_string(81, 140, f'行政書士法人チェスター 森町（{self.code}）', 11)
        pdf.draw_string(96, 118.25, '050-6864-7034')

        path2 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_野村證券_残高証明書申請書2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         '野村證券_残高証明書申請書.pdf'), page=2, open_bool=False)

        # os.makedirs(os.path.join(self.customer[0]['フォルダパス'], '金融機関手続', '残高証明書', '申請書'), exist_ok=True)

        pdf.pdf_marge(
            os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_野村證券_残高証明書申請書.pdf'),
            path1, path2)

def main():
    proc = Nomura()
    proc.balance_certificate()

if __name__ == '__main__':
    main()