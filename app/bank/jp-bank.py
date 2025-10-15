# ゆうちょ銀行
import app.utils as utils
import jaconv
import re
from app.controllers.pdf_create import PdfCreate
import os
from datetime import datetime

class JpBank:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.url = None
        self.code = 'G2069'
        self.customer_name = '鈴木　幡雄'
        self.customer_name_kana = 'すずき　はたお'
        self.heir_name = '臼杵　優子'
        self.heir_name_kana = 'うすき　ゆうこ'
        self.bank_account_number = '10150-18288791'
        self.subjects = '通常貯金'
        self.birthday = '1927/12/1'
        self.deathday = '2025/5/26'
        self.address = '東京都目黒区中町2丁目38番21号'
        self.heir_address = '東京都世田谷区若林1丁目2番20号'

        self.date = re.findall(r'\d+', datetime.now().strftime('%Y/%m/%d'))

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　','')}様（スタンダードプラン）\09.申請書類\01.残証申請書類'
        elif os.name == 'posix':
            print('posix')
            self.output_path = os.path.dirname(os.path.dirname(os.getcwd()))

        zipcode = utils.get_zipcode_from_address(self.address)
        self.zipcode = re.findall('[0-9]+', zipcode)
        print('self.zipcode:', self.zipcode)

        self.zipcode_heir = utils.get_zipcode_from_address(self.heir_address)
        print('self.zipcode_heir:', self.zipcode_heir)

        pattern = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
        self.address_pattern = re.findall(pattern, self.address)[0]
        print('self.address_pattern:', self.address_pattern)
        match = re.search(r'([^\d]+)(\d.*)', self.address_pattern[2])
        if match:
            self.place = match.group(1) # 最初のグループ（数字以外の文字）
            self.number = match.group(2)  # 2番目のグループ（数字とハイフンを含む部分）
            print(f"場所: {self.place}") # 出力: 場所: 夏見台
            print(f"番地: {self.number}")

        self.heir_address_pattern = re.findall(pattern, self.heir_address)[0]
        print('self.heir_address_pattern:', self.heir_address_pattern)
        match = re.search(r'([^\d]+)(\d.*)', self.heir_address_pattern[2])
        if match:
            self.heir_place = match.group(1)  # 最初のグループ（数字以外の文字）
            self.heir_number = match.group(2)  # 2番目のグループ（数字とハイフンを含む部分）
            print(f"相続人_場所: {self.heir_place}")  # 出力: 場所: 夏見台
            print(f"相続人_番地: {self.heir_number}")

        self.name = re.findall(r'^(.*?)[ 　](.*)$', self.customer_name)[0]
        print('被相続人', self.name)

        self.name_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.customer_name_kana))[0]
        print('被相続人カナ', self.name_kana)

        self.heir = re.findall(r'^(.*?)[ 　](.*)$', self.heir_name)[0]
        print('相続人', self.heir)

        self.heir_kana = re.findall(r'^(.*?)[ 　](.*)$', jaconv.hira2kata(self.heir_name_kana))[0]
        print('相続人カナ', self.heir_kana)

    def confirmation_table(self):
        # 1ページ目
        pdf = PdfCreate("A4")

        pdf.draw_string(61, 168, '✓', 8)
        pdf.draw_string(61, 164, '✓', 8)
        pdf.draw_string(61, 159, '✓', 8)
        pdf.draw_string(61, 155, '✓', 8)

        # 郵便番号
        pdf.draw_string(42, 129, self.zipcode[0][0], 12)
        pdf.draw_string(48, 129, self.zipcode[0][1], 12)
        pdf.draw_string(54, 129, self.zipcode[0][2], 12)
        pdf.draw_string(63, 129, self.zipcode[1][0], 12)
        pdf.draw_string(69, 129, self.zipcode[1][1], 12)
        pdf.draw_string(75, 129, self.zipcode[1][2], 12)
        pdf.draw_string(81, 129, self.zipcode[1][3], 12)

        # 住所
        pdf.draw_string(91, 129, self.address_pattern[0][:len(self.address_pattern[0]) - 1], 10)

        if self.address_pattern[0][-1] == '都':
            pdf.draw_string(106.5, 130, '〇')
        elif self.address_pattern[0][-1] == '道':
            pdf.draw_string(109.5, 130, '〇')
        elif self.address_pattern[0][-1] == '府':
            pdf.draw_string(106.5, 126.5, '〇')
        elif self.address_pattern[0][-1] == '県':
            pdf.draw_string(109.5, 126.5, '〇')

        pdf.draw_string(115, 129, self.address_pattern[1][:len(self.address_pattern[1]) - 1])

        if self.address_pattern[1][-1] == '市':
            pdf.draw_string(134, 131, '〇')
        elif self.address_pattern[1][-1] == '区':
            pdf.draw_string(134, 128.5, '〇')
        elif self.address_pattern[1][-1] == '郡':
            pdf.draw_string(134, 126, '〇')

        pdf.draw_string(42, 119, self.address_pattern[2])

        # 氏名
        pdf.draw_string(42, 110, jaconv.hira2kata(self.name_kana[0]), 12)
        pdf.draw_string(98, 110, jaconv.hira2kata(self.name_kana[1]), 12)
        pdf.draw_string(42, 102, self.name[0], 12)
        pdf.draw_string(98, 102, self.name[1], 12)

        # 生年月日
        if utils.convert_to_wareki2(self.birthday)[:2] == '明治':
            pdf.draw_string(38.5, 94, '✓', 8)
        elif utils.convert_to_wareki2(self.birthday)[:2] == '大正':
            pdf.draw_string(44.5, 94, '✓', 8)
        elif utils.convert_to_wareki2(self.birthday)[:2] == '昭和':
            pdf.draw_string(51, 94, '✓', 8)
        elif utils.convert_to_wareki2(self.birthday)[:2] == '平成':
            pdf.draw_string(57, 94, '✓', 8)
        elif utils.convert_to_wareki2(self.birthday)[:2] == '令和':
            pdf.draw_string(63.5, 94, '✓', 8)

        pdf.draw_string(71, 93.5,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.birthday))[0].zfill(2)[0], 12)
        pdf.draw_string(78, 93.5,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.birthday))[0].zfill(2)[1], 12)
        pdf.draw_string(88.5, 93.5,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.birthday))[1].zfill(2)[0], 12)
        pdf.draw_string(94.5, 93.5,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.birthday))[1].zfill(2)[1], 12)
        pdf.draw_string(106.5, 93.5,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.birthday))[2].zfill(2)[0], 12)
        pdf.draw_string(112.5, 93.5,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.birthday))[2].zfill(2)[1], 12)

        # 死亡日
        if utils.convert_to_wareki2(self.deathday)[:2] == '平成':
            pdf.draw_string(39, 87, '✓', 8)
        elif utils.convert_to_wareki2(self.deathday)[:2] == '令和':
            pdf.draw_string(53.5, 87, '✓', 8)

        pdf.draw_string(71, 87,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.deathday))[0].zfill(2)[0], 12)
        pdf.draw_string(78, 87,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.deathday))[0].zfill(2)[1], 12)
        pdf.draw_string(88.5, 87,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.deathday))[1].zfill(2)[0], 12)
        pdf.draw_string(94.5, 87,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.deathday))[1].zfill(2)[1], 12)
        pdf.draw_string(106.5, 87,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.deathday))[2].zfill(2)[0], 12)
        pdf.draw_string(112.5, 87,
                        re.findall('[0-9]+', utils.convert_to_wareki2(self.deathday))[2].zfill(2)[1], 12)

        ### 代表相続人
        pdf.draw_string(42, 70, self.zipcode_heir[0], 12)
        pdf.draw_string(48, 70, self.zipcode_heir[1], 12)
        pdf.draw_string(54, 70, self.zipcode_heir[2], 12)
        pdf.draw_string(63, 70, self.zipcode_heir[4], 12)
        pdf.draw_string(69, 70, self.zipcode_heir[5], 12)
        pdf.draw_string(75, 70, self.zipcode_heir[6], 12)
        pdf.draw_string(81, 70, self.zipcode_heir[7], 12)

        pdf.draw_string(91, 70, self.heir_address_pattern[0][:len(self.heir_address_pattern[0]) - 1], 10)
        if self.heir_address_pattern[0][-1] == '都':
            pdf.draw_string(106.5, 71.5, '〇', 10)
        elif self.heir_address_pattern[0][-1] == '道':
            pdf.draw_string(109.5, 71.5, '〇', 10)
        elif self.heir_address_pattern[0][-1] == '府':
            pdf.draw_string(106.5, 68.5, '〇', 10)
        elif self.heir_address_pattern[0][-1] == '県':
            pdf.draw_string(109.5, 68.5, '〇', 10)

        if not self.heir_address_pattern[1][-1] == '町':
            pdf.draw_string(115, 70, self.heir_address_pattern[1][:len(self.heir_address_pattern[1]) - 1])
        else:
            pdf.draw_string(115, 70, self.heir_address_pattern[1])

        if self.heir_address_pattern[1][-1] == '市':
            pdf.draw_string(134, 73, '〇', 10)
        elif self.heir_address_pattern[1][-1] == '区':
            pdf.draw_string(134, 70, '〇', 10)
        elif self.heir_address_pattern[1][-1] == '郡':
            pdf.draw_string(134, 67, '〇', 10)

        pdf.draw_string(42, 61, self.heir_address_pattern[2])

        # 相続人氏名
        pdf.draw_string(42, 52, jaconv.hira2kata(self.heir_kana[0]), 12)
        pdf.draw_string(98, 52, jaconv.hira2kata(self.heir_kana[1]), 12)
        pdf.draw_string(42, 43, self.heir[0], 12)
        pdf.draw_string(98, 43, self.heir[1], 12)

        # 連絡先
        # contact = re.findall('[0-9]+', self.customer['連絡先_携帯']) if self.customer[
        #                                                                     '連絡先_携帯'] != '' else re.findall(
        #     '[0-9]+', self.customer['連絡先_自宅'])

        path1 = os.path.join(self.output_path, f'【{self.code}】{self.heir[0]}様_ゆうちょ_相続確認表1.pdf')
        pdf.pdf_save(path1, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'ゆうちょ_相続確認表_20230508改正.pdf'), page=3, open_bool=False)

        # 2ページ目
        pdf = PdfCreate("A4")

        ## 弊社内容
        pdf.draw_string(43, 72, '1')
        pdf.draw_string(49.5, 72, '0')
        pdf.draw_string(55, 72, '3')
        pdf.draw_string(62.5, 72, '0')
        pdf.draw_string(69, 72, '0')
        pdf.draw_string(74, 72, '2')
        pdf.draw_string(80, 72, '8')

        pdf.draw_string(90, 72, '東京')
        pdf.draw_string(108, 73.5, '〇')
        pdf.draw_string(118, 72, '中央')
        pdf.draw_string(138, 75, '〇')

        pdf.draw_string(43, 63, '八重洲1-7-20  八重洲口会館2階')
        pdf.draw_string(40, 57, 'ｷﾞｮｳｾｲｼｮｼﾎｳｼﾞﾝ　ﾀﾞｲﾋｮｳｼｬｼﾝ　ｼﾐｽﾞ ｾﾝｻｸ', 6)
        pdf.draw_string(40, 52, '行政書士法人チェスター　代表社員', 8)
        pdf.draw_string(40, 48, f'清水　茜作　担当：森町（{self.code}）', 8)

        pdf.draw_string(103, 55, '0')
        pdf.draw_string(106.5, 55, '5')
        pdf.draw_string(110, 55, '0')
        pdf.draw_string(115, 55, '6')
        pdf.draw_string(118, 55, '8')
        pdf.draw_string(121, 55, '6')
        pdf.draw_string(125, 55, '4')
        pdf.draw_string(130, 55, '7')
        pdf.draw_string(133, 55, '0')
        pdf.draw_string(136.5, 55, '3')
        pdf.draw_string(140, 55, '4')

        pdf.draw_string(113, 48.5, '✓')
        pdf.draw_string(106.5, 38, '✓')
        pdf.draw_string(106.5, 28, '✓')

        path2 = os.path.join(self.output_path, f'【{self.code}】{self.heir[0]}様_ゆうちょ_相続確認表2.pdf')
        pdf.pdf_save(path2, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'ゆうちょ_相続確認表_20230508改正.pdf'), page=4, open_bool=False)

        # 3ページ目
        pdf = PdfCreate("A4")

        i = 0
        if self.bank_account_number:
            if self.subjects:
                pdf.draw_string(20, (130.5 - i * 10.5), self.subjects.replace('郵便', ''))
            pdf.draw_string(46, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[0].zfill(5)[0])
            pdf.draw_string(52, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[0].zfill(5)[1])
            pdf.draw_string(58, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[0].zfill(5)[2])
            pdf.draw_string(64, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[0].zfill(5)[3])
            pdf.draw_string(70, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[0].zfill(5)[4])
    
            pdf.draw_string(78, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[1].zfill(8)[0])
            pdf.draw_string(84, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[1].zfill(8)[1])
            pdf.draw_string(90, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[1].zfill(8)[2])
            pdf.draw_string(96, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[1].zfill(8)[3])
            pdf.draw_string(102, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[1].zfill(8)[4])
            pdf.draw_string(108, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[1].zfill(8)[5])
            pdf.draw_string(114, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[1].zfill(8)[6])
            pdf.draw_string(120, (130.5 - i * 10.5), str(self.bank_account_number).split('-')[1].zfill(8)[7])

        # 投資信託の有無
        pdf.draw_string(46, 48, '✓', 6)

        # 記号番号不明の調査
        pdf.draw_string(46, 39.5, '✓', 6)

        path3 = os.path.join(self.output_path, f'【{self.code}】{self.heir[0]}様_ゆうちょ_相続確認表3.pdf')
        pdf.pdf_save(path3, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'ゆうちょ_相続確認表_20230508改正.pdf'), page=5, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path, f'【{self.code}】{self.heir[0]}様_ゆうちょ_相続確認表.pdf'),
            path1, path2, path3)

        # 貯金等照会書
        pdf = PdfCreate("A4")

        pdf.draw_string(52, 223, '行政書士法人チェスター', 12)
        # pdf.draw_string(48, 143, '✓', 12)

        pdf.draw_string(19.5, 201, '✓', 8)
        pdf.draw_string(51, 167,
                        f'{jaconv.hira2kata(self.customer_name_kana)}')
        pdf.draw_string(51, 154, f'{self.customer_name}', 12)

        # 旧姓
        # pdf.draw_string(143, 167, jaconv.hira2kata(self.customer["旧姓_ふりがな"]))
        # pdf.draw_string(143, 154, self.customer["旧姓"], 12)
        # if not self.customer['旧姓'] == '':
        #     pdf.draw_string(143, 167, jaconv.hira2kata(self.customer['旧姓_ふりがな']))
        #     pdf.draw_string(143, 154, self.customer['旧姓'], 12)

        pdf.draw_string(49, 144, '✓', 12)
        customer_birthday = re.findall('[0-9]+', self.birthday)
        pdf.draw_string(136, 144, customer_birthday[0][0])
        pdf.draw_string(141, 144, customer_birthday[0][1])
        pdf.draw_string(147.5, 144, customer_birthday[0][2])
        pdf.draw_string(152, 144, customer_birthday[0][3])
        pdf.draw_string(164, 144, str(customer_birthday[1]).zfill(2)[0])
        pdf.draw_string(169, 144, str(customer_birthday[1]).zfill(2)[1])
        pdf.draw_string(181, 144, str(customer_birthday[2]).zfill(2)[0])
        pdf.draw_string(186, 144, str(customer_birthday[2]).zfill(2)[1])

        # 郵便番号
        customer_zipcode = self.zipcode
        pdf.draw_string(53, 132.5, customer_zipcode[0][0])
        pdf.draw_string(58, 132.5, customer_zipcode[0][1])
        pdf.draw_string(64, 132.5, customer_zipcode[0][2])
        pdf.draw_string(75, 132.5, customer_zipcode[1][0])
        pdf.draw_string(81, 132.5, customer_zipcode[1][1])
        pdf.draw_string(87, 132.5, customer_zipcode[1][2])
        pdf.draw_string(92, 132.5, customer_zipcode[1][3])

        # 連絡先

        # 住所
        pdf.draw_string(49, 122, self.address_pattern[0][:len(self.address_pattern[0]) - 1], 12)
        if self.address_pattern[0][-1] == '都':
            pdf.draw_string(68, 124, '✓')
        elif self.address_pattern[0][-1] == '道':
            pdf.draw_string(78, 124, '✓')
        elif self.address_pattern[0][-1] == '府':
            pdf.draw_string(68, 118, '✓')
        elif self.address_pattern[0][-1] == '県':
            pdf.draw_string(78, 118, '✓')
        pdf.draw_string(92, 122, self.address_pattern[1] + self.address_pattern[2], 12)

        # 旧住所
        # if self.customer['旧住所1']:
        #     prefectures = re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県', self.customer['旧住所1']).group()
        #     city = self.customer['旧住所1'].replace(prefectures, '')
        #     pdf.draw_string(49, 96, prefectures[0:len(prefectures) - 1], 12)
        #     if prefectures[-1] == '都':
        #         pdf.draw_string(69, 99, '✓')
        #     elif prefectures[-1] == '道':
        #         pdf.draw_string(78, 99, '✓')
        #     elif prefectures[-1] == '府':
        #         pdf.draw_string(69, 93.5, '✓')
        #     elif prefectures[-1] == '県':
        #         pdf.draw_string(78, 93.5, '✓')
        #     pdf.draw_string(92, 96, city, 12)

        # if self.customer['旧住所2']:
        #     pdf.draw_string(49, 69,
        #                     re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県', self.customer['旧住所2']).group(), 12)
        #     pdf.draw_string(92, 69, str(self.customer['旧住所2']).replace(
        #         re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県', self.customer['旧住所1']).group(), ''), 12)
        #
        # if self.customer['旧住所3']:
        #     pdf.draw_string(49, 45,
        #                     re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県', self.customer['旧住所3']).group(), 12)
        #     pdf.draw_string(92, 45, str(self.customer['旧住所2']).replace(
        #         re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県', self.customer['旧住所3']).group(), ''), 12)


        # if self.customer[15] == '-':
        #     pdf.draw_string(92, 122, self.customer[12] + self.customer[13] + self.customer[14], 12)
        # else:
        #     pdf.draw_string(92, 122,
        #                   self.customer[12] + self.customer[13] + self.customer[14] + self.customer[15], 12)

        # 調査対象項目
        pdf.draw_string(49, 37, '✓')
        pdf.draw_string(72, 37, '✓')
        pdf.draw_string(151, 37, '✓')
        pdf.draw_string(49, 30.5, '✓')
        pdf.draw_string(72, 30.5, '✓')
        pdf.draw_string(93, 30.5, '✓')  # その他
        pdf.draw_string(115, 31.5, '財形、積立、民営化前郵便貯金')

        path4 = os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_ゆうちょ_貯金等照会書1.pdf')
        pdf.pdf_save(path4, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'ゆうちょ_貯金等照会書（相続用）.pdf'), page=1, open_bool=False)


        pdf = PdfCreate("A4")
        pdf.draw_string(45, 264, '✓', 8)
        pdf.draw_string(83, 264, '✓', 8)

        customer_deathday = re.findall('[0-9]+', self.deathday)
        pdf.draw_string(133, 263, customer_deathday[0][0])
        pdf.draw_string(138, 263, customer_deathday[0][1])
        pdf.draw_string(144, 263, customer_deathday[0][2])
        pdf.draw_string(150, 263, customer_deathday[0][3])
        pdf.draw_string(162, 263, str(customer_deathday[1]).zfill(2)[0])
        pdf.draw_string(168, 263, str(customer_deathday[1]).zfill(2)[1])
        pdf.draw_string(179, 263, str(customer_deathday[2]).zfill(2)[0])
        pdf.draw_string(185, 263, str(customer_deathday[2]).zfill(2)[1])
        pdf.draw_string(83, 238, '相続のため')
        # pdf.draw_string(22, 207, '✓', 12)
        pdf.draw_string(86, 230, '1', 12)

        pdf.draw_string(92, 212, '1', 12)
        pdf.draw_string(97.5, 212, '1', 12)
        pdf.draw_string(104, 212, '3', 12)
        pdf.draw_string(109, 212, '2', 12)
        pdf.draw_string(115, 212, '0', 12)

        pdf.draw_string(139, 212, '2', 12)
        pdf.draw_string(144, 212, '3', 12)
        pdf.draw_string(150, 212, '0', 12)
        pdf.draw_string(156, 212, '9', 12)
        pdf.draw_string(162, 212, '3', 12)
        pdf.draw_string(168, 212, '3', 12)
        pdf.draw_string(173, 212, '6', 12)
        pdf.draw_string(178, 212, '1', 12)

        pdf.draw_string(81, 202, '✓', 12)
        path5 = os.path.join(self.output_path,
                             f'【{self.code}】{self.heir[0]}様_ゆうちょ_貯金等照会書2.pdf')
        pdf.pdf_save(path5, os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'assets/pdf',
                                         'ゆうちょ_貯金等照会書（相続用）.pdf'), page=2, open_bool=False)

        pdf.pdf_marge(
            os.path.join(self.output_path, f'{self.code}{self.heir[0]}様_ゆうちょ_相続確認表_{self.date[0]}{self.date[1]}{self.date[2]}.pdf'),
            path4, path5)


def main():
    proc = JpBank()
    proc.confirmation_table()


if __name__ == '__main__':
    main()