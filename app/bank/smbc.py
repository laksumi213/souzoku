# 三井住友銀行
from time import sleep

import app.utils as utils
import jaconv
import mojimoji
import re
import pyperclip
from app.controllers.pdf_create import PdfCreate
import os
from app._utils.web_operation import Web
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select


class Smbc:
    def __init__(self):
        super().__init__()
        self.proc = None
        self.url = None
        self.code = 'G2087'
        self.customer_name = '関谷　雄孝'
        self.customer_name_kana = 'せきや　ゆうこう'
        self.heir_name = '西澤　直子'
        self.heir_name_kana = 'にしざわ　なおこ'
        self.heir_tel = '090-6547-2471'
        self.account_number = '3332563'
        self.branch_name = '錦糸町'
        self.subjects = '普通預金'
        # self.trading_shop_code = '241'
        self.birthday = '1930/1/3'
        # self.birthday = re.findall('[0-9]+', self.birthday)
        self.deathday = '2025/6/27'
        # self.deathday = re.findall('[0-9]+', self.deathday)
        self.address = '東京都墨田区緑2丁目6番10号'
        self.building_name = ''
        self.heir_address = '東京都墨田区緑2丁目1番3号'
        self.heir_building_name = ''

        if os.name == 'nt':
            print('nt')
            self.output_path = fr'\\192.168.11.20\行政書士法人チェスター\01.個別ＪＯＢ\{self.code}{self.heir_name.replace('　','')}様（スタンダードプラン）\04.残高証明書・取引履歴'
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

    # 口座凍結
    def account_freezing(self):
        # 携帯電話番号の入力と画像認証
        self.proc = Web()
        url = 'https://inherit.smbc.co.jp/INR/#/SINR10101'
        self.proc.web_open(url)
        # messagebox.showinfo("", "「個人情報関係✔を入れてから」OKボタンをクリックしてください。")
        # 今回は最終的に表示される「次へ」ボタンのIDを待機要素とします。
        NEXT_BUTTON_ID = "UNQ_oranchor_1086"
        dynamic_element = (By.ID, NEXT_BUTTON_ID)
        # dynamic_element = (By.ID, "UNQ_formcontrolinputtextExt_1003")
        WebDriverWait(self.proc.driver, 60).until(
            EC.presence_of_element_located(dynamic_element)
        )
        print("動的コンテンツのロード完了を確認しました。")

        # # 最終的なHTMLソースコードを取得する
        # final_html_source = self.proc.driver.page_source
        # pyperclip.copy(final_html_source)
        # print("ソースのコピーが完了しました。")

        # ----------------------------------------------------
        # I. 同意事項の操作 (画面上部)
        # ----------------------------------------------------

        # 事前確認を「確認しました」にチェック
        self.proc.driver.find_element(By.ID, "UNQ_checkboxExt_1001").click()

        # 1. 規約のテキストエリアの親要素（overflow:autoを持つ）を特定
        #    ID: agree-window
        agree_container = self.proc.driver.find_element(By.ID, "agree-window")

        # 2. JavaScriptを使用して、要素のスクロール位置を最下部に強制的に移動させる
        #    - scrollTopをscrollHeight（コンテンツ全体の高さ）に設定し、強制的にスクロール完了イベントを発生させる
        self.proc.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", agree_container)

        # 3. スクロールイベント発火後、チェックボックスが有効になるのを待つ
        sleep(1)  # 短い待機

        # 4. その後、元のチェックボックスをクリックする
        consent_checkbox = self.proc.driver.find_element(By.ID, "UNQ_checkboxExt_1002")
        self.proc.driver.execute_script("arguments[0].click();", consent_checkbox)

        # ----------------------------------------------------
        # II. ご名義人さま（お亡くなりになられた方）について
        # ----------------------------------------------------

        # 名前（漢字・カナ）
        self.proc.driver.find_element(By.NAME, "targetSei").send_keys(self.name[0])
        self.proc.driver.find_element(By.NAME, "targetMei").send_keys(self.name[1])
        self.proc.driver.find_element(By.NAME, "targetSeiKana").send_keys(self.name_kana[0])
        self.proc.driver.find_element(By.NAME, "targetMeiKana").send_keys(self.name_kana[1])

        # ご住所（郵便番号・住所）
        self.proc.driver.find_element(By.NAME, "postnum01").send_keys(f'{self.zipcode[0]}{self.zipcode[1]}')
        self.proc.driver.find_element(By.XPATH, '//*[@id="UNQ_oranchor_1008"]/span').click()
        sleep(.5)

        # # 郵便番号検索はスキップし、直接住所を入力
        # self.proc.driver.find_element(By.NAME, "targetTodohuken").send_keys(self.address)
        # self.proc.driver.find_element(By.NAME, "targetSikuchoson").send_keys(T_SHIKU)
        self.proc.driver.find_element(By.NAME, 'targetBanchiChou').send_keys(re.findall(r'\d+', self.address_pattern[2])[0])
        self.proc.driver.find_element(By.NAME, 'targetBanchiBan').send_keys(re.findall(r'\d+', self.address_pattern[2])[1])
        self.proc.driver.find_element(By.NAME, 'targetBanchiGou').send_keys(re.findall(r'\d+', self.address_pattern[2])[2])
        if self.building_name:
            self.proc.driver.find_element(By.NAME, 'targetOther').send_keys(self.building_name)

        # 生年月日 (年/月/日)
        Select(self.proc.driver.find_element(By.NAME, "targetBirthDateYear")).select_by_visible_text(f'{utils.convert_to_wareki2(self.birthday)[:utils.convert_to_wareki2(self.birthday).find('年')]}（{re.findall(r'\d+', self.birthday)[0]}）')
        Select(self.proc.driver.find_element(By.NAME, "targetBirthDateMonth")).select_by_visible_text(re.findall(r'\d+', self.birthday)[1])
        Select(self.proc.driver.find_element(By.NAME, "targetBirthDateDay")).select_by_visible_text(re.findall(r'\d+', self.birthday)[2])

        # お亡くなりになられた日（生年月日と同じ操作）
        Select(self.proc.driver.find_element(By.NAME, "targetDateYear")).select_by_visible_text(f'{utils.convert_to_wareki2(self.deathday)[:utils.convert_to_wareki2(self.deathday).find('年')]}（{re.findall(r'\d+', self.deathday)[0]}）')
        Select(self.proc.driver.find_element(By.NAME, "targetDateMonth")).select_by_visible_text(re.findall(r'\d+', self.deathday)[1])
        Select(self.proc.driver.find_element(By.NAME, "targetDateDay")).select_by_visible_text(re.findall(r'\d+', self.deathday)[2])

        # お取引店・口座番号
        self.proc.driver.find_element(By.NAME, "targetTenban").send_keys(self.branch_code)

        if "普通" in self.subjects or "貯蓄" in self.subjects:
            # 普通・貯蓄に対応する表示テキストを選択
            target_text = "普通・貯蓄"
        elif "当座" in self.subjects:
            target_text = "当座"
        elif "定期" in self.subjects:
            target_text = "定期"
        elif "積立" in self.subjects:
            target_text = "積立"
        elif "外貨普通" in self.subjects:
            target_text = "外貨普通"
        elif "外貨定期" in self.subjects:
            target_text = "外貨定期"
        elif "投信" in self.subjects or "投資信託" in self.subjects:
            target_text = "投信"
        elif "納税" in self.subjects:
            target_text = "納税準備預金"
        elif "ローン" in self.subjects:
            target_text = "ローン"
        elif "証券" in self.subjects:
            target_text = "証券"
        else:
            target_text = ''
        if target_text:
            Select(self.proc.driver.find_element(By.NAME, "targetKamoku")).select_by_visible_text(target_text)
        self.proc.driver.find_element(By.NAME, "targetKouzaNum").send_keys(self.account_number)
        print("ご名義人さま情報を入力しました。")

        # ----------------------------------------------------
        # III. ご入力者さまについて
        # ----------------------------------------------------

        # 士業(※)の方はこちらをチェック
        # sleep(.5)
        self.proc.driver.execute_script("arguments[0].click();", self.proc.driver.find_element(By.ID, "sigyouflg1"))
        sleep(.5)

        # 名前（漢字・カナ）
        self.proc.driver.find_element(By.NAME, "ApplicantKatagaki").send_keys('行政書士法人チェスター')
        self.proc.driver.find_element(By.NAME, "ApplicantSimei").send_keys(f'森町翼（{self.code}）')
        self.proc.driver.find_element(By.NAME, "ApplicantKatagakiKana").send_keys('ギョウセイショシホウジンチェスター')
        self.proc.driver.find_element(By.NAME, "ApplicantSimeiKana").send_keys('モリマチツバサ')

        # 続柄
        self.proc.driver.find_element(By.NAME, "applicantGokankei").send_keys("相続人代理人")

        self.proc.driver.find_element(By.NAME, "applicantZipcode").send_keys('1030028')
        self.proc.driver.find_element(By.XPATH, '//*[@id="UNQ_oranchor_1032"]/span').click()
        sleep(.5)
        self.proc.driver.find_element(By.NAME, "applicantBanchiChou").send_keys('1')
        self.proc.driver.find_element(By.NAME, "applicantBanchiBan").send_keys('7')
        self.proc.driver.find_element(By.NAME, "applicantBanchiGou").send_keys('20')
        self.proc.driver.find_element(By.NAME, "applicantOther").send_keys('八重洲口会館2階')

        # 電話番号
        self.proc.driver.find_element(By.ID, "UNQ_formcontrolinputtextExt_10391").send_keys('050')
        self.proc.driver.find_element(By.ID, "UNQ_formcontrolinputtextExt_10392").send_keys('6864')
        self.proc.driver.find_element(By.ID, "UNQ_formcontrolinputtextExt_10393").send_keys('7034')

        # ----------------------------------------------------
        # IV. お手続者さまについて (ご入力者さま自身が行う前提)
        # ----------------------------------------------------

        # 「ご入力者さまご自身が相続のお手続も行われる場合、チェックをお願いします」にチェック
        self.proc.driver.find_element(By.ID, "UNQ_checkboxExt_1044").click()

        # 「手続者が弁護士、司法書士、行政書士、税理士のいずれかの資格を有する場合、チェックをお願いします」にチェック
        self.proc.driver.find_element(By.NAME, "sigyouShikakuUmu").click()

        # ----------------------------------------------------
        # V. その他相続に必要となる情報 (必須)
        # ----------------------------------------------------

        # 相続用残高証明書発行希望: 「有り」を選択 (value="1")
        self.proc.driver.find_element(By.ID, "UNQ_radiobuttonExt_1086").click()

        # 遺言の有無: 「無し」を選択 (value="0")
        self.proc.driver.find_element(By.ID, "UNQ_radiobuttonExt_1073").click()

        # 遺産分割協議書の有無: 「無し」を選択 (value="0")
        # self.proc.driver.find_element(By.ID, "UNQ_radiobuttonExt_1082").click()
        self.proc.driver.find_element(By.ID, "UNQ_radiobuttonExt_1083").click()

        # 相続人間の意見の相違: 「無し」を選択 (value="0")
        self.proc.driver.find_element(By.ID, "UNQ_radiobuttonExt_1085").click()

        # ----------------------------------------------------
        # VI. 次へボタンのクリック (画面下部にあるためJSクリックが安全)
        # ----------------------------------------------------

        next_button = self.proc.driver.find_element(By.ID, NEXT_BUTTON_ID)

        # JavaScriptを使用してボタンを強制的にクリック
        self.proc.driver.execute_script("arguments[0].click();", next_button)
        print("「次へ」ボタンをJavaScriptでクリックしました。")
        sleep(1)

        # ① 三井住友銀行にお預け入れの預金等の金融資産を受け取られる方 → 決まっていない (value="0")
        self.proc.driver.find_element(By.ID, "UNQ_radiobuttonExt_2014").click()

        # ② ご相続人さまの状況 → いずれにも該当しない (value="0")
        self.proc.driver.find_element(By.ID, "joukyouother-text").click()

        # JavaScriptを使用して要素をウィンドウの上端にスクロール
        self.proc.driver.execute_script("arguments[0].scrollIntoView(true);", self.proc.driver.find_element(By.XPATH, '//*[@id="bs201"]/div/div[2]/h2/span[1]'))


    def balance_certificate(self):
        # 残高証明書等作成依頼書
        pdf = PdfCreate("A4")

        # 住所
        pdf.draw_string(52, 259, '103-0028')
        pdf.draw_string(52, 249, '東京', 12)
        pdf.draw_string(73, 251.5, '〇', 14)
        pdf.draw_string(84, 252, '東京都中央区八重洲一丁目7-20 八重洲口会館2階', 12)
        pdf.draw_string(84, 247, f'担当：森町（{self.code}）', 12)

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
        self.deathday = re.findall('[0-9]+', self.deathday)
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
    # proc.account_freezing()
    proc.balance_certificate()


if __name__ == '__main__':
    main()