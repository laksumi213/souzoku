import re
import unicodedata
from app._utils.web_operation import Web
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# 以下のモジュールは未使用のため削除
# import os
# import app.utils as utils
# from datetime import datetime
from time import sleep  # 必要な箇所で利用するため残す

# ログイン情報の定数化
USER_ID = 'ABLV5270'
PASSWORD = 'gychester55'
LOGIN_URL = 'https://www.touki.or.jp/TeikyoUketsuke/'


def process_address_efficiently(address_string):
    """
    住所文字列を都道府県、市区町村・町域、番地・号に分割し、
    市区町村・町域、番地・号に含まれる半角英数字を全角に変換する。
    """

    # 1. 都道府県の抽出と、それ以外の部分の分割を同時に行う
    # ^(都道府県部分)(市区町村・町域以降の部分)$

    # 都道府県の正規表現パターン（元のコードのパターンを使用）
    pref_pattern = r'(東京都|北海道|(?:京都|大阪)府|.{2,3}県)'

    match = re.match(pref_pattern + r'(.+)', address_string)

    if not match:
        # マッチしない場合の適切なエラー処理
        return None, None, None

    prefectures = match.group(1)
    buf = match.group(2)  # 都道府県を除いた部分

    # 2. 「丁目」を区切りとして、町域と番地・号に分割
    # (.*丁目)(.*) にマッチさせる
    buf_match = re.match(r'(.*丁目)(.*)', buf)

    if buf_match:
        town_name_raw = buf_match.group(1)
        block_raw = buf_match.group(2)
    else:
        # 「丁目」がない場合（例: ○○市△△町 1-2-3）のフォールバック処理
        # ここでは町域全体をtown_nameとし、blockを空にしています。
        # 実際のデータ構造に応じて調整が必要です。
        town_name_raw = buf
        block_raw = ''

    # 3. 半角文字の全角変換 (最も効率的な方法)
    # NFKCは半角カナや半角英数字などを全角に統一するUnicodeの正規化形式
    # ただし、元のコードが意図している「半角英数字・記号のみ」の変換とは
    # 厳密には異なる場合がありますが、より一般的な住所正規化の手法です。

    # 半角文字を全角に変換する関数
    def to_zenkaku(text):
        # str.maketrans() を利用した元のロジックを簡潔にする
        # 全角←→半角の変換テーブルを簡単に作成
        return text.translate(
            str.maketrans(
                '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',
                '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝～'
            )
        )

    town_name = to_zenkaku(town_name_raw)
    block = to_zenkaku(block_raw)

    return prefectures, town_name, block


def touki(address, target='土地'):
    proc = Web()

    # 1. サイトを開き、要素の出現を待機
    proc.web_open(LOGIN_URL)

    try:
        WebDriverWait(proc.driver, 10).until(
            EC.presence_of_element_located((By.ID, "userId"))
        )
    except Exception as e:
        print(f"ログインページのロード中にタイムアウトしました: {e}")
        proc.driver.quit()
        return

    # 2. IDとパスワードの入力
    proc.driver.find_element(By.ID, 'userId').send_keys('ABLV5270')
    proc.driver.find_element(By.ID, 'password').send_keys('gychester55')
    LOGIN_BUTTON_XPATH = "//button[contains(@class, 'CForwardLong')]/span[text()='ログイン']"
    proc.driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()


    # 4. 強制ログイン（セッション切れ/二重ログイン時の処理）
    try:
        # 強制ログインボタンのXPATHを特定
        # 強制ログイン画面のHTMLがないため、元コードのXPATHを仮に利用します。
        FORCE_LOGIN_XPATH = "/html/body/div/div[1]/div[4]/div[2]/form/button[2]/span"

        force_login_button = WebDriverWait(proc.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, FORCE_LOGIN_XPATH))
        )
        # 要素が見つかった場合（強制ログイン画面が出た場合）のみクリック
        force_login_button.click()

        # 強制ログイン後のページ遷移を待機（例: トップページにある要素を待つ）
        # WebDriverWait(proc.driver, 10).until(...)

    except:
        # タイムアウトした場合（強制ログイン画面が出なかった場合）は何もしないで続行
        pass

    # リンクテキストが「不動産請求」である要素を待機してクリック
    try:
        fudosan_link = WebDriverWait(proc.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "不動産請求"))
        )
        fudosan_link.click()
    except Exception as e:
        print(f"不動産請求ボタンのクリックに失敗しました: {e}")

    pref, town, blk = process_address_efficiently(address)

    # --- 不動産種別（土地/建物）のラジオボタン操作 ---
    if target == '建物':
        # 建物にチェックを入れる
        BUILDING_RADIO_ID = "fuShozaiTypeTATEMONO"
        try:
            building_radio = WebDriverWait(proc.driver, 10).until(
                EC.element_to_be_clickable((By.ID, BUILDING_RADIO_ID))
            )
            building_radio.click()
            print("不動産種別を「建物」に設定しました。")
        except Exception as e:
            print(f"「建物」ラジオボタンのクリックに失敗しました: {e}")

    # '土地' の場合はデフォルトでチェックされているため、明示的な操作はスキップ（ここでは 'else' は不要）

    Select(proc.driver.find_element(By.NAME, "todofukenShozai")).select_by_visible_text(pref)
    proc.driver.find_element(By.NAME, "fuShozaiChokusetuNyuryoku").click()
    proc.driver.find_element(By.NAME, 'chibanKuiki').send_keys(town)
    proc.driver.find_element(By.NAME, 'chibanKaoku').send_keys(blk)

    KYODO_TANPO_YES_ID = "fuKyodoTanpoYES"
    kyodo_tanpo_yes = WebDriverWait(proc.driver, 10).until(
        EC.element_to_be_clickable((By.ID, KYODO_TANPO_YES_ID))
    )
    kyodo_tanpo_yes.click()

    # 土地/建物の請求事項のチェックボックス
    # 土地: 土地所在図/地積測量図 (fuShozai)
    # 建物: 建物図面/各階平面図 (fuZumen)

    # if target == '土地':
    #     # 土地の場合: 「土地所在図/地積測量図」にチェック
    #     CHECKBOX_ID = "fuShozai"
    #     print("不動産種別が「土地」のため、「土地所在図/地積測量図」にチェックを入れます。")
    # elif target == '建物':
    #     # 建物の場合: 「建物図面/各階平面図」にチェック
    #     CHECKBOX_ID = "fuZumen"
    #     print("不動産種別が「建物」のため、「建物図面/各階平面図」にチェックを入れます。")
    # else:
    #     CHECKBOX_ID = None
    #     print("「土地」または「建物」の指定がないため、土地・建物関連のチェックボックスは操作しません。")
    #
    # if CHECKBOX_ID:
    #     try:
    #         target_checkbox = WebDriverWait(proc.driver, 10).until(
    #             EC.element_to_be_clickable((By.ID, CHECKBOX_ID))
    #         )
    #
    #         # チェックボックスがすでにチェックされていない場合のみクリック
    #         if not target_checkbox.is_selected():
    #             target_checkbox.click()
    #             print(f"請求事項のチェックボックス (ID: {CHECKBOX_ID}) をチェックしました。")
    #         else:
    #             print(f"請求事項のチェックボックス (ID: {CHECKBOX_ID}) は既にチェック済みです。")
    #
    #     except Exception as e:
    #         print(f"請求事項のチェックボックス (ID: {CHECKBOX_ID}) の操作に失敗しました: {e}")

    # 確定ボタン
    CONFIRM_BUTTON_XPATH = "//button[contains(@class, 'CForward')]/span[contains(text(), '確定')]"

    try:
        confirm_button = WebDriverWait(proc.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, CONFIRM_BUTTON_XPATH))
        )
        confirm_button.click()
    except Exception as e:
        print(f"確定ボタンのクリックに失敗しました: {e}")


if __name__ == '__main__':
    touki(address='東京都目黒区駒場3丁目916-41')
    # touki(address='東京都目黒区駒場3丁目906-25', target='建物')