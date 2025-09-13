import os
from pathlib import Path
import platform
import configparser
from datetime import datetime
import re
import requests
from zengin_code import Bank
import mojimoji

WAREKI_START = {
    '令和': datetime(2019, 5, 1),
    '平成': datetime(1989, 1, 8),
    '昭和': datetime(1926, 12, 25),
    '大正': datetime(1912, 1, 1),
    '明治': datetime(1868, 1, 1)
}

if platform.system() == 'Windows':
    import ctypes
else:
    import subprocess


def ime_on():
    # print('platform.system():', platform.system())
    if platform.system() == 'Windows':
        user32 = ctypes.WinDLL(name="user32")
        imm32 = ctypes.WinDLL(name="imm32")
        h_wnd = user32.GetForegroundWindow()
        h_imc = imm32.ImmGetContext(h_wnd)
        imm32.ImmSetOpenStatus(h_imc, True)
        imm32.ImmReleaseContext(h_wnd, h_imc)
        # print('Windows ime_on')
    else:
        # applescript = r'tell application "System Events" to keystroke (key code {104})'
        # subprocess.run(["osascript", "-e", applescript])
        applescript = '''
        tell application "System Events"
            keystroke (key code {104})
        end tell
        '''
        subprocess.Popen(['osascript', '-e', applescript])
        # print('mac ime_on')


def ime_off():
    if platform.system() == 'Windows':
        user32 = ctypes.WinDLL(name="user32")
        imm32 = ctypes.WinDLL(name="imm32")
        h_wnd = user32.GetForegroundWindow()
        h_imc = imm32.ImmGetContext(h_wnd)
        imm32.ImmSetOpenStatus(h_imc, False)
        imm32.ImmReleaseContext(h_wnd, h_imc)
    else:
        applescript = r'tell application "System Events" to keystroke (key code 102)'  # IME OFF
        subprocess.run(["osascript", "-e", applescript])


def get_parent_path():
    return Path(os.path.dirname(__file__)).parent


def get_database_path():
    parent_path = get_parent_path()
    return str(Path(parent_path, 'database', 'inheritance.db'))


def get_config_path():
    return str(Path(get_parent_path(), 'config', 'config.ini'))


def read_config():
    config = configparser.ConfigParser()
    config.read(get_config_path(), encoding='CP932')
    return config


def convert_to_wareki2(s):
    try:
        dt = re.findall('[0-9]+', s)
        y = int(dt[0])
        m = int(dt[1])
        d = int(dt[2])
        y_m_d = datetime(y, m, d)
        if WAREKI_START['令和'] <= y_m_d:
            reiwa_year = WAREKI_START['令和'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '令和'
        elif WAREKI_START['平成'] <= y_m_d:
            reiwa_year = WAREKI_START['平成'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '平成'
        elif WAREKI_START['昭和'] <= y_m_d:
            reiwa_year = WAREKI_START['昭和'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '昭和'
        elif WAREKI_START['大正'] <= y_m_d:
            reiwa_year = WAREKI_START['大正'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '大正'
        elif WAREKI_START['明治'] <= y_m_d:
            reiwa_year = WAREKI_START['明治'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '明治'
        else:
            return '不明'

        if year == 1:
            # year = '元'
            year = '1'

        return f'{era_str}{str(year)}年{m}月{d}日'
    except Exception as e:
        print(e)
        return ''


def get_zipcode_from_address(address):
    """
    住所から郵便番号を取得する関数

    Args:
        address (str): 検索したい住所（例: "東京都千代田区霞が関"）

    Returns:
        str: 該当する郵便番号、またはNone
    """
    url = 'https://zipcoda.net/api'
    try:
        response = requests.get(url,  {"address": address})
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる
        data = response.json()

        if data["items"]:
            # 該当する郵便番号が見つかった場合
            return re.sub(r'(\d{3})(\d{4})', r'\1-\2', data["items"][0]["zipcode"])
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        return None


def zipcode_to_address(zipcode):
    URL = 'https://zipcloud.ibsnet.co.jp/api/search'

    if '-' in str(zipcode):
        zipcode = int(zipcode.replace('-', ''))

    res = requests.get(URL, params={'zipcode': zipcode})
    res = res.json()
    try:
        address = [res['results'][0]['address1'], res['results'][0]['address2'], res['results'][0]['address3']]
    except Exception as e:
        print(e)
        address = None
    # print(address)
    return address


def convert_seireki(wareki_s, e):
    era = {
        'r': '令和',
        'h': '平成',
        's': '昭和',
        't': '大正',
        'm': '明治'
    }

    era_dic = {
        "明治": 1868,
        "大正": 1912,
        "昭和": 1926,
        "平成": 1989,
        "令和": 2019
    }

    tmp = re.findall('[0-9]+', wareki_s)

    if len(tmp) == 2:
        e.control.value = f'{datetime.now().strftime("%Y")}/{tmp[0]}/{tmp[1]}'
        return

    try:
        if wareki_s[0] == 'r' or wareki_s[0] == 'h' or wareki_s[0] == 's' or wareki_s[0] == 't' or wareki_s[0] == 'm':
            wareki = era[wareki_s[0]] + tmp[0]
        else:
            wareki = wareki_s
    except Exception as e:
        wareki = wareki_s
        print(e)

    s = re.match(r'(明治|大正|昭和|平成|令和)([0-9]+|元)', str(wareki))
    if s is None:
        return wareki_s
    y = int(s.group(2)) if s.group(2) != '元' else 1
    e.control.value = f'{era_dic[s.group(1)] + y - 1}/{tmp[1]}/{tmp[2]}'

def bank_search(name=None, code=None):
    banks = {}
    name = mojimoji.han_to_zen(name).strip().replace('銀行', '')

    # 銀行名とコードで検索
    if name and code:
        name = name.strip()
        code = str(code).strip()
        for bank_code in Bank.all:
            bank = Bank[bank_code]
            if ((bank.name.startswith(name) or bank.hira.startswith(name) or bank.roma.startswith(
                    mojimoji.zen_to_han(name)))
                    and (bank.code.startswith(mojimoji.zen_to_han(code)))):
                banks[bank.name] = bank_code
                print('# 銀行名とコードで検索')

    # 銀行名で検索
    elif name:
        name = mojimoji.han_to_zen(name).strip().replace('銀行', '')
        # print('name:', name)
        for bank_code in Bank.all:
            bank = Bank[bank_code]
            # print('bank_code:', bank_code, bank.name)
            if (bank.name.startswith(name) or
                    bank.hira.startswith(name) or
                    bank.roma.startswith(mojimoji.zen_to_han(name))):
                # print('bank_code:', bank_code, bank.name)
                banks[bank.name] = bank_code
                # 銀行名の「銀行」や「信金」などを取得
                # gincode = Gincode
                # bank_name = gincode.get_gincode(bank_code)[2]
                # banks[bank_name] = bank_code

    # コードで検索
    elif code:
        # 銀行名の「銀行」や「信金」などを取得
        gincode = Gincode
        code = str(code).strip()
        bank_name = gincode.get_gincode(code)[2]
        print('gincode.get_gincode(bank_code):', gincode.get_gincode(code))
        banks[bank_name] = code

    return banks.items()

def branch_code_search(bank_code, branch_name):
    branch_name = branch_name.strip()
    branch_name = branch_name.replace('支店', '')
    bank = Bank[bank_code]
    for branch_code in bank.branches:
        # 検索する支店名と一致する場合、支店コードを返す
        if bank.branches[branch_code].name == branch_name:
            return branch_code